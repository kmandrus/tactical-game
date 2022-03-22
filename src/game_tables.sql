DROP TABLE IF EXISTS board_tiles;
DROP TABLE IF EXISTS tile;
DROP TABLE IF EXISTS piece;

CREATE TABLE piece (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image_filepath VARCHAR(255) NOT NULL
);

CREATE TABLE tile (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    is_impassible BOOLEAN NOT NULL,
    is_filled BOOLEAN NOT NULL,
    red INTEGER NULL,
    green INTEGER NULL,
    blue INTEGER NULL
);

CREATE TABLE board_tiles (
    board_name VARCHAR(255) NOT NULL,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    tile_id INTEGER NOT NULL,
    piece_id INTEGER NULL,

    PRIMARY KEY (board_name, x, y),
    FOREIGN KEY (tile_id) REFERENCES tile(id),
    FOREIGN KEY (piece_id) REFERENCES piece(id)
);

INSERT INTO
    piece
    (name, image_filepath)
VALUES
    ('Makeda', 'token_1.png'),
    ('Teferi', 'token_2.png'),
    ('Sakoura', 'token_3.png'),
    ('Dihya', 'token_4.png')
;

INSERT INTO
    tile
    (name, is_impassible, is_filled, red, green, blue)
VALUES
    ('grass', FALSE, TRUE, 0, 180, 60),
    ('lava', TRUE, TRUE, 255, 0, 0)
;