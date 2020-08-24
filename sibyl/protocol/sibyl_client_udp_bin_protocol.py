# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
import struct
import time
import binascii
import codecs
import sys
class SibylClientUdpBinProtocol(DatagramProtocol):
    """
        The class implementing the Sibyl client protocol.  It has
        the following attributes:

        .. attribute:: proxy

            The reference to the SibylCientProxy (instance of the
            :py:class:`~sibyl.main.sibyl_client_proxy.SibylClientProxy` class).

            .. warning::
                All interactions between the client protocol and the user
                interface *must* go through the SibylClientProxy.  In other
                words you must call one of the methods of
                :py:class:`~sibyl.main.sibyl_client_proxy.SibylClientProxy` whenever
                you would like the user interface to do something.

        .. attribute:: serverAddress

            The address of the server.

        .. attribute:: serverPort

            The port number of the server.

        .. note::
            You must not instantiate this class.  This is done by the code
            called by the main function.

        .. note::
            You have to implement this class.  You may add any attribute and
            method that you see fit to this class.  You must implement two
            methods:
            :py:meth:`~sibyl.main.protocol.sibyl_cliend_udp_text_protocol.sendRequest`
            and
            :py:meth:`~sibyl.main.protocol.sibyl_cliend_udp_text_protocol.datagramReceived`.
            See the corresponding documentation below.
        """

    def __init__(self, sibylClientProxy, port, host):
        """The implementation of the UDP Text Protocol.

        Args:
            sibylClientProxy: the instance of the client proxy,
                        this is the only way to interact with the user
                        interface;
            port: the port number of the server;
            host: the address of the server.
        """
        self.serverAddress = host
        self.serverPort = port
        self.clientProxy = sibylClientProxy

    def sendRequest(self, line):
        """Called by the controller to send the request

        The :py:class:`~sibyl.main.sibyl_client_proxy.SibylClientProxy` calls
        this method when the user clicks on the "Send Question" button.

        Args:
            line (string): the text of the question

        .. warning::
            You must implement this method.  You must not change the parameters,
            as the controller calls it.

        """
        #pass
        during=time.time()
        during=int(during)
        print(during,'during')
   
        byte_line=bytes(line,encoding='utf-8')
        
        data_hex=binascii.hexlify(byte_line) 
        
        during_hex=hex(during)[2:]
    
        
        
        packet_length= int(len(during_hex)/2+2+len(data_hex)/2)

        packet_length_hex=hex(packet_length)[2:]
        
        datagram=struct.pack(str(len(data_hex))+'s',data_hex)

       
      
       
        print('length',packet_length_hex) 
        print('messss',during,packet_length,data_hex)
        form='QQ'+str(len(data_hex))+'s'
        
       # datagram=struct.pack('vvv',during_hex,packet_length_hex,data_hex)
        datagram=struct.pack('QQ'+str(len(data_hex))+'s',during,packet_length,data_hex)
       # datagram=struct.pack('QQ',during,packet_length)
      #  datagram=struct.pack(form,during,packet_length,data_hex)
        print(datagram,'test datagram') 
        self.transport.write(datagram,(self.serverAddress,self.serverPort)) 
    def datagramReceived(self, datagram, host):
        """Called by Twisted whenever a datagram is received

        Twisted calls this method whenever a datagram is received.

        Args:
            datagram (bytes): the payload of the UPD packet;
            host_port (tuple): the source host and port number.

        .. warning::
            You must implement this method.  You must not change the parameters,
            as Twisted calls it.

        """
        #pass
        print('client has received the success feedback from server',host)
    
