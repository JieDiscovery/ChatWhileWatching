# -*- coding: utf-8 -*-
from twisted.internet.protocol import Protocol
import logging
import struct

logging.basicConfig()
moduleLogger = logging.getLogger('c2w.protocol.tcp_chat_client_protocol')
import time

class c2wTcpChatClientProtocol(Protocol):

    def __init__(self, clientProxy, serverAddress, serverPort):
        """
        :param clientProxy: The clientProxy, which the protocol must use
            to interact with the Graphical User Interface.
        :param serverAddress: The IP address (or the name) of the c2w server,
            given by the user.
        :param serverPort: The port number used by the c2w server,
            given by the user.

        Class implementing the UDP version of the client protocol.

        .. note::
            You must write the implementation of this class.

        Each instance must have at least the following attribute:

        .. attribute:: clientProxy

            The clientProxy, which the protocol must use
            to interact with the Graphical User Interface.

        .. attribute:: serverAddress

            The IP address of the c2w server.

        .. attribute:: serverPort

            The port number used by the c2w server.

        .. note::
            You must add attributes and methods to this class in order
            to have a working and complete implementation of the c2w
            protocol.
        """

        #: The IP address of the c2w server.
        self.serverAddress = serverAddress
        #: The port number used by the c2w server.
        self.serverPort = serverPort
        #: The clientProxy, which the protocol must use
        #: to interact with the Graphical User Interface.
        self.clientProxy = clientProxy
        
        
        self.num=0
        self.movieList=[('The Night Before Christmas', '127.0.0.1', 1100), ('Battleship Potemkin', '127.0.0.1', 1070)]
                
        self.userList=[]
        self.i=3
        self.datagram=b''
        
    def test():
            print('i wanna test')    

    def sendLoginRequestOIE(self, userName):
        """
        :param string userName: The user name that the user has typed.

        The client proxy calls this function when the user clicks on
        the login button.
        """

        #moduleLogger.debug('loginRequest called with username=%s', userName)
        print('the time when it receives a new data',time.time())
        numSequence=self.num
        self.num+=1
        print('number of sequence',numSequence)
        
        TypeBin=bin(0)
        Type=TypeBin[2:].rjust(8,"0")
        
        NumSeqBin=bin(numSequence)
        NumSeq=NumSeqBin[2:].rjust(10,"0")
        
        LongueurInt=len(userName)+1
        
        LongueurBin=bin(LongueurInt)
        Longueur=LongueurBin[2:].rjust(14, "0")
        
        head=Type+NumSeq+Longueur
        print(head,'head')
        
        HeaderUserNameBin=bin(len(userName))
        HeaderUserName=HeaderUserNameBin[2:].rjust(8,"0")

        UserNameString='' 
        for i in userName:
            print(i)
            BinEach=bin(ord(i))
            m=BinEach[2:].rjust(8,"0")
            UserNameString=UserNameString+m
            print('test usernamestring',UserNameString)
       
        Corps=HeaderUserName+UserNameString
        
        datagramBIN=Type+NumSeq+Longueur+Corps
        
        print(userName) 
        self.userName=userName
        print(self.userName,'self de username while logging in ')
        userName=userName.encode("utf-8")
        print(int(head,2),len(userName),'test errors in struct')
        datagram=struct.pack('>Ib%ds'%len(userName),int(head,2),len(userName),userName)
        print(datagram,'datagram')
        self.transport.write(datagram)
        
        

    def sendChatMessageOIE(self, message):
        """
        :param message: The text of the chat message.
        :type message: string

        Called by the client proxy when the user has decided to send
        a chat message

        .. note::
           This is the only function handling chat messages, irrespective
           of the room where the user is.  Therefore it is up to the
           c2wChatClientProctocol or to the server to make sure that this
           message is handled properly, i.e., it is shown only by the
           client(s) who are in the same room.
        """
        (64,numSeq,message)
        m1=struct.pack('b%ds'%len(self.userName),len(self.userName))
        m2=struct.pack('b%ds'%len(message),len(message))
        ,self.userName,len(message),message

    def sendJoinRoomRequestOIE(self, roomName):
        print('hi i wanna enter this movie room')    
        """
        :param roomName: The room name (or movie title.)

        Called by the client proxy  when the user
        has clicked on the watch button or the leave button,
        indicating that she/he wants to change room.

        .. warning:
            The controller sets roomName to
            c2w.main.constants.ROOM_IDS.MAIN_ROOM when the user
            wants to go back to the main room.
        """
        print('now i am trying to entre a video room',roomName)
        if(type(roomName)==str):
            numSequence=self.num
            self.num+=1
            print('number of sequence',numSequence)
            
            TypeBin=bin(48)
            Type=TypeBin[2:].rjust(8,"0")
            
            NumSeqBin=bin(numSequence)
            NumSeq=NumSeqBin[2:].rjust(10,"0")
            
          
           
            print('check the name of room',roomName,type(roomName))
            LongueurInt=len(roomName)+1
            
            LongueurBin=bin(LongueurInt)
            Longueur=LongueurBin[2:].rjust(14, "0")
            
            head=Type+NumSeq+Longueur
            print(head,'head')
            
            
            roomName=roomName.encode("utf-8")
           
            datagram=struct.pack('>Ib%ds'%len(roomName),int(head,2),len(roomName),roomName)
            
            self.transport.write(datagram)
            print(datagram,'datagram for entring a video room')
            
            #self.clientProxy.setUserListONE(('5alice',ROOM_IDS.MOVIE_ROOM))
            
            
            print('check the join movie room',self.userName, roomName,type(self.userName), type(roomName))
            self.clientProxy.userUpdateReceivedONE(self.userName,'threzr')
   
            self.clientProxy.joinRoomOKONE()

            
        else:
            print('now i am leaving present movie room')
            self.clientProxy.joinRoomOKONE()
            
        

    def sendLeaveSystemRequestOIE(self):
        """
        Called by the client proxy  when the user
        has clicked on the leave button in the main room.
        """
        pass

    def dataReceived(self, data):
        """
        :param data: The data received from the client (not necessarily
                     an entire message!)

        Twisted calls this method whenever new data is received on this
        connection.
        """
        print('strrr;;now receivea data',data,len(data))
        self.datagram+=data
        print('the length of daatgram',len(self.datagram))
        print(self.datagram,'now the datagram is')
        
        

        '''
        
        if(len(self.datagram)==8):
                
                ack=struct.pack('>I',int(b'01010000000000000000000000000000',2))
                
                self.transport.write(ack)
                print('hi send an ack',ack)
        if(len(self.datagram)==26):
                
                ack=struct.pack('>I',int(b'01010000000000000100000000000000',2))
                
                self.transport.write(ack)
                print('hi send an ack',ack)
        
      
       
        
        
        
        if(self.i==3):
                print('hi 3')
                ack=struct.pack('>I',int(b'01010000000000000000000000000000',2))
                
                self.transport.write(ack)
                print(ack,'ack est1')
                self.i=self.i-1
                print(self.i)
                ack=b''
              
        elif(self.i==2):
                print('hi 2')        
                ack=struct.pack('>I',int(b'01010000000000000100000000000000',2)) 
                print('test ack in client',ack)
                self.transport.write(ack)
                print(ack,'aacke test2')
                self.i=self.i-1
                
        #ack=struct.pack('>I',int(b'01010000000000000100000000000000',2))       
        
                
        
        
        typeDatagram=struct.unpack('b',data[0:1])
        print(typeDatagram[0],'typeDatagram')
        print('hei',(typeDatagram[0]==80))
        self.clientProxy.initCompleteONE(self.userList,self.movieList)
        if(typeDatagram[0]!=80):
                print('send an ack')
                typeAck=80
                print('hi')
                dataHead=struct.unpack('>I',data[0:4])
                print(dataHead,'datahead')
                numSequenceBin=(bin(dataHead[0])[2:].rjust(32,'0')[8:18])
                
                typeAck=bin(typeAck)[2:].rjust(8,"0")
                numSeq=numSequenceBin
                print(numSeq,'number seq')
                longueur=bin(0)
                longueurAck=longueur[2:].rjust(14,"0")
                
                ack=typeAck+numSequenceBin+longueurAck
                
                ack=struct.pack('>I',int(ack,2))
                print('test ack in client',ack)
                
                

                #self.transport.write(ack)
                if(typeDatagram[0] == 1):##Connexion etablie
                        print('The connection is created!')
                        self.clientProxy.initCompleteONE(self.userList,self.movieList)
                        

                
                if(typeDatagram[0] == 2):##Connexion echouee
                        self.clientProxy.connectionRejectedONE('userName exists')
        '''
        

                
             
           
