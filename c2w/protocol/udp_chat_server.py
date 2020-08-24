# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
from c2w.main.lossy_transport import LossyTransport
import logging
import struct
from c2w.main.constants import ROOM_IDS
import time
import re
logging.basicConfig()
from twisted.internet import reactor
moduleLogger = logging.getLogger('c2w.protocol.udp_chat_server_protocol')
print('version of tuesday')
from twisted.internet.reactor import callLater

print('this is the version of 2017/11/22 22:30')
class c2wUdpChatServerProtocol(DatagramProtocol):


                 
    def __init__(self, serverProxy, lossPr):
        print('begin the initilization of this class')    
        """
        :param serverProxy: The serverProxy, which the protocol must use
            to interact with the user and movie store (i.e., the list of users
            and movies) in the server.
        :param lossPr: The packet loss probability for outgoing packets.  Do
            not modify this value!

        Class implementing the UDP version of the client protocol.

        .. note::
            You must write the implementation of this class.

        Each instance must have at least the following attribute:

        .. attribute:: serverProxy

            The serverProxy, which the protocol must use
            to interact with the user and movie store in the server.

        .. attribute:: lossPr

            The packet loss probability for outgoing packets.  Do
            not modify this value!  (It is used by startProtocol.)

        .. note::
            You must add attributes and methods to this class in order
            to have a working and complete implementation of the c2w
            protocol.
        """
        #: The serverProxy, which the protocol must use
        #: to interact with the server (to access the movie list and to 
        #: access and modify the user list).
        self.serverProxy = serverProxy
        self.lossPr = lossPr
        self.ackReceived = {}
        self.num=0
        #iniitilization of sequence number is 0

        self.online=0
        #self.online: the number of users in the server, to ensure if the server is sature
       
        #test correct:self.resend = None
        self.tryTime={}	
        self.numAttendu={}
        self.resend=None
        
        self.isSend={}
        self.wasReceived=True
       
       
       
        print('firstly show the movie list',self.serverProxy.getMovieList)
        self.movieList={}
        

        for m in self.serverProxy.getMovieList():
                
                print( "Movie title: ", m.movieTitle,m.movieId)
                print('ip', self.serverProxy.getMovieAddrPort(m.movieTitle)[0])
                print('port', self.serverProxy.getMovieAddrPort(m.movieTitle)[1])
                self.serverProxy.startStreamingMovie(m.movieTitle)
                
                #begin the streaming in all movie rooms
                #heer can be better: if this movie room is no person, we can stop the streaming
                self.movieList[m.movieTitle]=[0,[]]
        print('movie list is ',self.movieList) 
       
        
        print('test user list in server',self.serverProxy.getUserList())
        print('write a fonction which starts when the procedure is lanced')
        self.list={}
        ticks = time.time()
        print('for thesfdfdsd present time is:',ticks)
        
    def numConstruct(self):
        #each time before we send a datagram need to generate a number sequence
        # and agument self.num which means the next number seq ready to be sent
        # ensure the number returns to 0 when it arrives at 2047
        numSequence=self.num
        if self.num==2047:
            self.num=0
        else: 
            self.num+=1
        return numSequence   
        
        #okay  
         
    def testUsername(self,username):
        #param: username  in format string
        #in spec we know that the format of username need to be:
        #1. the length is not over 255 caracteres
        #2. it begin by a alphabet and maybe some alphabet/numbers
        if(len(username)>256):
                print('the length of username is too long so that no valid')
                return false
        else:
                if not(username[0].isalpha()):
                        print('the beginning of username is not an alphabet')
                        return False
                else:
                        if not(username[1:].isalnum()):
                                print('the following string of username isnot num/alpha ')
                                return False
                        else: return True
                        
     

    def sendMovieRoom(self,host_port):
        NumSalonP=0
        salonP=[]
        salonList={}
        
        corps0=b''
        
        
        for u in self.serverProxy.getUserList():
                print(u)
                if(u.userChatRoom==ROOM_IDS.MAIN_ROOM):
                        print('this user is in the main room')
                        NumSalonP+=1
                        salonP.append(u.userName)
                else:
                        print('gergze',u.userChatRoom)
                        print(self.movieList)
                        if u.userChatRoom in self.movieList:
                                self.movieList[u.userChatRoom][0]+=1
                                self.movieList[u.userChatRoom][1].append(u.userName)

        corps0+=struct.pack('>H',NumSalonP)
        print('exam for movie list: slef',self.movieList)
        for i in salonP:
                i=i.encode("utf-8")
                corps0+=struct.pack('b%ds'%len(i),len(i),i)
        for i in self.movieList:
                corps0+=struct.pack('>H',self.movieList[i][0])
                if not (self.movieList[i][1]==0):
                        print('this moivie room is not empty')
                        for i in self.movieList[i][1]:
                                i=i.encode("utf-8")
                                corps0+=struct.pack('b%ds'%len(i),len(i),i)
                        
                     
                
        print(corps0,'corps0 check itself')      

        TypeBin=bin(19)
        Type0=TypeBin[2:].rjust(8,"0")

        
        numSequence=self.num
        self.num+=1
        NumSeqBin=bin(numSequence)
        NumSeqUserList=NumSeqBin[2:].rjust(10,"0")
                        
        LongueurInt=1+len(corps0)+1
        LongueurBin=bin(LongueurInt)
        Longueur0=LongueurBin[2:].rjust(14, "0")
        
        #datagram_UserList=struct.pack('>IH',int(Type0+NumSeqUserList+Longueur0,2),numSalon)+corps0
        datagram_UserList=struct.pack('>IH',int(Type0+NumSeqUserList+Longueur0,2),2)+corps0
        
        self.transport.write(datagram_UserList,host_port)
        print('datagram of user list',datagram_UserList)

        


        movieListDatagram=self.movieListDatagram()
        

        self.sendDatagram(1,len(movieListDatagram),movieListDatagram,host_port)  
    def sendAndWait(self,datagram,numSeq,host_port):
            print('12')    
            print(numSeq,datagram,host_port)
            if (self.wasReceived):
                reactor.callLater(5,self.sendAndWait,datagram,numSeq,host_port)
            else:
        
                if self.tryTime[numSeq] <= 4 and self.ackReceived[numSeq] == False :
                        print('send agaim')    
                        self.transport.write(datagram,host_port)
                        print('resend the datagram',datagram)
                        self.tryTime[numSeq]+=1
                        self.resend[numSeq]=reactor.callLater(5,self.sendAgain,datagram,numSeq,host_port)
                else:
                    if(self.ackReceived[numSeq] == True ):
                        self.wasReceived=True
                        print('this datagram has been responded',datagram)
                    elif(self.tryTime[numSeq] > 4):
                        print('time our for the datagram\'s ack',datagram)  
                        userToDelete=self.serverProxy.getUserByAddress(host_port)
                        
    def startProtocol(self):
        """
        DO NOT MODIFY THE FIRST TWO LINES OF THIS METHOD!!

        If in doubt, do not add anything to this method.  Just ignore it.
        It is used to randomly drop outgoing packets if the -l
        command line option is used.
        """
        self.transport = LossyTransport(self.transport, self.lossPr)
        DatagramProtocol.transport = self.transport
        nomMovie=0

        for m in self.serverProxy.getMovieList():
                nomMovie+=1
                print( "Movie title: ", m.movieTitle,m.movieId)
                print('ip port', self.serverProxy.getMovieAddrPort(m.movieTitle)[0])
        print(nomMovie)
        
        
    def checkAck(self,host_port):
                print('now we are testing the ack')
                delay(1000)
                print('the ack is not received within 1000')
                return 0
                 
    '''
    def numConstruct(self):
        numSequence=self.num
        self.num+=1
        return numSequence 
        '''       
    def getTypeFromDatagram(self,datagram):
        #typeDatagram: int
        typeDatagram=struct.unpack('b',datagram[0:1])[0]
        return typeDatagram


    def getNumSeqFromDatagram(self,datagram):
        #numSequence: int
        unpack=struct.unpack('>I',datagram[0:4])
        print('unpack',bin(unpack[0])[2:].rjust(32,'0')[-24:-14])
        numSeq=int(bin(unpack[0])[2:].rjust(32,'0')[-24:-14],2)
        return numSeq
        
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
        
    def connFailedConstr(self):
        typeBin=bin(2)[2:].rjust(8,"0")
        numSequence=self.numConstruct()
        
        numSeqBin=bin(numSequence)[2:].rjust(10,"0")
        lengthBin=bin(0)[2:].rjust(14, "0")
        
        datagram=struct.pack('>I',int(typeBin+numSeqBin+lengthBin,2))
        numSeq=int(numSeqBin,2)
        return numSeq,datagram	
    def errorConstr(self,error):
        typeBin=bin(128)[2:].rjust(8,"0")
        numSequence=self.numConstruct()
        
        numSeqBin=bin(numSequence)[2:].rjust(10,"0")
        
        lengthBin=bin(len(error)+1)[2:].rjust(14, "0")
        head=typeBin+numSeqBin+lengthBin
        
        datagram=struct.pack('>Ib%ds'%len(error),int(head,2),len(error),error.encode('utf-8'))
        
        numSeq=int(numSeqBin,2)
        return numSeq,datagram
        
    def movieListDatagram(self):
            self.numMovie=0
            corpsMovie=b''
            for m in self.serverProxy.getMovieList():
                    ip=self.serverProxy.getMovieAddrPort(m.movieTitle)[0]
                    ip=re.findall(r"\d+",ip)
                    print('show me the ip after process',ip)
                    port=self.serverProxy.getMovieAddrPort(m.movieTitle)[1]
                    print('show me the port number ',port)
                    port=bin(port)
                    port=port[2:].rjust(14,"0")
                    
                    movieName=m.movieTitle
                    movieName=movieName.encode("utf-8")
                    print('shoe me the length of movie name',len(movieName),type(len(movieName)))
                    #corps+=struct.pack('b',len(movieName))
                 
                    corpsMovie+=struct.pack('b%ds4b'%len(movieName),len(movieName),movieName,int(ip[0]),int(ip[1]),int(ip[2]),int(ip[3]))
                    corpsMovie+=struct.pack('>H',int(port,2))
                    self.numMovie+=1
                    
                    
            movieListDatagram=struct.pack('>H',self.numMovie)+corpsMovie        
            return movieListDatagram           
        
    def sendAgain(self,datagram,numSeq,host_port):
            print('12')    
            print(numSeq,datagram,host_port)
        
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
                    print('time our for the datagram\'s ack',datagram)  
                    

    def sendDatagram(self,typeDatagram,longueur,Corps,host_port):
            typeDatagramBin=bin(typeDatagram)[2:].rjust(8,"0")
            numSeqInt=self.numConstruct()
            numSeqBin=bin(numSeqInt)[2:].rjust(14,'0')
            longueurBin=bin(longueur)[2:].rjust(10, "0")
            print(typeDatagramBin+numSeqBin+longueurBin,'test in senddatagram')
            datagram=struct.pack('>I',int(typeDatagramBin+numSeqBin+longueurBin,2))+Corps
            self.transport.write(datagram,host_port)    
                                
    def datagramReceived(self, datagram, host_port):
        """
        :param string datagram: the payload of the UDP packet.
        :param host_port: a touple containing the source IP address and port.
        
        Twisted calls this method when the server has received a UDP
        packet.  You cannot change the signature of this method.
        """
        print('receice a datagram from',datagram,host_port)
        #here if need a test for mal format message
        typeDatagram=self.getTypeFromDatagram(datagram)
        print('receice a datagram from',datagram,host_port,'at the type of:',typeDatagram)

        #except we receive an acquitement, we must send back a message of acquitement    
        numReceived=self.getNumSeqFromDatagram(datagram)

       
                        
        if(typeDatagram == 80):
                print('now the server receive an ack from client:',datagram)
                numSeqAck=self.getNumSeqFromAck(datagram)
                print('the number of sequence ack is:',numSeqAck)                        
                self.ackReceived[numSeqAck] = True
        
        
        if not host_port in self.isSend:
            self.isSend[host_port]=True
            self.numAttendu[host_port]=0
            
        
        if(typeDatagram != 80 ):
                '''    
                if not (numReceived==self.numAttendu[host_port]):
                
                print(numReceived,self.numAttendu)
                print('the number sequence received is not the num seq wait')
                numSeq,errorDatagram=self.errorConstr('Numero de sequence inattendu')
                print('send tht datagram of error:',errorDatagram)
                self.ackReceived[numSeq]=False
                self.transport.write(errorDatagram,host_port)
                return 
                #if the number of sequence is not correct, ignore this message
                '''
                self.numAttendu[host_port]+=1
                ack=self.ackConstructor(datagram)
                print('send an ack:',ack,'to be a response of datagram:',datagram)
                self.transport.write(ack,host_port)
                
                if(typeDatagram == 0):
                            
                        print('this is a request of connection to server')
                        print(datagram[5:])
                        print(len(datagram[5:]))
                        userName=struct.unpack('%ds'%len(datagram[5:]),datagram[5:])[0].decode("utf-8")
        
                        userNameLength=len(userName)
                        userNameComplete=str(userNameLength)+userName
                        print('THE INPUT USERNAME IS :',userName,'username complete',userNameComplete)
                
                        if(self.online>=512):
                                
                                print('now the server is sature and no longer resource for a new user')
        
                                numSeq,datagram=self.connFailedConstr()
                                self.transport.write(datagram,host_port)
                                self.ackReceived[numSeq]=False
                                print('send a datagtam refuse',datagram)
                                print('set self.ackReceived:',numSeq,'to false')
                                numSeq,errorDatagram=self.errorConstr('Serveur sature')
                                print('send tht datagram of error:',errorDatagram)
                                self.ackReceived[numSeq]=False
                                self.transport.write(errorDatagram,host_port)
                                print('set self.ackReceived:',numSeq,'to false')
                        elif(self.testUsername(userName)==False):
                                print('this username is not in the correct format')
                                numSeq,datagram=self.connFailedConstr()
                                self.transport.write(datagram,host_port)
                                self.ackReceived[numSeq]=False
                                print('send a datagtam refuse',datagram)
                                print('set self.ackReceived:',numSeq,'to false')
                                numSeq,errorDatagram=self.errorConstr('Mauvais nom d’utilisateurur')
                                print('send tht datagram of error:',errorDatagram)
                                self.ackReceived[numSeq]=False
                                self.transport.write(errorDatagram,host_port)
                                typeDatagram=struct.unpack('>b',errorDatagram[0:1])
                                print(typeDatagram[0],'typeDatagram errror',errorDatagram)
                                print('set self.ackReceived:',numSeq,'to false')
                        elif(self.serverProxy.userExists(userName)):
                                print('this username is already in use and existing user list:',self.serverProxy.getUserList())
                                numSeq,datagram=self.connFailedConstr()
                                self.transport.write(datagram,host_port)
                                self.ackReceived[numSeq]=False
                                print('send a datagtam refuse',datagram)
                                print('set self.ackReceived:',numSeq,'to false')
                                
                                 
                                numSeq,errorDatagram=self.errorConstr('Utilisateur deja existant')
                                print('send tht datagram of error:',errorDatagram)
                                self.ackReceived[numSeq]=False
                                self.transport.write(errorDatagram,host_port)
                                print('set self.ackReceived:',numSeq,'to false')
                        else:
                                print('this user can be allowed in')
                                print('test the user list:',self.serverProxy.getUserList())
                                self.online+=1
                                #this username is admitted
                                print('username valid')
                                TypeBin=bin(1)
                                Type=TypeBin[2:].rjust(8,"0")
                                numSequence=self.numConstruct()
                                NumSeqBin=bin(numSequence)
                                NumSeq=NumSeqBin[2:].rjust(10,"0")
                                                
                                LongueurInt=0
                                LongueurBin=bin(LongueurInt)
                                Longueur=LongueurBin[2:].rjust(14, "0")
                                print(Type+NumSeq+Longueur,'datagram beform packing')
                        
                                
                                datagram=struct.pack('>I',int(Type+NumSeq+Longueur,2))
        
                                self.transport.write(datagram,host_port)
                                self.tryTime[numSequence]=0 
                                self.ackReceived[numSequence]=False 
                                #CORRECT:self.resend = reactor.callLater(5,self.sendAndWait,datagram,numSequence,host_port) $
                                print('check resend',self.resend) 
                                self.resend={}
                                self.resend[numSequence]=None
                                self.resend[numSequence]=reactor.callLater(5,self.sendAgain,datagram,numSequence,host_port)
                                print(self.tryTime,self.resend)
                                for i in self.serverProxy.getUserList():
                                    print(i,'test all user in the list 1420')
                                print('final test for user list',self.serverProxy.getUserList())    
                                self.serverProxy.addUser(userName,ROOM_IDS.MAIN_ROOM,None,host_port)
                                
                                #self.serverProxy.addUser('linue', 'Great Guy')
                                print('check if user is add to the list',self.serverProxy.getUserList())
                                #now we send a datagram of movie list to client
                                
                                #numSalon initial 1 cause we must have a main room
                                
                                
                             
                                NumSalonP=0
                                salonP=[]
                                salonList={}
                                
                                corps0=b''
                                print('test for user list change while a new user',self.serverProxy.getUserList())
                                '''
                                [<Instance of c2wUser; userName=alice, userChatRoom=<class 'c2w.main.constants.ROOM_IDS.MAIN_ROOM'>, 
                                userChatInstance=None, userAddress=('127.0.0.1', 46602)>, <Instance of c2wUser; 
                                userName=aliceff, userChatRoom=<class 'c2w.main.constants.ROOM_IDS.MAIN_ROOM'>, userChatInstance=None, userAddress=('127.0.0.1', 36153)>]
                                '''
                                self.movieList0={}        


                                for m in self.serverProxy.getMovieList():
                                                self.movieList0[m.movieTitle]=[0,[]]
                                        

                                
                                for u in self.serverProxy.getUserList():
                                        print(u)
                                        if(u.userChatRoom==ROOM_IDS.MAIN_ROOM):
                                                print('this user is in the main room')
                                                NumSalonP+=1
                                                salonP.append(u.userName)
                                        else:
                                                if u.userChatRoom in self.movieList:
                                                        self.movieList0[u.userChatRoom][0]+=1
                                                        self.movieList0[u.userChatRoom][1].append(u.userName)
                                self.movieList=self.movieList0
                                corps0+=struct.pack('>H',NumSalonP)
                                print('test salonP',salonP)
                                print('exam for movie list: slef',self.movieList)
                                for i in salonP:
                                        i=i.encode("utf-8")
                                        corps0+=struct.pack('b%ds'%len(i),len(i),i)
                                for i in self.movieList:
                                        corps0+=struct.pack('>H',self.movieList[i][0])
                                        if not (self.movieList[i][1]==0):
                                                print('this moivie room is not empty')
                                                for i in self.movieList[i][1]:
                                                        i=i.encode("utf-8")
                                                        corps0+=struct.pack('b%ds'%len(i),len(i),i)
                                                
                                             
                                        
                                print(corps0,'corps0 check itself')      
        
                                TypeBin=bin(19)
                                Type0=TypeBin[2:].rjust(8,"0")
                                Type0=TypeBin[2:].rjust(8,"0")
        
        
                                
                                numSequence=self.num
                                self.num+=1
                                NumSeqBin=bin(numSequence)
                                NumSeqUserList=NumSeqBin[2:].rjust(10,"0")
                                                
                                LongueurInt=1+len(corps0)+1
                                LongueurBin=bin(LongueurInt)
                                Longueur0=LongueurBin[2:].rjust(14, "0")
                                
                                #datagram_UserList=struct.pack('>IH',int(Type0+NumSeqUserList+Longueur0,2),numSalon)+corps0
                                datagram_UserList=struct.pack('>IH',int(Type0+NumSeqUserList+Longueur0,2),len(self.movieList)+1)+corps0
                                
                                #self.transport.write(datagram_UserList,host_port)
                                sendList=[]
                                for u in self.serverProxy.getUserList():
                                        print(u. userChatRoom)


                                
                                        if(u. userChatRoom==ROOM_IDS.MAIN_ROOM):
                                                sendList.append(u.userAddress)
                                print('send list check',sendList)
                                if (len(sendList)>0):
                                        for i in sendList:
                                                self.transport.write(datagram_UserList,i)
                                
                                print('datagram of user list',datagram_UserList)
                        
                                
        
        
                                movieListDatagram=self.movieListDatagram()
                                
                                
        
                                self.sendDatagram(16,len(movieListDatagram),movieListDatagram,host_port)
                                
        
                                        
                                #corps+=struct.pack('b%ds4b>H'%len(movieName),len(movieName),movieName,ip[0],ip[1],ip[2],ip[3],int(port,2))
                                #movieList.apppend((m.movieTitle,self.serverProxy.getMovieAddrPort(m.movieTitle)[0],self.serverProxy.getMovieAddrPort(m.movieTitle)[1]))
                                
                                
        
                        
                        '''
                        
                        
                        print('add a user in the list of user')
                        
                        start_end[numSequence]=timeit.timeit()
                        print('test the start time of waiting an ack',start_end[numSequence], start_end)
                        
                        print('room ids ',ROOM_IDS.MAIN_ROOM)
                        
                        #now we need to send a datagram about movie list to client
                        
                        self.transport.write(movieList,host_port)
                        
                        
                        for m in self.serverProxy.getMovieList():
                                print('get movie list',m.movieId)
                        for u in self.serverProxy.getUserList():
                                print('user name: ', u.userName,u.userChatRoom)
                                if(u.userChatRoom==ROOM_IDS.MAIN_ROOM):
                                        print('okay')
                                if not(u.userChatRoom==ROOM_IDS.MOVIE_ROOM):
                                        print(' not okay')
                        
                        #if this datagram for connection is not received by our client
                        #this means the ack from client is not received here'''
                        
                        
                elif(typeDatagram == 48 or typeDatagram == 49):
                        print('now the server receives an request of entring/quitting the video room',typeDatagram)
                        
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
                        print('send an ack for entring the video room',ack) 
                        if(typeDatagram == 48):
                        
                                lenroomName=datagram[4]
                                roomName=struct.unpack('%ds'%lenroomName,datagram[5:])[0].decode('utf-8')
                                #self.serverProxy.addUser(userName,ROOM_IDS.MOVIE_ROOM,None,host_port)
                                
                                print('now the user is in the room',roomName)
                                print('show me the user List now',self.serverProxy.getUserList())
                                print('username to change its position',self.serverProxy.getUserByAddress(host_port).userName)
                                
                                self.serverProxy.updateUserChatroom(self.serverProxy.getUserByAddress(host_port).userName,roomName)
                                print('show me the user List now WHEN I ENTER MOVIE ROOM',self.serverProxy.getUserList())
                        else:   
                                roomBefore=self.serverProxy.getUserByAddress(host_port).userChatRoom
                                self.serverProxy.updateUserChatroom(self.serverProxy.getUserByAddress(host_port).userName,ROOM_IDS.MAIN_ROOM)
                                print('show me the user List now WHEN I QUIT MOVIE ROOM',self.serverProxy.getUserList())
                                Type0=bin(18)[2:].rjust(8,"0")
                                numSequence=self.num
                                self.num+=1
                                NumSeqBin=bin(numSequence)
                                NumSeqUserList=NumSeqBin[2:].rjust(10,"0")

                                corps=b''
                            
                                sendListRoom=[]	
                                peopleRoom=[]
                                for u in self.serverProxy.getUserList():
                                        print(u. userChatRoom,roomBefore)
                                        if(u. userChatRoom==roomBefore):
                                                print('hi a friend in this movie room')
                                               
                                                sendListRoom.append(u.userAddress)
                                                peopleRoom.append(u.userName)
                                                                
                                if(len(peopleRoom)>0):
                                        
                                    corps+=struct.pack('>H',len(peopleRoom)) 
                                    for i in peopleRoom:
                                        corps+=struct.pack('b%ds'%len(i),len(i),i.encode('utf-8'))            
                                    print('send list check',sendListRoom)

                                
                                
                                
                                LongueurInt=len(corps)
                                LongueurBin=bin(LongueurInt)
                                Longueur0=LongueurBin[2:].rjust(14, "0")
                                head=Type0+NumSeqUserList+Longueur0
                                datagram=struct.pack('>I',int(head,2))+corps
                                if (len(sendListRoom)>0):
                                        print('send list to users in salon',datagram)
                                        for i in sendListRoom:
                                            self.transport.write(datagram,i)  

        
                        
                        
                        
                        NumSalonP=0
                        salonP=[]
                        salonList={}
                        
                        corps0=b''
                        print('test for user list change while a new user',self.serverProxy.getUserList())
                        '''
                        [<Instance of c2wUser; userName=alice, userChatRoom=<class 'c2w.main.constants.ROOM_IDS.MAIN_ROOM'>, 
                        userChatInstance=None, userAddress=('127.0.0.1', 46602)>, <Instance of c2wUser; 
                        userName=aliceff, userChatRoom=<class 'c2w.main.constants.ROOM_IDS.MAIN_ROOM'>, userChatInstance=None, userAddress=('127.0.0.1', 36153)>]
                        '''
                        
                        
                        self.movieList0={}
                        for u in self.serverProxy.getUserList():
                                print(u)
                                if(u.userChatRoom==ROOM_IDS.MAIN_ROOM):
                                        print('this user is in the main room')
                                        NumSalonP+=1
                                        salonP.append(u.userName)
                                else:   
                                        
                                        for m in self.serverProxy.getMovieList():
                                                self.movieList0[m.movieTitle]=[0,[]]
                                        print('test userchatroom and movie list',u.userChatRoom,self.movieList)
                                        if u.userChatRoom in self.movieList:
                                                print('yes fina a user in movie room')
                                                self.movieList0[u.userChatRoom][0]+=1
                                                self.movieList0[u.userChatRoom][1].append(u.userName)
                        
                        self.movieList=self.movieList0
                        corps0+=struct.pack('>H',NumSalonP)
                        print('test salonP',salonP)
                        print('exam for movie list: self',self.movieList)
                        for i in salonP:
                                i=i.encode("utf-8")
                                corps0+=struct.pack('b%ds'%len(i),len(i),i)
                        for i in self.movieList:
                                corps0+=struct.pack('>H',self.movieList[i][0])
                                if not (self.movieList[i][1]==[]):
                                        print('this moivie room is not empty')
                                        for i in self.movieList[i][1]:
                                                i=i.encode("utf-8")
                                                corps0+=struct.pack('b%ds'%len(i),len(i),i)
                        print(corps0,'corps0 check itself')      

                        TypeBin=bin(19)
                        Type0=TypeBin[2:].rjust(8,"0")
                       


                        
                        numSequence=self.num
                        self.num+=1
                        NumSeqBin=bin(numSequence)
                        NumSeqUserList=NumSeqBin[2:].rjust(10,"0")
                                        
                        LongueurInt=1+len(corps0)+1
                        LongueurBin=bin(LongueurInt)
                        Longueur0=LongueurBin[2:].rjust(14, "0")
                        
                        #datagram_UserList=struct.pack('>IH',int(Type0+NumSeqUserList+Longueur0,2),numSalon)+corps0
                        datagram_UserList=struct.pack('>IH',int(Type0+NumSeqUserList+Longueur0,2),len(self.movieList)+1)+corps0
                        
                        #self.transport.write(datagram_UserList,host_port)
                        sendList=[]
                        for u in self.serverProxy.getUserList():
                                print(u. userChatRoom)
                                if(u. userChatRoom==ROOM_IDS.MAIN_ROOM):
                                        sendList.append(u.userAddress)
                                        
                        print('send list check',sendList)
                        if (len(sendList)>0):
                                for i in sendList:
                                        self.transport.write(datagram_UserList,i)
                        
                        print('datagram of user list for type 48 / 49',datagram_UserList)
                        

                        
                        
                        if(typeDatagram == 48):
                                                     
                                Type0=bin(18)[2:].rjust(8,"0")
                                numSequence=self.num
                                self.num+=1
                                NumSeqBin=bin(numSequence)
                                NumSeqUserList=NumSeqBin[2:].rjust(10,"0")

                                corps=b''
                            
                                sendListRoom=[]	
                                peopleRoom=[]
                                for u in self.serverProxy.getUserList():
                                        print(u. userChatRoom,roomName)
                                        if(u. userChatRoom==roomName):
                                                print('hi a friend in this movie room')
                                               
                                                sendListRoom.append(u.userAddress)
                                                peopleRoom.append(u.userName)
                                                                
                                if(len(peopleRoom)>0):
                                        
                                    corps+=struct.pack('>H',len(peopleRoom)) 
                                    for i in peopleRoom:
                                        corps+=struct.pack('b%ds'%len(i),len(i),i.encode('utf-8'))            
                                    print('send list check',sendListRoom)

                                
                                
                                
                                LongueurInt=len(corps)
                                LongueurBin=bin(LongueurInt)
                                Longueur0=LongueurBin[2:].rjust(14, "0")
                                head=Type0+NumSeqUserList+Longueur0
                                datagram=struct.pack('>I',int(head,2))+corps
                                if (len(sendListRoom)>0):
                                        print('send list to users in salon',datagram)
                                        for i in sendListRoom:
                                            self.transport.write(datagram,i)   
                                                
                        
                        
                elif(typeDatagram == 3):    
                        print('now there is a user who wanna quit the system',host_port)
                        #del self.numAttendu[host_port]
                        self.serverProxy.removeUser(self.serverProxy.getUserByAddress(host_port).userName)
                        #self.serverProxy.updateUserChatroom(self.serverProxy.getUserByAddress(host_port).userName,ROOM_IDS.OUT_OF_THE_SYSTEM_ROOM)
                                             
                        self.online-=1
                        print('self.online',self.online)
                        print('show me the user List when someOne LEAVE',self.serverProxy.getUserList())
                        
                        
                        NumSalonP=0
                        salonP=[]
                        salonList={}
                        
                        corps0=b''
                        print('test for user list change while a new user',self.serverProxy.getUserList())
                        '''
                        [<Instance of c2wUser; userName=alice, userChatRoom=<class 'c2w.main.constants.ROOM_IDS.MAIN_ROOM'>, 
                        userChatInstance=None, userAddress=('127.0.0.1', 46602)>, <Instance of c2wUser; 
                        userName=aliceff, userChatRoom=<class 'c2w.main.constants.ROOM_IDS.MAIN_ROOM'>, userChatInstance=None, userAddress=('127.0.0.1', 36153)>]
                        '''
                        self.movieList0={}

                        for m in self.serverProxy.getMovieList():
                                                self.movieList0[m.movieTitle]=[0,[]]
                        for u in self.serverProxy.getUserList():
                                print(u)
                                if(u.userChatRoom==ROOM_IDS.MAIN_ROOM):
                                        print('this user is in the main room')
                                        NumSalonP+=1
                                        salonP.append(u.userName)
                                else:
                                        if u.userChatRoom in self.movieList:
                                                self.movieList0[u.userChatRoom][0]+=1
                                                self.movieList0[u.userChatRoom][1].append(u.userName)
                        self.movieList=self.movieList0
                        corps0+=struct.pack('>H',NumSalonP)
                        print('test salonP',salonP)
                        print('exam for movie list: slef',self.movieList)
                        for i in salonP:
                                i=i.encode("utf-8")
                                corps0+=struct.pack('b%ds'%len(i),len(i),i)
                        for i in self.movieList:
                                corps0+=struct.pack('>H',self.movieList[i][0])
                                if not (self.movieList[i][1]==0):
                                        print('this moivie room is not empty')
                                        for i in self.movieList[i][1]:
                                                i=i.encode("utf-8")
                                                corps0+=struct.pack('b%ds'%len(i),len(i),i)
                                        
                                     
                                
                        print(corps0,'corps0 check itself')      

                        TypeBin=bin(19)
                        Type0=TypeBin[2:].rjust(8,"0")
                        Type0=TypeBin[2:].rjust(8,"0")


                        
                        numSequence=self.num
                        self.num+=1
                        NumSeqBin=bin(numSequence)
                        NumSeqUserList=NumSeqBin[2:].rjust(10,"0")
                                        
                        LongueurInt=1+len(corps0)+1
                        LongueurBin=bin(LongueurInt)
                        Longueur0=LongueurBin[2:].rjust(14, "0")
                        
                        #datagram_UserList=struct.pack('>IH',int(Type0+NumSeqUserList+Longueur0,2),numSalon)+corps0
                        datagram_UserList=struct.pack('>IH',int(Type0+NumSeqUserList+Longueur0,2),len(self.movieList)+1)+corps0
                        
                        #self.transport.write(datagram_UserList,host_port)
                        sendList=[]
                        for u in self.serverProxy.getUserList():
                                print(u. userChatRoom)


                        
                                if(u. userChatRoom==ROOM_IDS.MAIN_ROOM):
                                        sendList.append(u.userAddress)
                        print('send list check',sendList)
                        if (len(sendList)>0):
                                for i in sendList:
                                        self.transport.write(datagram_UserList,i)
                        
                        print('boss int quit 3 test: datagram of user list',datagram_UserList)
                
                        
                        
                        
                        
                        
                elif(typeDatagram == 64):
                        print('there is a user speaking')
        
                
                        datagram=struct.pack('b',65)+datagram[1:]
                        
                        lenUsername=datagram[4]
        
                        userName=struct.unpack('%ds'%lenUsername,datagram[5:5+lenUsername])[0]
                        userName=userName.decode('utf-8')
                        print('test userbnal talking',userName,len(userName))
                        uSend=self.serverProxy.getUserByName(userName)
                        print('user name in 64',userName)
                        sendList=[]
                        for u in self.serverProxy.getUserList():
                   
                                
                                if(not u==uSend and u.userChatRoom==uSend.userChatRoom):
                                        sendList.append(u.userAddress)
                        print('test send list',sendList)                
                        if (len(sendList)>0):
                                for i in sendList:
                                        self.transport.write(datagram,i)
        
                        
        
                                          
                        
                                
                                
                        
                        
                        
        
        





