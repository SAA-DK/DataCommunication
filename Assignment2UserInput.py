import re
from socket import *
import ssl

###
#
# @titel		Assignment 2 - SMTP			
#
# @author		Sebastian A. Almfort
# @version		Python 3.9.11
# @date			Marts 2022
# @Institute	DTU (Technical University of Denmark)
# @course		62577 Data Communication
#
###


# Intro message
print("""Before continueing the following thing should be prepared:
	* The right settings in the used gmail should be set up
	* Username and Password for the used gmail in Base 64. Use following link: https://www.base64decode.org/
	* The Mailadress of the gmail that is used
	* The mailadress of the recieving person  
	
	And the last ting, REMEMBER to follow the instruktions.\n""")


msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
#Fill in start
mailserver = 'smtp.gmail.com'
port = 587
#Fill in end

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket.connect((mailserver,port))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

tlsStart = 'STARTTLS\r\n'
clientSocket.send(tlsStart.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

# Send HELO command and print server response.
#heloCommand = 'EHLO localhost\r\n' # EHLO for extended SMTP
heloCommand = input()
#print(heloCommand)

if heloCommand == 'EHLO localhost':
	heloCommand = 'EHLO localhost\r\n'
	clientSocket.send(heloCommand.encode())
	recv1 = clientSocket.recv(1024).decode()
	print(recv1)	
elif heloCommand == 'HELO localhost':
	heloCommand = 'HELO localhost\r\n'
	clientSocket.send(heloCommand.encode())
	recv1 = clientSocket.recv(1024).decode()
	print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Start TLS connection
tlsStart = 'STARTTLS\r\n'
clientSocket.send(tlsStart.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

# Use SSL to wrap the socket
scc = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)


#Authentication layer for tcl
authText = 'AUTH LOGIN \r\n' 
print('AUTH LOGIN\r\n')
scc.send(authText.encode())
recv = scc.recv(1024).decode()
print(recv)

print("Username is: \n")
usernameInput = input()
username = ''+usernameInput+'\r\n' 
scc.send(username.encode())
recv2 = scc.recv(1024).decode()
print(recv2)

print("Password is: ")
passwdInput = input()
passwd = ''+passwdInput+'\r\n'
#passwd = 'QW5uM09HMTVBazI4MDIyMQ== \r\n'
scc.send(passwd.encode())
recv2 = scc.recv(1024).decode()
print(recv2)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
# Fill in start
print('Which mailadress is the mail from? ')
mailAdrr = input()
mailFromClient = 'MAIL FROM: '+mailAdrr+'\r\n'
scc.send(mailFromClient.encode())
recv2 = scc.recv(1024).decode()
print(recv2)
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
print('Which RCPT is it send to? ')
rcptAdrr = input()
rcptTo = 'RCPT TO: '+rcptAdrr+'\r\n'
scc.send(rcptTo.encode())
recv3 = scc.recv(1024).decode()
print(recv3)
# Fill in end

# Subject of the mail
print('What is the subject of the mail? ')
subject = input()


# Send DATA command and print server response.
# Fill in start
Data = 'DATA\r\n'
print(Data)
scc.send(Data.encode())
recv4 = scc.recv(1024).decode()
print(recv4)
# Fill in end



# Send message data.
# Fill in start 
# To, From and subject in mail
msg = '''From: From Person '''+mailAdrr+'''
To: To Person '''+rcptAdrr+'''
Subject: '''+subject+'''
\r\n '''
scc.send(msg.encode())

# The mail text
while msg != '.':
    	msg = input()
    	scc.send(msg.encode())
    	space = '\n'
    	scc.send(space.encode())
	
endmsg = "\r\n.\r\n"
scc.send(endmsg.encode())
recv1 = scc.recv(1024).decode()
print(recv1)


# Ending mail
print('End mail? ')
quit = input()
Quit = 'QUIT\r\n'
if quit == 'QUIT':
	scc.send(Quit.encode())
	recv1 = scc.recv(1024).decode()
	print(recv1)
