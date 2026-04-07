
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Example script')

# Add an argument
parser.add_argument('name', help='Your name')

# Parse the arguments
args = parser.parse_args()

# Print a message
print(f'Hello, {args.name}!')
