import os
import filecmp
import operator
import collections
import datetime
import csv

def getData(file):
#Input: file name
#Ouput: return a list of dictionary objects where 
#the keys will come from the first row in the data.

#Note: The column headings will not change from the 
#test cases below, but the the data itself will 
#change (contents and size) in the different test 
#cases.

	#Your code here:
	l = []
	headings = []
	with open(file,"r") as f:
		for lines in f.readlines():
			d = {}
			a = lines.split(",")
			# if heading is empty, populate the headings
			if len(headings) == 0:
				for heading in a:
					headings.append(heading)
			else:
				for i in range(0, len(headings)):
					d[headings[i].strip("\n")] = a[i].strip("\n")
				l.append(d)
	return(l)

#Sort based on key/column
def mySort(data,col):
#Input: list of dictionaries
#Output: Return a string of the form firstName lastName

	#Your code here:
	s = ""
	l = []
	l = sorted(data, key=operator.itemgetter(col))
	s = l[0]["First"] + " " + l[0]["Last"]
	return s

#Create a histogram
def classSizes(data):
# Input: list of dictionaries
# Output: Return a list of tuples ordered by
# ClassName and Class size, e.g 
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]

	#Your code here:
	result = {'Senior': 0, 'Junior': 0, 'Sophomore': 0, 'Freshman': 0}
	for i in data:
		if i["Class"] == 'Senior':
			result['Senior'] += 1
		elif i["Class"] == 'Junior':
			result['Junior'] += 1
		elif i['Class'] == 'Sophomore':
			result['Sophomore'] += 1
		else:
			result['Freshman'] += 1
	result = sorted(result.items(), key = operator.itemgetter(1), reverse = True)
	return result



# Find the most common day of the year to be born
def findDay(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB

	#Your code here:
	date = []
	l = []
	for i in a:
		date.append(i["DOB"])
	for day in date:
		l += day.rsplit("/")[1:-1]
	counter = collections.Counter(l).most_common(1)
	return int(counter[0][0])


# Find the average age (rounded) of the Students
def findAge(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB

	#Your code here:
	date = []
	today = datetime.date.today()
	days = []
	bday = []
	total = 0

	for i in a:
		date.append(i["DOB"])
	for day in date:
		days.append(datetime.datetime.strptime(day, "%m/%d/%Y"))
	for x in days:
		bday.append(today.year - x.year - ((today.month, today.day) < (x.month, x.day)))
	for j in bday:
		total += j
	final = round(total/len(bday))
	return final

#Similar to mySort, but instead of returning single
#Student, all of the sorted data is saved to a csv file.
def mySortPrint(a,col,fileName):
#Input: list of dictionaries, key to sort by and output file name
#Output: None

	#Your code here:
	for i in a:
		del i["Class"]
		del i["DOB"]
	l = sorted(a, key=operator.itemgetter(col))
	headers = ["First", "Last", "Email"]

	with open(fileName, "w") as f:
		w = csv.DictWriter(f, headers, lineterminator='\n')
		w.writerows(l)



################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ",end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),40)
	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',15)
	total += test(mySort(data2,'First'),'Adam Rocha',15)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',15)
	total += test(mySort(data2,'Last'),'Elijah Adams',15)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',15)
	total += test(mySort(data2,'Email'),'Orli Humphrey',15)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],10)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],10)

	print("\nThe most common day of the year to be born is:")
	total += test(findDay(data),13,10)
	total += test(findDay(data2),26,10)
	
	print("\nThe average age is:")
	total += test(findAge(data),39,10)
	total += test(findAge(data2),41,10)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,10)


	print("Your final score is: ",total)
# Standard boilerplate to call the main() function that tests all your code.
if __name__ == '__main__':
    main()

