SELECT COUNT(DISTINCT SellerID)
FROM Sale INNER JOIN User ON SellerID = UserID
WHERE Rating > 1000;