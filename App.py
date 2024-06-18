



     
import telnetlib 
import getpass 
# Set the Telnet server address and port number 


class App: 
    def __init__(self,telnet,host ,port  , ip):
        
        self .telnet = telnet 
        self.ip = ip
        self.host = host 
        self.port  = port 
        self.cmdf = f"ping -t  {ip}"
    def runn(self):
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
        
    
    
    def  sendcmd(self,hosst , c,username ,password):
        
        
        print(f"Logging in as '{username}'") 
        password = getpass.getpass()
        command = "dir"
        tn = telnetlib.Telnet(self.host, self.port)
        
        # Wait for the login prompt 
        tn.read_until(b"login: ",timeout=5) 

        # Enter the username and wait for the password prompt 
        tn.write(username.encode('ascii') + b"\n") 
        tn.read_until(b"Password: ",timeout=5) 
        # Enter the password and wait for the shell prompt 
        tn.write(password.encode('ascii') + b"\n") 
        tn.read_until(b"# ") 

        # Execute the command and wait for the output 
        tn.write(command.encode('ascii') + b"\n") 
        output = tn.read_until(b"# ") 

        # Print the output 
        print(output.decode('ascii')) 

        # Close the Telnet connection 
        tn.close() 
        
        



class Runner :
    
    def __init__(self,username, password , ip ,host,timeout=5,port=80):
        self.username = username 
        self.password =password 
        self.ip = ip 
        self.host =host 
        self.timeout= timeout
        self.port = port
    def runner_(self,hosting):
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
       
        
        with telnetlib.Telnet(self.host) as tn:
                tn.read_until(b"login: ", timeout=self.timeout)
                tn.write(self.username.encode('utf-8') + b"\n")
                tn.read_until(b"Password: ", timeout=self.timeout)
                tn.write(self.password.encode('utf-8') + b"\n")       
                output0 = tn.read_until(b"#", timeout=self.timeout).decode('utf-8')
                print(output0) 
                commond1 = "wl -i wl0 up"
                tn.write(commond1.encode('utf-8') + b"\n")
                output1 = tn.read_until(b"#", timeout=self.timeout).decode('utf-8') 
                print(output1)
                
                for cm in commands:
                    
                    for k,v in cm.items() :
                        if "#" in output0: 
                            tn.write(v.encode('utf-8') + b"\n")
                            output_ = tn.read_until(b"#", timeout=self.timeout).decode('utf-8') 
                            print(output_)
                            
                            
                        
                        
    



 


 





    
    
    

if __name__==  '__main__':
    import subprocess
    subprocess.call(["filereader.exe"])
    
    print("attenting ....")
    
    import time 
    time.sleep(1)
    
    
    host = "192.168.5.1"
    port  =80
    telnet = f"telnet {host}"
    ip ="192.168.5.1"
    
    HOST = "192.168.5.1"
    user = "root"
    password = "root"
    
    app =Runner(user,password,ip,HOST,5,port)
    app.runner_(telnet)
    
    
    import  time 
    
    
    time.sleep(10)
    
    
    
    print("enter key to quit \n")
    q = input("enter key .... \n />")
    

 
    
    
    #app.sendcmd("ping -t 192.168.5.1",telnet,"root","root")
    
    
    
    
       
    