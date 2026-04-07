
import sched
import time

# Create a scheduler
scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print(f'Event: {name}')

# Schedule events
scheduler.enter(2, 1, print_event, argument=('first',))
scheduler.enter(4, 1, print_event, argument=('second',))

# Run the scheduler
scheduler.run()
