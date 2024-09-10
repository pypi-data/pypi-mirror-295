import turtle

def draw_letter(pen, letter, character, color):
    pen.color(color)
    pen.penup()
    start_x, start_y = pen.position()  # Store the starting position
    
    # Patterns for each letter (grid-based representation)
    patterns = {
        'A': ["  *  ", " * * ", "*****", "*   *", "*   *"],
        'B': ["**** ", "*   *", "**** ", "*   *", "**** "],
        'C': [" *** ", "*    ", "*    ", "*    ", " *** "],
        'D': ["**** ", "*   *", "*   *", "*   *", "**** "],
        'E': ["*****", "*    ", "**** ", "*    ", "*****"],
        'F': ["*****", "*    ", "**** ", "*    ", "*    "],
        'G': [" *** ", "*    ", "* ***", "*   *", " *** "],
        'H': ["*   *", "*   *", "*****", "*   *", "*   *"],
        'I': ["*****", "  *  ", "  *  ", "  *  ", "*****"],
        'J': ["*****", "   * ", "   * ", "*  * ", " **  "],
        'K': ["*   *", "*  * ", "***  ", "*  * ", "*   *"],
        'L': ["*    ", "*    ", "*    ", "*    ", "*****"],
        'M': ["*   *", "** **", "* * *", "*   *", "*   *"],
        'N': ["*   *", "**  *", "* * *", "*  **", "*   *"],
        'O': [" *** ", "*   *", "*   *", "*   *", " *** "],
        'P': ["**** ", "*   *", "**** ", "*    ", "*    "],
        'Q': [" *** ", "*   *", "* * *", "*  **", " ****"],
        'R': ["**** ", "*   *", "**** ", "*  * ", "*   *"],
        'S': [" ****", "*    ", " *** ", "    *", "**** "],
        'T': ["*****", "  *  ", "  *  ", "  *  ", "  *  "],
        'U': ["*   *", "*   *", "*   *", "*   *", " *** "],
        'V': ["*   *", "*   *", "*   *", " * * ", "  *  "],
        'W': ["*   *", "*   *", "* * *", "** **", "*   *"],
        'X': ["*   *", " * * ", "  *  ", " * * ", "*   *"],
        'Y': ["*   *", " * * ", "  *  ", "  *  ", "  *  "],
        'Z': ["*****", "   * ", "  *  ", " *   ", "*****"]
    }

    # Fetch the pattern for the letter, default to an empty pattern if not found
    pattern = patterns.get(letter.upper(), ["     ", "     ", "     ", "     ", "     "])

    # Draw the pattern on the screen
    for row in pattern:
        pen.setx(start_x)  # Reset to the starting x position for each row
        for char in row:
            if char == "*":
                pen.write(character, font=("Arial", 12, "bold"))  # Draw the selected character
            pen.forward(15)  # Move right to the next position
        pen.sety(pen.ycor() - 20)  # Move down to the next row


def draw_name(name, character, color):
    # Set up the screen
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Draw Your Name")

    # Set up the turtle
    pen = turtle.Turtle()
    pen.speed(1)
    pen.hideturtle()  # Hide the default turtle shape

    # Set starting position closer to the left
    x, y = -300, 100  # Adjusted starting position to reduce the blank space
    pen.penup()
    pen.goto(x, y)
    pen.pendown()

    # Draw each letter in the name
    for letter in name:
        draw_letter(pen, letter, character, color)  # Draws each letter based on the pattern
        pen.penup()
        pen.goto(pen.xcor() + 70, y)  # Move to the next letter position
        pen.pendown()

    # Wait for user to close the window
    screen.mainloop()

# Input from user
user_name = input("Enter your name: ")
selected_character = input("Enter the character to draw with: ")
desired_color = input("Enter the desired color (e.g., red, blue): ")

# Call the function to draw the name
draw_name(user_name, selected_character, desired_color)
