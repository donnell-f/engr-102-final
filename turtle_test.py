import turtle
import re

SIZE = 10


def carriageReturn(numsquares):
    """Return the turtle to the beginning of the next line
        in preparation for drawing the next row of grid squares."""
    turtle.right(180)
    turtle.forward(SIZE*numsquares)
    turtle.left(90)
    turtle.forward(SIZE)
    turtle.left(90)


def drawSquares(colorname, num):
    """Draw `num` squares in a row as a single rectangle."""

    turtle.color(colorname)
    turtle.pendown()
    turtle.begin_fill()
    turtle.forward(SIZE*num)
    turtle.right(90)
    turtle.forward(SIZE)
    turtle.right(90)
    turtle.forward(SIZE*num)
    turtle.right(90)
    turtle.forward(SIZE)
    turtle.end_fill()
    turtle.penup()
    turtle.right(90)
    turtle.forward(SIZE*num)


def drawTitle(titleCode):
    """Draw the title given the encoded title string (see comment in `encodeTitle()`)."""
    
    numsquares = titleCode[0][1]

    for c in titleCode:
        match c[0]:
            case "X":
                drawSquares("red", c[1])
            case ".":
                drawSquares("yellow", c[1])
            case "\n":
                carriageReturn(numsquares)
            case _:
                raise ValueError


def encodeTitle(titleStr):
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


def runTheTurtle():
    # Read contents of the ascii art file into `title`.
    title = ""
    with open("title_art.txt", "r") as f:
        title = f.read()

    # Set up the screen all nice and pretty.
    screen = turtle.Screen()
    screen.setup(width=700, height=330)

    # Position the turtle slightly turtle.left of center, to make room for the inbound title.
    turtle.speed(0)
    turtle.penup()
    turtle.right(180)
    turtle.forward(150)
    turtle.right(180)

    # Turn the raw title string into a compressed encoding.
    # This helps speed up the drawing process.
    encodedTitle = encodeTitle(title)

    # At long last, draw the title.
    drawTitle(encodedTitle)


if __name__=="__main__":
    runTheTurtle()

