#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# Author:       Leeza Kotze                                   
# Created:      January 2022                                                    
# Description:  Python Programming - Project 1 
#               SERVER PROGRAM
#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


import socket
import mysql.connector

#Create Server class and its function
class Server:
    def __init__(self, port, listen = 5, timeout = 10, buf = 4096, queueSize = 10):
        self.port = port
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
        self.listen = listen                                         
        self.timeout = timeout
        self.bufsize = buf

    def send(self, client_conn, string):
        print(f'SEND THIS: {string}')
        client_conn.send(bytes(string, encoding = "ascii"))
    
    def recv(self, client_conn):
        return str(client_conn.recv(self.bufsize), encoding = "ascii")
        

    def run(self):       

        self.soc.bind(("127.0.0.1", self.port))     # Bind to the port
        self.soc.listen(self.listen)                # Put the socket into listening mode
        print(f"Server started...\nPort:{self.port} \n")
        
        client_conn, address = self.soc.accept() # Accept connection with the client
        print(f"Connection from {address} has been established.")
          
        while True:
            print("start of while loop")
                
               
                
            sql_conn = mysql.connector.connect(
                                    user       = "videoStoreUser"
                                    ,password   = "Qweasd1"
                                    ,host       = "localhost"
                                    ,database   = "video_store"
                                    )  
                            
                
            #Create a new 'cursor' object with every request. Connection to MySql db
            cursor = sql_conn.cursor()
                         
            #data received from client. We use an array to specify which option the client selected
                
            data = server.recv(client_conn)
            dataArray = data.split(',')
            
            #The option selected by client
            print(f'Client sent this request: {dataArray[0]}')
                
                
            #Check if customer exists for use of option 1
            if dataArray[0] == 'checkIfCustomerExists':
                cursor.execute(f"SELECT custId, fname, sname, address, phone FROM customers WHERE phone = '{dataArray[1]}';")
                rows = cursor.fetchall()
                
                try: #Errorhandling              
                    if not rows: #Check if variable exists
                        response = "customerDoesNotExist"
                    else:
                        for row in rows:
                            custId  = row[0]     #"custId"
                            fname   = row[1]     #"fname"
                            sname   = row[2]     #"sname"
                            address = row[3]     #"address"                       
                        
                        response = f"customerExists,{fname},{sname},{address},{custId}"
                except:
                    print("Error: Unable to fetch data.")
            #OPTION 1       
            elif dataArray[0] == 'registerNewCustomer':
                cursor.execute(f"INSERT INTO customers (fname,sname,address,phone) VALUES('{dataArray[1]}', '{dataArray[2]}','{dataArray[3]}','{dataArray[4]}');")
                response = "customerRegistered"
                    
            #OPTION 2
            elif dataArray[0] == 'registerMovie':
                print(f"registerMovie selected sucessfully. Data to be processed: {dataArray[1]}, {dataArray[2]}")
                cursor.execute(f"SELECT videoVer FROM videos WHERE vname = '{dataArray[1]}' AND videoType = '{dataArray[2]}' ORDER BY videoVer DESC LIMIT 1;")
                rows = cursor.fetchall()
                    
                if not rows:        
                    version = 1
                else:
                    for row in rows:
                        version = int(row[0]) + 1
                            
                      
                cursor.execute(f"INSERT INTO videos (videoVer,vname,videoType,dateAdded) VALUES('{version}','{dataArray[1]}','{dataArray[2]}',CURDATE());")
                response = "videoRegistered"
                
            #Check movie availability
            elif dataArray[0] == 'movieStatus':
                cursor.execute(f"SELECT videoVer, IfNull(dateReturn, '') FROM hire WHERE videoId = '{dataArray[1]} ORDER BY dateReturn DESC LIMIT 1';")
                rows = cursor.fetchall()
                    
                print("Check movie status \n", rows)
                    
                if not rows:
                    cursor.execute(f"SELECT videoVer FROM videos WHERE videoId = '{dataArray[1]}';")
                    rows = cursor.fetchall()
                        
                    if not rows:
                        response = "movieNotExist, Null"
                        
                    for row in rows:
                        videoVer = row[0]
                                        
                        response = f"movieAvailable,{videoVer}"
                    
                else:
                    for row in rows:
                        videoVer     = row[0]
                        dateReturn   = row[1] 
                        
                        print("Return date: ", dateReturn)
                        
                        if dateReturn == "":
                            response = "movieUnavailable, Null"
                                    
                        elif dateReturn != "":
                            response = f"movieAvailable,{videoVer}"
                        
                        else:
                            print("Error with rent out process")
                print("response: ",response)
                
            #OPTION 3
            elif dataArray[0] == 'hireOutMovie':
                cursor.execute(f"INSERT INTO hire (custId, videoId, videoVer, dateHired) VALUES('{dataArray[1]}','{dataArray[2]}','{dataArray[3]}',CURDATE());")
                response = "movieHiredOut"
                
            #OPTION 4
            elif dataArray[0] == 'returnMovie':                
                cursor.execute(f'UPDATE hire SET dateReturn = CURDATE() WHERE videoId = {dataArray[1]}')                
                response = "movieReturned"              
                
            #OPTION X (EXIT)
            elif dataArray[0] == "endSession":
                cursor.close()
                break  #Exit the loop for the network session to be ended             
                 
            #Send response to client server
            self.send(client_conn, response)
            print("response: ",response)
            print("Response sent")
                
            #Close cursor in order for a new 'cursor' object to be created with every request to MySQL db.
            cursor.close()
            print("Cursor closed")
                
            #Implement changes to db via MySQL
            sql_conn.commit()
                
            #Close connection to MySQL db
                
            sql_conn.close
                
            print('END of while loop')
            
        # Close the connection with the client        
        client_conn.close() 
        print('Client conenction Closed')


server = Server(8081, listen = 1000)
server.run() 
