import math

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





def main():
	filePath = 'glasshw1.csv'
	data = readFile(filePath)
	GaussianNB(data)

if __name__== "__main__":
	main()	