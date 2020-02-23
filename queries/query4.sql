WITH maxes AS(SELECT MAX(Currently) AS maxed FROM Sale)

SELECT ItemID
FROM Sale, maxes
WHERE Currently = maxed;