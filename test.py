import re

text = re.sub('<[^<]+>', "", open("small.txt").read())
print(text)