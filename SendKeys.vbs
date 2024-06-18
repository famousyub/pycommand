set OBJECT=WScript.CreateObject("WScript.Shell")
WScript.sleep  250 
OBJECT.SendKeys "root{ENTER}" 
WScript.sleep 1000 
OBJECT.SendKeys "root{ENTER}"
WScript.sleep 150 
OBJECT.SendKeys "wl -i wl0 up{ENTER}" 
WScript.sleep 250 



OBJECT.SendKeys "wl -i wl0 up{ENTER}" 
WScript.sleep 1000 

OBJECT.SendKeys "wl -i wl0 phy_rxgainerr_5gl -4 -12 -12 -6{ENTER}" 
WScript.sleep 1000 

OBJECT.SendKeys "wl -i wl0 phy_rxgainerr_5gm -4 -12 -12 -6{ENTER}" 
WScript.sleep 1000 

OBJECT.SendKeys "wl -i wl0 phy_rxgainerr_5gh -7 -7 -8 -6{ENTER}" 
WScript.sleep 1000 


OBJECT.SendKeys "wl -i wl0 down{ENTER}" 
WScript.sleep 1000 


OBJECT.SendKeys "wl -i wl0 wrvar rxgainerr5ga0=60,60,57,0{ENTER}" 
WScript.sleep 1000 



OBJECT.SendKeys "wl -i wl0 wrvar rxgainerr5ga1=24,24,0,0{ENTER}" 
WScript.sleep 1000 

OBJECT.SendKeys "wl -i wl0 wrvar rxgainerr5ga2=24,24,31,0{ENTER}" 
WScript.sleep 1000 


OBJECT.SendKeys "wl -i wl0 wrvar rxgainerr5ga3=30,30,1,0{ENTER}"
WScript.sleep 1000


