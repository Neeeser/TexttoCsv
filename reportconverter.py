## Converts Trade Report into CSV file
## Andrew Neeser 6/14/23

import sys
import os
import csv
import pandas

# Checks if there are enough args
if len(sys.argv) < 3:
    print(
        "Usage ./reportconverter input.txt nameofoupt.csv \n   options:\n     -o, --Overwrite      Automatically overwrites outputfile\n     -x, --Xcel      Converts to excel format"
    )
    sys.exit(1)


# Checks if input file exists
if not os.path.isfile(sys.argv[1]):
    print("Input file does not exist or is not a valid file")
    sys.exit(1)

input_file = open(sys.argv[1], "r", newline="")

output_file = ""

## Checks if file exists if it does it will overwrite with the flag or on user input else it will just make a file with that name
if os.path.isfile(sys.argv[2]):
    if "-o" in sys.argv or "--Overwrite" in sys.argv:
        output_file = open(sys.argv[2], "w+", newline="")
    else:
        user = input("Output file already exists are would you like to overwrite? y/n")
        if user == "y":
            output_file = open(sys.argv[2], "w+", newline="")
        else:
            print("Will not overwrite file program exiting")
            sys.exit(1)
else:
    output_file = open(sys.argv[2], "w+", newline="")


## Start reading in data from text file

fields = [
    [
        "Port",
        "CUSIP",
        "Amount",
        "TicketType",
        "TradeDT",
        "SettleDt",
        "Price",
        "Dealer",
        "TicketNo",
    ]
]

number_breaks = 0
# Reads lines up until the trades
for line in input_file:
    if "-------------------" in line:
        number_breaks += 1
        if number_breaks == 2:
            break
        continue

# Reads the headers and fields
for line in input_file:
    if "-------------------" in line:
        break
    fields.append(line.split())

input_file.close()

# Add Blank rows 4 6 10
for row in fields:
    row.insert(3, " ")
    row.insert(5, "  ")
    row.insert(9, "   ")


# Write fields to csv file
with output_file as csvfile:
    # Creates csv
    csvwriter = csv.writer(csvfile)

    # Writes the fields
    csvwriter.writerows(fields)

print("Wrote to -> ", os.path.abspath(sys.argv[2]))

output_file.close

if "-x" in sys.argv or "--Xcel" in sys.argv:
    name_no_extension = sys.argv[2].split(".")

    csv = pandas.read_csv(
        sys.argv[2],
        delimiter=",",
    )

    csv.to_excel(name_no_extension[0] + ".xlsx", index=False)
