CREATE DATABASE morfors;

CREATE TABLE customer  					-- information om kunderna
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


CREATE TABLE driver  					-- information om chaufförerna
	(pers_nr CHAR(11) NOT NULL,
	firstname VARCHAR(30) NOT NULL,
	lastname VARCHAR(30) NOT NULL,
	country VARCHAR(30) NOT NULL,
	city VARCHAR(30) NOT NULL,
	post_nr VARCHAR(10) NOT NULL,
	street VARCHAR(30) NOT NULL,
	tel_nr VARCHAR(15) NOT NULL,
	PRIMARY KEY (pers_nr));


CREATE TABLE city 						-- information om städerna/hållplatserna bolaget kör till
	(city_name VARCHAR(30) NOT NULL,
	country VARCHAR(30) NOT NULL,
	post_nr VARCHAR(10) NOT NULL,
	street VARCHAR(30) NOT NULL,
	PRIMARY KEY (city_name));			-- hållplatsens adress


CREATE TABLE trip	  					-- företagets alla planerade turer
	(trip_id INT AUTO_INCREMENT,
	startdest VARCHAR(30) NOT NULL,		-- startdestinationens stad
	enddest VARCHAR(30) NOT NULL,		-- ankomstdestinationens stad
	starttime DATETIME NOT NULL,  		-- tid och datum för avgång
	arrival DATETIME NOT NULL,  		-- tid och datum för ankomst
	price VARCHAR(10) NOT NULL,  		-- pris per person
	empty_seats INT NOT NULL,  			-- antal lediga platser
	driver CHAR(11),					-- chaufför för resan
	PRIMARY KEY (trip_id),
	FOREIGN KEY (startdest) references city(city_name),
	FOREIGN KEY (enddest) references city(city_name));


CREATE TABLE booking					-- kundernas bokade turer
	(email VARCHAR(50) NOT NULL,		-- kundens email
	trip_id INT NOT NULL,				-- id för turen som kunden bokat
	nr_of_seats INT NOT NULL,			-- antalet platser som kunden bokar
	PRIMARY KEY (email, trip_id),
	FOREIGN KEY (email) references customer (email),
	FOREIGN KEY (trip_id) references trip (trip_id));
