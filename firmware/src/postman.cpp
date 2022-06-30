#include <Arduino.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
int postMan()
{
    int sockfd, portno, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    char buffer[256];
    portno = atoi("5080");
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        Serial.println("ERROR opening socket");
    server = gethostbyname("localhost");
    if (server == NULL) {
        Serial.println("ERROR, no such host\n");
    }
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);
    serv_addr.sin_port = htons(portno);
    if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
        Serial.println("ERROR connecting");
    Serial.println("Please enter the message: ");
    bzero(buffer,256);
    fgets(buffer,255,stdin);
    n = write(sockfd,buffer,strlen(buffer));
    if (n < 0) 
         Serial.println("ERROR writing to socket");
    bzero(buffer,256);
    n = read(sockfd,buffer,255);
    if (n < 0) 
         Serial.println("ERROR reading from socket");
    Serial.println(buffer);
    close(sockfd);
    return 0;
}
