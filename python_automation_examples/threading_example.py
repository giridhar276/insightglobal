
import threading
import time

def worker():
    print('Worker')
    time.sleep(2)
    print('Worker done')

# Create a thread
thread = threading.Thread(target=worker)

# Start the thread
thread.start()

# Wait for the thread to complete
thread.join()
print('Thread completed')
