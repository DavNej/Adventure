DROP TABLE IF EXISTS users;
CREATE TABLE users(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	user_name CHAR(30) NOT NULL,
    adventure_id INT,
    stage INT,
    life INT,
    coins INT
);

INSERT INTO users(user_name, adventure_id, stage, life, coins)
VALUES
	('test', 1, 2, 80, 20)
;

DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS adventures;
CREATE TABLE adventures(
	id INT NOT NULL PRIMARY KEY,
    adventure_name VARCHAR(255)
);

INSERT INTO adventures()
VALUES 
	(1, 'Little Bunny'),
	(2, 'Little Cat')
;

CREATE TABLE questions(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    adventure_id INT,
    stage INT,
    text VARCHAR(255),
    image VARCHAR(255),
    FOREIGN KEY adventure_id(adventure_id)
    REFERENCES adventures(id)
    ON DELETE CASCADE
);

INSERT INTO questions(adventure_id, stage, text, image)
VALUES 
	(1, 1, 'You run into a bunny, what do you do?','bunny.jpg'),
    (1, 2, 'The bunny gave you an apple, what\'s your next move?','apple.jpg'),
    (1, 3, 'The bunny got offended and called his friend the giagantic gorilla, what do you do?','gorilla.jpg'),
    (1, 4, 'Oh an elephant!! What\'s your next move?','elephant.jpg'),
    
	(2, 1, 'You run into a cat, what do you do?','cat.jpg'),
    (2, 2, 'The cat gave you a pear, what\'s your next move?','pear.jpg'),
    (2, 3, 'The cat got offended and called his friend the giagantic snake, what do you do?','snake.jpg'),
    (2, 4, 'Oh a bear!! What\'s your next move?','bear.jpg')
;

CREATE TABLE options(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    question_id INT,
    option_text VARCHAR(255),
    life_loss INT,
    coin_loss INT,
    choice INT,
    FOREIGN KEY question_id(question_id)
    REFERENCES questions(id)
    ON DELETE CASCADE
);

INSERT INTO options(question_id, choice, option_text, life_loss, coin_loss)
VALUES
	(1, 1, 'Try to make it your meal', 20, 0),
    (1, 2, 'Give him 15 coins', 20, 15),
    (1, 3, 'Try to caress him', 0, 0),
    (1, 4, 'Ask for direction', 0, 10),
    
    (2, 1, 'Eat it!', 50, 0),
    (2, 2, 'Give him 10 coins in exchange', 0, 10),
    (2, 3, 'Ignore it', 10, 0),
    (2, 4, 'Ask for direction', 0, 10),
    
    (3, 1, 'Eat it!', 50, 0),
    (3, 2, 'Give him all off my coins', 0, 100),
    (3, 3, 'Ignore him', 100, 0),
    (3, 4, 'Give him a banana', 0, 10),
    
    (4, 1, 'Say hi!', 50, 0),
    (4, 2, 'Give him 15 coins', 20, 15),
    (4, 3, 'Ignore him', 100, 0),
    (4, 4, 'Give him peanuts', 0, 10),
    
    
	(5, 1, 'Try to make it your meal', 20, 0),
    (5, 2, 'Give him 10 coins', 20, 10),
    (5, 3, 'Try to put water on him', 0, 10),
    (5, 4, 'Ask for direction', 0, 10),
    
    (6, 1, 'Eat it!', 50, 0),
    (6, 2, 'Give him 15 coins in exchange', 0, 15),
    (6, 3, 'Ignore it', 10, 0),
    (6, 4, 'Ask for direction', 0, 0),
    
    (7, 1, 'Eat it!', 50, 0),
    (7, 2, 'Give him all off my coins', 0, 100),
    (7, 3, 'Ignore him', 100, 0),
    (7, 4, 'Give him a mouse', 0, 10),
    
    (8, 1, 'Say hi!', 50, 0),
    (8, 2, 'Give him 15 coins', 100, 15),
    (8, 3, 'Ignore him', 100, 0),
    (8, 4, 'Give him honey', 0, 10)    
;