"""
SDK Auto Tester - Mobile App (Material Design)
KivyMD를 사용한 예쁜 UI
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
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
import threading
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.test_runner import TestRunner


class HomeScreen(MDScreen):
    """홈 화면 - Material Design"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'

        # 메인 레이아웃
        layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # 상단 앱바
        toolbar = MDTopAppBar(
            title="SDK 자동 검증기",
            elevation=3,
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(toolbar)

        # 스크롤 뷰
        scroll = ScrollView()
        content = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # 설정 카드
        config_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(220),
            padding=dp(15),
            spacing=dp(10),
            elevation=2
        )

        config_card.add_widget(MDLabel(
            text="테스트 설정",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        ))

        # BLE 시리얼 입력
        self.serial_input = MDTextField(
            hint_text="BLE 시리얼 넘버",
            text="610031",
            mode="rectangle",
            size_hint_y=None,
            height=dp(50)
        )
        config_card.add_widget(self.serial_input)

        # 패킷 수 입력
        self.packet_input = MDTextField(
            hint_text="타겟 패킷 수",
            text="60",
            mode="rectangle",
            input_filter="int",
            size_hint_y=None,
            height=dp(50)
        )
        config_card.add_widget(self.packet_input)

        content.add_widget(config_card)

        # 테스트 항목 카드
        test_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(250),
            padding=dp(15),
            spacing=dp(5),
            elevation=2
        )

        test_card.add_widget(MDLabel(
            text="테스트 항목",
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        ))

        # 체크박스 리스트
        self.checkboxes = {}

        for test_id, test_name, default in [
            ('read', 'Read 테스트', True),
            ('writeget', 'WriteGet 테스트', True),
            ('notify', 'Notify 테스트', True),
            ('packet', '패킷 모니터링', False)
        ]:
            item = OneLineAvatarIconListItem(text=test_name)
            checkbox = MDCheckbox(active=default, size_hint=(None, None), size=(dp(48), dp(48)))
            item.add_widget(checkbox)
            self.checkboxes[test_id] = checkbox
            test_card.add_widget(item)

        content.add_widget(test_card)

        # 시작 버튼 (큰 FAB 스타일)
        start_btn = MDRaisedButton(
            text="테스트 시작",
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

    def start_test(self, instance):
        """테스트 시작"""
        config = {
            'serial': self.serial_input.text,
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
    """테스트 진행 화면 - Material Design"""

    status_text = StringProperty('준비 중...')
    progress_value = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'testing'

        layout = MDBoxLayout(orientation='vertical')

        # 상단 앱바
        toolbar = MDTopAppBar(
            title="테스트 진행 중",
            elevation=3,
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(toolbar)

        # 컨텐츠 카드
        card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            elevation=3,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # 상태 아이콘 (중앙)
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

        # 상태 텍스트
        self.status_label = MDLabel(
            text=self.status_text,
            halign="center",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        card.add_widget(self.status_label)

        # 진행률 바
        self.progress_bar = MDProgressBar(
            value=0,
            type="determinate",
            size_hint=(1, None),
            height=dp(4)
        )
        card.add_widget(self.progress_bar)

        # 진행률 텍스트
        self.progress_label = MDLabel(
            text="0%",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )
        card.add_widget(self.progress_label)

        # 로그 스크롤뷰
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

        # 취소 버튼
        cancel_btn = MDFlatButton(
            text="취소",
            size_hint=(1, None),
            height=dp(48)
        )
        cancel_btn.bind(on_press=self.cancel_test)
        card.add_widget(cancel_btn)

        layout.add_widget(card)
        self.add_widget(layout)
        self.test_runner = None

    def start_test(self, config):
        """테스트 시작"""
        self.status_text = '테스트 시작 중...'
        self.progress_value = 0
        self.progress_bar.value = 0
        self.log_label.text = ''

        # 아이콘 회전 애니메이션
        self.status_icon.icon = "loading"

        self.test_runner = TestRunner(config, self.update_callback)
        thread = threading.Thread(target=self.test_runner.run)
        thread.daemon = True
        thread.start()

    def update_callback(self, status, progress, log):
        """진행 상황 업데이트"""
        def update_ui(dt):
            self.status_label.text = status
            self.progress_bar.value = progress
            self.progress_label.text = f'{int(progress)}%'

            # 로그 추가
            current_log = self.log_label.text
            new_log = current_log + '\n' + log if current_log else log
            lines = new_log.split('\n')
            if len(lines) > 15:
                lines = lines[-15:]
            self.log_label.text = '\n'.join(lines)

            # 완료 시 아이콘 변경
            if progress >= 100:
                self.status_icon.icon = "check-circle"
                self.status_icon.text_color = (0.2, 0.8, 0.4, 1)
                Clock.schedule_once(self.show_result, 2)

        Clock.schedule_once(update_ui, 0)

    def show_result(self, dt):
        """결과 화면으로 이동"""
        app = MDApp.get_running_app()
        result_screen = app.root.get_screen('result')
        result_screen.set_result(self.test_runner.get_result())
        app.root.current = 'result'

    def cancel_test(self, instance):
        """테스트 취소"""
        if self.test_runner:
            self.test_runner.cancel()
        app = MDApp.get_running_app()
        app.root.current = 'home'


class ResultScreen(MDScreen):
    """결과 화면 - Material Design"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'result'

        layout = MDBoxLayout(orientation='vertical')

        # 상단 앱바
        toolbar = MDTopAppBar(
            title="테스트 결과",
            elevation=3,
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(toolbar)

        # 스크롤뷰
        scroll = ScrollView()
        content = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # 결과 요약 카드
        summary_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(150),
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

        content.add_widget(summary_card)

        # 상세 결과 카드
        detail_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(300),
            padding=dp(20),
            elevation=2
        )

        detail_card.add_widget(MDLabel(
            text="상세 결과",
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

        # 버튼들
        btn_box = MDBoxLayout(size_hint=(1, None), height=dp(56), spacing=dp(10))

        share_btn = MDRaisedButton(
            text="공유",
            md_bg_color=(0.2, 0.8, 0.4, 1)
        )
        share_btn.bind(on_press=self.share_result)
        btn_box.add_widget(share_btn)

        home_btn = MDRaisedButton(
            text="홈으로",
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
        """결과 설정"""
        self.result_data = result

        # 오류 체크
        if result.get('error'):
            self.result_icon.icon = "alert-circle"
            self.result_icon.text_color = (1, 0.3, 0.3, 1)
            self.result_label.text = "오류 발생"
            self.detail_label.text = result['error']
            return

        passed = result.get('passed', 0)
        failed = result.get('failed', 0)
        total = passed + failed

        # 아이콘 및 색상 설정
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
        self.result_label.text = f'성공: {passed}/{total}\n성공률: {success_rate}%'

        # 상세 결과
        details = []
        for test_name, test_result in result.get('tests', {}).items():
            icon = '✅' if test_result else '❌'
            details.append(f'{icon} {test_name}')

        self.detail_label.text = '\n'.join(details) if details else '테스트 결과 없음'

    def share_result(self, instance):
        """결과 공유"""
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')

            intent = Intent()
            intent.setAction(Intent.ACTION_SEND)
            intent.putExtra(Intent.EXTRA_TEXT, String(str(self.result_data)))
            intent.setType('text/plain')

            currentActivity = PythonActivity.mActivity
            currentActivity.startActivity(Intent.createChooser(intent, String('결과 공유')))
        except:
            print('공유 기능은 Android에서만 작동합니다')

    def go_home(self, instance):
        """홈으로 이동"""
        app = MDApp.get_running_app()
        app.root.current = 'home'


class SDKAutoTesterApp(MDApp):
    """메인 앱 - Material Design"""

    def build(self):
        """앱 빌드"""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = MDScreenManager()
        sm.add_widget(HomeScreen())
        sm.add_widget(TestingScreen())
        sm.add_widget(ResultScreen())
        return sm


if __name__ == '__main__':
    SDKAutoTesterApp().run()
