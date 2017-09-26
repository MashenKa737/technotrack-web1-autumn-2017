# -*- coding: utf-8 -*-
import socket
import sys
import os

def show_home(informLines) :
    for string in informLines[1:] :
        if string.startswith ('User-Agent:') :
            return bytes("HTTP/1.1 200 Ok\r\n\r\n" + 
                         "Hello, mister!\nYou are:" + 
                         string[11:], 'utf-8')
    else :
        return bytes("HTTP/1.1 404 Not found\r\n\r\n" +
                     "Hello, unknown mister!\n", 'utf-8')
    
def show_media(path) :
    #print (os.getcwd())
    return bytes("HTTP/1.1 200 Ok\r\n\r\n" + 
                 '\n'.join(os.listdir(path)), 'utf-8')
 
def show_files(requestPath) :
    path = "../files/" + requestPath[7:]
    if os.path.exists(path) :
        if os.path.isfile(path) :
            print (path + " is file")
            fileToOpen = open(path)
            return bytes("HTTP/1.1 200 Ok\r\n\r\n" + 
                         fileToOpen.read(), 'utf-8')
        elif os.path.isdir(path) :
            print (path + " is dir")
            return show_media(path)        
    return bytes("HTTP/1.1 404 Not found\r\n\r\n" +
                 "File not found\n", 'utf-8')
    
def get_response(request):
    informLines = str(request, 'utf-8').splitlines()
    if informLines[0].startswith ('GET') :
        getRequests = informLines[0].split(" ")[1]
        print (getRequests)
        if getRequests == '/' :
            return show_home(informLines)    
        elif getRequests == "/media" or getRequests == "/media/" :
            return show_media("../files")
        elif getRequests.startswith('/media/') :
            return show_files(getRequests)
        elif getRequests == "/test" or getRequests == "/test/" :
            return request
        else :
            return bytes("HTTP/1.1 404 Not found\r\n\r\n" + 
                         "Page not found\n", 'utf-8')
    else :
        return bytes("HTTP/1.1 404 Not found\r\n\r\n" + 
                     "I'm not ready for this request, sorry(((\n", 'utf-8')
        


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # bind server to adress localhost:8000
server_socket.listen(0)  # enable a server to accept a reasonable number of connections 

print ('Started')

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print ('Got new client', client_socket.getsockname())  # print the client’s own address
        request_string = client_socket.recv(2048)  # receive 2Kb block of data about client
        client_socket.send(get_response(request_string))  # client send request to the server
        client_socket.close()
    except KeyboardInterrupt:  # we are there if server is interrupted
        print ('Stopped')
        server_socket.close()  # mark the server socket closed
        sys.exit()
