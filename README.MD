# Programs you must install prior using this application

1. Install Python version 3.7+ that includes Pip by visiting https://www.python.org/downloads/
2. Download "swig.exe" from http://www.swig.org/download.html and extract the folder anywhere. Make sure to set that folder path within Window's (User) environment variable.
3. Download "ffmpeg" from https://www.gyan.dev/ffmpeg/builds/ and extra the folder anywhere. Make sure to set that folder path within Window's (User) environment variable.
4. Download and install VS Build Tools. Once installed, use the program to get Microsoft C++ package.
5. Install Python dependencies and PyAudio by running "install.bat" file. This must be done last as "swig.exe" and Microsoft C++ is required to be installed before dependency installation!

# Usage
1. Git clone the repo
2. Install dependencies by executing `install.bat`
3. Setup the `.env` file with the proper info
4. Modify the item list within `settings.py`. You may also change `headless` to `False` if you want to see the actual chrome browsers at work otherwise leave it `True` to hide them
5. Run the script using `start.bat`
6. To clean up or if the app hangs when attempting to close/stop it, you need to run `kill.bat` to close all hidden chrome.exe's

# NOTES
1. Goodbyerecaptcha solving recaptcha test has been disabled due to the library being created as one whole asyncio task. Unable to get it to work as a nested asyncio task. By avoiding recaptcha test, I have added sleep (varies between 1-3 seconds) between page navigation and between entering login details to avoid being flagged as a bot.
