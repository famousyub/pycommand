import  os 

import  sys 




cmd="""

wl -i wl0 up
wl -i wl0 phy_rxgainerr_5gl -4 -12 -12 -6
wl -i wl0 phy_rxgainerr_5gm -4 -12 -12 -6
wl -i wl0 phy_rxgainerr_5gh -7 -7 -8 -6
wl -i wl0 down

wl -i wl0 wrvar rxgainerr5ga0=60,60,57,0
wl -i wl0 wrvar rxgainerr5ga1=24,24,0,0
wl -i wl0 wrvar rxgainerr5ga2=24,24,31,0
wl -i wl0 wrvar rxgainerr5ga3=30,30,1,0
"""

cmd2 ="dir"

os.system(cmd2)

