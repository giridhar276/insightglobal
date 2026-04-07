
import os

# List all files and directories in the current directory
print(os.listdir('.'))

# Create a new directory
os.mkdir('new_dir')

# Rename the directory
os.rename('new_dir', 'renamed_dir')

# Remove the directory
os.rmdir('renamed_dir')
