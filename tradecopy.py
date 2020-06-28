from tqdm import tqdm
import requests
import datetime
from pathlib import Path
from zipfile import ZipFile
import os
import pandas as pd

dateFVal = False
dateTVal = False
validDates = False
rejected = False
form = '%d/%m/%Y'
Path("C:/Tradecopy/Data/RAW/NSE-EOD/").mkdir(parents=True, exist_ok=True)
Path("C:/Tradecopy/Data/PROCESSED/NSE-EOD/").mkdir(parents=True, exist_ok=True)
Path("C:/Tradecopy/Data/PROCESSED/NSE-EOD-ASCII/").mkdir(parents=True, exist_ok=True)

while True:
	choice = input(
		"type 1 for tradecopy(create data), 2 for tradeASCII(Existing data), 3 for tradecopy(using existing data) or 'quit': ")

	if choice == "1":
		while not validDates:
			rejected = False
			while not dateFVal:
				dateFrom = input("Input the date from: ")
				try:
					dateF = datetime.datetime.strptime(dateFrom, form)
					dateFVal = True
				except ValueError:
					print("Date is in the incorrect format, use the format: dd/mm/yyyy")

			while not dateTVal:
				dateTo = input("Input the date to: ")
				try:
					dateT = datetime.datetime.strptime(dateTo, form)
					dateTVal = True
				except ValueError:
					print("Date is in the incorrect format, use the format: dd/mm/yyyy")

			if dateT >= dateF:
				validDates = True
			else:
				print("The dateTo value is before the dateFrom value, hence invalid dates")
				dateFVal = False
				dateTVal = False
				validDates = False
				rejected = True

			if dateF > datetime.datetime(2010, 1, 1) and validDates:
				validDates = True
			else:
				if not rejected:
					print("At least one of your date values are before 2010, pick more recent dates")
				dateFVal = False
				dateTVal = False
				validDates = False
				rejected = True

			if dateF < datetime.datetime.now() and dateT < datetime.datetime.now() and validDates:
				validDates = True
			else:
				if not rejected:
					print("At least one of your date values are after the current date, pick historical dates")
				dateFVal = False
				dateTVal = False
				validDates = False
				rejected = True

		print(dateF)
		print(dateT)
		numberofdays = (dateT - dateF).days + 1
		for single_date in (dateF + datetime.timedelta(n) for n in range(numberofdays)):
			date = single_date.strftime("%d-%b-%Y").upper()
			date_array = date.split("-")
			day = date_array[0]
			month = date_array[1]
			year = date_array[2]
			url = "https://archives.nseindia.com/content/historical/EQUITIES/" + year + "/" + month + "/cm" + day + month + year + "bhav.csv.zip"
			print(url)
			filepath = "C:/Tradecopy/Data/RAW/NSE-EOD/" + year + "/cm" + day + month + year + "bhav.csv"
			if not os.path.exists(filepath):
				try:
					response = requests.get(url, stream=True, timeout=3)
					Path("C:/Tradecopy/Data/RAW/NSE-EOD/" + year).mkdir(parents=True, exist_ok=True)
					with open(filepath + ".zip", "wb") as handle:
						for data in tqdm(response.iter_content()):
							handle.write(data)
					with ZipFile(filepath + ".zip", 'r') as zip_ref:
						zip_ref.extractall("C:/Tradecopy/Data/RAW/NSE-EOD/" + year + "/")
					os.remove(filepath + ".zip")
					df = pd.read_csv(filepath)
					for i in range(0, len(df.index)):
						df.iat[i, 10] = single_date.strftime("%Y%m%d")
						if not os.path.exists(
								"C:/Tradecopy/Data/PROCESSED/NSE-EOD/NSE_" + single_date.strftime("%Y%m%d") + ".txt"):
							df.iloc[[i], [0, 10, 2, 3, 4, 5, 8]].to_csv(
								"C:/Tradecopy/Data/PROCESSED/NSE-EOD/NSE_" + single_date.strftime("%Y%m%d") + ".txt",
								header=False, index=False)
						else:
							df.iloc[[i], [0, 10, 2, 3, 4, 5, 8]].to_csv(
								"C:/Tradecopy/Data/PROCESSED/NSE-EOD/NSE_" + single_date.strftime("%Y%m%d") + ".txt",
								mode="a", header=False, index=False)
				except requests.exceptions.Timeout:
					print("Url does not exist skipping date: " + day + month + year)
					continue
			else:
				print("File already exists, date = " + day + month + year)

	elif choice == "2":
		paths = []
		for root, dirs, files in os.walk("C:/Tradecopy/Data/RAW/NSE-EOD/"):
			for file in files:
				if file.endswith(".csv"):
					paths.append(root + "/" + file)
		for filepath in paths:
			single_date = datetime.datetime.strptime(filepath[37:46], "%d%b%Y")
			print("Processing " + filepath)
			df = pd.read_csv(filepath)
			for i in range(0, len(df.index)):
				df.iat[i, 10] = single_date.strftime("%y%m%d")
				if not os.path.exists("C:/Tradecopy/Data/PROCESSED/NSE-EOD/" + df.iat[i, 0] + ".csv"):
					df.iloc[[i], [0, 10, 2, 3, 4, 5, 8]].to_csv(
						"C:/Tradecopy/Data/PROCESSED/NSE-EOD-ASCII/" + df.iat[i, 0] + ".txt", header=True, index=False)
				else:
					df.iloc[[i], [0, 10, 2, 3, 4, 5, 8]].to_csv(
						"C:/Tradecopy/Data/PROCESSED/NSE-EOD-ASCII/" + df.iat[i, 0] + ".txt", mode="a", header=False,
						index=False)

	elif choice == "3":
		paths = []
		for root, dirs, files in os.walk("C:/Tradecopy/Data/RAW/NSE-EOD/"):
			for file in files:
				if file.endswith(".csv"):
					paths.append(root + "/" + file)
		for filepath in paths:
			single_date = datetime.datetime.strptime(filepath[37:46], "%d%b%Y")
			if os.path.exists("C:/Tradecopy/Data/PROCESSED/NSE-EOD/NSE_" + single_date.strftime("%Y%m%d") + ".txt"):
				print("File already exists: " + "NSE_" + single_date.strftime("%Y%m%d") + ".txt")
			else:
				print("Processing " + filepath)
				df = pd.read_csv(filepath)
				for i in range(0, len(df.index)):
					df.iat[i, 10] = single_date.strftime("%Y%m%d")
					if not os.path.exists(
							"C:/Tradecopy/Data/PROCESSED/NSE-EOD/NSE_" + single_date.strftime("%Y%m%d") + ".txt"):
						df.iloc[[i], [0, 10, 2, 3, 4, 5, 8]].to_csv(
							"C:/Tradecopy/Data/PROCESSED/NSE-EOD/NSE_" + single_date.strftime("%Y%m%d") + ".txt",
							header=False, index=False)
					else:
						df.iloc[[i], [0, 10, 2, 3, 4, 5, 8]].to_csv(
							"C:/Tradecopy/Data/PROCESSED/NSE-EOD/NSE_" + single_date.strftime("%Y%m%d") + ".txt",
							mode="a", header=False, index=False)

	elif choice.upper() == "QUIT":
		break

	else:
		print("Undefined Choice, retry.")
