SELECT name, language, percentage FROM languages LEFT JOIN countries ON countries.id = country_id WHERE language="Slovene" ORDER BY percentage DESC;
SELECT countries.name, count(*) as cities FROM cities LEFT JOIN countries ON cities.country_id=countries.id GROUP BY countries.name;
SELECT cities.name, cities.population FROM cities WHERE cities.country_id=136 AND cities.population > 500000 ORDER BY cities.population DESC;
SELECT countries.name, languages.language, languages.percentage FROM languages LEFT JOIN countries ON countries.id = languages.country_id WHERE percentage>89.0 GROUP BY countries.name ORDER BY percentage DESC;
SELECT name, surface_area, population FROM countries WHERE surface_area < 501 AND population > 100000;
SELECT name, government_form, capital, life_expectancy FROM countries WHERE capital > 200 AND government_form="Constitutional Monarchy" AND life_expectancy > 75;
SELECT countries.name, cities.name, cities.district, cities.population FROM cities LEFT JOIN countries ON countries.id = country_id WHERE country_id=9 AND district="Buenos Aires" AND cities.population > 500000;
SELECT name, COUNT(*) as countries FROM countries GROUP BY region ORDER by countries DESC;
