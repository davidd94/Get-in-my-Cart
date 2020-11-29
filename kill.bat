@ECHO OFF
ECHO Killing script and cleaning up...

taskkill /F /IM chrome.exe

SET FOLDER=%UserProfile%\AppData\Local\pyppeteer\pyppeteer\.dev_profile

CD /
DEL /F/Q/S "%FOLDER%" > NUL
RMDIR /Q/S "%FOLDER%"
EXIT
