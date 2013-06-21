#ifndef _SINGLE_LIST_H
#define _SINGLE_LIST_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct node_data {
	char *Mac;
	int Time;
}Node_data;

typedef struct tagNode {
	Node_data *Data;
	struct tagNode *NextNode;
}Node;

Node* SL_CreateNode (Node_data *NewData)
{
	Node *NewNode = (Node*)malloc(sizeof(Node));
	NewNode->Data = NewData;
	NewNode->NextNode = NULL;
	return NewNode;
}

void SL_DestroyNode(Node *Node)
{
	free(Node);
}
void SL_AppendNode(Node **Head,Node *NewNode)
{
	if( (*Head) == NULL )
		*Head = NewNode;
	else {
		Node *Tail = (*Head);
		while (Tail->NextNode != NULL) {
			Tail = Tail->NextNode;
		}
		Tail->NextNode = NewNode;
	}
}

void SL_RemoveNode (Node **Head,Node *Remove)
{
	if(*Head == Remove)
		*Head = Remove->NextNode;
	else {
		Node *Current = *Head;
		while( Current != NULL && Current->NextNode != Remove ) {
			Current = Current->NextNode;
		}
		if( Current != NULL )
			Current->NextNode = Remove->NextNode;
	}
}
	
Node* SL_Create(char *Mac,int Time)
{
	Node_data *NewData;
	Node *NewNode;

	NewData=(Node_data*)malloc(sizeof(Node_data));
	NewData->Mac = Mac;
	NewData->Time = Time;
	NewNode = SL_CreateNode(NewData);

	return NewNode;
}
void SL_Insert(Node **Head,char *Mac,int Time)
{
	Node *NewNode=SL_Create(Mac,Time);
	SL_AppendNode(Head,NewNode);
}

void SL_Delete(Node **Head,int Time)
{
	char system_message[100];
	Node *Current = *Head;
	while( Current != NULL ) {
		if(Current->Data->Time < Time) {
			printf("Node %s is Deleted(time = %d)\n",Current->Data->Mac,Current->Data->Time);
		        memset(system_message,0,100);
		        strcat(system_message,"/usr/sbin/iptables -t nat -D MAC_AUTH -i br-lan -m mac --mac-source ");
		        strcat(system_message,Current->Data->Mac);
		        strcat(system_message," -j ACCEPT");
		        printf("msg = %s (%d)\n",system_message,Current->Data->Time);
		        system(system_message);
		
			SL_RemoveNode(Head,Current);
			SL_DestroyNode(Current);

		}
		Current = Current->NextNode;
	}
}
#endif

