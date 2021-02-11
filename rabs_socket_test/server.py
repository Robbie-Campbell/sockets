import socket
import threading

"""
Create the constants:
PORT: The port the server is running on
HEADER: The byte size of messages sent to the server
SERVER: Get the IP address of the server
ADDR: The host location as a tuple
FORMAT: Decodes messages back out of UTF-8
DISCONNECT_MESSAGE: If this message is returned, the client disconnects
"""
PORT = 5050
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Create an ipv4 internal server and then strean it
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server with the address provided
server.bind(ADDR)

# The method that handles the client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # Connection is active until changed to false
    connected = True
    while connected:

        # Get the message and then make sure it isn't blank
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:

            # Convert the message into integers
            msg_length = int(msg_length)

            # Get the string value of the message
            msg = conn.recv(msg_length).decode(FORMAT)

            # Disconnect from the server cleanly
            if msg == DISCONNECT_MESSAGE:
                connected = False
                conn.send("Successfully Disconnected")
                break
            # Print the message and who sent it
            print(f"[{addr}] {msg}")

            # Verify the message has been recieved
            conn.send("Message Recieved".encode(FORMAT))
    
    # Close the client connection to the server
    conn.close()


# Start up the server
def start():
    # Server starts to listen out for new connections
    print("[STARTING] Server starting...")
    server.listen()
    print("[SERVER] Server is listening...")

    # Run the server until it is closed
    while True:

        # Get the information from the incoming client
        conn, addr = server.accept()
        
        # Start threading clients so that more than one client action can happen at once
        thread = threading.Thread(target=handle_client, args=[conn, addr])
        thread.start()

        # Print the active connections
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 5}")


# Run the main function
if __name__ == "__main__":
    start()