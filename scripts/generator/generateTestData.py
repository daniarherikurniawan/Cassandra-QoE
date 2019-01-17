import uuid
import names
from random import randint
from faker import Faker
import csv

fake = Faker()

# with open('dataset/users-1.csv', newline='') as myFile:  
# 	reader = csv.reader(myFile, delimiter='|', quoting=csv.QUOTE_NONE)
# 	for row in reader:
# 		print(row)

myFields = [['id','name','address','salary','phone']]
csv.register_dialect('myDialect', delimiter='|', quoting=csv.QUOTE_NONE)
for y in range(0,100):
	print('File-'+str(y))
	myFile = open('dataset/data-users-'+str(y)+'.csv', 'w')  
	writer = csv.writer(myFile, dialect='myDialect')
	writer.writerows(myFields)
	for x in range(1,700000):
		if(x%10000 == 0):
			print('.', end='', flush = True)
		dataset = [[uuid.uuid1(), fake.name(), fake.address().replace('\n',', '), randint(4000, 100000), randint(1000000, 9000000)]]
		writer.writerows(dataset)
	print('\n')

myFile.close()
