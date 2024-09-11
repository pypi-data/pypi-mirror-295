@echo off

set "NO_VERIFY_FLAG=--no-verify-java"

set "BASEPATH=%~dp0"
set "ENV_DIR=%BASEPATH%"

REM Remove the trailing backslash from ENV_DIR
if "%ENV_DIR:~-1%"=="\" set "ENV_DIR=%ENV_DIR:~0,-1%"

set "args=%*"
set "scripts="converter-frontend.bat" "tiling-advisor.bat" "converter-fm2lm.bat" "converter-backend.bat" "converter-packer.bat" "converter-main.bat""

for %%s in (%scripts%) do (
    if not exist "%%~s" (
        call :warning "Script '%%~s' does not exist in %ENV_DIR%."
    )
)

REM Check for the flag in command line arguments
if "%~1" == "%NO_VERIFY_FLAG%" (
    set "args=!args:%NO_VERIFY_FLAG%=!"
) else (
		where java >nul 2>nul
		if %errorlevel% neq 0 (
				call :warning "It seems that Java is not installed. Please make sure Java 17 is set up correctly."
				call :warning "You can set JAVA_HOME environment variable to point to the directory where Java 17 is installed."
				call :warning "Example: "
                call :warning "  setx JAVA_HOME \path\to\java\17"
                call :warning "  Open a new command line and type:"
                call :warning "  setx PATH \"%%PATH%%;%%JAVA_HOME%%\""
        )else (
			for /f "tokens=*" %%a in ('java -version 2^>^&1') do (
				echo %%a | findstr /c:"17." > nul
				if  errorlevel 1 (
                    call :warning "Java 17 not found!"
                    call :warning "Please make sure you have Java 17 installed and configured correctly."
                    call :warning "You can set JAVA_HOME environment variable to point to the directory where Java 17 is installed."
                    call :warning "Example: "
                    call :warning "  setx JAVA_HOME \path\to\java\17"
                    call :warning "  Open a new command line and type:"
                    call :warning "  setx PATH \"%%PATH%%;%%JAVA_HOME%%\""
                    call :warning "You can suppress this warning by using the '--no-verify-java' flag."
				)
			)
		)
	)
call %ENV_DIR%\converter-main.bat --env-dir %ENV_DIR% %args%
goto :eof

:warning
    for /f "tokens=1-5 delims=/: " %%a in ("%date% %time%") do (
        set day=%%a
        set month=%%b
        set year=%%c
        set hour=%%d
        set minute=%%e
    )
    echo %year%-%month%-%day% %hour%:%minute% WARNING: ^%~1
goto :eof





