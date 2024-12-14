-- Starts MAriaDB 
-- cd "C:\Program Files\MariaDB 10.5\bin"
-- mysql -u root -p < path\to\setup_bible_verses.sql    --password is Cleopatra02@

CREATE DATABASE IF NOT EXISTS bible_verses;

USE Bible_verses;

CREATE TABLE verses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference VARCHAR(50) NOT NULL,
    text TEXT NOT NULL,
    translation VARCHAR(50) DEFAULT 'NIV'
);

CREATE TABLE emotions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE verse_emotions (
    verse_id INT,
    emotion_id INT,
    PRIMARY KEY (verse_id, emotion_id),
    FOREIGN KEY (verse_id) REFERENCES verses(id) ON DELETE CASCADE,
    FOREIGN KEY (emotion_id) REFERENCES emotions(id) ON DELETE CASCADE
);

--Insert Emotion
INSERT INTO emotions (name) VALUES ('anger'), ('anxiety'), ('forgiveness'), 
('hope'), ('sadness'), ('envy'), ('hopelessness'), ('lust'), ('depression'), ('happiness'), ('love'), 
('joy');

--Insert a Verse
INSERT INTO verses (reference, text) 
VALUES ('John 3:16', 'For God so loved the world...');

-- Link Verse to emotion
INSERT INTO verse_emotions (verse_id, emotion_id) VALUES (1, 4);  -- Assuming 'hope' has id 4
