"""
Direct BLE communication for Android.
Uses Android BluetoothGatt API via jnius (no dependency on external apps).
GATT callbacks are handled by a pure-Java GattCallbackHelper (no PythonJavaClass)
to avoid Android background-thread ClassLoader issues.
"""
import os
import time
import threading

IS_ANDROID = 'ANDROID_ARGUMENT' in os.environ or 'ANDROID_ROOT' in os.environ

_DEBUG_FILE = '/data/data/com.wellysis.sdkautotester/files/ble_debug.txt'

def _dbg(msg):
    """Write a debug line to a file readable via adb shell run-as."""
    try:
        with open(_DEBUG_FILE, 'a') as f:
            f.write(msg + '\n')
    except Exception:
        pass

# ─── Standard Bluetooth SIG UUIDs ────────────────────────────────────────────
BATTERY_SVC        = "0000180f-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL      = "00002a19-0000-1000-8000-00805f9b34fb"

DEVINFO_SVC        = "0000180a-0000-1000-8000-00805f9b34fb"
MODEL_NUMBER       = "00002a24-0000-1000-8000-00805f9b34fb"
SERIAL_NUMBER      = "00002a25-0000-1000-8000-00805f9b34fb"
FIRMWARE_REVISION  = "00002a26-0000-1000-8000-00805f9b34fb"
HARDWARE_REVISION  = "00002a27-0000-1000-8000-00805f9b34fb"
SOFTWARE_REVISION  = "00002a28-0000-1000-8000-00805f9b34fb"

# ─── Wellysis S-Patch device-specific UUIDs ──────────────────────────────────
# TODO: Replace with actual values from the Wellysis SDK documentation.
WELLYSIS_SVC        = "TODO_WELLYSIS_SERVICE_UUID"
WELLYSIS_CONTROL    = "TODO_WELLYSIS_CONTROL_CHAR_UUID"    # Start/Pause/Restart/Stop
WELLYSIS_ECG_NOTIFY = "TODO_WELLYSIS_ECG_NOTIFY_CHAR_UUID"

# ─── Control command bytes ────────────────────────────────────────────────────
# TODO: Replace with actual byte values from the Wellysis SDK documentation.
CMD_START   = bytes([0x01])
CMD_PAUSE   = bytes([0x02])
CMD_RESTART = bytes([0x03])
CMD_STOP    = bytes([0x04])
CMD_RESET   = bytes([0x05])

# ─── Android BLE setup ───────────────────────────────────────────────────────
HAS_BLE = False
_BLE_INIT_ERROR = "BLE is only available on Android"

if IS_ANDROID:
    try:
        from jnius import autoclass, PythonJavaClass, java_method

        _BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        _BluetoothDevice  = autoclass('android.bluetooth.BluetoothDevice')
        _BluetoothGattCharacteristic = autoclass(
            'android.bluetooth.BluetoothGattCharacteristic')
        # Pure-Java callback helper — no PythonJavaClass needed
        _GattCallbackHelper = autoclass(
            'com.wellysis.sdkautotester.GattCallbackHelper')
        _UUID            = autoclass('java.util.UUID')
        _PythonActivity  = autoclass('org.kivy.android.PythonActivity')
        HAS_BLE = True
    except Exception as _e:
        _BLE_INIT_ERROR = str(_e)


if HAS_BLE:
    class _LeScanCallback(PythonJavaClass):
        """Java BluetoothAdapter.LeScanCallback for BLE device discovery."""
        __javainterfaces__ = ['android/bluetooth/BluetoothAdapter$LeScanCallback']
        __javacontext__ = 'app'

        def __init__(self, on_device):
            super().__init__()
            self._on_device = on_device

        @java_method('(Landroid/bluetooth/BluetoothDevice;I[B)V')
        def onLeScan(self, device, rssi, scanRecord):
            name = device.getName() or ""
            address = device.getAddress() or ""
            if address:
                self._on_device(name, address)


class BLEManager:
    """Android BLE GATT manager. Call connect() before any read/write."""

    def __init__(self):
        self._gatt = None
        self._cb   = None      # GattCallbackHelper (Java) — stores all GATT state
        self._scan_cb = None
        self._adapter = _BluetoothAdapter.getDefaultAdapter() if HAS_BLE else None

    # ── Device discovery ─────────────────────────────────────────────────────

    def scan_for_device(self, serial_keyword, timeout=10):
        """Scan for nearby BLE devices; return first (name, address) whose name
        contains serial_keyword, or None. Does NOT require pre-pairing."""
        if not HAS_BLE or not self._adapter:
            return None
        if not self._adapter.isEnabled():
            raise RuntimeError("Bluetooth is not enabled")

        found = threading.Event()
        result = [None]

        def on_device(name, address):
            if serial_keyword.lower() in name.lower():
                result[0] = (name, address)
                found.set()

        cb = _LeScanCallback(on_device)
        self._scan_cb = cb
        self._adapter.startLeScan(cb)
        try:
            found.wait(timeout=timeout)
        finally:
            self._adapter.stopLeScan(cb)
            self._scan_cb = None

        return result[0]

    def get_bonded_devices(self):
        """Return paired Bluetooth devices as list of (name, address) tuples."""
        if not HAS_BLE or not self._adapter:
            return []
        bonded = self._adapter.getBondedDevices()
        if not bonded:
            return []
        result = []
        it = bonded.iterator()
        while it.hasNext():
            d = it.next()
            result.append((d.getName() or "Unknown", d.getAddress()))
        return result

    def is_enabled(self):
        """Return True if Bluetooth is enabled."""
        return bool(HAS_BLE and self._adapter and self._adapter.isEnabled())

    # ── Connection ───────────────────────────────────────────────────────────

    def connect(self, address, timeout=15):
        """Connect to BLE device by MAC address (AA:BB:CC:DD:EE:FF)."""
        if not HAS_BLE:
            raise RuntimeError(_BLE_INIT_ERROR)
        if not self._adapter.isEnabled():
            raise RuntimeError("Bluetooth is not enabled")

        activity = _PythonActivity.mActivity
        device   = self._adapter.getRemoteDevice(address)

        # GattCallbackHelper extends BluetoothGattCallback directly in Java —
        # no PythonJavaClass / no classloader issues.
        self._cb = _GattCallbackHelper()

        _dbg(f"connectGatt → {address}")
        self._gatt = device.connectGatt(
            activity, False, self._cb, _BluetoothDevice.TRANSPORT_LE)
        _dbg(f"connectGatt returned: {self._gatt}")

        # Wait for connection (state == 2 = STATE_CONNECTED)
        deadline = time.time() + timeout
        while self._cb.getConnectionState() != 2 and time.time() < deadline:
            time.sleep(0.1)
        _dbg(f"connectionState after wait: {self._cb.getConnectionState()}")
        if self._cb.getConnectionState() != 2:
            raise RuntimeError(f"Connection timeout ({address})")

        # Wait for service discovery
        deadline = time.time() + timeout
        while not self._cb.isServicesDiscovered() and time.time() < deadline:
            time.sleep(0.1)
        _dbg(f"servicesDiscovered: {self._cb.isServicesDiscovered()}")
        if not self._cb.isServicesDiscovered():
            raise RuntimeError("Service discovery timeout")

    def disconnect(self):
        """Disconnect and release GATT resources."""
        if self._gatt:
            self._gatt.disconnect()
            self._gatt.close()
            self._gatt = None
        self._cb = None

    @property
    def is_connected(self):
        return (self._gatt is not None and
                self._cb is not None and
                self._cb.getConnectionState() == 2)

    # ── GATT read ────────────────────────────────────────────────────────────

    def read(self, svc_uuid, char_uuid, timeout=5):
        """Read a characteristic. Returns raw bytes."""
        if not self.is_connected:
            raise RuntimeError("Not connected")
        svc = self._gatt.getService(_UUID.fromString(svc_uuid))
        if not svc:
            raise RuntimeError(f"Service not found: {svc_uuid}")
        ch = svc.getCharacteristic(_UUID.fromString(char_uuid))
        if not ch:
            raise RuntimeError(f"Characteristic not found: {char_uuid}")

        self._cb.clearRead()
        self._gatt.readCharacteristic(ch)

        deadline = time.time() + timeout
        while not self._cb.isReadDone() and time.time() < deadline:
            time.sleep(0.05)
        if not self._cb.isReadDone():
            raise RuntimeError("Read timeout")

        raw = self._cb.getReadValue()
        return bytes(raw) if raw else b''

    def read_string(self, svc_uuid, char_uuid, timeout=5):
        """Read a characteristic and decode as UTF-8 string."""
        return self._decode_str(self.read(svc_uuid, char_uuid, timeout))

    def read_uint8(self, svc_uuid, char_uuid, timeout=5):
        """Read a single-byte integer characteristic."""
        raw = self.read(svc_uuid, char_uuid, timeout)
        return raw[0] if raw else 0

    # ── GATT write ───────────────────────────────────────────────────────────

    def write(self, svc_uuid, char_uuid, value, timeout=5):
        """Write bytes to a characteristic."""
        if not self.is_connected:
            raise RuntimeError("Not connected")
        svc = self._gatt.getService(_UUID.fromString(svc_uuid))
        if not svc:
            raise RuntimeError(f"Service not found: {svc_uuid}")
        ch = svc.getCharacteristic(_UUID.fromString(char_uuid))
        if not ch:
            raise RuntimeError(f"Characteristic not found: {char_uuid}")

        ch.setValue(list(value))
        self._cb.clearWrite()
        self._gatt.writeCharacteristic(ch)

        deadline = time.time() + timeout
        while not self._cb.isWriteDone() and time.time() < deadline:
            time.sleep(0.05)
        if not self._cb.isWriteDone():
            raise RuntimeError("Write timeout")
        if not self._cb.isWriteOk():
            raise RuntimeError("Write failed (GATT error)")

    # ── Notifications ────────────────────────────────────────────────────────

    def enable_notify(self, svc_uuid, char_uuid, callback=None):
        """Enable BLE notifications. callback is ignored (use read_notify to poll)."""
        if not self.is_connected:
            raise RuntimeError("Not connected")
        svc = self._gatt.getService(_UUID.fromString(svc_uuid))
        ch  = svc.getCharacteristic(_UUID.fromString(char_uuid))
        self._gatt.setCharacteristicNotification(ch, True)
        self._cb.clearNotify()

        CCCD = "00002902-0000-1000-8000-00805f9b34fb"
        desc = ch.getDescriptor(_UUID.fromString(CCCD))
        if desc:
            desc.setValue([0x01, 0x00])
            self._gatt.writeDescriptor(desc)
        time.sleep(0.2)

    def read_notify(self, timeout=5):
        """Block up to timeout seconds for the next notification packet."""
        if not self.is_connected:
            raise RuntimeError("Not connected")
        raw = self._cb.pollNotify(int(timeout * 1000))
        return bytes(raw) if raw else b''

    def disable_notify(self, svc_uuid, char_uuid):
        """Disable BLE notifications."""
        if not self.is_connected:
            return
        svc = self._gatt.getService(_UUID.fromString(svc_uuid))
        if svc:
            ch = svc.getCharacteristic(_UUID.fromString(char_uuid))
            if ch:
                self._gatt.setCharacteristicNotification(ch, False)

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _decode_str(raw):
        if not raw:
            return ""
        try:
            return raw.decode('utf-8').strip('\x00').strip()
        except Exception:
            return raw.hex()
