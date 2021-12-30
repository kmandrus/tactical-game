import tac.hex.controller.db_delegate as db_delegate

db = db_delegate.PostgresDelegate('tactical_game')
print(db.board_exists("test"))
print(db.board_exists("dne"))


