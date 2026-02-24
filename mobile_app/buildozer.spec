[app]

# 앱 제목
title = SDK Auto Tester

# 패키지 이름
package.name = sdkautotester

# 패키지 도메인
package.domain = com.wellysis

# 소스 디렉토리
source.dir = .

# 소스 파일 패턴
source.include_exts = py,png,jpg,kv,atlas

# 버전
version = 1.0.0

# 요구사항 (Android 호환 패키지만 포함)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,pillow

# 앱 아이콘 (선택)
#icon.filename = %(source.dir)s/data/icon.png

# Presplash (선택)
#presplash.filename = %(source.dir)s/data/presplash.png

# 앱 방향 (landscape, portrait, all)
orientation = portrait

# 전체화면
fullscreen = 0

# 안드로이드 권한
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android API 버전
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# Android 아키텍처 (메모리 절약을 위해 arm64-v8a만 빌드)
android.archs = arm64-v8a

# 로그 활성화
log_level = 2

# 디버그 모드
debug = 1

[buildozer]

# 빌드 디렉토리
build_dir = ./.buildozer

# Bin 디렉토리
bin_dir = ./bin

# 로그 레벨
log_level = 2

# 경고 무시
warn_on_root = 1
