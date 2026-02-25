"""
Direct BLE communication for Android.
Uses Android BluetoothGatt API via jnius (no dependency on external apps).
"""
import os
import time
import threading

IS_ANDROID = 'ANDROID_ARGUMENT' in os.environ or 'ANDROID_ROOT' in os.environ

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
        _BluetoothGattCharacteristic = autoclass(
            'android.bluetooth.BluetoothGattCharacteristic')
        _UUID = autoclass('java.util.UUID')
        _PythonActivity = autoclass('org.kivy.android.PythonActivity')
        HAS_BLE = True
    except Exception as _e:
        _BLE_INIT_ERROR = str(_e)


if HAS_BLE:
    class _GattCallback(PythonJavaClass):
        """Java BluetoothGattCallback implementation."""
        __javainterfaces__ = ['android/bluetooth/BluetoothGattCallback']
        __javacontext__ = 'app'

        def __init__(self, manager):
            super().__init__()
            self.mgr = manager

        @java_method('(Landroid/bluetooth/BluetoothGatt;II)V')
        def onConnectionStateChange(self, gatt, status, newState):
            STATE_CONNECTED = 2
            if newState == STATE_CONNECTED:
                self.mgr._connected = True
                gatt.discoverServices()
            else:
                self.mgr._connected = False
                self.mgr._services_discovered = False

        @java_method('(Landroid/bluetooth/BluetoothGatt;I)V')
        def onServicesDiscovered(self, gatt, status):
            if status == 0:  # GATT_SUCCESS
                self.mgr._services_discovered = True

        @java_method('(Landroid/bluetooth/BluetoothGatt;'
                     'Landroid/bluetooth/BluetoothGattCharacteristic;I)V')
        def onCharacteristicRead(self, gatt, characteristic, status):
            if status == 0:
                v = characteristic.getValue()
                self.mgr._read_value = bytes(v) if v else b''
            self.mgr._read_done.set()

        @java_method('(Landroid/bluetooth/BluetoothGatt;'
                     'Landroid/bluetooth/BluetoothGattCharacteristic;I)V')
        def onCharacteristicWrite(self, gatt, characteristic, status):
            self.mgr._write_ok = (status == 0)
            self.mgr._write_done.set()

        @java_method('(Landroid/bluetooth/BluetoothGatt;'
                     'Landroid/bluetooth/BluetoothGattCharacteristic;)V')
        def onCharacteristicChanged(self, gatt, characteristic):
            v = characteristic.getValue()
            data = bytes(v) if v else b''
            if self.mgr._notify_cb:
                self.mgr._notify_cb(data)


class BLEManager:
    """Android BLE GATT manager. Call connect() before any read/write."""

    def __init__(self):
        self._gatt = None
        self._cb = None
        self._connected = False
        self._services_discovered = False
        self._read_value = None
        self._read_done = threading.Event()
        self._write_ok = False
        self._write_done = threading.Event()
        self._notify_cb = None
        self._adapter = _BluetoothAdapter.getDefaultAdapter() if HAS_BLE else None

    # ── Device discovery ─────────────────────────────────────────────────────

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
        device = self._adapter.getRemoteDevice(address)
        self._cb = _GattCallback(self)
        self._connected = False
        self._services_discovered = False
        self._gatt = device.connectGatt(activity, False, self._cb)

        deadline = time.time() + timeout
        while not self._connected and time.time() < deadline:
            time.sleep(0.1)
        if not self._connected:
            raise RuntimeError(f"Connection timeout ({address})")

        deadline = time.time() + timeout
        while not self._services_discovered and time.time() < deadline:
            time.sleep(0.1)
        if not self._services_discovered:
            raise RuntimeError("Service discovery timeout")

    def disconnect(self):
        """Disconnect and release GATT resources."""
        if self._gatt:
            self._gatt.disconnect()
            self._gatt.close()
            self._gatt = None
        self._connected = False
        self._services_discovered = False

    @property
    def is_connected(self):
        return self._connected and self._gatt is not None

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
        self._read_done.clear()
        self._read_value = None
        self._gatt.readCharacteristic(ch)
        if not self._read_done.wait(timeout):
            raise RuntimeError("Read timeout")
        return self._read_value

    def read_string(self, svc_uuid, char_uuid, timeout=5):
        """Read a characteristic and decode as UTF-8 string."""
        raw = self.read(svc_uuid, char_uuid, timeout)
        return self._decode_str(raw)

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
        self._write_done.clear()
        self._gatt.writeCharacteristic(ch)
        if not self._write_done.wait(timeout):
            raise RuntimeError("Write timeout")
        if not self._write_ok:
            raise RuntimeError("Write failed (GATT error)")

    # ── Notifications ────────────────────────────────────────────────────────

    def enable_notify(self, svc_uuid, char_uuid, callback):
        """Enable BLE notifications. callback(data: bytes) is called on each packet."""
        if not self.is_connected:
            raise RuntimeError("Not connected")
        svc = self._gatt.getService(_UUID.fromString(svc_uuid))
        ch = svc.getCharacteristic(_UUID.fromString(char_uuid))
        self._gatt.setCharacteristicNotification(ch, True)
        self._notify_cb = callback

        # Write CCC descriptor to enable server-side notifications
        CCCD = "00002902-0000-1000-8000-00805f9b34fb"
        desc = ch.getDescriptor(_UUID.fromString(CCCD))
        if desc:
            desc.setValue([0x01, 0x00])
            self._gatt.writeDescriptor(desc)
        time.sleep(0.2)

    def disable_notify(self, svc_uuid, char_uuid):
        """Disable BLE notifications."""
        if not self.is_connected:
            return
        svc = self._gatt.getService(_UUID.fromString(svc_uuid))
        if svc:
            ch = svc.getCharacteristic(_UUID.fromString(char_uuid))
            if ch:
                self._gatt.setCharacteristicNotification(ch, False)
        self._notify_cb = None

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _decode_str(raw):
        if not raw:
            return ""
        try:
            return raw.decode('utf-8').strip('\x00').strip()
        except Exception:
            return raw.hex()
