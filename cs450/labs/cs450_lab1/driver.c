#include <stdio.h>

#include "thread.h"
#include "schedule.h"

int main() {

  struct thread *new_thread;

  init_scheduler();

  new_thread = create_thread(0, THREAD_READY, "Thread1", 20);
  schedule_thread(new_thread);

  new_thread = create_thread(1, THREAD_READY, "Thread2", 10);
  schedule_thread(new_thread);

  new_thread = create_thread(2, THREAD_READY, "Thread3", 15);
  schedule_thread(new_thread);

  new_thread = create_thread(3, THREAD_READY, "Thread4", 15);
  schedule_thread(new_thread);

  print_schedule();

  return 0;

}
