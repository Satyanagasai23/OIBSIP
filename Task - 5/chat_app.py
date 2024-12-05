import socket
import threading

def handle_client(client_socket, addr, other_client):
    """Handles communication from a connected client."""
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[{addr}] {message}")
            if other_client:
                other_client.sendall(f"Client {addr}: {message}".encode('utf-8'))
        except ConnectionResetError:
            break
    print(f"[DISCONNECTED] {addr}")
    client_socket.close()

def run_server():
    """Starts the server and handles two clients."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 5555))
        server.listen(2)
        print("[SERVER STARTED] Waiting for clients to connect...")
        
        clients = []
        while len(clients) < 2:
            client_socket, addr = server.accept()
            clients.append(client_socket)
            thread2 = threading.Thread(target=handle_client, args=(client_socket, addr, clients[0] if len(clients) == 2 else None))
            thread2.start()
            thread2.join()

        print("[SERVER READY] Both clients connected. Messages will now be relayed.")
        for client in clients:
            client.sendall("Connected! You can now chat.".encode('utf-8'))

def receive_messages(client):
    """Receive messages from the server."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:  # Connection closed by server
                print("[SERVER DISCONNECTED]")
                break
            print(f"\n{message}")
        except ConnectionResetError:
            print("[ERROR] Connection lost with the server.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break
    client.close()

def run_client():
    """Starts the client and connects to the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect(("127.0.0.1", 5555))
            print("[CONNECTED TO SERVER] You can start chatting.")
        except ConnectionRefusedError:
            print("[ERROR] Unable to connect to the server. Make sure the server is running.")
            return
        except socket.gaierror:
            print("[ERROR] Invalid server address.")
            return
        
        # Start a thread to receive messages from the server
        thread1 = threading.Thread(target=receive_messages, args=(client,), daemon=True)
        thread1.start()
        thread1.join()

        while True:
            message = input("You: ").strip()
            if not message:  # Skip empty messages
                print("[WARNING] Cannot send an empty message.")
                continue
            if message.lower() == "quit":
                break
            try:
                client.sendall(message.encode('utf-8'))
            except BrokenPipeError:
                print("[ERROR] Server is unreachable. Connection lost.")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                break

if __name__ == "__main__":
    mode = input("Enter mode (server/client): ").strip().lower()
    if mode == "server":
        run_server()
    elif mode == "client":
        run_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")