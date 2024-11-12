
#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# Author:       Leeza Kotze                                   
# Created:      January 2022                                                    
# Description:  Python Programming - Project 1 
#               CLIENT PROGRAM
#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


import socket

# Create Client class and its functions
class Client:
    def __init__(self, host, port,bufsize = 1024, timeout = 10):
        self.client = socket.socket( socket.AF_INET,socket.SOCK_STREAM )    # Create a socket object
        self.host = host
        self.port = port
        self.bufsize = bufsize
        self.timeout = timeout

    def close(self):
        self.client.close()
       
    def send(self, string):
        self.client.send( bytes( string, "ascii" ) )
        
    def recv(self):
        return str( self.client.recv( self.bufsize ), encoding = "ascii" )

    def connect(self):
        self.client.connect( (self.host, self.port) )   # Establish connection with the server
#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
  
if  __name__ == "__main__":
    client = Client("localhost", 8081)
    client.connect()
    
    while True:
            
        #__________________Selection Menu :__________________
        print("")
        print("============================================")
        print("|              VIDEO STORE                 |")
        print("============================================")
        print("| 1. Register Customer                     |")
        print("| 2. Register Movie                        |")
        print("============================================")
        print("| 3. Hire Out Movie                        |")
        print("| 4. Return Movie                          |")
        print("============================================")
        print("| x. Exit                                  |")
        print("============================================")
        print(" ")
                        
        # Client makes a selection:
        choice = input("Choice: ")    
#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
            
        # Register a customer:
        if choice == "1":
            print("Register customer: ")
            cell = str(input("Please enter customer cellphone number: "))

            #only allow for digits
            if not cell.isdigit():
                print("Cell phone entered contains characters. Cell phones may only contain digits.")
                continue
                
            data = f"checkIfCustomerExists,{cell}"
                
            # Send cell to server to see if customer already exist.
            client.send(data)
                
            # Data returned from DB assigned to a variable.
            response = client.recv()   
                
            # Cell not registered with a customer. Proceed with registering a new customer:
            if response == 'customerDoesNotExist':
                print("Please enter customer's details")
                first_name =    str(input("First name: "))
                surname =       str(input("Surname: "))
                addr =          input("Address: ")
                    
                data = f'registerNewCustomer,{first_name},{surname},{addr},{cell}'
                print(data)
                           
                # Send register new client request to server.
                client.send(data)   #error
                print('After Send')                
                # Receive confirmation that request was executed.
                response = client.recv()  
                    
                if response == 'customerRegistered':
                    print(f" \nCustomer '{first_name} {surname}' has been registered.")
                
                else:
                    print('An error occured during customer registration')
                
            # Cell is already registered with a customer.               
            else:
                print(f"\nThe cellphone number '{cell}' has already been registered\n ")
                continue                
#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
 
            # Register a movie: 
        elif choice == "2":
            
            while True:
                print("Register Movie: ")       
                movie_name = input("Please enter Movie name: ")
                movie_type = str(input("Please enter Movie type (R = Red/ New, B = Black/ Old): "))
                
                if movie_type != "B" and movie_type != "R":
                    print("\n Movie registration unsuccessful. Invalid selection of movie type. Options are 'B' and 'R' - need to be capitalized \n***Please try again*** \n")
                    continue
                 
                
                data = f'registerMovie,{movie_name},{movie_type}'
                
                
                # Send register new movie request to server.
                client.send(data)
                    
                # Receive confirmation that request was executed.
                response = client.recv()      #This has an error                           
                
                
                if response == 'videoRegistered':
                    print(f"\nVideo '{movie_name}' has been registered.")
                    break
#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________ 
         
        # Hire Out movie:
        elif choice == "3":
                
            print("Hire Out Movie: ")
            
            while True:                                                                         
                cell = input("\nPlease enter customer cellphone number: ")
                
                
                data = f"checkIfCustomerExists,{cell}"
                    
                # Send cell to server to see whether customer is registered.
                client.send(data)
                    
                # Server gives response on whether customer is registered.
                response = client.recv()                                                                  

                dataArray = response.split(',')
                    
                
                # If Customer is registered, display details
                if dataArray[0] == "customerExists":                        
                    print(f"\nCustomer selected: \nName: {dataArray[1]} {dataArray[2]} \nAddress: {dataArray[3]} \nCellphone: {cell}")
                    
                    custId = dataArray[4]
                        
                    # Verify whether correct customer is selected 
                    correct_customer_check = input("\nIs this the correct customer (Y/N): ")    

                    
                    # Proceed with hire process if correct customer
                    if correct_customer_check == "y" or correct_customer_check == "Y":                                
                                                
                        while True:
                            # Check to see wether movie is available to be checked out
                            video_Id = input("Please enter the video id or select 'x' to return to menu: ")   
                            
                            # To exit back to main Menu
                            if video_Id == "x" or video_Id == "X":
                                break
                            
                            data = f"movieStatus, {video_Id}"
                            
                            # Send movie id to server 
                            client.send(data)
                            
                            reply = client.recv()
                                                   
                            # Server gives response on movie availability as well as the movieVer of the id supplied
                            response = reply.split(',')   
                            
                            availability    = response[0]      
                            videoVer        = response[1]
                            
                            if availability == "movieAvailable":
                                    # Complete hire process
                                    data = f"hireOutMovie,{custId},{video_Id},{videoVer}"
                                
                                    # Send hire out request to server.
                                    client.send(data)
                                    
                                    response = client.recv() 
                                    
                                    if response == "movieHiredOut":
                                        print(f"\nVideo {video_Id} successfully rented out.")
                                        break
                                        
                                    else:
                                        print("Error: Movie unable to be checked out")
                            
                            elif availability == "movieUnavailable":
                                print("\n Movie is currently checked-out. Please select a different movie.\n")
                            
                            elif availability == "movieNotExist":
                                print("\n Movie not stocked at this store. Please select a different movie.\n")
                                                        
                            else:
                                print("An error occured.")
                        
                        break
    
                    # Return to cell input since the cell number did not return the intended customer.
                    elif correct_customer_check == "n" or correct_customer_check == "N":       
                        print("Restarting attempt")
                        continue
                        
                    # Errorhandling
                    else:                                                                       
                        print("Not a valid response. Please re-attempt")
                        continue
                        
                # The customer is not registered yet.
                else:
                    not_reg_select = input(f"\nCellphone number is not linked to a registered customer. \nWould you like to:\n   1.Try a different cellphone number \n   2.Register a new customer \n\nChoice:")

                    # Allow user to try another cell number 
                    if not_reg_select == "1":
                        continue

                    # Exit loop to return to main menu where user can select register a new customer option
                    elif not_reg_select == "2":
                        print("\nPlease select 1 at the menu to register a customer.")          
                        break
                        
                    #Errorhandling
                    else:
                        print("Not a valid response. Please re-attempt")                        
                        continue    
 #________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________ 
            
        # Return Movie:
        elif choice == "4":
            
            print("Return a Movie: ")
            
            returned_movieId = input("Please enter the Id of the movie being returned: ")
            
            #Check movie status
            data = f"movieStatus, {returned_movieId}"
            
            client.send(data)
                        
            reply = client.recv()
            response = reply.split(',')   
            availability    = response[0]               
            
            if availability == "movieUnavailable":
                data = f"returnMovie,{returned_movieId}"
                client.send(data)
                
                response = client.recv()
                
                if response == 'movieReturned':
                    print(f"\nVideo {returned_movieId} returned")
                
            
            elif availability == "movieNotExist":
                print("Selected movie not stocked at this store.")
            
            else:
                print("Unable to return a movie that is not checked out.")
               
 #________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
            
        # Exit:
        elif choice == "X" or choice == "x":   
            print("\n==============\nSession ended.\n==============\n \n \n")
            data = f'endSession'
            client.send(data)                           # Send request to Server
                
            self.client_socket.close()
            break                                       # End session by exiting loop    
#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
          
        # Errorhandling:
        else:
            print("Invalid selection made. Please select from the menu")    
            continue
#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________      

wait = input()