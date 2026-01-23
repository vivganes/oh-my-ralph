@echo off
echo ========================================
echo Building ralphy
echo ========================================
echo.

echo Step 1: Running tests...
call run_tests.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo BUILD FAILED: Tests did not pass
    echo ========================================
    exit /b 1
)

echo.
echo Step 2: Building package...
python -m pip install --upgrade build
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install build tools
    exit /b 1
)

python -m build
if %ERRORLEVEL% NEQ 0 (
    echo Failed to build package
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL
echo ========================================
echo Package built in dist\ directory
echo.
