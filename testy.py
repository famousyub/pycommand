import getpass
import telnetlib

""" In the next step we will set the host whether it will be local or 
any other IP but it should be reachable in order to work it correctly. """

HOST = "192.168.5.1"

""" In the next step we will input the user to enter the remote 
account name or username or login depending on the model and device 
and stored it in a variable name user in this example. 
And also we will input the password from user and stored in a 
variable named password in this example. """

user = input("Enter your remote account: ")
password = getpass.getpass()

""" In next step we are using telnet class and pass HOST as an 
argument to it and it will open a telnet connection or socket 
with the target device. """

tn = telnetlib.Telnet(HOST)

"""In next step, we will read until the occurrence of that word which
 is mentioned in the function argument. In this case this word is "login".
 And this word, we will write the word that user entered above in the code """

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")

"""If there is any password entered by user then it will read until the 
occurrence of word password and then after that it will write the password
what user entered. """

if password:
  tn.read_until(b"Password: ")
  tn.write(password.encode('ascii') + b"\n")
tn.write(b"ls\n")
print(tn.read_all().decode('ascii'))