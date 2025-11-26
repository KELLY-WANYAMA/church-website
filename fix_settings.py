import re

with open('eldoret/settings.py', 'r') as f:
    content = f.read()

# Fix the broken SECRET_KEY and DEBUG lines
content = re.sub(r"SECRET_KEY =\s*DEBUG = True\s*'", "SECRET_KEY = '", content)
content = re.sub(r"DEBUG = True\s*DEBUG = True", "DEBUG = True", content)

with open('eldoret/settings.py', 'w') as f:
    f.write(content)
