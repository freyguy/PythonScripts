import json
import os
import subprocess

### Takes list of strings to iterate over ###

domains = [""]

### Variable outputText holds path to final output ###

outputTextPath = "/PATH TO FINAL OUTPUT FILE/"

### Below clears the final output file ###

open(outputTextPath, "w").close()

### Loop that runs over domains in list and runs through DNSTwist,
### outputting the final text file and removing the .json file DNSTwist produces

for domain in domains:
	outputJsonFile = "/PATH TO OUTPUT DNSTWIST JSON FILE/dnstwist_" + str(domain) + ".json"
	subprocess.run(["dnstwist", "-f", "json", "-o", outputJsonFile, "-r", domain])
	f = open(outputJsonFile,"r")
	with open(outputTextPath, "a") as dnsedl:
		for line in f.readlines():
			if "domain-name" in line:
				x=(len(line) - 3)
				newLine = ((line[24:x]))
				if newLine == domain:
					pass
				else:
					dnsedl.write(newLine + "\n")
			else:
				pass
	subprocess.run(["rm", "-f", outputJsonFile])
