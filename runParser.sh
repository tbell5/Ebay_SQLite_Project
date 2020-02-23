python skeleton_parser.py ./ebay_data/items-*.json
sort tempSale.dat     | sort | uniq > Sale.dat
sort tempUser.dat     | sort | uniq > User.dat
sort tempBid_On.dat   | sort | uniq > Bid_On.dat
sort tempCategory.dat | sort | uniq > Category.dat
rm tempSale.dat tempUser.dat tempBid_On.dat tempCategory.dat
sqlite3 AuctionBase < create.sql
sqlite3 AuctionBase < load.txt
