
import subprocess

# Run a command and capture its output
result = subprocess.run(['echo', 'Hello, World!'], capture_output=True, text=True)
print(result.stdout)

# Run a command without waiting for it to complete
process = subprocess.Popen(['sleep', '2'])
print('Process started')
process.wait()
print('Process completed')
