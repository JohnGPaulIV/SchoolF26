#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "thread.h"

struct thread *create_thread(tid_t tid, enum thread_status status, char *name, int prio) {

  struct thread *new_thread = (struct thread *)malloc(sizeof(struct thread));
  if (new_thread == NULL) return NULL;

  new_thread->tid = tid;
  new_thread->status = status;
  new_thread->priority = prio;
  memcpy(&(new_thread->name), name, 16);
  (new_thread->name)[15] = '\x00';

  return new_thread;

}

void print_thread(struct thread *t){

  if (t == NULL)
    printf("Thread is NULL\n");
  else
    printf("Thread %d\n\tStatus: %d\n\tName: %s\n\tPrio: %d\n\n", t->tid, t->status, t->name, t->priority);

}

