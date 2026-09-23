#include <stdio.h>
#include "tests/threads/tests.h"
#include "threads/init.h"
#include "threads/malloc.h"
#include "threads/synch.h"
#include "threads/thread.h"
#include "devices/timer.h"

#define NUM_THREADS 4
#define MAX_NAME_LEN 10

static void sleeper(void *);

/**
 * Author: John Gilbert Paul IV
 * Honor Code Statement: I, John Gilbert Paul IV, swear that I have completed this
 *                       Assignment with regard and in accordance to the JMU Academic Honor Code.
 */

/* Information about the test. */
struct sleep_test
{
  int64_t start; /* Current time before thread sleeps. */
  int64_t end;   /* Current time after thread wakes up */
  tid_t tid;
};

void test_alarm_with_thread(void)
{

  struct sleep_test test;

  msg("Creating a thread to sleep 100 ticks.");
  msg("The thread will return the ticks in which it slept and ran again.");

  /* Start thread. */
  thread_create("thread 0", PRI_DEFAULT, sleeper, &test);

  /* Wait long enough for the thread to finish. */
  timer_sleep(300);

  msg("Test started at clock time %d", test.start);
  msg("Thread resumed at clock time %d", test.end);
}

void test_alarm_with_many(void)
{

  struct sleep_test *tests = calloc(NUM_THREADS, sizeof(struct sleep_test));
  char **t_names = calloc(NUM_THREADS, sizeof(char *));
  if (!tests)
    return;

  msg("begin");
  msg("Creating %d threads to sleep 100 ticks each.", NUM_THREADS);
  msg("Each thread will return the ticks in which it slept and ran again.");

  for (int i = 0; i < NUM_THREADS; i++)
  {
    t_names[i] = calloc(MAX_NAME_LEN, sizeof(char));
    snprintf(t_names[i], MAX_NAME_LEN, "thread %d", i);
    tests[i].tid = thread_create(t_names[i], PRI_DEFAULT, sleeper, &tests[i]);

    timer_sleep(1);
  }

  for (int i = 0; i < NUM_THREADS; i++)
  {
    msg("Thread %d", tests[i].tid);
    msg("\tTest started at clock time %d", tests[i].start);
    msg("\tThread resumed at clock time %d", tests[i].end);

    free(t_names[i]);
  }

  msg("end");

  free(t_names);
  free(tests);
}

/* Sleeper thread. */
static void
sleeper(void *test_)
{
  struct sleep_test *test = test_;

  test->start = timer_ticks();
  timer_sleep(100);
  test->end = timer_ticks();
}
