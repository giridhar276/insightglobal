
import shutil

# Copy a file
shutil.copy('source.txt', 'destination.txt')

# Copy a directory
shutil.copytree('source_dir', 'destination_dir')

# Remove a directory
shutil.rmtree('destination_dir')

# Move a file or directory
shutil.move('source.txt', 'new_location.txt')
