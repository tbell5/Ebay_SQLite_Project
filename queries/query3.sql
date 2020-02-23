WITH ids AS (SELECT ItemID
		FROM Category
		GROUP BY ItemID
		HAVING COUNT(Name) = 4)
SELECT COUNT(ItemID)
FROM ids;