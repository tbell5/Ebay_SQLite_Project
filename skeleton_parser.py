
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"
isFirstFile = True

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Replace " with ""
"""
def transformStr(val):
    return '"' + sub(r'"', '""', val) + '"'

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    global isFirstFile
    if(isFirstFile):
        fSale = open("./tempSale.dat", "w+")
        fUsers = open("./tempUser.dat", "w+")
        fCategory = open("./tempCategory.dat", "w+")
        fBid_On = open("./tempBid_On.dat", "w+")
        isFirstFile = False
    else:
        fSale = open("./tempSale.dat", "a")
        fUsers = open("./tempUser.dat", "a")
        fCategory = open("./tempCategory.dat", "a")
        fBid_On = open("./tempBid_On.dat", "a")
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            parseSaleTuple(fSale, fUsers, item)
            parseBidOnTuple(fBid_On, fUsers, item)
            parseCategoryTuple(fCategory, item)

    fSale.close()
    fUsers.close()
    fCategory.close()
    fBid_On.close()
"""
Print values to f in order specified by the attributes of the Sales table.
Returns without printing if any of the required attributes are missing.
If Buy_Price attribute is missing, prints NULL to f for that attribute.
"""
def parseSaleTuple(fSale, fUsers, atrbs):

    # transform attributes [strings, dates, dollars]
    atrbs["Name"] = transformStr(atrbs["Name"])
    atrbs["Seller"]["UserID"] = transformStr(atrbs["Seller"]["UserID"])
    atrbs["Location"] = transformStr(atrbs["Location"])
    atrbs["Country"] = transformStr(atrbs["Country"])
    if("Description" in atrbs and not atrbs["Description"] is None):
        atrbs["Description"] = transformStr(atrbs["Description"])
    else:
        atrbs["Description"] = "NULL"
    atrbs["First_Bid"] = transformDollar(atrbs["First_Bid"])
    atrbs["Currently"] = transformDollar(atrbs["Currently"])
    atrbs["Started"] = transformDttm(atrbs["Started"])
    atrbs["Ends"] = transformDttm(atrbs["Ends"])
    if("Buy_Price" in atrbs and not atrbs["Buy_Price"] is None):
        atrbs["Buy_Price"] = transformDollar(atrbs["Buy_Price"])
    else:
        atrbs["Buy_Price"] = "NULL"

    # record sale tuple
    fSale.write(atrbs["ItemID"] + columnSeparator
      + atrbs["Seller"]["UserID"] + columnSeparator
      + atrbs["Name"] + columnSeparator
      + atrbs["Description"] + columnSeparator
      + atrbs["First_Bid"] + columnSeparator
      + atrbs["Currently"] + columnSeparator
      + atrbs["Number_of_Bids"] + columnSeparator
      + atrbs["Started"]+ columnSeparator
      + atrbs["Ends"] + columnSeparator
      + atrbs["Buy_Price"] + "\n")

    # record userTuple
    fUsers.write(atrbs["Seller"]["UserID"] + columnSeparator
      + atrbs["Seller"]["Rating"] + columnSeparator
      + atrbs["Country"] + columnSeparator
      + atrbs["Location"] + '\n')

def parseBidOnTuple(fBid_On, fUsers, atrbs):

    # loop through bids [if any]
    if(atrbs["Bids"] is None):
        return
    for bid in atrbs["Bids"]:

        # transform attributes [strings, dates, dollars]
        bid["Bid"]["Time"] = transformDttm(bid["Bid"]["Time"])
        bid["Bid"]["Bidder"]["UserID"] = transformStr(bid["Bid"]["Bidder"]["UserID"])
        bid["Bid"]["Amount"] = transformDollar(bid["Bid"]["Amount"])
        if("Country" in bid["Bid"]["Bidder"] and not bid["Bid"]["Bidder"]["Country"] is None):
            bid["Bid"]["Bidder"]["Country"] = transformStr(bid["Bid"]["Bidder"]["Country"])
        else:
            bid["Bid"]["Bidder"]["Country"] = "NULL"
        if("Location" in bid["Bid"]["Bidder"] and not bid["Bid"]["Bidder"]["Location"] is None):
            bid["Bid"]["Bidder"]["Location"] = transformStr(bid["Bid"]["Bidder"]["Location"])
        else:
            bid["Bid"]["Bidder"]["Location"] = "NULL"

        # record bid tuple
        fBid_On.write(atrbs["ItemID"] + columnSeparator
          + bid["Bid"]["Bidder"]["UserID"] + columnSeparator
          + bid["Bid"]["Time"] + columnSeparator
          + bid["Bid"]["Amount"] + '\n')

        # record user tuple
        fUsers.write(bid["Bid"]["Bidder"]["UserID"] + columnSeparator
          + bid["Bid"]["Bidder"]["Rating"] + columnSeparator
          + bid["Bid"]["Bidder"]["Country"] + columnSeparator
          + bid["Bid"]["Bidder"]["Location"] + '\n')

def parseCategoryTuple(fCategory, atrbs):
    for category in atrbs["Category"]:
        fCategory.write(atrbs["ItemID"] + columnSeparator
        + transformStr(category) + '\n')

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print('Usage: python skeleton_json_parser.py <path to json files>')
        sys.exit(1)

    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
