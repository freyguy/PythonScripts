### IMPORT PANXAPI.PY ###

import subprocess
from xml.etree import ElementTree as ET

### INSERT PATH TO OBJECT LIST BELOW ###

document = open(PATH TO OBJECT LIST,"r")

########################################

panxapiPath = input("Provide path to panxapi.py: ")

objList = []

dictionaryRemoval = {}

valueList = []

counter = 0

errorList = []

for x in document:
	objList.append(x.rstrip('\n'))

### INSERT PANORAMA SPECIFIC INFORMATION ###

hostname = input("Provide Panorama IP address: ") 
config_xpath = input("Provide xpath for configuration: ")
api_key = SPECIFIC PANORAMA API KEY

### API KEY RETRIEVAL: https://docs.paloaltonetworks.com/pan-os/8-1/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/get-your-api-key#


# addObj = subprocess.Popen(['py.exe', PATH TO panxapi.py', 
# 	'-h', hostname, '-K', api_key, '-xr', '-S', '<ip-netmask>' + ip_addr + '</ip-netmask>', config_xpath + '/address/' 
# 	+ 'entry[@name=\'' + obj + "']"], stdout=subprocess.PIPE)

# print(output)

AddrGroup = subprocess.check_output(['python3.exe', panxapiPath,
	'-h', hostname, '-K', api_key, '-xr', '-s', config_xpath + '/address-group'], universal_newlines=True)

root = ET.fromstring(AddrGroup)


def removeObjectsInAddrGroup(AddressGroup, AddressObject):
	### Removes Objects from specified address groups
	subprocess.check_output(['py.exe', panxapiPath, 
	'-h', hostname, '-K', api_key, '-xr', '-d', config_xpath + '/address-group/entry[@name=\"' + AddressGroup + '\"]/static/member[text()=\"' + AddressObject + '\"]' ], universal_newlines=True)


def removeObjects(AddressObject):
	### Removes Objects from specified address groups
	try:
		subprocess.check_output(['py.exe', panxapiPath, 
		'-h', hostname, '-K', api_key, '-xr', '-d', config_xpath + '/address/entry[@name=\"' + AddressObject + '\"]' ], universal_newlines=True)
		print('\n')
	except subprocess.CalledProcessError:
		errorHandling(AddressObject)

def errorHandling(x):
	errorList.append(x)

def printErrors():
	if len(errorList) > 0:
		print('-'*30)
		print("Address objects not deleted due to error:")
		print('-'*30)
		for i in errorList:
			print('\t--> ' + i + '\n')
	else:
		print('-'*30)
		print("TASK COMPLETED SUCCESSFULLY")
		print('-'*30)
		

### Load list from file. If objects added to dictionary remove from list, else, leave on list to iterate through along with dictionary values ###


for entry in root.findall('entry'):       ### Successfully Prints Each Address Group Individually
	entryName = entry.get('name')
	dictionaryRemoval.setdefault(entryName, [])
	for members in root.findall(".//*[@name=\'" + entryName + "\']/*/member"):          ### Successfully Prints Each Address Object Individually
		addrObj = members.text
		for addrObjToDelete in objList:
			if addrObj == addrObjToDelete:
				dictionaryRemoval[entryName].append(addrObj)
				# print(addrObj + " in address group " + entryName + " added to deletion list\r")

				#### RUN COMMAND HERE TO REMOVE FROM PALO ALTO | ITERATING HERE WILL HELP REPLACING VALUES IN DICTIONARY ### 

print('\r')
print('-' * 30)
print('Final list of deletion items: ')
print('-' * 30)

### Iterate over dictionary of items to delete and 

for k in dictionaryRemoval:
	for v in dictionaryRemoval[k]:
		if v is not None:
			print('Deleting object - ' + v + '- from address group -' + k)
			removeObjectsInAddrGroup(k, v)
		else:
			break
		
for k in dictionaryRemoval:
	for v in dictionaryRemoval[k]:
		if v is not None:
			print('Deleting object - ' + v)
			removeObjects(v)
		else:
			break


printErrors()






### ITERATE LIST ###

	### IS ADDRESS OBJECT IN ADDRESS GROUP ###

		### IF YES, DELETE FROM GROUP ###

		### IF NO, CONTINUE ###

	### REMOVE ADDRESS OBJECT ###


###	print('Address ' + %s + ' removed from configuration.' % address)