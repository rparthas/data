CREATE TABLE `cities` (
  `id` INTEGER UNSIGNED NOT NULL,
  `country` VARCHAR(50),
  `city` VARCHAR(150),
  PRIMARY KEY (`id`)
);

-- Insert 3 example lines into table cities
INSERT INTO `cities`(`id`, `country`, `city`) VALUES (1, "USA", "Palo Alto");
INSERT INTO `cities`(`id`, `country`, `city`) VALUES (2, "Czech Republic", "Brno");
INSERT INTO `cities`(`id`, `country`, `city`) VALUES (3, "USA", "Sunnyvale");

-- Create staging table for export
CREATE TABLE `staging_cities` LIKE `cities`;

-- Create table countries
CREATE TABLE `countries` (
  `country_id` INTEGER UNSIGNED NOT NULL,
  `country` VARCHAR(50),
  PRIMARY KEY (`country_id`)
);

-- Insert 2 example lines into table countries
INSERT INTO `countries`(`country_id`, `country`) VALUES (1, "USA");
INSERT INTO `countries`(`country_id`, `country`) VALUES (2, "Czech Republic");

-- Create normalized variant of table cities
CREATE TABLE `normcities` (
  `id` INTEGER UNSIGNED NOT NULL,
  `country_id` INTEGER UNSIGNED NOT NULL,
  `city` VARCHAR(150),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`country_id`) REFERENCES `countries`(`country_id`)
);

-- Insert 3 example lines into table normcities
INSERT INTO `normcities`(`id`, `country_id`, `city`) VALUES (1, 1, "Palo Alto");
INSERT INTO `normcities`(`id`, `country_id`, `city`) VALUES (2, 2, "Brno");
INSERT INTO `normcities`(`id`, `country_id`, `city`) VALUES (3, 1, "Sunnyvale");

-- Create visits table that is suitable for incremental import
CREATE TABLE `visits` (
  `id` INTEGER UNSIGNED NOT NULL,
  `city` VARCHAR(50),
  `last_update_date` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`last_update_date`)
);

-- Insert couple of records to table visits
INSERT INTO `visits`(`id`, `city`, `last_update_date`) VALUES(1, "Freemont", "1983-05-22 01:01:01");
INSERT INTO `visits`(`id`, `city`, `last_update_date`) VALUES(2, "Jicin", "1987-02-02 02:02:02");
