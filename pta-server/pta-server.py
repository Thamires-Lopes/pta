from socket import *
import os

# CONFIGURAÇÃO
# python pta-client.py 127.0.0.1 11550 user1
serverPort = 11550
# Cria o Socket TCP (SOCK_STREAM) para rede IPv4 (AF_INET)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
# Socket fica ouvindo conexoes. O valor 1 indica que uma conexao pode ficar na fila
serverSocket.listen(1)
# Pegando lista de usuários do arquivo users.txt
usersTxt = open("users.txt", "r")
listOfUsers = usersTxt.read().splitlines()
usersTxt.close()
# Pegando nome dos arquivos
path = 'files'
listOfFiles = os.listdir(path)

approved = False


def checkUser(user):
    if(user in listOfUsers):
        return True
    else:
        return False


def sendListFiles():
    numberOfFiles = len(listOfFiles)
    stringOfFiles = ",".join(listOfFiles)
    answer = str(numberOfFiles) + " " + stringOfFiles
    return answer


while 1:
    try:
        if(approved == False):
            connectionSocket, addr = serverSocket.accept()

        received = connectionSocket.recv(1024).decode('ascii')
        msg = received.split()
        seqNumber = msg[0]
        command = msg[1]
        close = False
        answer = str(seqNumber) + " "

        if(approved == False and command != "CUMP"):
            close = True
            answer += "NOK"

        if command == "CUMP":
            if checkUser(msg[2]):
                approved = True
                answer += "OK"
            else:
                close = True
                answer += "NOK"

        if(approved):
            close = False
            if command == "LIST":
                try:
                    answer += "ARQS" + sendListFiles()
                except:
                    answer += "NOK"
            elif command == "PEGA":
                try:
                    filePath = path + "/" + msg[2]
                    sizeOfFile = os.stat(filePath).st_size
                    answer += "ARQ" + str(sizeOfFile) + str(sizeOfFile)
                except:
                    answer += "ARQ" + "NOK"
            elif command == "TERM":
                approved = False
                answer += "OK"
                close = True

        if close:
            connectionSocket.send(answer.encode())
            connectionSocket.close()
        else:
            print(answer)
            connectionSocket.send(answer.encode())

    except(KeyboardInterrupt, SystemExit):
        break

serverSocket.shutdown(SHUT_RDWR)
serverSocket.close()
