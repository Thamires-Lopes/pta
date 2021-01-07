from socket import *
import os

serverPort = 11550
# Cria o Socket TCP (SOCK_STREAM) para rede IPv4 (AF_INET)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
# Socket fica ouvindo conexoes. O valor 1 indica que uma conexao pode ficar na fila
serverSocket.listen(1)

# Pegando lista de usuários do arquivo users.txt
usersTxt = open("users.txt", "r")
listOfUsers = usersTxt.read().splitlines()

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
        # Cria um socket para tratar a conexao do cliente
        connectionSocket, addr = serverSocket.accept()
        received = connectionSocket.recv(1024).decode('ascii')
        msg = received.split()
        seqNumber = msg[0]
        command = msg[1]
        if approved == False:
            if(command == "CUMP"):
                if checkUser(msg[2]):
                    approved = True
                    answer = seqNumber + " " + "OK"
                    answer = answer.encode()
                    connectionSocket.send(answer)

                else:
                    answer = seqNumber + " " + "NOK"
                    answer = answer.encode()
                    connectionSocket.send(answer)
                    connectionSocket.close()
            else:
                answer = seqNumber + " " + "NOK"
                answer = answer.encode()
                connectionSocket.send(answer)
                connectionSocket.close()
        else:

            if msg[1] == "LIST":
                try:
                    answer = seqNumber + " " + sendListFiles()
                    answer = answer.encode()
                    connectionSocket.send(answer)
                except:
                    answer = seqNumber + " " + "NOK"
                    answer = answer.encode()
                    connectionSocket.send(answer)

            elif msg[1] == "PEGA":
                try:
                    filePath = path + "/" + msg[2]
                    sizeOfFile = os.stat(filePath).st_size
                    answer = seqNumber + " " + \
                        str(sizeOfFile) + str(sizeOfFile)
                    answer = answer.encode()
                    connectionSocket.send(answer)

                except:
                    answer = seqNumber + " " + "NOK"
                    answer = answer.encode()
                    connectionSocket.send(answer)

            elif msg[1] == "TERM":
                answer = "OK"
                answer = answer.encode()
                connectionSocket.send(answer)
                connectionSocket.close()
    except (KeyboardInterrupt, SystemExit):
        break
serverSocket.shutdown(SHUT_RDWR)
serverSocket.close()

# while 1:
#     try:
#         # Cria um socket para tratar a conexao do cliente
#         connectionSocket, addr = serverSocket.accept()
#         sentence = connectionSocket.recv(1024)
#         capitalizedSentence = sentence.upper()
#         connectionSocket.send(capitalizedSentence)
#         connectionSocket.close()
#     except (KeyboardInterrupt, SystemExit):
#         break

# serverSocket.shutdown(SHUT_RDWR)
# serverSocket.close()
