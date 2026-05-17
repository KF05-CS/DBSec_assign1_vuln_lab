CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

INSERT INTO users(username, password)
VALUES ('admin', 'supersecret'),
('aya','aya123'),
('maryam','maryam123');

-- Credit cards table (sensitive financial data)
CREATE TABLE credit_cards (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    card_number VARCHAR(20),
    expiry VARCHAR(5)
);

INSERT INTO credit_cards (user_id, card_number, expiry) VALUES 
    (2, '4111-1111-1111-1111', '12/26'),
    (3, '5555-5555-5555-4444', '06/26');

CREATE TABLE flags (
    id SERIAL PRIMARY KEY,
    flag TEXT
);

INSERT INTO flags(flag)
VALUES ('FLAG{postgres_time_based_blind_sqli}');