import math
import operator

# Steps:
# 1. Calculate class priors P(1), P(2)
# 2. Divide the dataset into two parts, 1 and 2.
# 3. Calculate mean and stdev for all attributes separately for both classes.
# 4. For a new data-point, calculate

def readFile(filePath):
	with open(filePath) as f:
		data = [line.split() for line in f]
	data = [i[0].split(',') for i in data]
	return data


# Function to calculate standard deviation, given data points and mean
def stdev(column, mean):
	std = 0
	differences = [x - mean for x in column]
	sq_differences = [d ** 2 for d in differences]
	ssd = sum(sq_differences)
	variance = ssd / len(column)

	sd = math.sqrt(variance)
	return sd


def log_prob(sigma, mean, x):

	temp1 = - math.log(2 * math.pi * (sigma)**2) * 0.5
	temp2 = - 0.5 * ((eval(x) - mean)/(sigma))**2

	log_prob_x = temp1 + temp2
	return log_prob_x


def trainGaussianNB(data):

	resClass = list()

	# List all the class labels
	resClass.append([i[10] for i in data])
	resClass = resClass[0]


	# Calculate the mean and variances for each attribute corresponding to each class.
	data2 = list()
	data1 = list()

	#Divide the data into two classes:
	for i in data:
		if i[10] == '1':
			data1.append(i)
		elif i[10] == '2':
			data2.append(i)

	#Calculate means of all attributes for both classes
	sumCol1 = [sum(eval(row[i]) for row in data1) for i in range(1, len(data1[0]) - 1)]
	meanList1 = [x / len(data1) for x in sumCol1]

	sumCol2 = [sum(eval(row[i]) for row in data2) for i in range(1, len(data2[0]) - 1)]
	meanList2 = [x / len(data2) for x in sumCol2]


	# Extracting only the data attributes. (the first column is the index and the last attribute is the class).
	dataAttributes1 = [i[1:-1] for i in data1]
	dataAttributes2 = [i[1:-1] for i in data2]


	# Lists of standard deviations
	stdDev1 = list()
	stdDev2 = list()

	for i in range(0,9):

		column = [eval(row[i]) for row in dataAttributes1]
		stdDev1.append(stdev(column, meanList1[i]))

		column = [eval(row[i]) for row in dataAttributes2]
		stdDev2.append(stdev(column, meanList2[i]))

	return ([meanList1,meanList2], [stdDev1, stdDev2])


def testGaussianNB(meanList, stdevList, data):
	# We find sum of log probabilities for both classes. We assign the class with a higher probability.


	dataAttr = [i[1:-1] for i in data]

	actualResClass = [i[-1] for i in data]
	predictedResClass = list()
	meanList1, meanList2 = meanList[0], meanList[1]
	stdevList1, stdevList2 = stdevList[0], stdevList[1]

	# Prior probabilities
	p = dict()
	p['1'] = float(actualResClass.count('1'))/len(actualResClass)
	p['2'] = float(actualResClass.count('2'))/len(actualResClass)

	# Calculate for Class 1.
	# iterate over data points.
	for i in dataAttr:
		# iterate over attributes
		sum_log_prob1 = 0
		sum_log_prob2 = 0
		for j in range(0,len(i)):
			sum_log_prob1 += log_prob(stdevList1[j], meanList1[j], i[j])
			sum_log_prob2 += log_prob(stdevList2[j], meanList2[j], i[j])

		p1 = sum_log_prob1 + math.log(p['1'])
		p2 = sum_log_prob2 + math.log(p['2'])

		if(p1 > p2):
			predictedResClass.append('1')
		else:
			predictedResClass.append('2')

	#Calculate accuracy:
	correct_predictions = 0

	for i in range(len(actualResClass)):
		if(actualResClass[i] == predictedResClass[i]):
			correct_predictions += 1

	accuracy = (float(correct_predictions)/len(actualResClass))
	return accuracy



def kFoldCrossValidate(data, k):

	# Splitting the dataset in k parts.
	partSize = len(data)/k
	accuracyList = list()
	for i in range(0,k):

		train_data = data[0:i*partSize] + data[(i+1)*partSize:]
		test_data = data[i*partSize:(i+1)*partSize]

		(meanList, stdevList) = trainGaussianNB(train_data)
		accuracy = testGaussianNB(meanList, stdevList, test_data)
		print "For iteration: ", i+1 , " accuracy = ", accuracy
		accuracyList.append(accuracy)

	averageAccuracy = reduce(lambda x, y: x + y, accuracyList) / len(accuracyList)
	print "Average accuracy from cross validation: ", averageAccuracy


def main():
	filePath = 'glasshw1.csv'
	data = readFile(filePath)

	#Train the Naive Bayes classifier on the given data.
	(meanList, stdevList) = trainGaussianNB(data)

	#Test the classifier on the training data.
	accuracy = testGaussianNB(meanList, stdevList, data)
	print "Accuracy of Naive Bayes Classifier: ", accuracy

	print "Enter k for Cross Validation: "
	k = int(raw_input())

	kFoldCrossValidate(data, k)


if __name__== "__main__":
	main()