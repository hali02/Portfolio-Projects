--Inital look at our dataset
SELECT * 
FROM VideoGamesSales
LIMIT 10

--How many total rows are in this table?
SELECT 
	COUNT(game_title)
FROM VideoGamesSales

--Is there any missing data?
SELECT 
	COUNT(*) AS MissingValues
FROM VideoGamesSales
WHERE 
	game_title is NULL
    or platform is NULL
    or review is NULL
    or global is NULL
    or genre is NULL
    or publisher is NULL

--How many unique games are in the dataset?
SELECT
	COUNT (DISTINCT(game_title))
FROM VideoGamesSales

--How many unique platforms are in the dataset?
SELECT
	COUNT(DISTINCT(platform))
FROM VideoGamesSales

--How many unique publishers are there?
SELECT
	COUNT(DISTINCT(publisher))
FROM VideoGamesSales

--How many games has each publisher released?
SELECT
	publisher,
    COUNT(DISTINCT(game_title)) as num_games
FROM VideoGamesSales
GROUP BY publisher
ORDER BY num_games DESC

--What is the average units sold (in millions) for games in this dataset?
SELECT
	AVG(global)
FROM VideoGamesSales

--What is the game with the most units sold? Who published it? What was the platform? How many units were sold?
SELECT 
	game_title,
    publisher,
    platform,
    global
FROM VideoGamesSales
WHERE global = (SELECT MAX(global)
               FROM VideoGamesSales)

--What platform has sold the most games?
SELECT
	platform,
	SUM(global) as total_sold
FROM VideoGamesSales
GROUP BY platform
ORDER BY total_sold DESC

--What publisher has sold the most games?
SELECT
	publisher,
	SUM(global) as total_sold
FROM VideoGamesSales
GROUP BY publisher
ORDER BY total_sold DESC

--What is the average units sold per genre?
SELECT
	genre,
	AVG(global)
FROM VideoGamesSales
GROUP BY genre

--What genre has sold the most games?
SELECT
	genre,
	SUM(global) as total_sold
FROM VideoGamesSales
GROUP BY genre
ORDER BY total_sold DESC

--Do newer games sell more or do older games sell more?
SELECT
	year, 
	SUM(global) as total_sold
FROM VideoGamesSales
GROUP BY year
ORDER BY total_sold DESC

--How many units of the top twenty games were sold compared to the average units sold of that game's genre, publisher, and platform?
SELECT
	game_title,
    global,
    platform,
	publisher,
	genre,
    AVG(global) OVER (PARTITION BY platform) as avg_platform,
    AVG(global) OVER (PARTITION BY publisher) as avg_publisher,
    AVG(global) OVER (PARTITION BY genre) as avg_genre
FROM VideoGamesSales
ORDER BY global DESC
LIMIT 20

--Do games with higher reviews have on average higher sales?
SELECT 
	MIN(review) as min,
    MAX(review) as max
FROM VideoGamesSales

SELECT CASE
	WHEN review < 60 THEN 'Poor'
  WHEN review BETWEEN 60 AND 75 THEN 'Fair'
  WHEN review BETWEEN 75 and 85 THEN 'Good'
  WHEN review BETWEEN 85 AND 90 THEN 'Very Good'
  WHEN review BETWEEN 90 AND 100 THEN 'Excellent'
  ELSE 'unreviewed'
    END AS review_bucket,
  AVG(global) as avg_sold
FROM VideoGamesSales
GROUP BY review_bucket
ORDER BY avg_sold

--Does the price of the game effect how many units are sold?
SELECT CASE
	WHEN cost < 60 THEN 'Cheap'
  WHEN review BETWEEN 60 AND 100 THEN 'Moderate'
  WHEN review BETWEEN 100 AND 150 THEN 'Expensive'
  ELSE 'Very Expensive'
    END AS price_bucket,
  AVG(global) as avg_sold
FROM 
	VideoGamesSales as sales
LEFT JOIN 
	VideoGamesPrice as price
ON
	sales.game_title = price.game_title
GROUP BY price_bucket
ORDER BY avg_sold
