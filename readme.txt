--> To Do:

Refactor model, demo, and test to use Dimensions and Point NamedTuples

Fix alignment and height of BoardView

Re-test and update first demo.

Add type hints and documentation.

Ensure all components work correctly

Migrate to Pytest

Move Board#move_piece to Game class

Develop a persistence strategy

Research unique random identifiers

Figure out how to write tests that expect a certain function to be called.
One place this is relevant is in #update and #render tests in the view package.

Add a remove sprite feature to the model and view board classes.

Raise an error if a piece or sprite already has an id when instantiating
a new character.

Create the controller versions of board and character classes.

Add tests for the controller package.

Change BoardView to read it's dimensions off of its surface. This implies the
BoardView will always be the size of its surface.

Pathfinding

Add a coordinate overlay to TileView
    
--> Completed:

Convert position tuples to NamedTuples

Combine the HexagonView and HexBoardView into one module. Sprite probably needs
to go in there too - it computes a bunch of stuff based on the assumption it lives
on a hex grid.

Make a battlemap that renders a token

Break draw method into update and render

Move sprites by clicking on the screen

Add character class responsible for linking pieces and sprites with a unique
id property. 

Break out #next_frame() method for view objects. The idea is to
do any computations related to animation/position/etc, (so, the #draw() stuff),
then render the frame separately. Maybe use the #update() -> #render() naming
scheme instead?

Create a 'character' class in the controller that links a Piece and its View.

Methods for adding and looking up characters by id

Upon completion of a sprite's move, it can optionally execute a callback.

Click a sprite to select it, then click to move. 

Run all tests... add another token then commit the above. Not bad!

Major file restructuring to fix imports

Movement paths as the primary form of movement

Deprecate Board_View #move in favor of calling a new #move directly on the
sprite 

Rework entire project to properly follow MVC
    BoardController
    TileController

Map Editor
    Tile has impassible property, Board has appropriate methods to get and set
    the property with
    Wired up editor class to grab the hex position of mouse clicks.
    Fill color in hexes when impassible
    Finish Editor Class
    Click to swap tile from walkable to unwalkable
    Save/Load from text file

Look up how to send SQL code to the database from python

DB saving and loading of maps in postgres
    Write save method in the map editor that generates SQL code

--> Thought Bubble
What problem does the character class solve? It links the sprite and piece
classes from the view and model. What is it used for? To locate the associated
sprite for a piece. I don't think this identification needs to go Sprite -- >
Piece either. Which is curious. I wonder if there is a way to streamline it
if we only need Piece --> Sprite lookup. 

