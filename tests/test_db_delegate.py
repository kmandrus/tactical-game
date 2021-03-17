import tac.hex.controller.db_delegate as db_delegate

db = db_delegate.PostgresDelegate('tactical_game')
tile_data = db.fetch_tile_data(1)
print(tile_data)
