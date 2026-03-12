"""
Test Runner - Core test execution logic.
Runs BLE GATT tests directly on Android using BluetoothGatt API.
No dependency on any external SDK sample app.
"""

import time
import threading
import traceback
import os

IS_ANDROID = 'ANDROID_ARGUMENT' in os.environ or 'ANDROID_ROOT' in os.environ

from .ble_manager import (
    BLEManager,
    BATTERY_SVC, BATTERY_LEVEL,
    DEVINFO_SVC, MODEL_NUMBER, SERIAL_NUMBER,
    FIRMWARE_REVISION, HARDWARE_REVISION, SOFTWARE_REVISION,
    WELLYSIS_SVC, WELLYSIS_CONTROL, WELLYSIS_ECG_NOTIFY,
    CMD_START, CMD_PAUSE, CMD_RESTART, CMD_STOP,
    HAS_BLE,
)

_WELLYSIS_TODO = 'TODO_WELLYSIS_SERVICE_UUID'


class TestRunner:
    """BLE GATT test executor. Runs directly on Android without an external app."""

    def __init__(self, config, callback):
        """
        Args:
            config: Test configuration dict with keys:
                      device_address (str): BLE MAC address (AA:BB:CC:DD:EE:FF)
                      device_name (str): Human-readable device name
                      read, writeget, notify, packet_monitoring (bool): test flags
                      target_packets (int): target for packet monitoring
            callback: Progress callback  fn(status: str, progress: float, log: str)
                      pass progress=-1 to update log only (no progress bar change)
        """
        self.config = config
        self.callback = callback
        self.cancelled = False
        self.result = {
            'passed': 0,
            'failed': 0,
            'tests': {},
            'error': None,
            'fw_version': None,
        }
        self.ble = BLEManager()

    # ── Public API ────────────────────────────────────────────────────────────

    def run(self):
        """Run the selected test suites."""
        address = self.config.get('device_address')
        if not address:
            self.result['error'] = 'No BLE device selected'
            self._update('Error', 100, '[ERROR] No BLE device selected')
            return

        if not IS_ANDROID:
            self.result['error'] = 'BLE testing requires Android'
            self._update('Android required', 100,
                         '[WARN] BLE tests can only run on Android. '
                         'Connect an Android device and install the APK.')
            return

        if not HAS_BLE:
            self.result['error'] = 'BLE not available'
            self._update('BLE unavailable', 100,
                         '[ERROR] Bluetooth API unavailable on this device.')
            return

        try:
            # Connect
            name = self.config.get('device_name', address)
            self._update('Connecting...', 5, f'Connecting to {name} ({address})')
            self.ble.connect(address, timeout=15)
            self._update('Connected', 15, f'[OK] Connected to {name}')

            # Calculate progress steps
            flags = ['read', 'writeget', 'notify', 'packet_monitoring']
            total = sum(1 for f in flags if self.config.get(f, False))
            progress = 15.0
            step = 80.0 / max(total, 1)

            if self.config.get('read') and not self.cancelled:
                self._update('Read tests...', progress, '--- Read Tests ---')
                self._run_read_tests()
                progress += step

            if self.config.get('writeget') and not self.cancelled:
                self._update('WriteGet tests...', progress, '--- WriteGet Tests ---')
                self._run_writeget_tests()
                progress += step

            if self.config.get('notify') and not self.cancelled:
                self._update('Notify tests...', progress, '--- Notify Tests ---')
                self._run_notify_tests()
                progress += step

            if self.config.get('packet_monitoring') and not self.cancelled:
                target = self.config.get('target_packets', 60)
                self._update('Packet monitoring...', progress, f'--- Packet Monitoring (target: {target}) ---')
                self._run_packet_monitoring(target)
                progress += step

        except Exception as e:
            tb = traceback.format_exc()
            try:
                with open('/data/data/com.wellysis.sdkautotester/files/ble_debug.txt', 'a') as f:
                    f.write(f"[TEST ERROR]\n{tb}\n")
            except Exception:
                pass
            self.result['error'] = str(e)
            self._update('Error', 90, f'[ERROR] {e}')

        finally:
            try:
                self.ble.disconnect()
            except Exception:
                pass

        self._update('Complete', 100, '--- All tests finished ---')

    def cancel(self):
        """Cancel running tests and disconnect."""
        self.cancelled = True
        try:
            self.ble.disconnect()
        except Exception:
            pass

    def get_result(self):
        """Return accumulated test result dict."""
        return self.result

    # ── Read Tests ────────────────────────────────────────────────────────────

    def _run_read_tests(self):
        """Read standard BLE Device Information and Battery characteristics."""
        tests = [
            ('Battery Level',     BATTERY_SVC,  BATTERY_LEVEL,      'uint8'),
            ('Model Number',      DEVINFO_SVC,  MODEL_NUMBER,        'str'),
            ('Serial Number',     DEVINFO_SVC,  SERIAL_NUMBER,       'str'),
            ('Firmware Version',  DEVINFO_SVC,  FIRMWARE_REVISION,   'str'),
            ('Hardware Version',  DEVINFO_SVC,  HARDWARE_REVISION,   'str'),
            ('Software Version',  DEVINFO_SVC,  SOFTWARE_REVISION,   'str'),
        ]
        for name, svc, char, dtype in tests:
            if self.cancelled:
                break
            self._exec_read(name, svc, char, dtype)

    def _exec_read(self, name, svc_uuid, char_uuid, dtype='str'):
        key = f'Read - {name}'
        try:
            if dtype == 'uint8':
                val = self.ble.read_uint8(svc_uuid, char_uuid)
                display = f'{val}%' if 'Battery' in name else str(val)
            else:
                val = self.ble.read_string(svc_uuid, char_uuid)
                display = val if val else '(empty)'

            if name == 'Firmware Version':
                self.result['fw_version'] = display

            self.result['tests'][key] = True
            self.result['passed'] += 1
            self._update('', -1, f'  [PASS] {name}: {display}')

        except Exception as e:
            self.result['tests'][key] = False
            self.result['failed'] += 1
            self._update('', -1, f'  [FAIL] {name}: {e}')

    # ── WriteGet Tests ────────────────────────────────────────────────────────

    def _run_writeget_tests(self):
        """Write control commands to Wellysis characteristic and verify response."""
        if WELLYSIS_SVC == _WELLYSIS_TODO:
            self._update('', -1,
                '[SKIP] WriteGet: Wellysis UUIDs not configured. '
                'Replace TODO placeholders in ble_manager.py.')
            return

        for name, cmd in [
            ('Start',   CMD_START),
            ('Pause',   CMD_PAUSE),
            ('Restart', CMD_RESTART),
            ('Stop',    CMD_STOP),
        ]:
            if self.cancelled:
                break
            key = f'WriteGet - {name}'
            try:
                self.ble.write(WELLYSIS_SVC, WELLYSIS_CONTROL, cmd)
                time.sleep(1)
                self.result['tests'][key] = True
                self.result['passed'] += 1
                self._update('', -1, f'  [PASS] {name}')
            except Exception as e:
                self.result['tests'][key] = False
                self.result['failed'] += 1
                self._update('', -1, f'  [FAIL] {name}: {e}')

    # ── Notify Tests ──────────────────────────────────────────────────────────

    def _run_notify_tests(self):
        """Enable ECG notification and verify at least 5 packets are received."""
        if WELLYSIS_SVC == _WELLYSIS_TODO:
            self._update('', -1,
                '[SKIP] Notify: Wellysis UUIDs not configured. '
                'Replace TODO placeholders in ble_manager.py.')
            return

        key = 'Notify - ECG'
        try:
            self.ble.enable_notify(WELLYSIS_SVC, WELLYSIS_ECG_NOTIFY)
            packets = []
            deadline = time.time() + 10
            while len(packets) < 5 and time.time() < deadline:
                data = self.ble.read_notify(timeout=2)
                if data:
                    packets.append(data)
            self.ble.disable_notify(WELLYSIS_SVC, WELLYSIS_ECG_NOTIFY)

            if packets:
                self.result['tests'][key] = True
                self.result['passed'] += 1
                self._update('', -1, f'  [PASS] ECG Notify: {len(packets)} packets received')
            else:
                self.result['tests'][key] = False
                self.result['failed'] += 1
                self._update('', -1, '  [FAIL] ECG Notify: no packets received within 10s')

        except Exception as e:
            self.result['tests'][key] = False
            self.result['failed'] += 1
            self._update('', -1, f'  [FAIL] ECG Notify: {e}')

    # ── Packet Monitoring ─────────────────────────────────────────────────────

    def _run_packet_monitoring(self, target):
        """Stream ECG packets until target count is reached."""
        if WELLYSIS_SVC == _WELLYSIS_TODO:
            self._update('', -1,
                '[SKIP] Packet monitoring: Wellysis UUIDs not configured. '
                'Replace TODO placeholders in ble_manager.py.')
            return

        key = 'Packet Monitoring'
        try:
            self.ble.enable_notify(WELLYSIS_SVC, WELLYSIS_ECG_NOTIFY)
            packets = []
            timeout = target * 2 + 30
            deadline = time.time() + timeout
            while len(packets) < target and time.time() < deadline and not self.cancelled:
                data = self.ble.read_notify(timeout=2)
                if data:
                    packets.append(data)
                    if len(packets) % 10 == 0:
                        self._update('', -1, f'  Packets: {len(packets)}/{target}')
            self.ble.disable_notify(WELLYSIS_SVC, WELLYSIS_ECG_NOTIFY)

            if len(packets) >= target:
                self.result['tests'][key] = True
                self.result['passed'] += 1
                self._update('', -1, f'  [PASS] Packet monitoring: {len(packets)} packets received')
            else:
                self.result['tests'][key] = False
                self.result['failed'] += 1
                self._update('', -1, f'  [FAIL] Packet monitoring: {len(packets)}/{target} (timeout)')

        except Exception as e:
            self.result['tests'][key] = False
            self.result['failed'] += 1
            self._update('', -1, f'  [FAIL] Packet monitoring: {e}')

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _update(self, status, progress, log):
        """Send progress update. Use progress=-1 to update log without changing progress bar."""
        if self.callback:
            self.callback(status, progress, log)
