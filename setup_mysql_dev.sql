-- Create the database named hbnb_dev_db if it does not already exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create the MySQL user hbnb_dev with the specified password if the user does not already exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the hbnb_dev_db database to the hbnb_dev user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant select privileges on the performance_schema database to the hbnb_dev user
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';