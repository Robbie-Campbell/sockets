import socket

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

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Method to send message
def send(msg):

    # Encode the message intp utf-8
    message = msg.encode(FORMAT)

    # Get the message length and pad it to be the same length as header
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    # Send the message, header and decode the message from the server
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

if __name__ == "__main__":
    send("Are we working?")