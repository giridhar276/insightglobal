
import re

# Find all occurrences of a pattern in a string
text = 'The quick brown fox jumps over the lazy dog'
pattern = r'\b\w{4}\b'
matches = re.findall(pattern, text)
print(matches)

# Replace all occurrences of a pattern in a string
replaced_text = re.sub(pattern, '****', text)
print(replaced_text)
