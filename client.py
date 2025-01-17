import socket
import threading 
import sys

HOST, PORT = "127.0.0.1", 5555


def receive(client: socket.socket, nickname: str):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if message == "NickName":
                client.send(nickname.encode("utf-8"))
                # message = client.recv(1024).decode("utf-8")
                # print(message)
                continue

            print(message)
        except Exception as e:
            stop(f"recive error : {e}")
            break

def write(client : socket.socket, nickname: str):
    while True:
        try:
            message = f'{nickname} : {input("> ")}'
            client.send(message.encode("utf-8"))
        except Exception as e :
            stop(f"write error : {e}")
            break

def stop(e: str):
    # for t in threading.enumerate():
    #     t.join()

    client.close()
    
    print(e)
    print("Disconnecting from the server...")

    sys.exit()
        

def main():
    nickname = input("Enter a nickname: ")
    while not nickname.strip():
        nickname = input("Enter a nickname: ")

    global client
    client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    receive_message = threading.Thread(target=receive, args=(client, nickname))
    receive_message.start()

    write_message = threading.Thread(target=write, args=(client, nickname))
    write_message.start()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        stop("main error : {e}")