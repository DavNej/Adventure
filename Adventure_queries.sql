SELECT *
FROM users
WHERE user_name = 'test' AND adventure_id = 1;

SELECT *
FROM questions
WHERE adventure_id = 1 AND stage = 1;

SELECT * FROM options WHERE question_id = 1;

-- UPDATE users
-- SET
-- 	stage = 2,
-- 	life = life - 10,
--     coins = coins - 5
-- WHERE user_name = 'dav' AND adventure_id = 1;

SELECT coin_loss, life_loss FROM options WHERE choice = 1 AND question_id = (
	SELECT id
    FROM questions
    WHERE adventure_id = 1 AND stage = 1
);
-- ----------------------------------------------------------------------------------------
DESC users;

SELECT * FROM users;
SELECT * FROM adventures;
SELECT * FROM questions;
SELECT * FROM options;

SELECT *
FROM options
ORDER BY question_id
LIMIT 4;
-- ----------------------------------------------------------------------------------------