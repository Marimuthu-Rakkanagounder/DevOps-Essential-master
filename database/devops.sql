CREATE TABLE register (
    user_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username text NOT NULL,
    email varchar(50) UNIQUE NOT NULL,
    password text NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
