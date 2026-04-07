
import multiprocessing

def worker(num):
    print(f'Worker: {num}')

# Create and start multiple processes
for i in range(5):
    process = multiprocessing.Process(target=worker, args=(i,))
    process.start()
    process.join()
