import socket
import threading
import sys

MAX_CAPACITY: int = 20
HOST, PORT = "127.0.0.1", 5555

clients_nickname_hash : dict[socket.socket, str]= dict() 


def handle_clients(client: socket.socket):
    """
        accepts and handlels clients as much as the capacity allows 
    """
    if len(clients_nickname_hash) > MAX_CAPACITY:
        client.send("server capacity is maxed out....")
        return 

    try:
        message = client.recv(1024).decode("utf-8")
        while message:
            if len(message) > 0:
                broadcast_message(message)
            message = client.recv(1024).decode("utf-8")
    except Exception as e:
            nickname = clients_nickname_hash.pop(client)
            broadcast_message(f"{nickname} left the chat.")
            print(e)

def broadcast_message(message: str):
    '''
        sends out one client message to every other client 
    '''
    for client in clients_nickname_hash.keys():
        client.send(message.encode("utf-8"))

def stop():
    """
        closes all the client connections
    """
    for client in clients_nickname_hash.keys():
        client.send("Shutting down the server ...".encode("utf-8"))
        client.close()
        
        if client in clients_nickname_hash:
            clients_nickname_hash.pop(client)

def main():
    with socket.socket(socket.AF_INET,  socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen()

        while True:
            conn, address = s.accept()
            print(f"connected with {address}")

            conn.send("NickName".encode("utf-8"))
            nickname = conn.recv(1024).decode("utf-8")
            clients_nickname_hash[conn] = nickname
            
            print(f"conn : {conn}, nickname: {nickname}")
            broadcast_message(f"{nickname} joined the chat")
            conn.send("connected to the server...".encode("utf-8"))

            t = threading.Thread(target=handle_clients, args=(conn, ))
            t.start()
    

if __name__ == "__main__":
    print("server is running...")
    try :
        main()
    except KeyboardInterrupt:
        stop()
        sys.exit()
    except Exception as e:
        print("main Error : " + str(e))
    