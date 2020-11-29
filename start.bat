@ECHO OFF
ECHO Running Get in My Cart app...

cmd /c "cd /d %CD%\env\Scripts & activate & cd /d    %CD% & python getinmycart.py"
