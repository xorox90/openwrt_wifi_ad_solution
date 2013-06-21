#ifndef _EPOLL_SERVER
#define _EPOLL_SERVER

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "single_list.h"

static char* substr(char* input_data)
{
        int i,size;
        char *first_comma;
        char *second_comma;
        char *ret_message;

        first_comma=strchr(input_data,',');
        if(first_comma == NULL)
                return NULL;
        *first_comma=' ';
        first_comma++;

        second_comma=strchr(input_data,',');
        if(second_comma == NULL)
                return NULL;

        size = (int)second_comma-(int)first_comma;

        ret_message=(char*)calloc(size+1,sizeof(char));
        strncpy(ret_message,first_comma,size);

        return ret_message;

}
int add_list(Node **list,const char* data)
{
	char *mac,*time_c;
	int times;
	char *copy_data=strdup(data);
	char system_message[100];

	mac=substr(copy_data);
	time_c=substr(copy_data);
	if(mac == NULL || time_c == NULL) {
		free(copy_data);
		free(time_c);
		return -1;
	}
	times = atoi(time_c) + time(0);

	SL_Insert(list,mac,times);

	memset(system_message,0,100);
	strcat(system_message,"/usr/sbin/iptables -t nat -I MAC_AUTH -i br-lan -m mac --mac-source ");
	strcat(system_message,mac);
	strcat(system_message," -j ACCEPT");
	printf("msg = %s (%d)\n",system_message,times);
	system(system_message);

	free(copy_data);
	free(time_c);
	return 0;
}


#endif
