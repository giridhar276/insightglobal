
import glob

# Find all Python files in the current directory
print(glob.glob('*.py'))

# Find all text files in the current directory and subdirectories
print(glob.glob('**/*.txt', recursive=True))
