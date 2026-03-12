"""
SDK Auto Tester - Mobile App (Material Design)
KivyMD-based UI for SDK validation testing on Android.
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image as KivyImage
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
import threading
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.test_runner import TestRunner
from core.ble_manager import BLEManager, IS_ANDROID


class HomeScreen(MDScreen):
    """Home screen - select BLE device and configure tests."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.selected_device_address = None
        self.selected_device_name = None

        layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        toolbar = MDTopAppBar(
            title="S-patch SDK",
            elevation=3,
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(toolbar)

        scroll = ScrollView()
        content = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # ── Product image header ──────────────────────────────────────────────
        img_card = MDCard(
            size_hint=(1, None),
            height=dp(150),
            md_bg_color=(0, 0, 0, 1),
            elevation=0,
            radius=[dp(8), dp(8), dp(8), dp(8)]
        )
        product_img = KivyImage(
            source='spatch_logo.png',
            size_hint=(1, 1),
            fit_mode='contain'
        )
        img_card.add_widget(product_img)
        content.add_widget(img_card)

        # ── BLE Device selection card ─────────────────────────────────────────
        device_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(340),
            padding=dp(15),
            spacing=dp(8),
            elevation=2
        )

        device_card.add_widget(MDLabel(
            text="BLE Device",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        ))

        self.selected_label = MDLabel(
            text="No device selected",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(24)
        )
        device_card.add_widget(self.selected_label)

        # Scrollable list of bonded (paired) devices
        self.device_list = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(100),
            spacing=dp(4)
        )
        dev_scroll = ScrollView(size_hint=(1, None), height=dp(90))
        dev_scroll.add_widget(self.device_list)
        device_card.add_widget(dev_scroll)

        refresh_btn = MDFlatButton(
            text="Refresh Paired Devices",
            size_hint=(1, None),
            height=dp(36)
        )
        refresh_btn.bind(on_press=lambda x: self.refresh_devices())
        device_card.add_widget(refresh_btn)

        # ── Serial number search ──────────────────────────────────────────────
        device_card.add_widget(MDLabel(
            text="Or enter serial number to scan & connect:",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(22)
        ))

        serial_row = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(8)
        )

        self.serial_input = MDTextField(
            hint_text="e.g.  610136",
            mode="rectangle",
            size_hint_x=0.7,
            size_hint_y=None,
            height=dp(50)
        )
        serial_row.add_widget(self.serial_input)

        find_btn = MDRaisedButton(
            text="Find",
            size_hint_x=0.3,
            size_hint_y=None,
            height=dp(50),
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        find_btn.bind(on_press=lambda x: self.find_by_serial())
        serial_row.add_widget(find_btn)

        device_card.add_widget(serial_row)

        content.add_widget(device_card)

        # ── Test settings card ────────────────────────────────────────────────
        settings_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(100),
            padding=dp(15),
            spacing=dp(10),
            elevation=2
        )

        settings_card.add_widget(MDLabel(
            text="Test Settings",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        ))

        self.packet_input = MDTextField(
            hint_text="Target Packet Count",
            text="60",
            mode="rectangle",
            input_filter="int",
            size_hint_y=None,
            height=dp(50)
        )
        settings_card.add_widget(self.packet_input)

        content.add_widget(settings_card)

        # ── Test items card ───────────────────────────────────────────────────
        test_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(250),
            padding=dp(15),
            spacing=dp(5),
            elevation=2
        )

        test_card.add_widget(MDLabel(
            text="Test Items",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        ))

        self.checkboxes = {}

        for test_id, test_name, default in [
            ('read', 'Read Test', True),
            ('writeget', 'WriteGet Test', True),
            ('notify', 'Notify Test', True),
            ('packet', 'Packet Monitoring', False)
        ]:
            item = OneLineAvatarIconListItem(text=test_name)
            checkbox = MDCheckbox(active=default, size_hint=(None, None), size=(dp(48), dp(48)))
            item.add_widget(checkbox)
            self.checkboxes[test_id] = checkbox
            test_card.add_widget(item)

        content.add_widget(test_card)

        # ── Start button ──────────────────────────────────────────────────────
        start_btn = MDRaisedButton(
            text="Start Test",
            size_hint=(1, None),
            height=dp(56),
            md_bg_color=(0.2, 0.8, 0.4, 1),
            elevation=3
        )
        start_btn.bind(on_press=self.start_test)
        content.add_widget(start_btn)

        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)

        # Auto-scan bonded devices on first load
        Clock.schedule_once(lambda dt: self.refresh_devices(), 0.5)

    def refresh_devices(self):
        """Reload bonded BLE devices and display as selectable buttons."""
        self.device_list.clear_widgets()
        try:
            ble = BLEManager()
            devices = ble.get_bonded_devices()
        except Exception:
            devices = []

        if not devices:
            self.device_list.add_widget(MDLabel(
                text="No paired BLE devices found.",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(30)
            ))
            return

        for name, address in devices:
            btn = MDFlatButton(
                text=f"{name}  ({address})",
                size_hint=(1, None),
                height=dp(44)
            )
            btn.bind(on_press=lambda x, n=name, a=address: self.select_device(n, a))
            self.device_list.add_widget(btn)

        # Expand list height to fit all devices
        self.device_list.height = dp(44) * len(devices)

    def find_by_serial(self):
        """Scan for nearby BLE devices and select the one matching the serial number.
        No pre-pairing required — the app scans and initiates connection directly.
        """
        serial = self.serial_input.text.strip()
        if not serial:
            self.selected_label.text = "Enter a serial number first."
            self.selected_label.theme_text_color = "Error"
            return

        if getattr(self, '_scanning', False):
            return  # prevent concurrent scans

        self._scanning = True
        self.selected_label.text = f"Scanning for '{serial}'..."
        self.selected_label.theme_text_color = "Secondary"

        def do_scan():
            result = None
            err = None
            try:
                ble = BLEManager()
                result = ble.scan_for_device(serial, timeout=10)
            except Exception as e:
                err = str(e)
            Clock.schedule_once(lambda _dt: self._on_scan_done(serial, result, err), 0)

        threading.Thread(target=do_scan, daemon=True).start()

    def _on_scan_done(self, serial, result, error):
        """Called on the main thread when BLE scan finishes."""
        self._scanning = False
        if error:
            self.selected_device_address = None
            self.selected_label.text = f"Scan error: {error}"
            self.selected_label.theme_text_color = "Error"
        elif result:
            name, address = result
            self.selected_device_name = name
            self.selected_device_address = address
            self.selected_label.text = f"Found: {name}"
            self.selected_label.theme_text_color = "Primary"
        else:
            self.selected_device_address = None
            self.selected_label.text = f"'{serial}' not found nearby. Is the device powered on?"
            self.selected_label.theme_text_color = "Error"

    def select_device(self, name, address):
        """Store selected device from paired list and clear serial input."""
        self.selected_device_name = name
        self.selected_device_address = address
        self.selected_label.text = f"Selected: {name}"
        self.selected_label.theme_text_color = "Primary"
        self.serial_input.text = ""  # clear serial field when picking from list

    def start_test(self, instance):
        """Validate selection and navigate to testing screen."""
        if not self.selected_device_address:
            self.selected_label.text = "Please select a BLE device first!"
            self.selected_label.theme_text_color = "Error"
            return

        config = {
            'device_address': self.selected_device_address,
            'device_name': self.selected_device_name,
            'read': self.checkboxes['read'].active,
            'writeget': self.checkboxes['writeget'].active,
            'notify': self.checkboxes['notify'].active,
            'packet_monitoring': self.checkboxes['packet'].active,
            'target_packets': int(self.packet_input.text) if self.packet_input.text else 60
        }

        app = MDApp.get_running_app()
        testing_screen = app.root.get_screen('testing')
        testing_screen.start_test(config)
        app.root.current = 'testing'


class TestingScreen(MDScreen):
    """Test progress screen - Material Design"""

    status_text = StringProperty('Initializing...')
    progress_value = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'testing'
        self._current_progress = 0

        layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(
            title="Test In Progress",
            elevation=3,
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(toolbar)

        card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            elevation=3,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        icon_box = MDBoxLayout(size_hint=(1, None), height=dp(80))
        self.status_icon = MDIcon(
            icon="cog",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.2, 0.6, 1, 1),
            font_size="64sp"
        )
        icon_box.add_widget(self.status_icon)
        card.add_widget(icon_box)

        self.status_label = MDLabel(
            text=self.status_text,
            halign="center",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        card.add_widget(self.status_label)

        self.progress_bar = MDProgressBar(
            value=0,
            type="determinate",
            size_hint=(1, None),
            height=dp(4)
        )
        card.add_widget(self.progress_bar)

        self.progress_label = MDLabel(
            text="0%",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )
        card.add_widget(self.progress_label)

        log_scroll = ScrollView(size_hint=(1, 1))
        self.log_label = MDLabel(
            text="",
            halign="left",
            valign="top",
            size_hint_y=None
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        log_scroll.add_widget(self.log_label)
        card.add_widget(log_scroll)

        cancel_btn = MDFlatButton(
            text="Cancel",
            size_hint=(1, None),
            height=dp(48)
        )
        cancel_btn.bind(on_press=self.cancel_test)
        card.add_widget(cancel_btn)

        layout.add_widget(card)
        self.add_widget(layout)
        self.test_runner = None

    def start_test(self, config):
        """Start the test."""
        self._current_progress = 0
        self.status_label.text = 'Starting test...'
        self.progress_bar.value = 0
        self.progress_label.text = '0%'
        self.log_label.text = ''
        self.status_icon.icon = "loading"
        self.status_icon.text_color = (0.2, 0.6, 1, 1)

        self.test_runner = TestRunner(config, self.update_callback)
        thread = threading.Thread(target=self.test_runner.run)
        thread.daemon = True
        thread.start()

    def update_callback(self, status, progress, log):
        """Update progress. progress=-1 means log-only (no progress bar change)."""
        def update_ui(dt):
            if status:
                self.status_label.text = status
            if progress >= 0:
                self._current_progress = progress
                self.progress_bar.value = progress
                self.progress_label.text = f'{int(progress)}%'

            if log:
                current_log = self.log_label.text
                new_log = current_log + '\n' + log if current_log else log
                lines = new_log.split('\n')
                if len(lines) > 20:
                    lines = lines[-20:]
                self.log_label.text = '\n'.join(lines)

            if self._current_progress >= 100:
                self.status_icon.icon = "check-circle"
                self.status_icon.text_color = (0.2, 0.8, 0.4, 1)
                Clock.schedule_once(self.show_result, 2)

        Clock.schedule_once(update_ui, 0)

    def show_result(self, dt):
        """Navigate to result screen."""
        app = MDApp.get_running_app()
        result_screen = app.root.get_screen('result')
        result_screen.set_result(self.test_runner.get_result())
        app.root.current = 'result'

    def cancel_test(self, instance):
        """Cancel the test."""
        if self.test_runner:
            self.test_runner.cancel()
        app = MDApp.get_running_app()
        app.root.current = 'home'


class ResultScreen(MDScreen):
    """Result screen - Material Design"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'result'

        layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(
            title="Test Results",
            elevation=3,
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(toolbar)

        scroll = ScrollView()
        content = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        summary_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(170),
            padding=dp(20),
            elevation=3
        )

        self.result_icon = MDIcon(
            icon="check-circle",
            halign="center",
            font_size="48sp",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.4, 1)
        )
        summary_card.add_widget(self.result_icon)

        self.result_label = MDLabel(
            text="",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(60)
        )
        summary_card.add_widget(self.result_label)

        self.fw_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        )
        summary_card.add_widget(self.fw_label)

        content.add_widget(summary_card)

        detail_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(300),
            padding=dp(20),
            elevation=2
        )

        detail_card.add_widget(MDLabel(
            text="Detailed Results",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        ))

        detail_scroll = ScrollView()
        self.detail_label = MDLabel(
            text="",
            halign="left",
            valign="top",
            size_hint_y=None
        )
        self.detail_label.bind(texture_size=self.detail_label.setter('size'))
        detail_scroll.add_widget(self.detail_label)
        detail_card.add_widget(detail_scroll)

        content.add_widget(detail_card)

        btn_box = MDBoxLayout(size_hint=(1, None), height=dp(56), spacing=dp(10))

        share_btn = MDRaisedButton(
            text="Share",
            md_bg_color=(0.2, 0.8, 0.4, 1)
        )
        share_btn.bind(on_press=self.share_result)
        btn_box.add_widget(share_btn)

        home_btn = MDRaisedButton(
            text="Home",
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        home_btn.bind(on_press=self.go_home)
        btn_box.add_widget(home_btn)

        content.add_widget(btn_box)

        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)
        self.result_data = None

    def set_result(self, result):
        """Set result data and update UI."""
        self.result_data = result

        if result.get('error'):
            self.result_icon.icon = "alert-circle"
            self.result_icon.text_color = (1, 0.3, 0.3, 1)
            self.result_label.text = "Error occurred"
            self.detail_label.text = result['error']
            self.fw_label.text = ""
            return

        passed = result.get('passed', 0)
        failed = result.get('failed', 0)
        total = passed + failed

        if failed == 0 and total > 0:
            self.result_icon.icon = "check-circle"
            self.result_icon.text_color = (0.2, 0.8, 0.4, 1)
        elif total == 0:
            self.result_icon.icon = "alert-circle"
            self.result_icon.text_color = (1, 0.6, 0, 1)
        else:
            self.result_icon.icon = "alert-circle"
            self.result_icon.text_color = (1, 0.3, 0.3, 1)

        success_rate = int((passed / total) * 100) if total > 0 else 0
        self.result_label.text = f'Passed: {passed}/{total}\nPass rate: {success_rate}%'

        fw = result.get('fw_version')
        self.fw_label.text = f'Firmware: {fw}' if fw else ''

        details = []
        for test_name, test_result in result.get('tests', {}).items():
            icon = 'PASS' if test_result else 'FAIL'
            details.append(f'[{icon}] {test_name}')

        self.detail_label.text = '\n'.join(details) if details else 'No test results'

    def share_result(self, instance):
        """Share results via Android share intent."""
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')

            result = self.result_data or {}
            passed = result.get('passed', 0)
            failed = result.get('failed', 0)
            fw = result.get('fw_version', 'N/A')

            text = (
                f"SDK Auto Tester Results\n"
                f"Firmware: {fw}\n"
                f"Passed: {passed}  Failed: {failed}\n"
                f"Pass rate: {int(passed/(passed+failed)*100) if passed+failed else 0}%\n\n"
            )
            for name, res in result.get('tests', {}).items():
                text += f"[{'PASS' if res else 'FAIL'}] {name}\n"

            intent = Intent()
            intent.setAction(Intent.ACTION_SEND)
            intent.putExtra(Intent.EXTRA_TEXT, String(text))
            intent.setType('text/plain')

            currentActivity = PythonActivity.mActivity
            currentActivity.startActivity(Intent.createChooser(intent, String('Share Results')))
        except Exception:
            pass

    def go_home(self, instance):
        """Return to home screen."""
        app = MDApp.get_running_app()
        app.root.current = 'home'


class SDKAutoTesterApp(MDApp):
    """Main app - Material Design"""

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = MDScreenManager()
        sm.add_widget(HomeScreen())
        sm.add_widget(TestingScreen())
        sm.add_widget(ResultScreen())
        return sm

    def on_start(self):
        """Request Bluetooth runtime permissions on Android 12+ at app start."""
        if IS_ANDROID:
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.BLUETOOTH_SCAN,
                    Permission.BLUETOOTH_CONNECT,
                    Permission.ACCESS_FINE_LOCATION,
                ])
            except Exception:
                pass


if __name__ == '__main__':
    SDKAutoTesterApp().run()
