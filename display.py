#!usr/bin/env python3
# Manage CLI display/printing. A lot of the printing involves ASCII box shapes.

from holder import Holder
from playfield import Playfield
from tetromino_queue import TetrominoQueue

BOX_CHAR = {
    "top-left": "┌",
    "top-right": "┐",
    "bottom-left": "└",
    "bottom-right": "┘",
    "vertical": "│",
    "horizontal": "─",
}

# See https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit for details on ANSI escape codes used below
SHAPE_PRINT = [
    " ",
    "\033[38;5;14mI\033[m",  # I -> cyan
    "\033[38;5;11mO\033[m",  # O -> yellow
    "\033[38;5;13mT\033[m",  # T -> purple
    "\033[38;5;10mS\033[m",  # S -> green
    "\033[38;5;9mZ\033[m",  # Z -> red
    "\033[38;5;12mJ\033[m",  # J -> blue
    "\033[38;5;208mL\033[m",  # L -> orange
]


def get_box_boundary_string(grid_width, boundary):
    """
    Return a string of ASCII horizontal box lines with a top corner on either end.
    """
    assert boundary in ["top", "bottom"]
    # Double the grid width value to account for the fact that the grid is double spaced
    char_width = grid_width * 2 + 1
    return (
        BOX_CHAR[boundary + "-left"]
        + BOX_CHAR["horizontal"] * char_width
        + BOX_CHAR[boundary + "-right"]
    )


def get_str_between_box_walls(input_str):
    """
    Return the input string between ASCII box walls
    """
    return " ".join(BOX_CHAR["vertical"] + input_str + BOX_CHAR["vertical"])


def get_str_in_box(input_str):
    """
    Return the input string enclosed in an ASCII box
    """
    input_lines = input_str.split("\n")
    # Get the width of the box
    width = len(max(input_lines))
    # Assemble and return the box
    return "\n".join(
        [get_box_boundary_string(width, "top")]
        + [get_str_between_box_walls(line) for line in input_lines]
        + [get_box_boundary_string(width, "bottom")]
    )


def colourise_string(input_str):
    colourised_string = input_str
    for grid_value, grid_print in enumerate(SHAPE_PRINT):
        colourised_string = colourised_string.replace(
            " {}".format(grid_value), " {}".format(grid_print)
        )
    return colourised_string


def get_display_element_string(element):
    """
    Take the display element and produce a colourised string in a box
    """
    assert isinstance(element, (Playfield, Holder, TetrominoQueue))
    return colourise_string(get_str_in_box(str(element)))


def clear_console_display():
    """
    Clear the console display using an ANSI escape code
    """
    # See https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences for more
    # information
    print("\033c\033[3J", end="")


def update_display(playfield, holder):
    """
    Claer the console and print a graphical representation of the playfield.
    """
    clear_console_display()
    # Print the progress metrics
    print(
        "num blocks placed = {}, num rows cleared = {}".format(
            playfield.num_blocks_placed, playfield.num_rows_cleared
        )
    )
    # Generate the string lists for individual elements.
    display_str_list = get_display_element_string(playfield).split("\n")
    holder_str_list = get_display_element_string(holder).split("\n")

    # Place the holder box besides the playfield box
    for row in range(len(holder_str_list)):
        display_str_list[row] += "  " + holder_str_list[row]

    # Rejoin and print the display string list.
    print("\n".join(display_str_list))


if __name__ == "__main__":
    print(get_str_in_box("TESTING\nTEST   "))
