import socket
import threading
import sys

MAX_CAPACITY: int = 20
HOST, PORT = "127.0.0.1", 5555

clients_nickname_hash : dict[socket.socket, str]= dict() 

def lockOut_client(client: socket.socket, message: str):
    client.send(str.encode("utf-8"))
    client.close()


def handle_clients(client: socket.socket):
    """
        accepts and handlels clients as much as the capacity allows 
    """
    if len(clients_nickname_hash) > MAX_CAPACITY:
        lockOut_client(client, "server capacity is maxed out....")
        return 

    message = ""
    try:
        message = client.recv(1024).decode("utf-8")
        while message:
                if message:
                    broadcast_message(message)
                message = client.recv(1024).decode("utf-8")
    except Exception as e:
            nickname = clients_nickname_hash.pop(client, None)
            if nickname:
                broadcast_message(f"{nickname} left the chat.")
                client.close()
            print(f"handling clients error : {e}")
            return

def broadcast_message(message: str):
    '''
        sends out one client message to every other client 
    '''
    for client in clients_nickname_hash.keys():
        client.send(message.encode("utf-8"))

def stop():
    """
        closes all the client connections (threads)
    """
    clients = list(clients_nickname_hash.keys())

    for client in clients:
        client.send("Shutting down the server ...".encode("utf-8"))
        client.close()
        
        if client in clients:
            clients_nickname_hash.pop(client)

    # for t in threading.enumerate():
    #     if t is threading.main_thread():
    #         continue
    #     t.join()
    
    print('everything stopped ...')

def main():
    with socket.socket(socket.AF_INET,  socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen()

        while True:
            client, address = s.accept()
            print(f"connected with {address}")

            client.send("NickName".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")
            if nickname in clients_nickname_hash.values():
                lockOut_client(client, "username already taken.")
                continue
            clients_nickname_hash[client] = nickname
            client.send(f"Welcome to the chat {nickname}".encode("utf-8"))
            
            print(f"conn : {client}, nickname: {nickname}")
            broadcast_message(f"{nickname} joined the chat")
            client.send("connected to the server...".encode("utf-8"))

            t = threading.Thread(target=handle_clients, args=(client, ))
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
    