import math
import operator

def readFile(filePath):
	with open(filePath) as f:
		data = [line.split() for line in f]
	data = [i[0].split(',') for i in data]
	return data

def GaussianNB(data):

	resClass = list()
	resClass.append([i[10] for i in data])
	resClass = resClass[0]

	p = dict() #dict of probabilities of resultant classes

	p['1'] = resClass.count('1')/200
	p['2'] = resClass.count('2')/200

	# Calculate the mean and variances for each attribute corresponding to each class.
	data2 = list()
	data1 = list()

	#Divide the data into two classes:
	for i in data:
		if i[10] == '1':
			data1.append(i)
		elif i[10] == '2':
			data2.append(i)

	#Take means of both classes
	sumCol1 = [sum(eval(row[i]) for row in data1) for i in range(1, len(data1[0]) - 1)]
	meanList1 = [x / 200 for x in sumCol1]

	sumCol2 = [sum(eval(row[i]) for row in data2) for i in range(1, len(data2[0]) - 1)]
	meanList2 = [x / 200 for x in sumCol2]

	dataAttributes = [i[1:-1] for i in data]

	stdDev1 = [sum([pow(map(operator.sub, i, meanList1), 2) for i in dataAttributes])]

	#variance = dict()








def main():
	filePath = 'glasshw1.csv'
	data = readFile(filePath)
	GaussianNB(data)

if __name__== "__main__":
	main()	