@ECHO OFF
ECHO Installing Dependencies for Get in My Cart app...

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

py -m pip install --user virtualenv

py -m venv env

cmd /c "cd /d %CD%\env\Scripts & activate & cd /d    %CD% & pip install -r requirements.txt & pip install downloads\PyAudio-0.2.11-cp38-cp38-win_amd64.whl"
