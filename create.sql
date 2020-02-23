drop table if exists Sale;
drop table if exists User;
drop table if exists Category;
drop table if exists Bid_On;

CREATE TABLE Sale (
    ItemID INTEGER,
    SellerID TEXT,
    Name TEXT,
    Description TEXT,
    First_Bid REAL,
    Currently REAL,
    Number_of_Bids INTEGER,
    Started DATE,
    Ends DATE,
    Buy_Price REAL,
    PRIMARY KEY(ItemID)
    FOREIGN KEY (SellerID) REFERENCES User(UserID)
);

CREATE TABLE User (
    UserID TEXT,
    Rating INTEGER,
    Country TEXT,
    Location TEXT,
    PRIMARY KEY(UserId)
);

CREATE TABLE Category (
    ItemID INTEGER,
    Name TEXT,
    PRIMARY KEY(Name, ItemID),
    FOREIGN KEY (ItemID) REFERENCES Sale(ItemID)
);

CREATE TABLE Bid_On (
    ItemID INTEGER,
    UserID TEXT,
    Time DATE,
    Amount REAL,
    PRIMARY KEY(UserID, ItemID, Amount, Time),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
    FOREIGN KEY (ItemID) REFERENCES Sale(ItemID)
);
