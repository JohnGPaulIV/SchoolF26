/*

CS 450 Lab1
Fall 2024

Name: John Gilbert Paul IV
Honor code statement:

*/

#include <stdio.h>

#include "thread.h"
#include "list.h"

#ifndef SCHEDULE_H
#define SCHEDULE_H
#include "schedule.h"
#endif

extern struct list scheduler;

void init_scheduler()
{

  // printf("init_scheduler() still needs to be implemented\n");
  list_init(&scheduler);
}

void schedule_thread(struct thread *to_schedule)
{

  // printf("schedule_thread() still needs to be implemented\n");
  // if (list_begin(&scheduler) == list_end(&scheduler))
  // {
  //   list_insert(list_end(&scheduler), &to_schedule->scheduler_elem);
  // }
  struct list_elem *e;
  for (e = list_begin(&scheduler); e != list_end(&scheduler); e = list_next(e))
  {
    struct thread *t = list_entry(e, struct thread, scheduler_elem);
    int p = t->priority;
    if (p < to_schedule->priority)
      break;
  }
  list_insert(e, &to_schedule->scheduler_elem);
}

void print_schedule()
{

  // printf("print_schedule() still needs to be implemented\n");
  printf("Printing schedule:\n");
  printf("__________________\n");
  int thread_n = 0;
  struct list_elem *e;
  for (e = list_begin(&scheduler); e != list_end(&scheduler); e = list_next(e))
  {
    struct thread *t = list_entry(e, struct thread, scheduler_elem);
    printf("Thread %d\n", thread_n++);
    printf("\tStatus: %d\n", t->status);
    printf("\tName: %s\n", t->name);
    printf("\tPrio: %d\n", t->priority);
  }
}
