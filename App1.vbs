set OBJECT=WScript.CreateObject("WScript.Shell")
WScript.sleep 150 
OBJECT.SendKeys "root{ENTER}" 
WScript.sleep 150 
OBJECT.SendKeys "root{ENTER}"
WScript.sleep 250 
OBJECT.SendKeys "wl -i wl0 up" 
WScript.sleep 520