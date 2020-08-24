# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
from c2w.main.lossy_transport import LossyTransport
import logging
import struct
import time
from c2w.main.constants import ROOM_IDS
from twisted.internet import reactor
logging.basicConfig()
moduleLogger = logging.getLogger('c2w.protocol.udp_chat_client_protocol')

print('this is the version of 2017/11/22 22:30')
class c2wUdpChatClientProtocol(DatagramProtocol):

    def __init__(self, serverAddress, serverPort, clientProxy, lossPr):
        """
        :param serverAddress: The IP address (or the name) of the c2w server,
            given by the user.
        :param serverPort: The port number used by the c2w server,
            given by the user.
        :param clientProxy: The clientProxy, which the protocol must use
            to interact with the Graphical User Interface.

        Class implementing the UDP version of the client protocol.

        .. note::
            You must write the implementation of this class.

        Each instance must have at least the following attributes:

        .. attribute:: serverAddress

            The IP address of the c2w server.

        .. attribute:: serverPort

            The port number of the c2w server.

        .. attribute:: clientProxy

            The clientProxy, which the protocol must use
            to interact with the Graphical User Interface.

        .. attribute:: lossPr

            The packet loss probability for outgoing packets.  Do
            not modify this value!  (It is used by startProtocol.)

        .. note::
            You must add attributes and methods to this class in order
            to have a working and complete implementation of the c2w
            protocol.
        """

        #: The IP address of the c2w server.
        self.serverAddress = serverAddress
        #: The port number of the c2w server.
        self.serverPort = serverPort
        #: The clientProxy, which the protocol must use
        #: to interact with the Graphical User Interface.
        self.clientProxy = clientProxy
        self.lossPr = lossPr
        self.num=0
        self.movieList=[]
        self.userList=[]
        self.ackReceived ={}
        self.tryTime={}	
        self.resend={}
        self.isrefused=False
        self.isWatching=True

        
        #each time we initiliaze the client, the number of sequence begins at 0
    
    
    def numConstruct(self):
        #each time we send a sequence, we need to use this function to realize the increasement ot 
        #sequence number  
            
        numSequence=self.num
        self.num+=1
        return numSequence   
    
    def datagramSplit(datagram):
        dataHead=struct.unpack('>I',datagram[0:4])
        numSequenceBin=(bin(datahHead[0])[2:].rjust(32,'0')[8:18])
        print(numSequenceBin)

        return(numSequenceBin)
        
        
     
    def ackConstructor(self):
        typeAck=80
        numSeq=datagramSplit(datagram)
        longueurAck=longueur[2:].rjust(14,"0")
        ack0bin=bin(typeAck)[2:].rjust(8,"0")+numSeq+longueurAck
        ack0=int(ack0bin,2)

        ack=struct.pack('>I',ack0)
        print(ack,'ack is constructed')
        return(ack)
       

       
    def startProtocol(self):
        """
        DO NOT MODIFY THE FIRST TWO LINES OF THIS METHOD!!

        If in doubt, do not add anything to this method.  Just ignore it.
        It is used to randomly drop outgoing packets if the -l
        command line option is used.
        """
        self.transport = LossyTransport(self.transport, self.lossPr)
        DatagramProtocol.transport = self.transport
    def headConstruct(self,typeDatagram,numSequence,longueur):
        #para all three are of the type int
        print('gihifhsidfhu',numSequence)

        Type=bin(typeDatagram)[2:].rjust(8,"0")
        

        NumSeq=bin(numSequence)[2:].rjust(10,"0")

        Longueur=bin(longueur)[2:].rjust(14, "0")
        
        head=Type+NumSeq+Longueur
        
        return(head)
    def sendAgain(self,datagram,numSeq,host_port):
            print('12')    
            print(numSeq,datagram,host_port)
            if self.isrefused==True:
                return
            if self.tryTime[numSeq] <= 4 and self.ackReceived[numSeq] == False :
                    print('send agaim')    
                    self.transport.write(datagram,host_port)
                    print('resend the datagram',datagram)
                    self.tryTime[numSeq]+=1
                    reactor.callLater(5,self.sendAgain,datagram,numSeq,host_port)
            else:
                if(self.ackReceived[numSeq] == True ):
                    print('this datagram has been responded',datagram)
                    
                elif(self.tryTime[numSeq] > 4):
                    print('time out for the datagram\'s ack',datagram)    
    
         
    def sendLoginRequestOIE(self, userName):
        """
        :param string userName: The user name that the user has typed.

        The client proxy calls this function when the user clicks on
        the login button.
        """
        numSequence=self.numConstruct()
        #each time when we need to send a new datagram to server, need to construct a new number of sequence
        print('number of sequence')

        head=self.headConstruct(0,numSequence,len(userName)+1)

        print(head,'head')
        
        self.resend[numSequence]=None
        HeaderUserName=bin(len(userName))[2:].rjust(8,"0")

        UserNameString='' 
        
        for i in userName:
            print(i)
            BinEach=bin(ord(i))
            m=BinEach[2:].rjust(8,"0")
            UserNameString=UserNameString+m
            print('test usernamestring',UserNameString)
       
        Corps=HeaderUserName+UserNameString
        
        datagramBIN=head+Corps
        
        print(userName) 
        self.userName=userName
        print(self.userName,'self de username while logging in ')
        userName=userName.encode("utf-8")
        print(int(head,2),len(userName),'test errors in struct')
        datagram=struct.pack('>Ib%ds'%len(userName),int(head,2),len(userName),userName)
        
        self.transport.write(datagram,(self.serverAddress,self.serverPort))
        
        self.tryTime[numSequence]=0 
        self.ackReceived[numSequence]=False 
        
        self.resend[numSequence]=reactor.callLater(5,self.sendAgain,datagram,numSequence,(self.serverAddress,self.serverPort))
        
        
        print(datagram)
        


 
    def sendChatMessageOIE(self, message):
        """
        :param message: The text of the chat message.
        :type message: string

        Called by the client proxy  when the user has decided to send
        a chat message

        .. note::
           This is the only function handling chat messages, irrespective
           of the room where the user is.  Therefore it is up to the
           c2wChatClientProctocol or to the server to make sure that this
           message is handled properly, i.e., it is shown only by the
           client(s) who are in the same room.
        """
        typeDatagramBin=bin(64)[2:].rjust(8,"0")
        numSeqInt=self.numConstruct()
        numSeqBin=bin(numSeqInt)[2:].rjust(10,'0')
        longueur=len(message)+len(self.userName)+2
        longueurBin=bin(longueur)[2:].rjust(14, "0")
        head=typeDatagramBin+numSeqBin+longueurBin
        m0=struct.pack('>I',int(head,2))
        m1=struct.pack('b%ds'%len(self.userName),len(self.userName),self.userName.encode('utf-8'))
        m2=struct.pack('b%ds'%len(message),len(message),message.encode('utf-8'))
        datagram=m0+m1+m2
        
        self.transport.write(datagram,(self.serverAddress,self.serverPort))
        print('senda message for chatting to the server',datagram)
                  

            
    def sendJoinRoomRequestOIE(self, roomName):
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
            self.isWatching=True
            self.nowRoom=roomName
                
            numSequence=self.numConstruct()
            
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
            
            
            self.transport.write(datagram,(self.serverAddress,self.serverPort))
            print(datagram,'datagram for entring a video room')
            
            #self.clientProxy.setUserListONE(('5alice',ROOM_IDS.MOVIE_ROOM))
            
            
            print('check the join movie room',self.userName, roomName,type(self.userName), type(roomName))
            self.clientProxy.userUpdateReceivedONE(self.userName,'threzr')
            print('is this youdoisuisoq')
   
            self.clientProxy.joinRoomOKONE()

            
        else:
            self.isWatching=True
            print('now i am leaving present movie room')
            numSequence=self.numConstruct()
            
            print('number of sequence',numSequence)
            
            TypeBin=bin(49)
            Type=TypeBin[2:].rjust(8,"0")
            
            NumSeqBin=bin(numSequence)
            NumSeq=NumSeqBin[2:].rjust(10,"0")
            
          
           
        
            LongueurInt=0
            
            LongueurBin=bin(LongueurInt)
            Longueur=LongueurBin[2:].rjust(14, "0")
            
            head=Type+NumSeq+Longueur
            print(head,'head')
            
            
           
           
            datagram=struct.pack('>I',int(head,2))
            
            
            self.transport.write(datagram,(self.serverAddress,self.serverPort))
            self.clientProxy.joinRoomOKONE()
            
        

    def sendLeaveSystemRequestOIE(self):
        """
        Called by the client proxy  when the user
        has clicked on the leave button in the main room.
        """
        print('hi now i am leaving this system')
        

        self.clientProxy.userUpdateReceivedONE(self.userName,ROOM_IDS.OUT_OF_THE_SYSTEM_ROOM)
        
  
       
        Type=3
        typeLeave=bin(Type)[2:].rjust(8,"0")
        
        numSequence=self.num
        self.num+=1
        NumSeqBin=bin(numSequence)
        NumSeq=NumSeqBin[2:].rjust(10,"0")


        longueur=bin(0)
        longueur=longueur[2:].rjust(14,"0")
        
        datagram=typeLeave+NumSeq+longueur

        datagram_leave=struct.pack('>I',int(datagram,2))
        self.transport.write(datagram_leave,(self.serverAddress,self.serverPort))
      
        
        self.clientProxy.applicationQuit()
    def test(self,datagram):
        if not(datagram==''):
                number=datagram[0:2]
                print( number)
                number=struct.unpack('>H',number)[0]
        
                print('number in room',number)
                if not(number==0):
                        datagram=datagram[2:]
                        for i in range(number):
                
                                lenI=struct.unpack('b',datagram[0])[0]
                                print(datagram[3:3+lenI])
                                list1.append(datagram[1:1+lenI])
                                datagram=datagram[1+lenI:]
                                
                        self.test(datagram)  
                         
    def buildSalon(self,datagram):
        print('exam datagram in buildSalon',datagram)
        if(len(datagram)==2 or len(datagram)==0):
            return
        numInRoom=struct.unpack('>H',datagram[0:2])[0]
        print(numInRoom,'nulber of users in the room presenr')
        if (numInRoom==0):
            datagram=datagram[2:]
            print(datagram,'datagram after 0')
        if not(numInRoom==0):
            datagram=datagram[2:]
            print(datagram,'datagram')
            for i in range(numInRoom):
                print('hi')
                print(datagram[0])
                lenUsername=datagram[0]
                print(type(lenUsername),lenUsername)
                username=struct.unpack('%ds'%lenUsername,datagram[1:1+lenUsername])[0]
                self.list1.append(username.decode('utf-8'))
                datagram=datagram[1+lenUsername:]
        print('length dqtqgrqm',len(datagram))
        print(self.list1,'self.list1')
        
        self.buildSalon(datagram)
                                
    def ackConstructor(self,datagram):
        typeAck=80
        dataHead=struct.unpack('>I',datagram[0:4])
        #split the number of sequence in this datagram

        numSeq=bin(dataHead[0])[2:].rjust(32,'0')[-24:-14]
        print(numSeq,'number of seq')
        lengthAck=bin(0)[2:].rjust(14,"0")
        print(bin(typeAck)[2:].rjust(8,"0"),numSeq,lengthAck,'check ack')
        ackInt=int(bin(typeAck)[2:].rjust(8,"0")+numSeq+lengthAck,2)
        ack=struct.pack('>I',ackInt) 
        return ack
        
    def getNumSeqFromAck(self,ack):
        #split the number of sequence from ack datagram
        unpack=struct.unpack('>I',ack)
        numSeq=int(bin(unpack[0])[-24:-14],2)
        return numSeq
        
    def datagramReceived(self, datagram, host_port):
        #time.sleep(6)
        print('test datagram received ',datagram)
        typeDatagram=struct.unpack('b',datagram[0:1])[0]
        print(typeDatagram,'typeDatagram')
        if(typeDatagram == 80):
            print('now the server receive an ack from client:',datagram)
            numSeqAck=self.getNumSeqFromAck(datagram)
            print('the number of sequence ack is:',numSeqAck)                        
            self.ackReceived[numSeqAck] = True

        if(typeDatagram != 80):
            print('receive a datagram not an ack?')
            #self.transport.write(ackConstructor(datagram),host_port)
            ack=self.ackConstructor(datagram)
            print('send an ack:',ack,'to be a response of datagram:',datagram)
            self.transport.write(ack,(self.serverAddress,self.serverPort))
           
            '''
            self.transport.write(ack,host_port)
            '''
           # numSeq=datagramSplit(datagram)
            
            
            '''
            numSequenceBin=(bin(dataHead[0])[2:].rjust(32,'0')[8:18])
  
            numSeq=numSequenceBin

            longueur=bin(0)
            longueurAck=longueur[2:].rjust(14,"0")
            ack=struct.pack('>I',0) 
            self.transport.write(ack,host_port)
            '''
            '''
            
            ack0bin=bin(typeAck)[2:].rjust(8,"0")+numSeq+longueurAck
            ack0=int(ack0bin,2)
            ack=struct.pack('>I',ack0) 
            self.transport.write(ack,host_port)
            '''
            if(typeDatagram == 1):##Connexion etablie
                print('The connection is created!')
                #here we need to build the movie list intelligent ici just for a test
                #movieList=[('Sintel - Trailer', '127.0.0.1', 1040), ('Great Guy', '127.0.0.1', 1090), 'Big Buck Bunny', '127.0.0.1', 1034), ('The Night Before Christmas', '127.0.0.1', 1100), ('Battleship Potemkin', '127.0.0.1', 1070)]
                #self.clientProxy.initCompleteONE([],movieList)
                
            if(typeDatagram== 2):##Connexion echouee
                self.isrefused=True
                
                print('now this admission request is refused')
                
            if(typeDatagram == -128):   
                print('receive an error message of type 128',datagram) 
                #erroMessage=
                error=datagram[5:].decode('utf-8')
                print(error,type(error))
                self.clientProxy.connectionRejectedONE(error)
                
                
             
            if(typeDatagram ==19):#receive the user list
                numSalon=datagram[4:6]
                print(numSalon,'0:split from datagram user list')
                numSalon=struct.unpack('>H',numSalon)[0]
                print(numSalon,'split from datagram user list')

                print('datagram with info user salon',datagram)
                numSalon=datagram[4:6]
                numSalon=struct.unpack('>H',numSalon)[0]
                list0=[]
                self.list1=[]
                print(numSalon)
                numSalonP=datagram[6:8]
                numSalonP=struct.unpack('>H',numSalonP)[0]
                print('numSalonP',numSalonP)
                datagram=datagram[8:]
                print(datagram,'test0')
                print('test user list datagram',datagram)
                if not (numSalonP==0):
                        print('the main room is not vide')
                        for i in range(numSalonP):
                                print(datagram[0],type(datagram[0]))
                                lenUsername=datagram[0]
                                print(lenUsername,'length of username')
                                username=struct.unpack('%ds'%lenUsername,datagram[1:1+lenUsername])[0]
                                print(username,type(username))
                                list0.append(username.decode('utf-8'))
                                datagram=datagram[1+lenUsername:]
                        print(datagram,len(datagram),2*(numSalon-1),'the last datagram')  
                        if (len(datagram)==2*(numSalon-1)):
                            print('no other users in movie room')
                        else:
                            print('anymore')
                            self.buildSalon(datagram)
                            

                            
                print(list0,'list0',self.list1,'list1')
                self.userList=[]
                if not (len(list0)==0):
                    print('0test',self.userList)
                    for i in list0:
                        self.userList.append((i,ROOM_IDS.MAIN_ROOM))
                if not (len(self.list1)==0):
                    print('1test',self.userList)
                    for i in self.list1:
                        self.userList.append((i,ROOM_IDS.MOVIE_ROOM)) 
                           
                #self.clientProxy.setUserListONE(self.userList)
                print(self.userList,'test self.userList for setOne')
                if(len(self.movieList)>0):
                    self.clientProxy. setUserListONE(self.userList)
                print('show me the result of userList',self.userList)
                

            if(typeDatagram ==16):#receive the movie list
                print('receive movie list for server')
                head=struct.unpack('>IH',datagram[0:6])
                print('head after unpacking',head)
                numMovie=int(head[1])
                corps=datagram[6:]
                print('corps of movieLIst',corps)
                head=bin(head[0]).rjust(32,"0")
                print('datargame head',head)
                
                
                print('check number of movie',numMovie)
                for i in range(numMovie):
                    print('hiiii',corps[0])
                    lenMovieName=corps[0]
                    print(i,type(i))
                    print('movie name 555',corps[1:1+lenMovieName])
                    movieName=corps[1:1+lenMovieName]
                    print('movie name',str(movieName))
                    print('movie name',type(movieName))
                    print('test movie name',str(movieName[2:]))
                    movieName=movieName.decode("utf-8")
                    ip=struct.unpack('4b',corps[1+lenMovieName:5+lenMovieName])
                    print(ip)
                    ipStr=str(ip[0])
                    for i in ip[1:]:
                        ipStr+='.'+str(i)
                        
                    print('test string ip',ipStr)
                    port=struct.unpack('>H',corps[5+lenMovieName:7+lenMovieName])
                    print(port,'test port')
                    print(int(port[0]))
                    port=int(port[0])
                    corps=corps[7+lenMovieName:]
                    
                    print(str(movieName),'hhhhh')
                    self.movieList.append((movieName,ipStr,port))
                    print('check if movie list is correct',self.movieList) 
                    print('check if movie list is correct',self.userList)
                    
                print('head',head)
                print(self.movieList,'if the movie list unpack by the client if correct',self.userList)
                
               
                self.clientProxy.initCompleteONE(self.userList,self.movieList)

            if(typeDatagram ==18):
                print('receive 18 datagram:',datagram)  
                numSame=datagram[5]
                listRoom=[]
                print('number of users in the same room',numSame)
                l=datagram[6:]
                for i in range(numSame):
                    lenName=l[0]
                    name=struct.unpack('%ds'%lenName,l[1:1+lenName])[0].decode('utf-8')
                    print('name test',name)
                    
                    listRoom.append((name,self.nowRoom))
                    l=l[1+lenName:]
                print('test listRoom',listRoom)
                self.clientProxy.setUserListONE(listRoom)    
                
            if(typeDatagram ==65):
                print('recieve 65',datagram)
                lenUsername=datagram[4]

                userName=struct.unpack('%ds'%lenUsername,datagram[5:5+lenUsername])[0]


               
                lenmss=datagram[5+lenUsername]
                print(datagram[5+lenUsername+lenmss:],len(datagram[5+lenUsername+1:]))
                mess=struct.unpack('%ds'%lenmss,datagram[6+lenUsername:])[0]
                print('the user',userName,type(userName), 'is send here',mess,type(mess))
                self.clientProxy.chatMessageReceivedONE(userName.decode('utf-8'), mess.decode('utf-8')) 
                    
        else:
            print('no case satisfied')
            
            
            
            
            '''
            if(typeDatagram == 1):##Connexion etablie
                print('The connection is created!')
                #self.clientProxy.initCompleteONE(userList,movieList)
                
            if(typeDatagram == 2):##Connexion echouee
                self.clientProxy.connectionRejectedONE('userName exists')
                print('Error connection(same userName)!')
            '''
                      
    """
        :param string datagram: the payload of the UDP packet.
        :param host_port: a touple containing the source IP address and port.

        Called **by Twisted** when the client has received a UDP
        packet.
        when we receive a datagram, firstly we need to split the datagram to 
        clearly see the part of Type, NumSeq, Longueur, Corps
    """ 
    """except we receive an acquitement, we must send back a message of acquitement    
    """
           
                    

