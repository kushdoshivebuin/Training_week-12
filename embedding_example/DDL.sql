CREATE TABLE IF NOT EXISTS example (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(768)
)