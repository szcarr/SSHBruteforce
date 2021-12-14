for /r D:\folder %%a in (*) do if "%%~nxa"=="SSHHackMain.py" set p=%%~dpa
if defined p (
echo %p%
) else (
echo File not found
)