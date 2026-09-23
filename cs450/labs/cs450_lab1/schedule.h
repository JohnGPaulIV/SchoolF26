#ifndef SCHEDULE_H
#define SCHEDULE_H

#include "thread.h"
#include "list.h"

struct list scheduler;

void init_scheduler();
void schedule_thread(struct thread *to_schedule);
void print_schedule();


#endif
