
import queue
import threading

# Create a queue
q = queue.Queue()

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print(f'Processing item: {item}')
        q.task_done()

# Create worker threads
threads = []
for i in range(3):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# Put items in the queue
for item in range(10):
    q.put(item)

# Block until all items are processed
q.join()

# Stop the worker threads
for i in range(3):
    q.put(None)
for t in threads:
    t.join()
