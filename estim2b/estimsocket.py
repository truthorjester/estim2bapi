#! env python

import socket
import time

class EstimSocket:

    def __init__(self, address="127.0.0.1", port=8089, verbose=True, udp=False):
        self._address = address
        self._port = port
        self._verbose = verbose
        self._udp = udp

    def open_socket(self):
        if self._udp:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.serversocket.bind(('', self._port))
        if not self._udp:
            self.serversocket.listen(1) # become a server socket
        
        if self._udp:
            print 'UDP Server started... waiting for data.'
            return None, None
        else:
            print 'TCP Server started... waiting for client to connect.'
            conn, addr = self.serversocket.accept()
            print 'New client {} connected.'.format(addr[0])
            print 'Running loop.'
            return conn, addr

        

    def start_server(self, max_incoming=1, callbacks=[], on_close=None):

        # handles the TCP vs UDP socket
        conn, addr = self.open_socket()

        while True:

            if self._udp:
                buf, addr = self.serversocket.recvfrom(1024)
            else:
                buf = conn.recv(1024)

            if len(buf) > 0:

                if self._verbose: 
                    print 'Received {} from {}.'.format(buf, addr[0])

                for i, callback in enumerate(callbacks):
                    # callbacks must accept two arguments: the buffer
                    # that was sent, and the address of the device that
                    # sent it.
                    if self._verbose:
                        print '  callback {} of {}...'.format(i, len(callbacks))
                    callback(buf, addr[0])

            else: # len(buf) <= 0
                print 'Client disconnected, will perform clean exit.'
                if on_close is not None:
                    print 'running cleanup...'
                    on_close()
                break

    def client_connect(self):
        self.clientsocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.clientsocket.connect( (self._address, self._port) )

    def client_send(self, buf):
        if self._verbose:
            print 'Sending {} to {}'.format(buf, self._address)
        self.clientsocket.send(buf)


if __name__ == "__main__":

    server = EstimSocket()
    server.start_server()

