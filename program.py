# 
# Samuel Geremew
# George Mason University
# 
# Analysis of Algorithms
# Dana Richards
#
#
# 2018 December 2nd
#
#



import random
# Each record of the input "file" has a field structure 
# (all field structures are the same)

# "file" is an array of records (10,000 records)
# Each record has an array of fields.
# record = an array of 20 fields f1,f2,f3,...,f20. 

# Each field f1,f2,f3,...,f20 has an integer value, between 1 and Ni. 
# You will generate random values for the Ni’s in the range 2 to 10. 

# You will create a input “file” of random records fields with 10,000 records. 
# (It is not a real file but is stored in an array of records, and the records 
# are just arrays themselves.)
#
############################################################################


# these are global counters for loop iterations for the 3 main algorithms
GREYCOUNT = 0
HORNERCOUNT = 0
RADIXCOUNT = 0



file = []		# "file" which contains 10,000 records
randomNs = []	# this is a list of the random Ni's

RECORDS = 10000
FIELDS = 20


# here we are creating a file
for i in range(0,FIELDS):
	Ni = random.randint(2,10)
	randomNs.append(Ni)
# record has 20 fields: f1,..,f20
for record in range(0,RECORDS):
	# Ni is a randomly generated value between 2 and 10

	# fill file with empty lists that we will add to next
	file.append([])

	for i in range(0,FIELDS):
		# each field has an integer value between 1 and Ni
		field = random.randint(1,(randomNs[i])-1)
		file[record].append(field)

#
# The 'full score' for a file will be computed as follows: for each successive 
# records compute the sum of the (positive) differences of corresponding 
# fields, and for the whole file it is the sum of these numbers. 
# 
# The 'binary score' for a file is computed by finding, for each successive 
# records, the number of corresponding fields that are different, and for the 
# whole file it is the sum of these.
#
#

def fullscore(file1):
	fscore = 0
	for r in range(1,RECORDS):
		for c in range(0,FIELDS):

			diff = file1[r-1][c] - file1[r][c]
			diff = abs(diff)
			fscore+=diff
	return fscore



def binaryscore(file1):
	bscore = 0
	for r in range(1,RECORDS):
		for c in range(0,FIELDS):

			diff = file1[r-1][c] - file1[r][c]
			diff = abs(diff)
			if diff > 0:
				bscore+=1
	return bscore

#
# print a file
#
#

def print_file(records, fields, file1):
	
	for record in range(0,records):
		print(f'({((record+1)):5})',end='')
		for i in range(0,fields):
			print(f'{file1[record][i]:3} ',end='')
		print()

################################################################################
# Your goal is to sort the input file in Gray-code order. You will implement 
# and evaluate three algorithms. You will need an algorithm A for sorting that 
# runs in O(n lg n) time; copy one from the book. In particular you should 
# implement these approaches:
# (a) use A with the procedure grayorder(X, Y ) (mentioned in Section-3)
# (b) use A after first calculating the rank of each with the left-to-right 
# 	“Horner’s rule” (mentioned in Section-3) and just use the rank as the sort 
# 	field (the rank would be a (m + 1)st field)
# (c) use the Radix sorting mentioned in Section-4.
################################################################################

#
# Python program for implementation of MergeSort which runs in O(n lg n) time
#
#

def mergeSort(file1):
    if len(file1)>1:
        global GREYCOUNT

        # Here file is being split into two halves
        mid = len(file1)//2
        lefthalf = file1[:mid]
        righthalf = file1[mid:]

        mergeSort(lefthalf)  # sort the first half
        mergeSort(righthalf) # sort the other half

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
        	# as it is specified in the specs and the paper we replace the 
        	# normal comparison with the greyOrder(X,Y) function
        	#
            # if lefthalf[i] < righthalf[j]:
            if greyOrder(lefthalf[i],righthalf[j]):
                file1[k]=lefthalf[i]
                i=i+1
            else:
                file1[k]=righthalf[j]
                j=j+1
            k=k+1
            GREYCOUNT+=1

        # was anything left?
        while i < len(lefthalf):
            file1[k]=lefthalf[i]
            i=i+1
            k=k+1
            GREYCOUNT+=1

        while j < len(righthalf):
            file1[k]=righthalf[j]
            j=j+1
            k=k+1
            GREYCOUNT+=1

#
# (a) use A with the procedure grayorder(X, Y ) (mentioned in Section-3)
#
#

# determines the grey order of two records
# returns a boolean value
def greyOrder(X,Y):
	total = 0
	global GREYCOUNT

	# scanning fields in records X and Y
	for i in range(0,FIELDS):

		if X[i] == Y[i]:
			total += X[i]
		else:
			# if total is even
			if total%2 == 0:
				return X[i] < Y[i]
			else:
				return Y[i] < X[i]
		GREYCOUNT+=1

#
# (b) use A after first calculating the rank of each with the left-to-right 
# 	“Horner’s rule” (mentioned in Section-3) and just use the rank as the sort 
# 	field (the rank would be a (m + 1)st field)
#
#


# rank() will give a record a rank by using a left to right scan in the 
# typical Horner's rule fashion
def rank(X,N):
	global HORNERCOUNT

	# starting with the first field in the record
	i = X[0]
	# j will start from the second field in the record
	for j in range(1,FIELDS):
		# if i is even
		if i%2 == 0:
			i2 = X[j]
		else:
			i2 = N[j]-1-X[j]
		i = (i*N[j]) + i2
		HORNERCOUNT+=1
	# append the rank for record X in the (m+1)th position
	X.append(i)

# calls rank() function for each record
def giveRank(file1):

	# calling rank function for each record 
	for record in range(0,RECORDS):
		rank(file1[record],randomNs)

		global HORNERCOUNT
		HORNERCOUNT+=1

# Here we use merge sort algorithm to sort the records by rank
def sortRank(file1):
	#file1.sort(key = lambda x: int(x[FIELDS]))
	if len(file1)>1:
		global HORNERCOUNT

		# Here file is being split into two halves
		mid = len(file1)//2
		lefthalf = file1[:mid]
		righthalf = file1[mid:]

		mergeSort(lefthalf)  # sort the first half
		mergeSort(righthalf) # sort the other half

		i=0
		j=0
		k=0

		while i < len(lefthalf) and j < len(righthalf):
			# the rank is stored in the (m+1)th position of the record
			if lefthalf[i][FIELDS] < righthalf[j][FIELDS]:
				file1[k]=lefthalf[i]
				i=i+1
			else:
				file1[k]=righthalf[j]
				j=j+1
			k=k+1
			HORNERCOUNT+=1

		# was any element left?
		while i < len(lefthalf):
			file1[k]=lefthalf[i]
			i=i+1
			k=k+1
			HORNERCOUNT+=1

		while j < len(righthalf):
			file1[k]=righthalf[j]
			j=j+1
			k=k+1
			HORNERCOUNT+=1

#
# (c) use the Radix sorting mentioned in Section-4.
#
#

# radix sort implemented but ordering records in grey ordering
def radix(L):
	global RADIXCOUNT

	for j in range(FIELDS-1,-1,-1):

		lists = []
		RADIXCOUNT+=1

		# forming empty lists L1,....,LNj
		for k in range(randomNs[j]):
			lists.append([])
			RADIXCOUNT+=1
		# for each record X from list L
		for X in L:
			xj = X[j]

			# here what was suggested in the paper
			# repalce 'append' with these four lines of code
			#
			# if xj is even
			if xj%2==0:
				lists[xj].append(X)
			else:
				lists[xj].insert(0,X)

			RADIXCOUNT+=1
		# form a new L by concatenating L1,....,LNj
		L = []
		for i in range(randomNs[j]):
			L = L+lists[i]
			RADIXCOUNT+=1

	return L

	






###############################################################################
#
# Print everything
#
#

print(f'Ni\'s: {randomNs}\n')
print(f'Original File\n-----------------------------')
#print_file(RECORDS,FIELDS,file)
print(f'Full Score: {fullscore(file)}')
print(f'Binary Score: {binaryscore(file)}\n\n')

greyfile = file[:]
mergeSort(greyfile)
print(f'greyOrder Sorted File\n-----------------------------')
#print_file(RECORDS,FIELDS,greyfile)
print(f'Number of loops: {GREYCOUNT}')
print(f'Full Score: {fullscore(greyfile)}')
print(f'Binary Score: {binaryscore(greyfile)}\n\n')

hornerfile = file[:]
giveRank(hornerfile)
sortRank(hornerfile)
print(f'Horner’s Ranking Sorted File\n-----------------------------')
#print_file(RECORDS,FIELDS,hornerfile)
print(f'Number of loops: {HORNERCOUNT}')
print(f'Full Score: {fullscore(hornerfile)}')
print(f'Binary Score: {binaryscore(hornerfile)}\n\n')

radixfile = file[:]
radixfile = radix(radixfile)
print(f'Radix Sorted File\n-----------------------------')
#print_file(RECORDS,FIELDS,radixfile)
print(f'Number of loops: {RADIXCOUNT}')
print(f'Full Score: {fullscore(radixfile)}')
print(f'Binary Score: {binaryscore(radixfile)}\n\n')






