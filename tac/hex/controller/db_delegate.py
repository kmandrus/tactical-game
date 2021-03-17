import psycopg2

class PostgresDelegate:
    def __init__(self, dbname):
        self.dbname = dbname
        self.connection = psycopg2.connect(f"dbname={self.dbname}")
    
    def fetch_tile_data(self, id_):
        SQL = """
            SELECT *
            FROM tile
            WHERE id=%s;
        """
        cursor = self.connection.cursor()
        cursor.execute(SQL, str(id_))
        row = cursor.fetchall()[0]
        cursor.close()
        return self.to_tile_data(row)
    
    def to_tile_data(self, row):
        id_, name, is_impassible, is_filled, *rgb = row
        return {
            'id': id_, 'name': name, 'is_impassible': is_impassible,
            'is_filled': is_filled, 'fill_color': rgb }

    
    def save_new_board(self, board_data):
        cursor = self.connection.cursor()
        SQL = """
            INSERT INTO board_tiles (board_name, x, y, tile_id, piece_id)
            VALUES (%(board_name)s, %(x)s, %(y)s, %(tile_id)s, %(piece_id)s);
            """
        for row in board_data:
            cursor.execute(SQL, row)
        self.connection.commit()
        cursor.close()
    
    def update_board(self, board_data):
        SQL = """
            UPDATE board_tiles
            SET tile_id=%(tile_id)s, piece_id=%(piece_id)s
            WHERE board_name=%(board_name)s AND x=%(x)s AND y=%(y)s;
        """
        cursor = self.connection.cursor()
        for row in board_data:
            cursor.execute(SQL, row)
        self.connection.commit()
        cursor.close()
