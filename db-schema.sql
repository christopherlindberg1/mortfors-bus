CREATE DATABASE morfors;


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
	country VARCHAR(30) NOT NULL,		-- country the city belongs to
	post_nr VARCHAR(10) NOT NULL,		-- ZIP code for bus stop
	street VARCHAR(30) NOT NULL,		-- street address for the bus stop
	PRIMARY KEY (city_name));


-- All trips that
CREATE TABLE trip
	(trip_id INT AUTO_INCREMENT,
	startdest VARCHAR(30) NOT NULL,	-- city of the start destination
	enddest VARCHAR(30) NOT NULL,		-- city of the end destination
	starttime DATETIME NOT NULL,  	-- date and time for when the trip begins
	arrival DATETIME NOT NULL,  		-- date and time for when the bus arrives
	price INT NOT NULL,  						-- price per person
	empty_seats INT NOT NULL,  			-- nr of available seats
	driver CHAR(11),								-- driver
	PRIMARY KEY (trip_id),
	FOREIGN KEY (startdest) references city(city_name),
	FOREIGN KEY (enddest) references city(city_name));


-- bookings
CREATE TABLE booking
	(email VARCHAR(50) NOT NULL,	-- customer's email
	trip_id INT NOT NULL,					-- id for trip
	nr_of_seats INT NOT NULL,			-- nr of tickets the customer has bought
	PRIMARY KEY (email, trip_id),
	FOREIGN KEY (email) references customer (email),
	FOREIGN KEY (trip_id) references trip (trip_id));
