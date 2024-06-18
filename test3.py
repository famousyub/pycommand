       
import telnetlib       
 
fg="""
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


commands =  [
    {
        "com1":"wl -i wl0 up"},
    
       { "com2":"wl -i wl0 phy_rxgainerr_5gl -4 -12 -12 -6"},
        {"com3":"wl -i wl0 phy_rxgainerr_5gm -4 -12 -12 -6"},
        {"com4":"wl -i wl0 phy_rxgainerr_5gh -7 -7 -8 -6"},
        
        
        {"com5":"wl -i wl0 down"},
        {"com6":"wl -i wl0 wrvar rxgainerr5ga0=60,60,57,0"},
       { "com7":"wl -i wl0 wrvar rxgainerr5ga1=24,24,0,0"},
        {"com8":"wl -i wl0 wrvar rxgainerr5ga2=24,24,31,0"},
        {"com9" :"wl -i wl0 wrvar rxgainerr5ga3=30,30,1,0"}
        
    
]       
HOST = "192.168.5.1"
user = "root"
password = "root"
 
with telnetlib.Telnet(HOST) as tn:
        tn.read_until(b"login: ", timeout=5)
        tn.write(user.encode('utf-8') + b"\n")
        tn.read_until(b"Password: ", timeout=5)
        tn.write(password.encode('utf-8') + b"\n")       
        output0 = tn.read_until(b"#", timeout=5).decode('utf-8')
        print(output0) 
        commond1 = "wl -i wl0 up"
        tn.write(commond1.encode('utf-8') + b"\n")
        output1 = tn.read_until(b"#", timeout=5).decode('utf-8') 
        print(output1)
        
        for cm in commands:
            print(cm)
            for k,v in cm.items() :
                tn.write(v.encode('utf-8') + b"\n")
                output_ = tn.read_until(b"#", timeout=5).decode('utf-8') 
                print(output_)
                
                
        