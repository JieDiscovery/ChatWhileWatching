# -*- coding: utf-8 -*-
import time
import sys
from twisted.internet.protocol import DatagramProtocol

class SibylClientUdpTextProtocol(DatagramProtocol):
    """
    The class implementing the Sibyl UDP text client protocol.  It has
    the following attributes:

    .. attribute:: proxy

        The reference to the SibylCientProxy (instance of the
        :py:class:`~sibyl.main.sibyl_client_proxy.SibylClientProxy` class).

        .. warning::
            All interactions between the client protocol and the user
            interface *must* go through the SibylClientProxy.  In other
            words you must call one of the methods of
            :py:class:`~sibyl.main.sibyl_client_proxy.SibylClientProxy`
            whenever you would like the user interface to do something.

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
        """The implementation of the UDP client text protocol.

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
        print(port,'port') 

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
       # print(type(during),type(line),'jie test')
        datagram=str(during)+':'+line
        
       # print(during) 
        #print(line)
        #print(datagram)
        datagram=datagram.encode('utf-8')
        self.datagram=datagram
        #transform datagram in the format of utf8
        print(datagram) 
        #print(self.serverPort)
	#datagram=str(during)+': '+line
        self.transport.write(datagram,(self.serverAddress,self.serverPort))

    def datagramReceived(self, datagram, host_port):
        print ("received",datagram,"from",host_port)
        #reactor.run()
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
        print(host_port,datagram)
        print('client has received the feedback from server',host_port,'datagram sent from port:',self.port,'host:',self.host,'is successfully sent')
