#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/epoll.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <time.h>
#include <pthread.h>
#include "epoll_server.h"



#define LISTEN_BACKLOG		256
#define PORT			"5000"
#define MAX_EPOLL_EVENTS 	10
#define DATA_SIZE		60

#define ADD_EV(a, b)	if (add_ev(a, b) == -1) { printf("Fail: add_ev"); exit(EXIT_FAILURE); }
#define DEL_EV(a, b)	if (del_ev(a, b) == -1) { printf("Fail: del_ev"); exit(EXIT_FAILURE); }

int add_ev(int efd, int fd);	/* Add epoll variable to epollfd */
int del_ev(int efd, int fd); /* delete epoll variabe from epollfd */
Node *list;
int check=1;

void *time_check(void *arg)
{
	while(check) {
		SL_Delete(&list,time(0));
		sleep(1);
	}
	pthread_exit((void*)100);
}


int main(void)
{
	/* network var			*/
	socklen_t	len_saddr;
	int		epollfd, ret_poll, fd, fd_listener, ret_recv;
	char		buf[DATA_SIZE];
	/* I/O multiplexing var */
	struct epoll_event	*ep_events;
	/* logical var 			*/
	int		rc_gai,i,j,ret_val;
	char 		command;
	struct addrinfo ai, *ai_ret;
	pthread_t	threads;
	Node		*current;


	memset(&ai, 0, sizeof(ai));
	ai.ai_family = AF_INET;
	ai.ai_socktype = SOCK_STREAM;
	ai.ai_flags = AI_ADDRCONFIG | AI_PASSIVE;

	if ((rc_gai = getaddrinfo(NULL, PORT, &ai, &ai_ret)) != 0) {
		printf("Fail: getaddrinfo():%s\n", gai_strerror(rc_gai));
		exit(EXIT_FAILURE);
	}

	if ((fd_listener = socket( ai_ret->ai_family, ai_ret->ai_socktype, ai_ret->ai_protocol)) == -1) {
		printf("Fail: socket()\n");
		exit(EXIT_FAILURE);
	}

	if(fcntl(fd_listener,F_SETFL,O_NONBLOCK | fcntl(fd_listener,F_GETFL)) == -1) {
		printf("Fail: fcntl()\n");
		exit(EXIT_FAILURE);
	}

	if(bind(fd_listener, ai_ret->ai_addr, ai_ret->ai_addrlen) == -1) {
		printf("Fail: bind()\n");
		exit(EXIT_FAILURE);
	}
	pthread_create(&threads,NULL,&time_check,(void*)NULL);

	listen(fd_listener, LISTEN_BACKLOG);

	if ((epollfd = epoll_create(1)) == -1) {
		printf("Fail: epoll_create()\n");
		exit(EXIT_FAILURE);
	}
	if ((ep_events = calloc(MAX_EPOLL_EVENTS , sizeof(struct epoll_event))) == NULL) {
		printf("Fail: calloc()\n");
		exit(EXIT_FAILURE);
	}

	ADD_EV(epollfd, fd_listener);

	while (1) {
		memset(buf,0,DATA_SIZE);
		if ((ret_poll = epoll_wait(epollfd, ep_events, MAX_EPOLL_EVENTS , -1)) == -1) {
//			printf("Disconnected\n");

		}
		for (i=0; i<ret_poll; i++) {
			if (ep_events[i].events & EPOLLIN) {
				/* connected */
				if (ep_events[i].data.fd == fd_listener) {
					struct sockaddr_storage saddr_c;
					while(1) {
						len_saddr = sizeof(saddr_c);
						fd = accept(fd_listener, (struct sockaddr *)&saddr_c, &len_saddr);
						if (fd == -1) {
							if (errno == EAGAIN) 
								break;
							break;
						}
						
						if(fcntl(fd,F_SETFL,O_NONBLOCK | fcntl(fd,F_GETFL)) == -1)
							printf("Fail : fcntl()\n");

						ADD_EV(epollfd, fd);
						printf("accept : add socket (%d)\n", fd);
					}
					continue;
				}
				/* Data Recevied*/
				if ((ret_recv = recv(ep_events[i].data.fd, buf, sizeof(buf), 0)) == -1) {
					printf("Fail: recv()\n");
				} else {
					if (ret_recv == 0) { /* closed */
						printf("fd(%d) : Session closed\n", ep_events[i].data.fd);
						DEL_EV(epollfd, ep_events[i].data.fd);
					} else { 		/* normal */

//						printf("recv(fd=%d,n=%d) = %.*s",ep_events[i].data.fd, ret_recv, ret_recv, buf);

						if(buf[1] == 'S') {
							printf("Save Address, recv(fd=%d,n=%d) = %.*s \n",ep_events[i].data.fd,ret_recv,ret_recv,buf);
							if(add_list(&list,buf) == -1) {
								memset(buf,0,DATA_SIZE);
								printf("Command Error-\n");
								strcpy(buf,"ERR-\n");
							}else{
								memset(buf,0,DATA_SIZE);
								strcpy(buf,"OK\n");
							}
							send( ep_events[i].data.fd ,buf ,sizeof(buf),0);
							DEL_EV(epollfd, ep_events[i].data.fd);
						} else {
							printf("Command Error, recv(fd=%d,n=%d) = %.*s \n",ep_events[i].data.fd,ret_recv,ret_recv,buf);
							memset(buf,0,DATA_SIZE);
							strcpy(buf,"ERR\n");
							send( ep_events[i].data.fd ,buf ,sizeof(buf),0);
							DEL_EV(epollfd, ep_events[i].data.fd);
						}
					}
				}
				printf("----------------------------------------------------\n");
				current = list;
				while(current != NULL) {
					printf("Mac = %s , Time = %d\n",current->Data->Mac,current->Data->Time);
					current = current->NextNode;

				}

				printf("----------------------------------------------------\n");

			}
		}
	}
	check=0;
	pthread_join(threads,(void**)ret_val);
	if(ret_val == 100)
		printf("Server Exit\n");
	return 0;
}

int add_ev(int efd, int fd)
{
	struct epoll_event ev;

	ev.events = EPOLLIN | EPOLLPRI;
	ev.data.fd = fd;
	if (epoll_ctl(efd, EPOLL_CTL_ADD, fd, &ev) == -1) {
		printf("fd(%d) EPOLL_CTL_ADD  Error(%d:%s)\n", fd, errno, strerror(errno));
		return -1;
	}

	return 0;
}

int del_ev(int efd, int fd)
{
	if (epoll_ctl(efd, EPOLL_CTL_DEL, fd, NULL) == -1) {
		printf("fd(%d) EPOLL_CTL_DEL Error(%d:%s)\n", fd, errno, strerror(errno));
		return -1;
	}
	close(fd);
	return 0;
}
