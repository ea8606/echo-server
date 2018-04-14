import socket
import sys


def client(msg, log_buffer=sys.stderr):
    """
    Send a message to a server and return the message
    received from the server.the

    Args:
         param1 (string): The message to send to the server
         param2 (file obj): default is stderr

    Return (string): The message that was received from the server
    """

    # Create a socket and connect to the server
    server_address = ('localhost', 10000)
    # Don't forget to encode the message to a byte object
    msg = msg.encode('utf8')
    sock = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.connect(server_address)
    print('connecting to {0} port {1}'.format(
        *server_address), file=log_buffer)

    total_received_bytes = 0
    total_bytes_expected = len(msg)

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg.decode('utf8')), file=log_buffer)
        sock.sendall(msg)
        message_received = b''
        while total_received_bytes < total_bytes_expected:
            chunk = sock.recv(16)
            # keep track of the actual message here
            message_received += chunk
            total_received_bytes += len(chunk)
            print('received "{0}"'.format(
                chunk.decode('utf8')), file=log_buffer)
    finally:
        print('closing socket', file=log_buffer)
        sock.close()

        return message_received.decode('utf8')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    print(client(msg))
