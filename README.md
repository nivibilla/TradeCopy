# TradeCopy
Processes NSE EOD data to MetaStock ASCII (7 column) format, using bhavcopy.csv from NSE severs

Creates directories C:/TradeCopy/Data/RAW/NSE-EOD and C:/TradeCopy/Data/PROCESSED/NSE-EOD

## Requirements
Python 3.8
#### And the following modules:
tqdm, requests, pandas

## Usage
Just run the program tradecopy.py and follow the instructions.
Data will be stored in the processed folder, do not delete the raw data, it is needed for the program to realise what dates have already been written.
Do not stop the program in the middle, if you do delete the whole "TradeCopy" folder and start again.

## Contact
IF you encounter any issues, raise them on the github page, or email me at nivibilla@gmail.com