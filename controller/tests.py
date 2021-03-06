import game as controller

#Character
class MockSprite:
    def __init__(self):
        self.id = None


class MockPiece:
    def __init__(self):
        self.id = None
    

character_1 = controller.Character(MockPiece(), MockSprite())
character_2 = controller.Character(MockPiece(), MockSprite())
assert character_1.sprite
assert character_1.piece
assert character_1.get_id()
assert character_1.get_id() == character_1.piece.id == character_1.sprite.id
assert character_2.get_id() == character_2.piece.id == character_2.sprite.id
assert character_1.get_id() is not character_2.get_id()
print("Controller unit tests successful!")
