filenames = ['result.txt','EnronDataset/validation.txt']

f1 = open(filenames[0], 'r')
f = open(filenames[1],'r')
for line in f:
    line1 = line.split()[0]
    line2 = f1.readline().rstrip('\n')
    if line1 == line2:
        print("Same "+line1)
    else:
        print("Different " + line1 + " " +line2)
    