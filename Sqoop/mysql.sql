CREATE USER 'sqoop'@'%' IDENTIFIED BY 'sqoop';

-- Create new database sqoop
CREATE DATABASE sqoop;

-- Grant all privileges to the new database to created user
GRANT ALL ON sqoop.* to 'sqoop'@'%';

-- in case MySQL runs on local machine
CREATE USER 'sqoop'@'localhost' IDENTIFIED BY 'sqoop';
GRANT ALL ON sqoop.* TO 'sqoop'@'localhost';
