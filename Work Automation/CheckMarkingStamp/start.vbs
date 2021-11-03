Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c check_marking_stamp.bat"
oShell.Run strArgs, 0, false