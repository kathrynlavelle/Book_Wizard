-- Select your database

-- Table structure for table `publishers`
DROP TABLE IF EXISTS `publishers`;

CREATE TABLE `publishers` (
  `publisher_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  `address` VARCHAR(255) DEFAULT NULL,
  `website` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`publisher_id`)
);

-- Dumping data for table `publishers`
INSERT INTO `publishers` VALUES
(1,'Penguin Random House','New York, USA','https://www.penguinrandomhouse.com'),
(2,'HarperCollins','New York, USA','https://www.harpercollins.com'),
(3,'Hachette Livre','Paris, France','https://www.hachette.com');

-- Table structure for table `books`
DROP TABLE IF EXISTS `books`;

CREATE TABLE `books` (
  `book_id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `isbn` VARCHAR(20) NOT NULL,
  `published_year` INT DEFAULT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `publisher_id` INT DEFAULT NULL,
  PRIMARY KEY (`book_id`),
  KEY `publisher_id` (`publisher_id`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`publisher_id`) REFERENCES `publishers` (`publisher_id`) ON DELETE SET NULL
);

-- Dumping data for table `books`
INSERT INTO `books` VALUES
(1,'Harry Potter and the Sorcerer\'s Stone','978-0747532743',1997,19.99,1),
(2,'1984','978-0451524935',1949,9.99,2),
(3,'The Lord of the Rings','978-0261102385',1954,25.99,1);

-- Table structure for table `genres`
DROP TABLE IF EXISTS `genres`;

CREATE TABLE `genres` (
  `genre_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`genre_id`)
);

-- Dumping data for table `genres`
INSERT INTO `genres` VALUES
(1,'Fantasy'),
(2,'Science Fiction'),
(3,'Dystopian'),
(4,'Adventure');

-- Table structure for table `authors`
DROP TABLE IF EXISTS `authors`;

CREATE TABLE `authors` (
  `author_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `bio` TEXT,
  PRIMARY KEY (`author_id`)
);

-- Dumping data for table `authors`
INSERT INTO `authors` VALUES
(1,'J.K.','Rowling','Author of the Harry Potter series'),
(2,'George','Orwell','Author of 1984 and Animal Farm'),
(3,'J.R.R.','Tolkien','Author of The Lord of the Rings');

-- Table structure for table `book_author`
DROP TABLE IF EXISTS `book_author`;

CREATE TABLE `book_author` (
  `book_id` INT NOT NULL,
  `author_id` INT NOT NULL,
  PRIMARY KEY (`book_id`, `author_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `book_author_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE,
  CONSTRAINT `book_author_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `authors` (`author_id`) ON DELETE CASCADE
);

-- Dumping data for table `book_author`
INSERT INTO `book_author` VALUES
(1,1),
(2,2),
(3,3);

-- Table structure for table `book_genre`
DROP TABLE IF EXISTS `book_genre`;

CREATE TABLE `book_genre` (
  `book_id` INT NOT NULL,
  `genre_id` INT NOT NULL,
  PRIMARY KEY (`book_id`, `genre_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `book_genre_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE,
  CONSTRAINT `book_genre_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`genre_id`) ON DELETE CASCADE
);

-- Dumping data for table `book_genre`
INSERT INTO `book_genre` VALUES
(1,1),
(3,1),
(2,3);


-- Table structure for table `inventory`
DROP TABLE IF EXISTS `inventory`;

CREATE TABLE `inventory` (
  `inventory_id` INT NOT NULL AUTO_INCREMENT,
  `book_id` INT NOT NULL,
  `quantity` INT DEFAULT '0',
  `location` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`inventory_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE
);

-- Dumping data for table `inventory`
INSERT INTO `inventory` VALUES
(1,1,100,'Warehouse A'),
(2,2,50,'Warehouse B'),
(3,3,75,'Warehouse C');
