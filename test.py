import re

text = re.sub('<[^<]+>', "", open("wsj/wsj.train").read())
print(text)