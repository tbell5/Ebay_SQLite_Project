# about
This project, originally completed for UW class CS564--Database Management Systems, is meant to demonstrate basic proficiency in building/querying SQL relations. In it, we formed an SQL database for Ebay auctions data, which was initially provided by a JSON file dump. We then wrote a series of SQLite queries to test and examine the data. 

Tools/techniques used in this Project:
- **JSON**; JSON file format and Python JSON library
- **Python**; for parsing the JSON data into .dat files
- **.dat**; file format used for bridge between JSON and SQL
- **Bulk loading**; used to transform .dat files to SQLite database
- **SQLite**; database management system used for storing/querying database
- **Bash**; scripting language used to easily build the database


# skeleton_parser.py
skeleton parser.py transforms the JSON files from ebay_data into four .dat 
files (one for each table in our SQL relational model). To run the program, 
invoke the included bash script by typing `sh runParser.sh`. Upon success, this
will initialize the .dat files (in the same directory as the parser) and 
populate them with Bulk Loading data. The .dat files are named after their 
corresponding SQL tables.
