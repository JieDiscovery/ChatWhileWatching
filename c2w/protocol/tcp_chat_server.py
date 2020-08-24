# -*- coding: utf-8 -*-
from twisted.internet.protocol import Protocol
import logging

import struct
import time
logging.basicConfig()
moduleLogger = logging.getLogger('c2w.protocol.tcp_chat_server_protocol')


class c2wTcpChatServerProtocol(Protocol):

    def __init__(self, serverProxy, clientAddress, clientPort):
        """
        :param serverProxy: The serverProxy, which the protocol must use
            to interact with the user and movie store (i.e., the list of users
            and movies) in the server.
        :param clientAddress: The IP address (or the name) of the c2w server,
            given by the user.
        :param clientPort: The port number used by the c2w server,
            given by the user.

        Class implementing the TCP version of the client protocol.

        .. note::
            You must write the implementation of this class.

        Each instance must have at least the following attribute:

        .. attribute:: serverProxy

            The serverProxy, which the protocol must use
            to interact with the user and movie store in the server.

        .. attribute:: clientAddress

            The IP address of the client corresponding to this 
            protocol instance.

        .. attribute:: clientPort

            The port number used by the client corresponding to this 
            protocol instance.

        .. note::
            You must add attributes and methods to this class in order
            to have a working and complete implementation of the c2w
            protocol.

        .. note::
            The IP address and port number of the client are provided
            only for the sake of completeness, you do not need to use
            them, as a TCP connection is already associated with only
            one client.
        """
        #: The IP address of the client corresponding to this 
        #: protocol instance.
        self.clientAddress = clientAddress
        #: The port number used by the client corresponding to this 
        #: protocol instance.
        self.clientPort = clientPort
        #: The serverProxy, which the protocol must use
        #: to interact with the user and movie store in the server.
        self.serverProxy = serverProxy
        self.num=0
        self.datagram=b''
        #

    def dataReceived(self, data):
        """
        :param data: The data received from the client (not necessarily
                     an entire message!)

        Twisted calls this method whenever new data is received on this
        connection.
        """
        print('the time when it receives a new data',time.localtime(time.time()))
        print('now receive a data',data)
        self.datagram+=data
        datagram=self.datagram
        print('show me the datagram while it receives a data',datagram)
        headType=struct.unpack('b',datagram[0:1])[0]
        print('hi')
        if (headType!=80):
            print('now we have a datagram not an ack')
            if(len(datagram)>=4):
                #the datagram not an ack has a complete head now
                print('test',bin(struct.unpack('>I',datagram[0:4])[0])[2:].rjust(32,'0')[-14:])
                numSeqBin=bin(struct.unpack('>I',datagram[0:4])[0])[2:].rjust(32,'0')[-24:-14]
                print('show the number of sequence',numSeqBin)
                lenCorps=int(bin(struct.unpack('>I',datagram[0:4])[0])[2:].rjust(32,'0')[-14:],2)
                print('longueur of this datagram should be',lenCorps)
                if(len(datagram)==lenCorps+4):
                    print('now the datagram is complete',self.datagram,'so we clear the self.datagram')
                    self.datagram=b''
                    typeAck=80
                    # numSeq=datagramSplit(datagram)
                    dataHead=struct.unpack('>I',datagram[0:4])
                    #print(dataHead,'datahead')
 

                    longueur=bin(0)
                    longueurAck=longueur[2:].rjust(14,"0")
                    print(bin(typeAck)[2:].rjust(8,"0"),'type/80')
                    ack0bin=bin(typeAck)[2:].rjust(8,"0")+numSeqBin+longueurAck
                    print('show me ack0bin',ack0bin,len(ack0bin),len(numSeqBin),len(longueurAck))
                    ack0=int(ack0bin,2)

                    ack=struct.pack('>I',ack0) 
                    print('show me the ack it sends',ack)
                    self.transport.write(ack)
                    if(headType == 0):
                        print('this is a request of connection to server')
                        userName=struct.unpack('%ds'%len(datagram[5:]),datagram[5:])[0].decode("utf-8")
                        userNameLength=len(userName)
                        userNameComplete=str(userNameLength)+userName
                        print('username complete',userNameComplete)
                        if (self.serverProxy.userExists(userName)):
                                #this username exists
                                #it will send a datagram to client of type 2
                                print('boss check that the user name exist')
                                
                                headType=bin(2)[2:].rjust(8,"0")
                                numSequence=self.num
                                
                                self.num+=1

                                NumSeqData=bin(numSequence)[2:].rjust(10,"0")
            
                                LongueurInt=0
                                LongueurBin=bin(LongueurInt)
                                Longueur=LongueurBin[2:].rjust(14, "0")
                                print('here ??',headType+NumSeqData+Longueur)
                        
                                data=struct.pack('>I',int(headType+NumSeqData+Longueur,2))
                                self.transport.write(data)
                                print('now the server sends a data to the client for refusing the login',data)
                        else:
                                print('username valid')
                                headType=bin(1)[2:].rjust(8,"0")
        
                                numSequence=self.num
                                
                                self.num+=1

                                NumSeqData=bin(numSequence)[2:].rjust(10,"0")
                                                
                                LongueurInt=0
                                LongueurBin=bin(LongueurInt)
                                Longueur=LongueurBin[2:].rjust(14, "0")
                                print(headType+NumSeqData+Longueur,'datagram beform packing')
        
                                data=struct.pack('>I',int(headType+NumSeqData+Longueur,2))
        
                                self.transport.write(data)   
                                
                                print('now the server sends a data to the client for loggin in',data)     
                    
            
            
        else:
            print('now this is a datagram of an ack')
            if(len(datagram)==4):
                print('now this is a complete ack')
                numSequence=struct.unpack('>I',datagram)
                print('now the number of sequence is:',numSequence)
                self.datagram=b''
                    
            
        
        print('head of datafgram',headType,type(headType),len(self.datagram[0:1]),type(self.datagram))
        
        
            
        
        if(len(self.datagram)==12):
            
        
            typedata=struct.unpack('b',data[0:1])[0]
            ack=struct.pack('bhbbh',80,0,1,0,0)
            self.transport.write(ack)
        if(len(self.datagram)==16):
            print(bin(struct.unpack('>I',data)[0]),'DATA RECEIVE')

            ack=struct.pack('9b',19,0,64,0,0,32,0,0,16)#b'1300400e0002000107726f6d617269630000'
            ack=b'\x13\x00@\x0e\x00\x02\x00\x01\x07romaric\x00\x00'
            self.transport.write(ack)  
        if(len(self.datagram)==20): 
            print(bin(struct.unpack('>I',data)[0]),'DATA RECEIVE')
            

            ack=b'\x10\x00\x80\x17\x00\x01\x0e3 Days to Kill\x00\x00\x00\x00N '
            self.transport.write(ack)                  
        '''
  
        self.datagram+=data
        ack=struct.pack('bhbbh',80,0,1,0,0)
            
        print('show ack in server',ack)
        print(len(self.datagram),'length of datagram',self.datagram)
        if(len(self.datagram)==12):
            ack=struct.pack('bhbbh',80,0,1,0,0)
            
            print('show ack in server',ack)
            self.transport.write(ack)
        if(len(self.datagram)==16):
            ack=struct.pack('bhbbh',80,0,1,0,0)
            
            print('show ack in server',ack)
            self.transport.write(ack)    

        if(typedata != 80):
         
            #self.transport.write(ackConstructor(data),host_port)
            typeAck=80
           # numSeq=dataSplit(data)

            numSequenceBin=(bin(self.num)[2:].rjust(32,'0')[8:18])
            self.num+=1
  
            numSeq=numSequenceBin
            print('show me the number of seq',numSeq)

            longueur=bin(0)
            longueurAck=longueur[2:].rjust(14,"0")
            ack0bin=bin(typeAck)[2:].rjust(8,"0")+numSeq+longueurAck
            ack0=int(ack0bin,2)
            ack=''

            ack=struct.pack('>I',ack0) 

        
            
            self.transport.write(ack)
           
            print('test',ack)
            
            print('this me')
            
            print(typedata,'type of data')
            if(typedata == 0):
                print('this is a request of connection to server')
                print(data[5:])
                print(len(data[5:]))
                userName=struct.unpack('%ds'%len(data[5:]),data[5:])[0].decode("utf-8")
                userNameLength=len(userName)
                userNameComplete=str(userNameLength)+userName
                print('username complete',userNameComplete)
                print(self.serverProxy.userExists(userName))
                
                if (self.serverProxy.userExists(userName)):
                                #this username exists
                                #it will send a data to client of type 2
                        print('boss check if the user name exist')
                        TypeBin=bin(2)
                        Type=TypeBin[2:].rjust(8,"0")
        
                        numSequence=self.num
                        self.num+=1
                        NumSeqBin=bin(numSequence)
                        NumSeq=NumSeqBin[2:].rjust(10,"0")
                                        
                        LongueurInt=0
                        LongueurBin=bin(LongueurInt)
                        Longueur=LongueurBin[2:].rjust(14, "0")
                        print('here ??',Type+NumSeq+Longueur)
                        
                        data=struct.pack('>I',int(Type+NumSeq+Longueur,2))
                        self.transport.write(data)
                        #start_end[numSequence]=timeit.timeit()
                        #print('test the start time of waiting an ack',start_end[numSequence], start_end)
                        #now it begins to wait the ack
        
                if not (self.serverProxy.userExists(userName)):
                        print('username valid')
                        TypeBin=bin(1)
                        Type=TypeBin[2:].rjust(8,"0")
        
                        numSequence=self.num
                        
                        self.num+=1
                        NumSeqBin=bin(numSequence)
                        NumSeq=NumSeqBin[2:].rjust(10,"0")
                                        
                        LongueurInt=0
                        LongueurBin=bin(LongueurInt)
                        Longueur=LongueurBin[2:].rjust(14, "0")
                        print(Type+NumSeq+Longueur,'data beform packing')
        
                        data=struct.pack('>I',int(Type+NumSeq+Longueur,2))            

                        self.transport.write(data)
                        print('yes send a data for allowing',data)
                
                if (typedata == 48):
                        print('now the server receives an request of entring the video room')
                        
                        typeAck=80
                         # numSeq=datagramSplit(datagram)
                        dataHead=struct.unpack('>I',datagram[0:4])
                        #print(dataHead,'datahead')
                        numSequenceBin=(bin(dataHead[0])[2:].rjust(32,'0')[8:18])
                         
                        numSeq=numSequenceBin
                         
                        longueur=bin(0)
                        longueurAck=longueur[2:].rjust(14,"0")
                        ack0bin=bin(typeAck)[2:].rjust(8,"0")+numSeq+longueurAck
                        ack0=int(ack0bin,2)
                         
                        ack=struct.pack('>I',ack0) 
                        self.transport.write(ack,host_port)
                        print('show me the user List now',self.serverProxy.getUserList())
                        print('send an ack for entring the video room',ack)                 
                
            if(typedata==48):
                print('now there is a user wanna enter')
        '''                    
            
        print('okay:')                 

