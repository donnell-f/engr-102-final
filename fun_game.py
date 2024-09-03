# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Cristian Reyna
#               Donnell Fulwiler
#               Caleb Glover
#               Vaidehi Singhal
# Section:      525
# Assignment:   Lab 13
# Date:         1 December 2023

from enum import Enum
import turtle

BLACK = chr(9675)
WHITE = chr(9679)

SIZE = 10    # Size of grid square to draw for MyTurtle class.
TITLE_ART = """. . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . X X X . . . . . . . . . . . . . X . . . . . . . . .
. . X . . X . . . . . . . . . . . . X . . . . . . . . .
. . X . . X . . . . . . . . . . X X X X X . . . . . . .
. . X X X . . X X X . . X X X . . . X . . . X X X . . .
. . X . . . X . . . X . X . . X . . X . . X . . . X . .
. . X . . . X X X X . . X . . X . . X . . X X X X . . .
. . X . . . X . . . . . X . . X . . X . . X . . . . . .
. . X . . . . X X X X . X . . X . . X . . . X X X X . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . .
"""



class GameStatus(Enum):
    BLACK_WINS = 1
    WHITE_WINS = 2
    IN_PROGRESS = 4


class InvalidMoveException(Exception):
    """For when the player's move is invalid."""
    pass


class GameClass:
    
    def __init__(self):
        # "○" = black
        # "●" = white
        # "." = empty
        self.board = [ [ "." for i in range(0,19) ] for j in range(0,19) ]
        self.numMoves = 0
        self.piece = WHITE    # Initialized for White to start.
        self.a = -10
        self.row = 0
        self.col = 0
        self.numCaptures = {}
        self.numCaptures[WHITE] = 0
        self.numCaptures[BLACK] = 0
        self.antiPiece = BLACK
        self.winner = {
            BLACK: GameStatus.BLACK_WINS,
            WHITE: GameStatus.WHITE_WINS
        }
    

    # Check if `row` and `col` are in a reasonable range.
    def inRange(self, row, col):
        return (row in range(0,19)) and (col in range(0,19))


    # Check if a move, at the inferred indices `self.row` and `self.col` would be valid.
    def validMove(self):
        return (self.row in range(0,19)) and (self.col in range(0,19)) and (self.board[self.row][self.col] == ".")


    # Check for sequential pieces of the current color in a given direction (specified by a row/column offset vector, v, in **index space**).
    # Returns true if it finds five or more pieces in a row.
    def checkWinDirection(self, v=(0,0)):
    
        sequence_length = 1

        # Check for a five-in-a-row in the direction of the POSITIVE direction vector.
        s = 0
        offrow = self.row
        offcol = self.col
        while (self.inRange(offrow, offcol)) and (self.board[offrow][offcol] == self.piece):
            s += 1
            offrow = self.row + s*v[0]    # The "+" here is the only difference.
            offcol = self.col + s*v[1]
        sequence_length += s - 1


        # Check for a five-in-a-row in the direction of the NEGATIVE direction vector.
        s = 0
        offrow = self.row
        offcol = self.col
        while (self.inRange(offrow, offcol)) and (self.board[offrow][offcol] == self.piece):
            s += 1
            offrow = self.row - s*v[0]    # The "-" here is the only difference.
            offcol = self.col - s*v[1] 
        sequence_length += s - 1
        

        # print(f"{sequence_length} for v={v}")    # DEBUG
        return (sequence_length >= 5)


    # Check to see if the move we just made in this game state was the winning move.
    def checkWin(self):

        # If either Black or White attains 5 captures, they win.        
        if self.numCaptures[self.piece] >= 5:
            return self.winner[self.piece]

        # Directional check visuals:
        # self.checkWinDirection(v=(1,1))    # \
        # self.checkWinDirection(v=(-1,1))   # /
        # self.checkWinDirection(v=(1,0))    # |
        # self.checkWinDirection(v=(0,1))    # _

        tests = [ self.checkWinDirection(v=(1,1)),
        self.checkWinDirection(v=(-1,1)),
        self.checkWinDirection(v=(1,0)),
        self.checkWinDirection(v=(0,1)) ]

        gameIsWon = any(tests)

        if not gameIsWon:
            return GameStatus.IN_PROGRESS
        elif gameIsWon:
            return self.winner[self.piece]
            

    # Capture in a specified direction, if possible.
    def tryCaptureDirection(self, v=(0,0)):
        offrow = self.row+v[0]*3
        offcol = self.col+v[1]*3

        if (self.inRange(offrow, offcol)) and (self.board[ self.row+v[0]*3 ][ self.col+v[1]*3 ] == self.piece):

            if (self.board[ self.row+v[0]*1 ][ self.col+v[1]*1 ] == self.antiPiece) and \
                (self.board[ self.row+v[0]*2 ][ self.col+v[1]*2 ] == self.antiPiece):
                self.board[ self.row+v[0]*1 ][ self.col+v[1]*1 ] = "."
                self.board[ self.row+v[0]*2 ][ self.col+v[1]*2 ] = "."
                self.numCaptures[self.piece] += 1


    # Check every available capture direction vector (in index space). Capture if possible.
    def checkCapture(self):
        self.tryCaptureDirection(v=(0,1))
        self.tryCaptureDirection(v=(-1,1))
        self.tryCaptureDirection(v=(-1,0))
        self.tryCaptureDirection(v=(-1,-1))
        self.tryCaptureDirection(v=(0,-1))
        self.tryCaptureDirection(v=(1,-1))
        self.tryCaptureDirection(v=(1,0))
        self.tryCaptureDirection(v=(1,1))
        


    # Places a stone, if placeable. Otherwise: raise exception.
    def placeStone(self):
        self.numMoves += 1
        if self.validMove():
            self.board[self.row][self.col] = self.piece
        else:
            raise InvalidMoveException
        

    # Switches between Black and White.
    def switchPiece(self):
        if self.piece == BLACK:
            self.piece = WHITE
        elif self.piece == WHITE:
            self.piece = BLACK
        
        if self.antiPiece == BLACK:
            self.antiPiece = WHITE
        elif self.antiPiece == WHITE:
            self.antiPiece = BLACK
    

    # Prints the board all nice and pretty like.
    def printBoard(self):
        print( "    " + "".join([str(i).ljust(3, " ") for i in range(1, 19 +1)]) )
        print( "\n".join([ str(i+1).ljust(4," ")+"  ".join(self.board[i]) for i in range(len(self.board)) ]) )
        print("-"*59)


    # Write the current board state to a file named `pente_board.txt`.
    def writeBoard(self):
        printmap = {
            BLACK: "o",
            WHITE: "x",
            ".": "."
        }

        for i in range(19):
            for j in range(19):
                self.board[i][j] = printmap[self.board[i][j]]

        finalstr = ("    " + "".join([str(i).ljust(3, " ") for i in range(1, 19 +1)])) + "\n" + ("\n".join([ str(i+1).ljust(4," ")+"  ".join(self.board[i]) for i in range(len(self.board)) ])) + "\n" + ("-"*59) + "\n"
        with open("pente_board.txt", "w") as f:
            f.write(finalstr)





class MyTurtle:

    def carriageReturn(self, numsquares):
        """Return the turtle to the beginning of the next line
            in preparation for drawing the next row of grid squares."""
        turtle.right(180)
        turtle.forward(SIZE*numsquares)
        turtle.left(90)
        turtle.forward(SIZE)
        turtle.left(90)


    def drawSquares(self, colorname, num):
        """Draw `num` squares in a row as a single rectangle."""

        turtle.color(colorname)
        turtle.pendown()
        turtle.begin_fill()
        turtle.forward(SIZE*num)    # Top edge
        turtle.right(90)
        turtle.forward(SIZE)    # Right edge
        turtle.right(90)
        turtle.forward(SIZE*num)    # Bottom edge
        turtle.right(90)
        turtle.forward(SIZE)    # Left edge
        turtle.end_fill()
        turtle.penup()    # Stop drawing...
        turtle.right(90)
        turtle.forward(SIZE*num)    # Return to the beginning of the next square.


    def drawTitle(self, titleCode):
        """Draw the title given the encoded title string (see comment in `encodeTitle()`)."""
        
        numsquares = titleCode[0][1]

        for c in titleCode:
            match c[0]:
                case "X":
                    self.drawSquares("red", c[1])
                case ".":
                    self.drawSquares("yellow", c[1])
                case "\n":
                    self.carriageReturn(numsquares)
                case _:
                    raise ValueError


    def encodeTitle(self, titleStr):
        """Given the string contents of the `title_art.txt` file, encode the string
            into an array of codons, where each codon of the form `(char, n)`
            describes a certain `char` repeated `n` times in the string."""

        titleStr = titleStr.replace(" ", "")   # Clear whitespace from the input (it is unnecessary).
        
        codons = []
        length = 1
        for i in range(len(titleStr) - 1):
            if titleStr[i] == titleStr[i+1]:
                length += 1
            elif titleStr[i] != titleStr[i+1]:
                codons.append( (titleStr[i], length) )
                length = 1
        
        return codons


    def runTurtle(self):
        # Make a title from the `TITLE_ART` constant.
        title = TITLE_ART

        # Set up the screen all nice and pretty.
        screen = turtle.Screen()
        screen.setup(width=700, height=330)
        
        # Call the window manager to bring the turtle graphics window to the top of the screen.
        window = screen.getcanvas().winfo_toplevel()
        window.call('wm', 'attributes', '.', '-topmost', '1')

        # Position the turtle slightly turtle.left of center, to make room for the inbound title.
        turtle.speed(0)
        turtle.penup()
        turtle.right(180)
        turtle.forward(150)
        turtle.right(180)

        # Turn the raw title string into a compressed encoding.
        # This helps speed up the drawing process.
        encodedTitle = self.encodeTitle(title)

        # At long last, draw the title.
        self.drawTitle(encodedTitle)


        # Close turtle graphics if user clicks.
        turtle.exitonclick()


    # Initialization function for this class. Doesn't really do anything.
    def __init__(self):
        pass






def main():

    # Ask user if they want to display the Turtle Graphics intro. If "y", use turtle graphics to draw a nice title.
    turtCheck = input("Display turtle intro (y/n)? ")
    turtCheck = True if turtCheck=="y" else False
    if turtCheck:
        turt = MyTurtle()
        try:
            turt.runTurtle()
        except:
            # If the user closes the window early it will produce an error, interrupting the flow of the program. This try-except will handle that error, if it occurs.
            print("Closing turtle...")

    print()

    # Start off the game by printing the rules.
    rules_str = "Rules of Pente:\n    - Players alternate turns placing stones of their color.\n    - You can capture opponent pieces by flanking exactly two\n      of their pieces with two pieces of your own.\n        - (e.g. \"XOOX\" --> \"X__X\").\n    - You can win by making five captures or placing five\n      stones in a row.\n    - Additionally, feel free to interrupt the control flow\n      using these \"Menu... \" prompts:\n        - instr: display these instructions again.\n        - quit: quit the game early.\n        - score: display score.\n        - (blank): continue with the normal flow of the game"
    print(rules_str)
    print()
    print()

    # Create an instance of the game.
    Game = GameClass()

    pieceName = {
        BLACK: "Black",
        WHITE: "White"
    }

    # Run the main loop of the game.
    while (True):
        Game.printBoard()

        # Print the menu and handle user input for it.
        minput = input(f"[{pieceName[Game.piece]}] Menu... ")
        match minput:
            case "instr":
                print(rules_str)
                print()
                print()
                continue

            case "quit":
                print()
                writeprompt = input("Would you like to write the board to a file before you go? (y/n): ")
                match writeprompt:
                    case "y":
                        Game.writeBoard()
                        print("Done! Thanks for playing!")
                    case "n":
                        print("Thanks for playing!")
                    case _:
                        Game.writeBoard()
                        print("Not sure what you said, but I wrote it anyway just to be safe.")
                break

            case "score":
                print(f"Black captures: {Game.numCaptures[BLACK]}")
                print(f"White captures: {Game.numCaptures[WHITE]}")
                print()
                print()
                continue

            case "":
                pass

            case _:
                print("I didn't quite get that. Try again.")
                print()
                print()
                continue


        # Take row/column input from user for piece placement. If invalid, `continue` the loop and try again.
        try:
            row = int(input(f"[{pieceName[Game.piece]}] enter row number: "))
            col = int(input(f"[{pieceName[Game.piece]}] enter column number: "))
        except ValueError:
            print("ERROR: invalid input. Try again.")
            print()
            print()
            continue

        # Set up the state of the board so as to place a stone at the user's desired index.
        Game.row = row - 1
        Game.col = col - 1

        # Try to place a stone. If position is invalid, `continue` the loop and try again.
        try:
            Game.placeStone()
            print()
            print()

        except InvalidMoveException:
            print("ERROR: invalid move. Try again.")
            print()
            print()
            continue


        # Check for any capture opportunities.
        Game.checkCapture()


        # Now that the stone has been placed, check and see if this move wins the game.
        status = Game.checkWin()


        # Depending on the outcome of `checkWin()`, this `switch` statement will
        # decide whether to close the game or keep it running.
        match status:

            case GameStatus.IN_PROGRESS:
                pass

            case GameStatus.BLACK_WINS:
                Game.printBoard()
                print(F"{BLACK}{BLACK} Game over! Black wins! {BLACK}{BLACK}")
                print("-"*59)
                print("Final score: ")
                print(f"Black captures: {Game.numCaptures[BLACK]}")
                print(f"White captures: {Game.numCaptures[WHITE]}")
                print("-"*59)

                # Write the final board state to a file, if desired.
                writeprompt = input("Would you like to write the final state of the board to a file? (y/n): ")
                print()
                match writeprompt:
                    case "y":
                        Game.writeBoard()
                        print("Done! Thanks for playing!")
                    case "n":
                        print("Thanks for playing!")
                    case _:
                        Game.writeBoard()
                        print("Not sure what you said, but I wrote it anyway just to be safe.")
                break


            case GameStatus.WHITE_WINS:
                Game.printBoard()
                print(f"{WHITE}{WHITE} Game over! White wins! {WHITE}{WHITE}")
                print("-"*59)
                print("Final score: ")
                print(f"Black captures: {Game.numCaptures[BLACK]}")
                print(f"White captures: {Game.numCaptures[WHITE]}")
                print("-"*59)

                # Write the final board state to a file, if desired.
                writeprompt = input("Would you like to write the final state of the board to a file? (y/n): ")
                print()
                match writeprompt:
                    case "y":
                        Game.writeBoard()
                        print("Done! Thanks for playing!")
                    case "n":
                        print("Thanks for playing!")
                    case _:
                        Game.writeBoard()
                        print("Not sure what you said, but I wrote it anyway just to be safe.")
                break


            case _:
                raise ValueError
                break
        
        
        # Finally, assuming the game is still running, switch whose turn it is.
        Game.switchPiece()





if __name__=="__main__":
    main()

