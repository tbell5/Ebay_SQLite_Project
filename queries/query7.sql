WITH bidids AS (SELECT DISTINCT ItemID
		FROM Bid_On
		WHERE Amount > 100)
SELECT COUNT(DISTINCT Name)
FROM bidids, Category
WHERE bidids.ItemID = Category.ItemID;
