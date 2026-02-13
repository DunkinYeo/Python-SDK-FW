@echo off
REM SDK 검증 테스트 실행 - Windows용

TITLE SDK 검증 테스트

color 0B
echo ============================================================
echo 🚀 SDK 검증 테스트
echo ============================================================
echo.

REM 전체 테스트 스위트 실행
if exist "scripts\run_full_test_suite.sh" (
    echo 전체 테스트 스위트를 실행합니다...
    echo.
    bash scripts/run_full_test_suite.sh
) else (
    echo ❌ 테스트 스크립트를 찾을 수 없습니다.
    echo.
    pause
)
