CREATE DATABASE mortfors_buss;


-- information about customers
CREATE TABLE customer
	(email VARCHAR(50) NOT NULL,
	firstname VARCHAR(30) NOT NULL,
	lastname VARCHAR(30) NOT NULL,
	country VARCHAR(30) NOT NULL,
	city VARCHAR(30) NOT NULL,
	post_nr VARCHAR(10) NOT NULL,
	street VARCHAR(30) NOT NULL,
	tel_nr VARCHAR(15),
	password VARCHAR(100) NOT NULL,
	registration_timestamp TIMESTAMP DEFAULT date_trunc('second', now()),
	PRIMARY KEY (email));


-- information about bus drivers
CREATE TABLE driver
	(pers_nr CHAR(11) NOT NULL,
	firstname VARCHAR(30) NOT NULL,
	lastname VARCHAR(30) NOT NULL,
	country VARCHAR(30) NOT NULL,
	city VARCHAR(30) NOT NULL,
	post_nr VARCHAR(10) NOT NULL,
	street VARCHAR(30) NOT NULL,
	tel_nr VARCHAR(15) NOT NULL,
	PRIMARY KEY (pers_nr));


-- Information about the cities the company has trips to
CREATE TABLE city
	(city_name VARCHAR(30) NOT NULL,
	country VARCHAR(30) NOT NULL,			-- country the city belongs to
	zip VARCHAR(10) NOT NULL,			-- ZIP code for bus stop
	street VARCHAR(30) NOT NULL,			-- street address for the bus stop
	PRIMARY KEY (city_name));


-- All trips available for booking
CREATE TABLE trip
	(trip_id SERIAL,
	startdest VARCHAR(30) NOT NULL,		-- city of the start destination
	enddest VARCHAR(30) NOT NULL,			-- city of the end destination
	departure TIMESTAMP NOT NULL,  		-- date and time for when the trip begins
	arrival TIMESTAMP NOT NULL,  			-- date and time for when the bus arrives
	price INT NOT NULL,  							-- price per person
	empty_seats INT NOT NULL,  				-- nr of available seats
	driver CHAR(11),									-- driver
	CONSTRAINT empty_seats_lower_limit CHECK(empty_seats > -1),
	CONSTRAINT empty_seats_upper_limit CHECK(empty_seats < 61),
	PRIMARY KEY (trip_id),
	FOREIGN KEY (startdest) REFERENCES city(city_name),
	FOREIGN KEY (enddest) REFERENCES city(city_name));


-- bookings
CREATE TABLE booking
	(email VARCHAR(50) NOT NULL,		-- customer's email
	trip_id INT NOT NULL,						-- id for trip
	nr_of_seats INT NOT NULL,				-- nr of tickets the customer has bought
	booking_timestamp TIMESTAMP DEFAULT date_trunc('second', now()),
	last_edit_timestamp TIMESTAMP DEFAULT date_trunc('second', now()),
	PRIMARY KEY (email, trip_id),
	FOREIGN KEY (email) REFERENCES customer (email),
	FOREIGN KEY (trip_id) REFERENCES trip (trip_id));


-- table for admins
CREATE TABLE admin
	(email VARCHAR(50) NOT NULL,
	firstname VARCHAR(30) NOT NULL,
	lastname VARCHAR(30) NOT NULL,
	password VARCHAR(100) NOT NULL,
	registration_timestamp TIMESTAMP DEFAULT date_trunc('second', now()),
	PRIMARY KEY (email));


-- View for nr of bookings per person last 365 days
CREATE VIEW nr_bookings_per_person_past_year as
SELECT c.firstname, c.lastname, c.email, count(b.email) AS bookings
FROM customer as c
JOIN booking as b
ON c.email = b.email
WHERE booking_timestamp > CURRENT_TIMESTAMP - INTERVAL '365 days'
GROUP BY c.email
ORDER BY bookings DESC;
