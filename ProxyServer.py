from socket import *
import sys

buffersize = 4096

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# The proxy server is listening at 8888 
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)


#C:\Users\Disra\Documents\Hub\School\Computer Networks\1- Web Proxy
#python3 ProxyServer.py 127.0.0.1
#http://127.0.0.1:8888/yahoo.com

while 1:
    fileExist = False
    # Strat receiving data from the client
    print('Ready to serve...')
    
    ## FILL IN HERE...
    ##Accpets the connection
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    
    #Grabs data from request
    message = tcpCliSock.recv(1024).decode()## FILL IN HERE...
    
    # Extract the filename from the given message
    ## FILL IN HERE...
    
    #Split first line
    split_message = message.split(" ")
    
    #Grab URL part from list and remove leading '/'
    resource_name = split_message[1].partition("/")[2]

    #1a Prints resource requested
    print('Resource name: ' + resource_name)
    
    if resource_name == '': #Edge case: Resource not found
        sys.exit('Error: Resource name not found.')

    #Formatting name
    host = 'www.' + resource_name
    #Formatting GET request
    get_req = 'GET '+'http://'+host+' HTTP/1.0\n\n'
    
    filetouse = resource_name + '.txt' ## FILL IN HERE...
    try:
        # Check wether the file exist in the cache
        ## FILL IN HERE...
        #Attempt to open file
        with open(filetouse, 'rb') as f:
            cached_page = f.read()
        
        fileExist = True
        # ProxyServer finds a cache hit and generates a response message
        ## FILL IN HERE.
        print('Sending cached page..')
        tcpCliSock.sendall(cached_page)
            
        
    # Error handling for file not found in cache, need to talk to origin server and get the file
    except IOError:
        print('Resource not in cache')
        if fileExist == False:
            #FILL IN HERE...
            try: ##Creating Request to resource##
                
                #Connecting
                res_sock = socket(AF_INET, SOCK_STREAM)
                res_sock.connect((host, 80))
                
                #Send request
                print('Fetching page..')
                res_sock.sendall(get_req.encode())
                
                res_message = res_sock.recv(buffersize)
                res_sock.close()
                
                if res_message == '':
                    raise Exception('Error: No data received')
                    break
                
                #Sending requested page to client
                print('Sending page to client..')
                tcpCliSock.sendall(res_message)
                
                #Open file for writing or create if doesn't exist
                print('Writing page to cache..')
                with open(filetouse, 'wb') as f:
                    f.write(res_message)           
                
            except IOError:
                print('Failed to write to file')
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n".encode())                             
            tcpCliSock.send("Content-Type:text/html\r\n".encode())
            tcpCliSock.send("\r\n".encode())
    # Close the client and the server sockets
    tcpCliSock.close() 
tcpSerSock.close()