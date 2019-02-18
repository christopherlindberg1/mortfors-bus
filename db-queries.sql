-- De tre första SQL-frågorna har körts från kommandotolken för att
-- applikationen ska ha något innehåll


INSERT INTO driver
VALUES 	('671215-6525', 'Jonas', 'Davidsson', 'Sverige', 'Malmö', '223 86', 'Gröna stigen 13', '040-336512'),
		('690409-7959', 'David', 'Eliasson', 'Sverige', 'Lund', '253 1', 'Blåa stigen 3', '048-795921'),
		('760205-1279', 'Christopher', 'Lindberg', 'Sverige', 'Malmö', '243 96', 'Gula gatan 7', '042-369512'),
		('711118-7692', 'Robert', 'Bergqvist', 'Sverige', 'Lund', '253 76', 'Grusvägen 14', '040-851222'),
		('900915-6390', 'Jesper', 'Jönsson', 'Sverige', 'Helsingborg', '253 86', 'Hbgvägen 13', '065-683112'),
		('660615-6526', 'Gunnel', 'Samuelsson', 'Sverige', 'Göteborg', '353 1', 'Isbanan 67', '076-239043'),
		('590215-1395', 'Bosse', 'Kvist', 'Sverige', 'Stockholm', '143 96', 'Blåhakevägen 4', '044-590939'),
		('880808-5494', 'Robert', 'Ohlsson', 'Sverige', 'Uppsala', '653 76', 'Uppväggen 66', '078-594383'),
		('851609-5490', 'Fabian', 'Svensson', 'Sverige', 'Gävle', '753 76', 'Bruna skogsvägen 16', '098-594654'),
		('761123-6992', 'Olle', 'Olofsson', 'Danmark', 'Köpenhamn', '853-776', 'Danskevaegen 5', '090-591211'),
		('910404-8943', 'Henrik', 'Gustavsson', 'Sverige', 'Kiruna', '953 76', 'Snöstigen 40', '060-523942');


INSERT INTO city (city_name, country, post_nr, street)
VALUES	('Malmö', 'Sverige', '212 54', 'Manetgatan 6'),
		('Helsingborg', 'Sverige', '259 45', 'Snäckgatan 50'),
		('Ystad', 'Sverige', '283 34', 'Astagatan 1'),
		('Göteborg', 'Sverige', '324 54', 'Ripgatan 9'),
		('Stockholm', 'Sverige', '111 11', 'Rungatan 22'),
		('Uppsala', 'Sverige', '580 95', 'Elinsgatan 75'),
		('Kiruna', 'Sverige', '879 95', 'Dorisgatan 14'),
		('Köpenhamn', 'Danmark', '124 542', 'Evagatan 8'),
		('Berlin', 'Tyskland', '124 864', 'Lövsångaregatan 67'),
		('Paris', 'Frankrike', '584 922', 'Fosievägen 54'),
		('Oslo', 'Norge', '549 49', 'Stjärngatan 12');


INSERT INTO trip (startdest, enddest, starttime, arrival, price, empty_seats, driver)
VALUES	('Malmö', 'Helsingborg', '2018-08-20 08:00:00', '2018-08-20 09:00:00', '99', 22, '671215-6525'),
		('Malmö', 'Ystad', '2018-08-20 08:00:00', '2018-08-20 09:00:00', '99', 22, '690409-7959'),
		('Stockholm', 'Uppsala', '2018-08-21 10:00:00', '2018-08-20 14:00:00', '199', 22, '711118-7692'),
		('Göteborg', 'Ystad', '2018-08-21 09:40:00', '2018-08-20 11:25:00', '99', 22, '900915-6390'),
		('Malmö', 'Paris', '2018-08-20 07:40:00', '2018-08-20 21:30:00', '399', 22, '660615-6526'),
		('Malmö', 'Oslo', '2018-08-20 08:40:00', '2018-08-21 12:00:00', '599', 22, '590215-1395'),
		('Uppsala', 'Köpenhamn', '2018-08-20 09:00:00', '2018-08-20 23:00:00', '399', 22, '880808-5494'),
		('Köpenhamn', 'Uppsala', '2018-08-21 08:00:00', '2018-08-20 22:00:00', '399', 22, '851609-5490'),
		('Göteborg', 'Stockholm', '2018-08-22 08:00:00', '2018-08-22 17:00:00', '299', 22, '761123-6992'),
		('Göteborg', 'Uppsala', '2018-08-22 08:00:00', '2018-08-20 17:00:00', '199', 22, '671215-6525'),
		('Stockholm', 'Paris', '2018-08-22 10:00:00', '2018-08-20 14:00:00', '599', 22, '910404-8943'),

		('Malmö', 'Helsingborg', '2018-08-23 08:00:00', '2018-08-23 09:00:00', '99', 22, '671215-6525'),
		('Malmö', 'Ystad', '2018-08-23 08:00:00', '2018-08-23 09:00:00', '99', 22, '690409-7959'),
		('Stockholm', 'Uppsala', '2018-08-23 10:00:00', '2018-08-23 14:00:00', '199', 22, '711118-7692'),
		('Göteborg', 'Ystad', '2018-08-23 09:40:00', '2018-08-23 11:25:00', '99', 22, '900915-6390'),
		('Malmö', 'Paris', '2018-08-23 07:40:00', '2018-08-23 21:30:00', '399', 22, '660615-6526'),
		('Malmö', 'Oslo', '2018-08-23 08:40:00', '2018-08-23 12:00:00', '599', 22, '590215-1395'),
		('Uppsala', 'Köpenhamn', '2018-08-23 09:00:00', '2018-08-23 23:00:00', '399', 22, '880808-5494'),
		('Köpenhamn', 'Uppsala', '2018-08-23 08:00:00', '2018-08-23 22:00:00', '399', 22, '851609-5490'),
		('Göteborg', 'Stockholm', '2018-08-23 08:00:00', '2018-08-23 17:00:00', '299', 22, '761123-6992'),
		('Göteborg', 'Uppsala', '2018-08-23 08:00:00', '2018-08-23 17:00:00', '199', 22, '671215-6525'),
		('Stockholm', 'Paris', '2018-08-23 10:00:00', '2018-08-23 14:00:00', '599', 22, '910404-8943'),

		('Malmö', 'Helsingborg', '2018-08-26 08:00:00', '2018-08-26 09:00:00', '99', 22, '671215-6525'),
		('Malmö', 'Ystad', '2018-08-26 08:00:00', '2018-08-26 09:00:00', '99', 22, '690409-7959'),
		('Stockholm', 'Uppsala', '2018-08-26 10:00:00', '2018-08-26 14:00:00', '199', 22, '711118-7692'),
		('Göteborg', 'Ystad', '2018-08-26 09:40:00', '2018-08-26 11:25:00', '99', 22, '900915-6390'),
		('Malmö', 'Paris', '2018-08-26 07:40:00', '2018-08-26 21:30:00', '399', 22, '660615-6526'),
		('Malmö', 'Oslo', '2018-08-26 08:40:00', '2018-08-26 12:00:00', '599', 22, '590215-1395'),
		('Uppsala', 'Köpenhamn', '2018-08-26 09:00:00', '2018-08-26 23:00:00', '399', 22, '880808-5494'),
		('Köpenhamn', 'Uppsala', '2018-08-26 08:00:00', '2018-08-26 22:00:00', '399', 22, '851609-5490'),
		('Göteborg', 'Stockholm', '2018-08-26 08:00:00', '2018-08-26 17:00:00', '299', 22, '761123-6992'),
		('Göteborg', 'Uppsala', '2018-08-26 08:00:00', '2018-08-26 17:00:00', '199', 22, '671215-6525'),
		('Stockholm', 'Paris', '2018-08-26 10:00:00', '2018-08-26 14:00:00', '599', 22, '910404-8943');


-- SQL-frågorna nedan körs via servern när användaren interagerar
-- med applikationen


-- Registrerar en ny användare
INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s),
(email, firstname, lastname, country, city, post_nr, street, tel_nr, password)


-- Hämtar all info om kunden med den email som angavs vid inloggning.
-- Används för att matcha lösenordet som skrivs in med det registrerade
-- lösenordet i databasen
"SELECT * FROM customer WHERE email = %s",
[email];


-- Hämtar info om alla tillgängliga turer
"SELECT * FROM trip ORDER BY startdest, enddest, starttime"


-- Updaterar antalet lediga platser för en tur när en bokning görs
"UPDATE trip SET empty_seats = %s WHERE trip_id = %s",
[seats_left, trip_id]


-- Registrerar en bokning tillhörande den inloggade personen
"INSERT INTO booking VALUES (%s, %s, %s)", [session["email"],
trip_id, nr_of_seats]


-- Hämtar turer som den inloggade personen har bokat
"SELECT t.trip_id, t.startdest, t.enddest, t.starttime, t.arrival, b.nr_of_seats
FROM trip as t
INNER JOIN booking as b
ON b.email = %s AND t.trip_id=b.trip_id
ORDER BY starttime",
[session["email"]]


-- Hämtar information om en tur som en kund har bokat
"""SELECT b.email, b.trip_id, b.nr_of_seats, t.trip_id, t.startdest,
t.enddest, t.starttime, t.arrival, t.price, t.empty_seats
FROM booking as b
JOIN trip as t
ON b.trip_id = %s b.trip_id = t.trip_id AND b.email = %s""",
[trip_id, session["email"]]


-- Updaterar antalet biljetter en kund har till en viss tur
"""UPDATE booking SET nr_of_seats = %s WHERE email = %s AND trip_id = %s""",
[nr_of_seats, session["email"], trip_id]


-- Tar bort en kunds bokning
"DELETE FROM booking WHERE trip_id = %s AND email = %s",
	[trip_id, session["email"]]
