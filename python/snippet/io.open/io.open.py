import io
import re

fs = io.open('data.txt')
for line in fs:
    print line
pattern = re.compile(r'[aA]pple')
while True:
    line = fs.readline()
    if line == '':
        break
    ret = pattern.search(line)
    pattern.match
    if ret is not None:
        print line
    else:
        print 'can not find apple'
