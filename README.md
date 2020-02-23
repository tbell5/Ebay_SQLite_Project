
# skeleton_parser.py
skeleton parser.py transforms the JSON files from ebay_data into four .dat 
files (one for each table in our SQL relational model). To run the program, 
invoke the included bash script by typing <sh runParser.sh>. Upon success, this
will initialize the .dat files (in the same directory as the parser) and 
populate them with Bulk Loading data. The .dat files are named after their 
corresponding SQL tables.

Currently, the program only parses data for the Sales.dat file, though it still
initializes the files for Bid_On, Users, and Category. Also note that the bash
file is currently set to only feed the parser the first JSON file of Ebay data.
