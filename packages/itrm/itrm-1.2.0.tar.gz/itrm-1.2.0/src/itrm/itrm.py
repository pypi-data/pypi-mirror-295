import numpy as np
import time
import math
import os
import sys
import shutil
import subprocess
import signal
from configparser import ConfigParser
if sys.platform == "win32":
    import msvcrt
else:
    import termios

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# Scalars
EPS         = 1e-16
GRAY_4BIT   = 90
GRAY_8BIT   = 242
COLS        = 60
ROWS        = 20

# Strings
CSI         = "\x1b["
RESET       = CSI + "0m"
BOLD        = CSI + "1m"
FRGND       = CSI + "38;5;"
HIDE_CURSOR = CSI + "?25l"
SHOW_CURSOR = CSI + "?25h"
ARROW_UP    = "A"
ARROW_DN    = "B"
ARROW_RT    = "C"
ARROW_LT    = "D"

# ------------------------------------------------------------------------------
# Generic functions
# ------------------------------------------------------------------------------

def set_color_maps(cmap):
    # Define the color lists.
    color_maps = { "spectrum": 0, "viridis": 1, "grays": 2,
            "reds": 3, "greens": 4, "blues": 5, "4bit": 6 }
    dark_colors = [
            [ 33,  40, 220, 202, 201,  93], # 0: spectrum
            [184, 113,  36,  30,  60,  53], # 1: viridis
            [253, 250, 247, 244, 241, 238], # 2: grays
            [197, 196, 160, 124,  88,  52], # 3: reds
            [ 47,  46,  40,  34,  28,  22], # 4: greens
            [ 27,  21,  20,  19,  18,  17], # 5: blues
            [ 34,  36,  32,  33,  31,  35]] # 6: 4bit
    lite_colors = [
            [ 75,  82, 228, 214, 213, 135], # 0: spectrum
            [227, 156,  79,  73, 103,  96], # 1: viridis
            [255, 252, 249, 246, 243, 240], # 2: grays
            [198, 197, 196, 160, 124,  88], # 3: reds
            [ 48,  47,  46,  40,  34,  28], # 4: greens
            [ 33,  27,  21,  20,  19,  18], # 5: blues
            [ 94,  96,  92,  93,  91,  95]] # 6: 4bit

    # Check the color map.
    cmap = cmap.lower()
    if cmap not in color_maps:
        print(f"cmap in {full_path} is not valid. It must be one of")
        for key in color_maps.keys():
            print(f"    '{key}'")
        print("Defaulting to '4bit'.")
        cmap = "4bit"

    # Evaluate the color name.
    n_color = color_maps[cmap]
    darks = dark_colors[n_color]
    lites = lite_colors[n_color]

    # Set foreground, gray, and bold commands.
    if cmap == "4bit":
        frgnd = CSI
        gray = GRAY_4BIT
    else:
        frgnd = FRGND
        gray = GRAY_8BIT

    return darks, lites, frgnd, gray, cmap


class Config:
    """
    This class creates, loads, and locates the configuration settings file.

    Attributes
    ----------
    uni : bool, default True
        Flag to use Unicode characters instead of ASCII characters.
    ar : float, default 0.48
        Aspect ratio (width to height) of the terminal characters.
    cmap : str, default "4bit"
        Name of the color map.
    bold : bool, default True
        Flag to use bold drawing characters in plot and iplot.
    darks : list, default 4bit dark map
        List of dark color values.
    lites : list, default 4bit light map
        List of light color values.
    frgnd : str, default FRGND
        Beginning of foreground color setting command string.
    gray : str, default {8-bit gray}
        Foreground gray color value.
    """

    # Initialize the configuration with default values.
    uni = True
    ar = 0.48
    cmap = "4bit"
    bold = True
    darks = [34, 36, 32, 33, 31, 35] # 4bit
    lites = [94, 96, 92, 93, 91, 95] # 4bit
    frgnd = CSI
    gray = GRAY_4BIT

    def __init__(self):
        """ This function modifies the global configurations in the config class
        and then save updates to the config.ini file. """

        # Get the full path of the configuration file.
        mod_path = os.path.abspath(__file__)
        dir_path = os.path.split(mod_path)[0]
        full_path = os.path.join(dir_path, "config.ini")

        # If the configuration file exists, read the settings.
        save_config = False
        if os.path.exists(full_path):
            # Load a configuration object with the config.ini file.
            configuration = ConfigParser()
            configuration.read(full_path)

            # Parse the contents of the "render" section.
            section = "render"
            if configuration.has_section(section):
                # Get option "uni".
                if configuration.has_option(section, "uni"):
                    Config.uni = configuration[section]["uni"] == "True"
                else:
                    save_config = True

                # Get option "ar" (aspect ratio).
                if configuration.has_option(section, "ar"):
                    try:
                        Config.ar = float(configuration["render"]["ar"])
                    except TypeError:
                        save_config = True
                else:
                    save_config = True

                # Get option "cmap" (color map).
                if configuration.has_option(section, "cmap"):
                    Config.cmap = configuration["render"]["cmap"]
                else:
                    save_config = True

                # Get option "bold".
                if configuration.has_option(section, "bold"):
                    Config.bold = configuration[section]["bold"] == "True"
                else:
                    save_config = True
            else:
                save_config = True
        else: # default settings
            save_config = True

        # Define the color lists.
        Config.darks, Config.lites, Config.frgnd, Config.gray, cmap \
                = set_color_maps(Config.cmap)
        if cmap != Config.cmap:
            Config.cmap = cmap
            save_config = True

        # Save the configuration.
        if save_config:
            # Build a configuration object.
            configuration = ConfigParser()
            configuration.add_section("render")
            configuration.set("render", "uni", str(Config.uni))
            configuration.set("render", "ar", str(Config.ar))
            configuration.set("render", "cmap", str(Config.cmap))
            configuration.set("render", "bold", str(Config.bold))

            # Write the file.
            try:
                fid = open(full_path, "w")
                configuration.write(fid)
                fid.close()
                print(f"config.ini file written at {full_path}.")
            except OSError:
                print(f"Could not write to file {full_path}.")

    def where():
        """ Return the location of the config.ini file. """

        # Get the full path of the config file.
        mod_path = os.path.abspath(__file__)
        dir_path = os.path.split(mod_path)[0]
        full_path = os.path.join(dir_path, "config.ini")

        # Print the location of the config file.
        if os.path.exists(full_path):
            return(full_path)
        else:
            return("config.ini file does not exist.")

    def what():
        """ Return the configuration parameters. """
        return f"uni:{Config.uni}, ar:{Config.ar}, " \
                f"cmap:{Config.cmap}, bold:{Config.bold}"


# Initialize the configuration.
Config()


def sigfigs(x, x_span):
    """ Calculate the number of significant figures (not decimal places) for x,
    given the range of x is x_span. """
    x = abs(x)
    x_span = abs(x_span)
    if (not np.isfinite(x)) or (x == 0):
        sigs = 1
    elif x_span == 0:
        sigs = 7
    else:
        sigs = max(2, math.ceil(np.log10(x)) - math.floor(np.log10(x_span)) + 3)
    return sigs


def ftostr(x, sigs=5):
    """ Format a number as a floating-point number string. """
    return f"{x:.{sigs}g}".replace("e+0", "e").replace("e-0", "e-")


def is_term():
    """ Check if this is a terminal. """
    if not (hasattr(sys.stdout, "isatty") and sys.stdout.isatty()):
        return False
    else:
        return True


class TermAttr:
    orig = None


def term_init():
    """ Prepare the terminal for receiving ANSI escape sequences and for running
    in raw mode. """
    if sys.platform == "win32":
        subprocess.call('', shell=True) # Enable ANSI escape sequences.
    else:
        signal.signal(signal.SIGINT, term_close)
        try:
            TermAttr.orig = termios.tcgetattr(0)
            tty_mode = TermAttr.orig.copy()
            tty_mode[3] &= ~termios.ICANON & ~termios.ECHO
            tty_mode[3] |= termios.ISIG  # Ctrl-c to exit
            termios.tcsetattr(0, termios.TCSANOW, tty_mode)
        except termios.error:
            pass


def term_read():
    """ Read a character from the keyboard. The arrow keys are converted to
    letters. """

    key = None
    if sys.platform == "win32":
        while key is None:
            key = msvcrt.getch()
            if key == b"\xe0": # escape
                key = msvcrt.getch()
                if key == b"H": # arrow up
                    key = "k"
                elif key == b"P": # arrow down
                    key = "j"
                elif key == b"M": # arrow right
                    key = "l"
                elif key == b"K": # arrow left
                    key = "h"
                elif key == b"\x8d": # alt arrow up on some terminals
                    key = "K"
                elif key == b"\x91": # alt arrow down on some terminals
                    key = "J"
                elif key == b"t": # alt arrow right on some terminals
                    key = "L"
                elif key == b"s": # alt arrow left on some terminals
                    key = "H"
                elif key == b"S": # delete
                    key = "q"
                else:
                    key = None
            elif key == b"\x00": # alt arrow
                key = msvcrt.getch()
                if key == b"\x98": # alt arrow up
                    key = "K"
                elif key == b"\xa0": # alt arrow down
                    key = "J"
                elif key == b"\x9d": # alt arrow right
                    key = "L"
                elif key == b"\x9b": # alt arrow left
                    key = "H"
                else:
                    key = None
            elif key in (b"\r", b"\x08"): # enter or backspace
                key = "q"
            elif 32 <= ord(key) <= 126:
                key = key.decode('utf-8')
            else:
                key = None
    else: # posix system
        while key is None:
            key = sys.stdin.read(1)
            if key == "\x1b": # escape
                key = sys.stdin.read(1)
                if key == "[": # CSI
                    key = sys.stdin.read(1)
                    if key == ARROW_UP: # arrow up
                        key = "k"
                    elif key == ARROW_DN: # arrow down
                        key = "j"
                    elif key == ARROW_RT: # arrow right
                        key = "l"
                    elif key == ARROW_LT: # arrow left
                        key = "h"
                    elif key == "1": # possible shift arrow
                        chars = sys.stdin.read(3)
                        if chars == ";2" + ARROW_UP: # shift arrow up
                            key = "K"
                        elif chars == ";2" + ARROW_DN: # shift arrow down
                            key = "J"
                        elif chars == ";2" + ARROW_RT: # shift arrow right
                            key = "L"
                        elif chars == ";2" + ARROW_LT: # shift arrow left
                            key = "H"
                    elif key == "3": # possible delete
                        key = sys.stdin.read(1)
                        if key == "~": # delete
                            key = "q"
                        else:
                            key = None
                    else:
                        key = None
                else:
                    key = None
            elif key == "\n": # enter
                key = "q"
            elif ord(key) == 127: # backspace
                key = "q"
            else:
                break
    return key


def term_size():
    """ Get the terminal size if available; return COLS, ROWS if not. """
    cols, rows = shutil.get_terminal_size(fallback=(COLS, ROWS))
    return cols, rows


def term_close(sig=None, frame=None):
    # Restore terminal settings
    if TermAttr.orig is not None:
        termios.tcsetattr(0, termios.TCSADRAIN, TermAttr.orig)

    # Carriage return and show the cursor.
    sys.stdout.write(SHOW_CURSOR + "\r")
    sys.stdout.flush()

    # Exit.
    if sig is not None:
        sys.exit(0)

# ------------------------------------------------------------------------------
# Plotting functions
# ------------------------------------------------------------------------------

def plot(x, y=None, label=None, rows=1, cols=1,
        ea=False, lg=None, overlay=False, cmap=None):
    """
    Create a text-based plot of the path defined by (x, y) using characters.
    If the size of the terminal can be found, that will be used for sizing the
    plot. Otherwise, default dimensions will be used. Note that this function
    does not plot connecting lines, only the points specified by the (x, y)
    pairs.

    Parameters
    ----------
    x : (K,) or (J, K) np.ndarray or (J, K) list of np.ndarrays
        Array of x-axis values, list of such arrays, or matrix of rows of x-axis
        values.
    y : (K,) or (J, K) np.ndarray or (J, K) list of np.ndarrays, default None
        Array of y-axis values, list of such arrays, or matrix of rows of y-axis
        values. If y is not provided, x will be used as the y array and
        x will be defined to be an array of indices (starting at zero).
    label : str, default ""
        Text to place at the bottom-right of the plot.
    rows : int, default 1
        Desired number of rows if greater than 1 or fraction of existing rows
        otherwise.
    cols : int, default 1
        Desired number of columns if greater than 1 or fraction of existing
        columns otherwise.
    ea : bool, default False
        Flag to apply equal axis scaling to the x and y axes. Because the
        appearance of proportionality is affected by the particular font chosen
        and the settings of the terminal emulator being used, the effective
        aspect ratio of the characters can be set with itrm.Config class.
    lg : str, default None
        Logarithmic scaling of axes. If None, both axes will have linear
        scaling. Otherwise, lg should be a string: "x", "y", or "xy".
    overlay : bool, default False
        Flag to print new plot on top of a previous plot.
    cmap : str, default None
        Name of the color map. This overrides the value defined in config.ini.

    Notes
    -----
    Non-finite (i.e., nan, inf, -inf) and imaginary values will be ignored.
    """

    # Ensure the label is a correct type.
    if (label is not None) and not isinstance(label, (str, list, tuple)):
        raise ValueError("label must be a string or None.")

    # Check if this is a full terminal.
    use_esc = is_term()

    # Initialize the data sets, canvas, view, and cursor.
    sets = Sets(x, y) # Form x and y into lists of arrays.
    canvas = Canvas(cols, rows, Config.uni, cmap, 7) # char sets, size, alloc.
    lg = "" if lg is None else lg.lower()
    view = View(sets, canvas, # Get limits of valid data and define view edges.
            xlg=("x" in lg), ylg=("y" in lg), ea=ea)

    # Evaluate the label.
    if (label is not None) and isinstance(label, (list, tuple)):
        label = label[0] if len(label) == sets.J + 1 else None

    # Hide the cursor and move the terminal cursor up if this plot is overlaid.
    # The "+ 2" accounts for the border.
    if use_esc:
        sys.stdout.write(HIDE_CURSOR)
        if overlay and (Canvas.rows_last_plot is not None):
            sys.stdout.write(CSI + str(Canvas.rows_last_plot + 2) + ARROW_UP)
        sys.stdout.flush()
        Canvas.rows_last_plot = canvas.rows

    # Update canvas size.
    canvas.check_size()
    canvas.update_size() # Set the integer size and alloc memory.

    # Map the data to the canvas.
    canvas.to_chars(sets, view)
    canvas.draw_chars(view, label, use_esc=use_esc)

    # Carriage return and show the cursor.
    if use_esc:
        sys.stdout.write("\r" + SHOW_CURSOR)
    sys.stdout.flush()


def iplot(x, y=None, label=None, rows=1, cols=1,
            lg=None, overlay=False, cmap=None):
    """
    Create an interactive, text-based plot of the path defined by (x, y) using
    characters. If the size of the terminal can be found, that will be used for
    sizing the plot. Otherwise, default dimensions will be used. Note that this
    function does not plot connecting lines, only the points specified by the
    (x, y) pairs. Once the function has been called, the terminal will be in
    interactive mode. The user can then control the cursor position, x-axis
    zoom, and various other settings with keybindings.

    Parameters
    ----------
    x : (K,) or (J, K) np.ndarray or (J, K) list of np.ndarrays
        Array of x-axis values, list of such arrays, or matrix of rows of x-axis
        values.
    y : (K,) or (J, K) np.ndarray or (J, K) list of np.ndarrays, default None
        Array of y-axis values, list of such arrays, or matrix of rows of y-axis
        values. If y is not provided, x will be used as the y array and
        x will be defined to be an array of indices (starting at zero).
    label : str or list of strings, default None
        Text to place at the bottom-right of the plot.
    rows : int, default 1
        Desired number of rows if greater than 1 or fraction of existing rows
        otherwise.
    cols : int, default 1
        Desired number of columns if greater than 1 or fraction of existing
        columns otherwise.
    lg : str, default None
        Logarithmic scaling of axes. If None, both axes will have linear
        scaling. Otherwise, lg should be a string: "x", "y", or "xy". The
        scaling is applied at render, not to the data. So, the text readout of
        the cursor will be in the original scaling of the data.
    overlay : bool, default False
        Flag to draw a new plot on top of a previous plot.
    cmap : str, default None
        Name of the color map. This overrides the value defined in config.ini.

    Keybindings
    -----------
    q, backspace, return    : exit interactive plot
    h, a, left              : move cursor left
    l, d, right             : move cursor right
    H, A, shift left        : move cursor left fast
    L, D, shift right       : move cursor right fast
    g                       : move cursor to start
    G                       : move cursor to end
    j, s, down              : zoom in
    k, w, up                : zoom out
    J, S, shift down        : zoom in fast
    K, W, shift up          : zoom out fast
    n                       : next data row
    N                       : previous data row
    m                       : next info set
    M                       : previous info set
    c, z                    : center view on cursor
    i                       : toggle individual view
    x                       : toggle x-axis logarithmic scaling
    y                       : toggle y-axis logarithmic scaling
    v                       : toggle ghost cursor
    fd                      : differentiate data
    fi                      : integrate data
    ff                      : get the FFT of the data
    ftl                     : trim left
    ftr                     : trim right
    fu                      : show only unique points (to 9th decimal place)
    f#a                     : apply weighted moving average of width #
    f#d                     : de-trend data with polynomial of degree #
    f#u                     : show only unique points (to #th decimal place)
    F                       : restore original data

    Notes
    -----
    Non-finite (i.e., nan, inf, -inf) and imaginary values will be ignored.

    Since the cursor can only be controlled horizontally and there is no way to
    properly handle a curve which doubles back, the x-axis values must
    monotonically increase. Monotonically decreasing x values will cause the
    x-axis and y-axis data to flip order.

    Equal-axis scaling is not a provided option because of the single-axis
    nature of the panning and zooming control.
    """

    # Ensure the label is a correct type.
    if (label is not None) and not isinstance(label, (str, list, tuple)):
        raise ValueError("label must be None, a string, "
                + "or list or tuple of strings.")

    # Check if this is a full terminal.
    if not is_term():
        sys.stdout.write("Not a proper terminal. Passing to plot.\n")
        plot(x, y, label, rows, cols, False, lg, overlay)
        return
    term_init()

    # Initialize the data sets, canvas, view, and cursor.
    sets = Sets(x, y) # Form x and y into lists of arrays with monotonic x.
    canvas = Canvas(cols, rows, Config.uni, cmap) # Define char sets, get size, alloc.
    lg = "" if lg is None else lg.lower()
    view = View(sets, canvas, # Get limits of valid data and define view edges.
            xlg="x" in lg, ylg="y" in lg)
    cursor = Cursor(sets, canvas, view, label) # Place the cursor at the closest
    # x to the middle of the view's middle column, define the jump size, and
    # initialize the label.

    # Hide the cursor and move the terminal cursor up if this plot is overlaid.
    # The "+ 2" accounts for the border.
    sys.stdout.write(HIDE_CURSOR)
    if overlay and (Canvas.rows_last_plot is not None):
        sys.stdout.write(CSI + str(Canvas.rows_last_plot + 2) + ARROW_UP)
    sys.stdout.flush()
    Canvas.rows_last_plot = canvas.rows

    # States and flags
    dj_sel = 0          # change to j_sel. Not 0 is flag to change j_sel
    zoom_factor = 1.0   # scale factor. Not 1.0 is flag to readjust view x axis
    jump_factor = 0.0   # cursor jump scale factor. Not 0.0 is flag to jump
    rescale = False     # flag to rescale the axis for linear or log
    recenter = False    # flag to center the view on the cursor position
    reclamp = True      # flag to readjust view y axis
    redraw = True       # flag to redraw the data to the canvas
    recursor = True     # flag to update cursor column and data readout
    single = False      # flag to show an single curve
    modified = False    # flag that the data has been modified

    while True:
        # Update canvas size.
        if canvas.check_size():
            canvas.update_size() # Set the integer size and alloc memory.
            cursor.set_jump_size(canvas, view) # Define dx based on columns.

            redraw = True
            recursor = True

        # Rescale the view.
        if rescale:
            view.reset(sets, canvas, cursor) # Redefine with same relative view.
            # |-- view.limit_x
            # |-- view.update_x_edges
            # |-- view.zoom_in_indices (needs updated x edges)
            # |-- view.clamp_y (needs k_lo and k_hi)
            #     |-- view.update_y_edges
            #     |-- view.update_row_zero
            cursor.reset(sets, canvas, view) # Aligns, gets dx, and gets y span.
            # |-- cursor.align (aligns x_cur with closest x value)
            #     |-- canvas.column (aligns x_cur with column center)
            # |-- cursor.set_jump_size
            # |-- cursor.y_span (gets range of y values in cursor column)
            #     |-- canvas.column

            redraw = True
            recursor = True
            rescale = False

        # Cycle the cursor selection.
        if dj_sel != 0:
            cursor.cycle_selection(dj_sel) # Change j_sel and update label.
            # |-- cursor.select_label

            reclamp = True
            recursor = True
            dj_sel = 0

        # Zoom the view.
        if zoom_factor != 1.0:
            view.zoom(zoom_factor, sets, canvas, cursor)
            # |-- view.limit_x
            # |-- view.update_x_edges
            # |-- view.zoom_in_indices
            # |-- view.zoom_out_indices
            cursor.set_jump_size(canvas, view) # Define dx based on columns.

            reclamp = True
            recursor = True
            zoom_factor = 1.0

        # Move the cursor.
        if jump_factor != 0.0:
            recenter = cursor.move(jump_factor, sets, canvas, view)
            # |-- canvas.column

            recursor = True
            jump_factor = 0.0

        # Recenter the view on the cursor.
        if recenter:
            view.center(sets, canvas, cursor)
            # |-- view.limit_x
            # |-- view.update_x_edges
            # |-- view.pan_indices

            reclamp = True
            recursor = True
            recenter = False

        # Readjust the view's y axis.
        if reclamp:
            view.clamp_y(sets, canvas, cursor)
            # |-- view.update_y_edges
            # |-- view.update_row_zero

            redraw = True
            reclamp = False

        # Remap the data to the canvas.
        if redraw:
            canvas.to_chars(sets, view, cursor.j_sel, single)
            canvas.draw_chars(view, cursor.label, cursor.j_label, modified)

            redraw = False

        # Update cursor column and data readout.
        if recursor:
            cursor.y_span(sets, canvas, view)
            # |-- canvas.column
            canvas.draw_cursor(sets, view, cursor)
            # |-- canvas.column

            recursor = False

        # Wait for a new input character.
        char = term_read()

        # Exit on "q", enter (return), backspace, or delete.
        if char == "q":
            break

        # Position
        elif char in ("l", "d"): # slow right
            jump_factor = 1.0
        elif char in ("h", "a"): # slow left
            jump_factor = -1.0
        elif char in ("L", "D"): # fast right
            jump_factor = 10.0
        elif char in ("H", "A"): # fast left
            jump_factor = -10.0
        elif char in ("c", "z"): # center view
            if (view.x_min == view.x_lo) and (view.x_max == view.x_hi):
                x_center = (view.x_max + view.x_min)/2
                jump_factor = (x_center - cursor.x_cur)/cursor.jump_size
            else:
                recenter = True
        elif char == "g": # jump to beginning
            jump_factor = (view.x_min - cursor.x_cur)/cursor.jump_size
        elif char == "G": # jump to ending
            jump_factor = (view.x_max - cursor.x_cur)/cursor.jump_size

        # Zoom
        elif char in ("k", "w"): # slow zoom out
            zoom_factor = 1.4142135623730950488
        elif char in ("j", "s"): # slow zoom in
            zoom_factor = 0.70710678118654752440
        elif char in ("K", "W"): # fast zoom out
            zoom_factor = 4.0
        elif char in ("J", "S"): # fast zoom in
            zoom_factor = 0.25

        # Selection
        elif char == "n": # select next
            dj_sel = 1
        elif char in ("N", "p"): # select previous
            dj_sel = -1
        elif char == "i": # toggle single
            single = not single
            reclamp = True
            recursor = True
            redraw = True
        elif char == "v": # toggle ghost cursor
            if cursor.x_gho is None:
                cursor.x_gho = cursor.x_cur
                cursor.k_gho = cursor.k_cur.copy()
            else:
                cursor.x_gho = None
                cursor.k_gho = None
                if canvas.info_mode == 5: # do not show ghost info
                    canvas.info_mode = 6
            redraw = True # update the info bar
            recursor = True # remove ghost and its metrics

        # Information mode
        elif char == "m": # select next
            if canvas.info_mode in [1, 2]:
                canvas.info_mode = ((canvas.info_mode + 0) % 2) + 1
                redraw = True # update view and label in info bar
                recursor = True # update cursor and metrics in info bar
            elif canvas.info_mode in [3, 4, 5, 6]:
                canvas.info_mode = ((canvas.info_mode - 2) % 4) + 3
                if (cursor.x_gho is None) and (canvas.info_mode == 5):
                    canvas.info_mode = 6
                redraw = True # update view and label in info bar
                recursor = True # update cursor and metrics in info bar
        elif char == "M": # select previous
            if canvas.info_mode in [1, 2]:
                canvas.info_mode = ((canvas.info_mode - 2) % 2) + 1
                redraw = True # update view and label in info bar
                recursor = True # update cursor and metrics in info bar
            elif canvas.info_mode in [3, 4, 5, 6]:
                canvas.info_mode = ((canvas.info_mode - 4) % 4) + 3
                if (cursor.x_gho is None) and (canvas.info_mode == 5):
                    canvas.info_mode = 4
                redraw = True # update view and label in info bar
                recursor = True # update cursor and metrics in info bar

        # Logarithmic scaling
        elif char == "x": # toggle x-axis logarithmic scaling
            view.xlg = not view.xlg
            rescale = True
        elif char == "y": # toggle y-axis logarithmic scaling
            view.ylg = not view.ylg
            rescale = True

        # Functions
        elif char == "f": # perform function on the data
            # Back up the original x and y values.
            if sets.xo is None:
                sets.duplicate()
            # Get the next character.
            char = term_read()
            if char == "d": # derivative
                sets.deriv()
                modified = True
                rescale = True
            elif char == "i": # integral
                sets.integ()
                modified = True
                rescale = True
            elif char == "f": # Fourier transform gain
                sets.dft()
                modified = True
                rescale = True
            elif char == "t": # trim
                char = term_read()
                if char == "l": # trim left
                    sets.trim(-1, cursor)
                    modified = True
                    rescale = True
                elif char == "r": # trim right
                    sets.trim(1, cursor)
                    modified = True
                    rescale = True
            elif char == "u": # unique
                if sets.unique():
                    modified = True
                    rescale = True
            elif char in "0123456789.":
                num_str = char
                while True:
                    char = term_read()
                    if char not in "0123456789":
                        break
                    num_str += char
                try:
                    num = int(num_str)
                    if char == "a": # weighted moving average filter
                        sets.wma(num)
                        modified = True
                        rescale = True
                    elif char == "d": # de-trend
                        sets.detrend(num)
                        modified = True
                        rescale = True
                    elif char == "u": # unique
                        if sets.unique(num):
                            modified = True
                            rescale = True
                except ValueError:
                    pass
        elif char == "F": # restore to original data
            if sets.xo is not None:
                sets.reset()
                modified = False
                rescale = True

    # Restore terminal settings.
    term_close()


class Sets:
    """
    Attributes
    ----------
    x : list of np.ndarrays
        List of arrays of x-axis values.
    y : list of np.ndarrays
        List of arrays of y-axis values.
    xo : list of np.ndarrays
        List of original arrays of x-axis values.
    yo : list of np.ndarrays
        List of original arrays of y-axis values.
    J : int
        Number of data sets (length of x and y).
    """

    def __init__(self, x, y=None): # Sets method
        self.x = x
        self.y = y
        self.xo = None
        self.yo = None
        self.lists() # ensure lists of 1D arrays
        self.J = len(self.x)
        self.reals() # ensure real values
        self.monotonic() # ensure x-axis monotonicity

    def lists(self): # Sets method
        """
        Ensure that x and y are lists of an equal number of np.ndarrays.
        """

        def to_list_of_arrays(x):
            if isinstance(x, np.ndarray): # arrays
                # Ensure real numbers.
                if np.iscomplexobj(x):
                    x = np.real(x)

                # Turn rows of an array into elements in a list.
                if np.ndim(x) == 1: # 1D
                    x_list = [x]
                elif np.ndim(x) == 2: # 2D
                    x_list = [x[j] for j in range(x.shape[0])]
                else: # ND
                    x_list = [x.flatten()]
            elif isinstance(x, (list, tuple)): # list, tuple
                x_list = []
                for j, xj in enumerate(x):
                    # Convert lists and tuples to arrays.
                    if isinstance(xj, (list, tuple)):
                        xj = np.array(xj)

                    # Expand each element of the list to a 1D array.
                    if isinstance(xj, np.ndarray):
                        # Ensure real numbers.
                        if np.iscomplexobj(xj):
                            xj = np.real(xj)

                        # Turn rows of an array into elements in the list.
                        if np.ndim(xj) == 1: # 1D
                            x_list.append(xj)
                        elif np.ndim(xj) == 2: # 2D
                            for m in range(xj.shape[0]):
                                x_list.append(xj[m])
                        else: # ND
                            x_list.append(x.flatten())
                    elif np.ndim(xj) == 0: # scalar
                        x_list.append(np.array([xj]))
                    else:
                        raise ValueError(f"Incompatible type: {type(xj)}")
            elif np.ndim(x) == 0: # scalar
                x_list = [np.array([x])]

            return x_list

        # Ensure x and y are lists of equal number of arrays.
        self.x = to_list_of_arrays(self.x)
        if self.y is None:
            self.y = self.x
            self.x = [np.arange(len(self.y[j])) for j in range(len(self.y))]
        else:
            self.y = to_list_of_arrays(self.y)
            if len(self.x) != len(self.y):
                if (len(self.x) == 1) and (len(self.y) > 1):
                    self.x = [self.x[0] for j in range(len(self.y))]
                elif (len(self.x) > 1) and (len(self.y) ==  1):
                    self.y = [self.y[0] for j in range(len(self.x))]
                else:
                    raise ValueError("x and y must have 1 or "
                            + "the same number of sets.")

        # Ensure sets in x and y are of equal length.
        for j in range(len(self.x)):
            if len(self.x[j]) != len(self.y[j]):
                raise ValueError("Each x and y set must be the same length: "
                        + f"{len(self.x[j])} vs {len(self.y[j])} in set {j}.")

    def reals(self): # Sets method
        """
        Ensure the x and y values are only real-valued arrays. This function
        will replace the original arrays if they are not real-valued.
        """
        for j in range(self.J):
            if np.iscomplexobj(self.x[j]):
                self.x[j] = np.real(self.x[j])
            if np.iscomplexobj(self.y[j]):
                self.y[j] = np.real(self.y[j])

    def monotonic(self): # Sets method
        """
        Ensure the x-axes are all monotonically increasing. This will push all
        negative infinities to the beginning and all positive infinities to the
        end, followed by all NaNs.
        """

        for j in range(self.J):
            # Get the data for this set.
            xj = self.x[j]
            yj = self.y[j]

            # Find the finite x values.
            is_x_fin = np.isfinite(xj)
            kk_fin = (is_x_fin).nonzero()[0]

            # Sort the values by x.
            dx = np.diff(xj[kk_fin])
            if np.all(dx >= 0):
                continue
            elif np.all(dx <= 0):
                xj = np.flip(xj)
                yj = np.flip(yj)
            else:
                mm = np.argsort(xj)
                xj = xj[mm]
                yj = yj[mm]

            # Save the sorted values.
            self.x[j] = xj
            self.y[j] = yj

        return self

    def duplicate(self): # Sets method
        """ Save a copy of the original lists of data arrays. """
        self.xo = [] # original list
        self.yo = [] # original list
        for j in range(self.J):
            self.xo.append(self.x[j].copy())
            self.yo.append(self.y[j].copy())

    def reset(self): # Sets method
        """ Restore the original x and y with the saved copies xo and yo. """
        if self.xo is None:
            return
        self.x = []
        self.y = []
        for j in range(self.J):
            self.x.append(self.xo[j].copy())
            self.y.append(self.yo[j].copy())
        self.xo = None
        self.yo = None

    def deriv(self): # Sets method
        """ Get the derivative of y with respect to x. """
        for j in range(self.J):
            # Filter the data to only finite values.
            is_x_fin = np.isfinite(self.x[j])
            is_y_fin = np.isfinite(self.y[j])
            kk = (is_x_fin & is_y_fin).nonzero()[0]
            xj = self.x[j][kk]
            yj = self.y[j][kk]

            # Get the differentials.
            dx = np.diff(xj)
            dy = np.diff(yj)

            # Replace x with the mid-points.
            self.x[j] = (xj[1:] + xj[:-1])/2

            # Replace y with the derivatives.
            self.y[j] = dy/dx

    def integ(self): # Sets method
        """ Get the integral of y with respect to x. """
        for j in range(self.J):
            # Filter the data to only finite values.
            is_x_fin = np.isfinite(self.x[j])
            is_y_fin = np.isfinite(self.y[j])
            kk = (is_x_fin & is_y_fin).nonzero()[0]
            xj = self.x[j][kk]
            yj = self.y[j][kk]

            # Get the differentials.
            dx = np.diff(xj)
            Y = np.cumsum(dx*(yj[1:] + yj[:-1])/2)

            # Replace x with the mid-points.
            self.x[j] = (xj[1:] + xj[:-1])/2

            # Replace y with the derivatives.
            self.y[j] = Y

    def wma(self, N): # Sets method
        """ Apply a weighted moving average. """
        for j in range(self.J):
            # Find the finite points.
            is_x_fin = np.isfinite(self.x[j])
            is_y_fin = np.isfinite(self.y[j])
            kk_fin = (is_x_fin & is_y_fin).nonzero()[0]

            # Get the data for this set.
            dx = np.diff(self.x[j][kk_fin])
            y = self.y[j][kk_fin]

            # Apply the weighted average N times.
            dx2 = 2*dx[:-1] + 2*dx[1:]
            for _ in range(N):
                y[1:-1] = (y[:-2]*dx[1:] + y[2:]*dx[:-1])/dx2 + y[1:-1]/2

            # Save the filtered values back into the data set.
            self.y[j][kk_fin] = y

    def detrend(self, N):
        """ De-trend the data with a polynomial of degree N. If N is zero, this
        function removes the bias. """
        for j in range(self.J):
            # Filter the data to only finite values.
            is_x_fin = np.isfinite(self.x[j])
            is_y_fin = np.isfinite(self.y[j])
            kk = (is_x_fin & is_y_fin).nonzero()[0]
            xj = self.x[j][kk]
            yj = self.y[j][kk]

            # Normalized x.
            xjn = xj/(xj[-1] - xj[0])

            # Build the H matrix.
            K = len(xjn)
            H = np.zeros((K, N + 1))
            H[:, 0] = np.ones(K)
            for col in range(1, N + 1):
                H[:, col] = xjn**col

            # Find the fitting coefficients.
            k = np.linalg.solve(H.T @ H, H.T) @ yj
            yj -= H @ k

            # Save the data.
            self.y[j][kk] = yj

    def dft(self): # Sets method
        """ Get the discrete Fourier transform. Nonuniformly-sampled data will
        be reinterpolated. """
        for j in range(self.J):
            # Filter the data to only finite values.
            kk = (np.isfinite(self.x[j]) & np.isfinite(self.y[j])).nonzero()[0]
            xj = self.x[j][kk]
            yj = self.y[j][kk]

            # Get the median time step.
            dx = np.diff(xj)
            T = np.median(dx)

            # Reinterpolate the data.
            if dx.max() - dx.min() > EPS:
                K = round((xj[-1] - xj[0])/T) + 1
                xx = np.arange(K)*T + xj[0]
                yj = np.interp(xx, xj, yj)

            # Get the scaled Fourier transform of y.
            Y = np.fft.fft(yj)/K

            # Crop the Fourier transform to the first half of the data (below
            # the Nyquist limit) and finish the scaling. The DC component should
            # not be doubled.
            K_h = K//2 + 1
            Y = Y[:K_h]*2
            Y[0] /= 2
            self.y[j] = np.abs(Y)

            # Build the frequency array.
            self.x[j] = np.arange(K_h)/((K-1)*T)

    def trim(self, lr, cursor): # Sets method
        """ Trim the data in each set left or right of the cursor. """
        if lr < 0: # trim left
            for j in range(self.J):
                k_cur = cursor.k_cur[j]
                self.x[j] = self.x[j][k_cur:]
                self.y[j] = self.y[j][k_cur:]
                if (cursor.k_gho is not None) \
                        and (cursor.k_gho[j] < cursor.k_cur[j]):
                    cursor.k_gho[j] = 0
                cursor.k_cur[j] = 0
        else: # trim right
            for j in range(self.J):
                k_cur = cursor.k_cur[j]
                self.x[j] = self.x[j][:k_cur+1]
                self.y[j] = self.y[j][:k_cur+1]
                if (cursor.k_gho is not None) \
                        and (cursor.k_gho[j] > cursor.k_cur[j]):
                    cursor.k_gho[j] = cursor.k_cur[j]

    def unique(self, dec=9): # Sets method
        """ Hide all but the unique points in each data set. The input dec is
        the number of decimal places to consider. """

        # Early escape if there is only one data set.
        if self.J == 1:
            return False

        # Find the common points.
        p_common = np.round(self.x[0] + 1j * self.y[0], dec)
        for j in range(1, self.J):
            p_j = np.round(self.x[j] + 1j * self.y[j], dec)
            p_common = np.intersect1d(p_common, p_j)

        # Early escape if there are no common values.
        if len(p_common) == 0:
            return False

        # Set all common points to nans.
        for j in range(self.J):
            p_j = np.round(self.x[j] + 1j * self.y[j], dec)
            kk = np.where(np.isin(p_j, p_common))
            self.y[j][kk] = np.nan

        return True

class Canvas:
    """
    Attributes
    ----------
    term_cols : int or None
        Columns of available space.
    term_rows : int or None
        Rows of available space.
    cols_target : int or float
        Target number of columns or fraction of width of window.
    rows_target : int or float
        Target number of rows or fraction of height of window.
    cols : int
        Resolved integer number of columns.
    rows : int
        Resolved integer number of rows.
    rows_last : int or None
        The number of rows during last draw.
    subcols : int
        Number of sub-columns.
    subrows : int
        Number of sub-rows.

    chars : (rows, cols) np.ndarray
        Matrix of characters to draw.
    dots : (Rows, Cols) np.ndarray
        Expanded matrix of dots. Though this is used in only one function, it is
        saved in order to reduce the number of times memory needs to be
        allocated.
    colors : (rows, cols) np.ndarray
        Matrix of foreground colors.
    chars_last : (rows, cols) np.ndarray
        Matrix of characters drawn last time.
    colors_last : (rows, cols) np.ndarray
        Matrix of foreground colors used last time.
    deltas : (rows, cols) np.ndarray
        Matrix of changed character cells.
    col_cur_last : int
        Last cursor column position.
    col_gho_last : int
        Last ghost cursor column position.

    uni : bool
        Flag to use Unicode or ASCII characters.
    border : dict
        Dictionary of border character values.
    blank : str
        Glyph for blank characters.
    darks : list, default {Config.darks}
        List of dark color values.
    lites : list, default {Config.lites}
        List of light color values.
    frgnd : str, default {Config.frgnd}
        Beginning of foreground color setting command string.
    gray : str, default {Config.gray}
        Foreground gray color value.

    info_mode : int
        Mode of the information display.
    view_space_min : int
        Minimum number of characters available for the view string.
    cursor_space_min : int
        Minimum number of characters available for the cursor string.
    metrics_space_min : int
        Minimum number of characters available for the metrics string.
    label_space_min : int
        Minimum number of characters available for the label string.
    view_space : int
        Calculated number of characters available for the view string.
    cursor_space : int
        Calculated number of characters available for the cursor string.
    metrics_space : int
        Calculated number of characters available for the metrics string.
    label_space : int
        Calculated number of characters available for the label string.

    Notes
    -----
    The chars matrix stores the grid of characters that should be drawn to the
    terminal inside the box outline. This grid with its colors is called the
    canvas.

    The dots matrix is an expanded grid where each sub-character point is a
    separate cell. So, with Braille characters when Unicode is used, each
    character expands to 8 cells, two across and four down. The data sets are
    mapped to this dots matrix which is then collapsed to the chars matrix:

                 .-----.    So that even single points will be plotted at the
        * *      | * * |    edges, indexing aligns 0 with the first sub-column
        * *   >  | * * |    and (Cols - 1) with the last sub-column:
        * *   >  | * * |
        * *      | * * |       |* *|* *|* *|* *|* *|    Cols = cols * subcols
                 '-----'        0 1 2 3 4 5 6 7 8 9     Cols = 10
        eight      one
        dots    character   This means the left-most sub-index is -0.5.

    The data sets are painted to the colors matrix, which stores a single
    integer for each character. That integer is a color index shifted by one.
    The shift is used so that a value of zero can represent no color.

    The deltas matrix serves to indicate which cells in the terminal grid need
    to be redrawn. This includes characters which have changed glyph or
    non-blank characters which have changed color. This requires that we keep
    track of the previous matrices of characters and colors. The delta will then
    be True wherever the last and current chars matrices do not match or
    wherever the last and current colors matrices do not match and the current
    chars matrix is non-blank. Where the current chars matrix is blank but the
    last was not, the deltas matrix will already have a True value. Where the
    both the current and last chars matrices are blank, it does not matter that
    the color might have changed.

    When the cursor is being redrawn, only the previous and current column
    numbers of the cursor are needed. The cursor is cleared and redrawn
    completely, without regard to deltas, because every cell will be altered.
    Every time the canvas is redrawn, the cursor is too. So, as long as the
    canvas keeps track of what needs to be done to clean up the cursor's last
    location, everything should be good and the deltas matrix does not need to
    be aware of the cursor.

    Because only the canvas drawing needs to be aware of the deltas, the deltas
    matrix does not need to be part of the Canvas class. It could be a temporary
    variable; however, making it part of the Canvas class can help reduce
    computational delay because the memory only needs to be allocated once.

    The last chars and colors matrices start as None. When the terminal window
    is resized and the whole canvas needs to be redrawn, these two matrices
    should be reset to None. Whenever they are None, the deltas matrix is set to
    all True. When the deltas matrix is done being updated the last matrices are
    set equal to the current.

    The info_mode can have one of 7 possible values:
        0: view - cursor - metrics - label
        1: view - cursor
        2: metrics - label
        3: view
        4: cursor
        5: metrics (skip if no ghost)
        6: label
        7: view - label
    When there is no cursor ghost, the space taken by metrics is distributed
    among the other display items. The following is the control-flow diagram:

        .---.                                                   .---.
        | 0 |<------------.             more space              | 7 |
        '---'             |                                     '---'
         | ^              |
         v |              |
        .---.           .---.
        | 1 |<--------->| 2 |
        '---'<----.     '---'<----.
         | ^      |      | ^      |
         v |      |      v |      |
        .---.   .---.   .---.   .---.
        | 3 |<->| 4 |<->| 5 |<->| 6 |   less space
        '---'   '---'   '---'   '---'

    The vertical transitions happen when the width of the plotting area changes.
    The horizontal transitions happen when the user cycles the info mode. Mode 7
    is used for the plot function.
    """

    # Memory of the rows of the last plot for the overlay option.
    rows_last_plot = None

    def __init__(self, cols, rows, uni, cmap=None, mode=0): # Canvas method
        """
        Initialize the canvas.

        Parameters
        ----------
        cols : int or float
            Target number of columns or fraction of the terminal window to use
            as the number of columns.
        rows : int or float
            Target number of rows or fraction of the terminal window to use as
            the number of rows.
        uni : bool, default True
            Flag specifying whether to use Unicode instead of ASCII characters.
        cmap : str, default None
            Name of the color map.
        mode : int, default 0
            Initial info_mode.
        """

        self.term_cols = None
        self.term_rows = None
        self.cols_target = cols
        self.rows_target = rows
        self.cols = None
        self.rows = None
        self.rows_last = None
        self.subcols = None
        self.subrows = None

        self.chars = None
        self.dots = None
        self.colors = None
        self.chars_last = None
        self.colors_last = None
        self.deltas = None
        self.col_cur_last = None
        self.col_gho_last = None

        self.uni = uni
        self.border = None
        self.blank = None
        self.darks = Config.darks.copy()
        self.lites = Config.lites.copy()
        self.frgnd = Config.frgnd
        self.gray = Config.gray

        self.info_mode = mode
        self.view_space_min = 45
        self.cursor_space_min = 45
        self.metrics_space_min = 60
        self.label_space_min = 30
        self.view_space = 0
        self.cursor_space = 0
        self.metrics_space = 0
        self.label_space = 0

        # Define the character set.
        self.char_set()

        # Update canvas size and allocate memory.
        self.check_size()
        self.update_size()

        # Define the color maps.
        if (cmap is not None) and (cmap != Config.cmap):
            self.darks, self.lites, self.frgnd, self.gray, _ \
                    = set_color_maps(cmap)

    def char_set(self): # Canvas method
        """
        Define the number of sub-columns, sub-rows, and the border and blank
        character values based on whether we want to use Unicode or ASCII
        characters. The light box drawing characters seem to be more commonly
        supported by font families than the heavy box drawing characters.
        """

        if self.uni:
            self.subcols = 2
            self.subrows = 4
            self.border = {
                    "tl": 0x250C, "tr": 0x2510, # top left and right
                    "h":  0x2500, "v":  0x2502, # horizontal and vertical
                    "vl": 0x251C, "vr": 0x2524, # vertical, left and right
                    "bl": 0x2514, "br": 0x2518} # bottom left and right
            self.blank = 0x2800
        else:
            self.subcols = 1
            self.subrows = 3
            self.border = {
                    "tl": 0x2E, "tr": 0x2E,     # top left and right
                    "h":  0x2D, "v":  0x7C,     # horizontal and vertical
                    "vl": 0x2B, "vr": 0x2B,     # vertical, left and right
                    "bl": 0x27, "br": 0x27}     # bottom left and right
            self.blank = 0x20

    def check_size(self): # Canvas method
        """ Check the size of the terminal window and return True if it has
        changed. """

        # Get the terminal size.
        term_cols, term_rows = term_size()
        term_rows -= 1 # Account for the prompt line.

        if (self.term_cols is None) or (self.term_cols != term_cols) \
                or (self.term_rows is None) or (self.term_rows != term_rows):
            self.term_cols = term_cols
            self.term_rows = term_rows
            return True

        return False

    def update_size(self): # Canvas method
        """
        Update the number of rows and columns of the canvas and allocate memory
        for the canvas matrices. The dimensions specify the region within the
        bounding box.
        """

        # Ignore non-positive dimensions.
        if self.cols_target <= 0:
            self.cols_target = 1
        if self.rows_target <= 0:
            self.rows_target = 1

        # Convert a fractional canvas size to columns and rows.
        if self.cols_target <= 1:
            self.cols = max(int(self.term_cols * self.cols_target), 3)
        else:
            self.cols = max(min(int(self.cols_target), self.term_cols), 3)
        if self.rows_target <= 1:
            self.rows = max(int(self.term_rows * self.rows_target), 3)
        else:
            self.rows = max(min(int(self.rows_target), self.term_rows), 3)

        # Adjust for the bounding box.
        self.cols -= 2
        self.rows -= 2

        # Get the dot dimensions.
        Cols = self.subcols * self.cols
        Rows = self.subrows * self.rows

        # Allocate memory for the canvas matrices.
        self.chars = np.full((self.rows, self.cols), self.blank, dtype=int)
        self.dots = np.zeros((Rows, Cols), dtype=bool)
        self.colors = np.zeros((self.rows, self.cols), dtype=int)
        self.deltas = np.zeros((self.rows, self.cols), dtype=bool)
        self.chars_last = None # needed to trigger a full redraw
        self.colors_last = None # needed to trigger a full redraw
        # The last chars and colors matrices are allocated within the
        # character-drawing function.

        # Define which tier of the information modes to use.
        space_left_side = self.view_space_min + self.cursor_space_min
        space_right_side = self.metrics_space_min + self.label_space_min
        if self.cols >= (space_left_side + space_right_side):
            tier = 0
        elif self.cols >= max(space_left_side, space_right_side):
            tier = 1
        else:
            tier = 2

        # Transition the information mode.
        transitions = [
                [0, 0, 0, 0, 0, 0, 0, 7],
                [1, 1, 2, 1, 1, 2, 2, 7],
                [3, 3, 5, 3, 4, 5, 6, 7]]
        self.info_mode = transitions[tier][self.info_mode]

        # Get the information spaces.
        if self.info_mode == 0:
            total_space_min = self.view_space_min + self.cursor_space_min \
                    + self.metrics_space_min + self.label_space_min
            self.view_space = round(self.view_space_min
                    * self.cols/total_space_min)
            self.cursor_space = round(self.cursor_space_min
                    * self.cols/total_space_min)
            self.metrics_space = round(self.metrics_space_min
                    * self.cols/total_space_min)
            self.label_space = self.cols - self.view_space \
                    - self.cursor_space - self.metrics_space
        elif self.info_mode in [1, 2]:
            total_space_min = max(self.view_space_min + self.cursor_space_min,
                    self.metrics_space_min + self.label_space_min)
            self.view_space = round(self.view_space_min
                    * self.cols/total_space_min)
            self.cursor_space = self.cols - self.view_space
            self.metrics_space = round(self.metrics_space_min
                    * self.cols/total_space_min)
            self.label_space = self.cols - self.metrics_space
        elif self.info_mode in [3, 4, 5, 6]:
            self.view_space = self.cols
            self.cursor_space = self.cols
            self.metrics_space = self.cols
            self.label_space = self.cols
        else:
            total_space_min = self.view_space_min + self.label_space_min
            self.view_space = round(self.view_space_min
                    * self.cols/total_space_min)
            self.label_space = self.cols - self.view_space

    def column(self, view, x): # Canvas method
        """
        Given an x-axis input value, get the corresponding column in the canvas.

        Parameters
        ----------
        view : View
            Object holding the current x and y view limits as well as the x and
            y-axis logarithmic scaling flags and the view's x-axis limit
            indices.
        x : float or array-like
            Value or array of values along the x-axis.

        Returns
        -------
        col : int or np.ndarray
            Value or array of values of column indices closest to the input x
            values.
        xc : float or np.ndarray
            Value or array of values along the x-axis aligned with the centers
            of character columns closest to the input x values.

        Notes
        -----
        The first and last points in view are centered on the first and last
        dots. So, the left most edge of the text columns has a negative 0.5
        sub-column index value (when using Braille) and a negative 0.25 column
        index value. Using Braille in Unicode mode, the center of the first
        character column is after the x_lo value and the last character column
        is before the x_hi value.
        """

        # Get the x-axis span of the view.
        x_span = view.x_hi - view.x_lo # (linear or log scale)

        # Get the total number of sub-columns of the current canvas.
        Cols = self.cols * self.subcols

        # Find the character columns (not sub-columns) in which the input x
        # values are found.
        Col = np.round((Cols - 1)*(x - view.x_lo)/x_span)
        col = np.floor(Col/self.subcols).astype(int)

        # Get the x-axis values of the centers of the character columns
        # corresponding to the input x values.
        shift = (self.subcols - 1)/(2*self.subcols)
        width = self.cols - 1 + 2*shift
        xc = x_span*(col + shift)/width + view.x_lo
        xc = np.clip(xc, view.x_min, view.x_max)

        return col, xc

    def to_chars(self, sets, view, j_sel=0, single=False): # Canvas method
        """
        Parameters
        ----------
        sets : Sets
            Object holding the lists of x and y data.
        view : View
            Object holding the current x and y view limits as well as the x and
            y-axis logarithmic scaling flags and the view's x-axis limit
            indices.
        j_sel : Cursor
            Object holding the cursor's x value, jump size and limit, array of x
            indices, and index of currently-selected data set.
        single : bool, default False
            Flag to show only an single data set.
        """

        # Get the view's span (linear or log scale).
        x_span = view.x_hi - view.x_lo
        y_span = view.y_hi - view.y_lo

        # Get total numbers of subrows and subcolumns.
        Cols = self.subcols * self.cols
        Rows = self.subrows * self.rows

        # Initialize the dots and colors matrices. These must be cleared because
        # only select points are set. The chars matrix is fully redefined.
        self.dots[:, :] = False
        self.colors[:, :] = 0 # no color

        # Define the list of data sets over which to iterate.
        if not single or (j_sel == 0):
            if j_sel == 0:
                jj = np.arange(sets.J)
            else:
                jj = np.array([j for j in range(sets.J) if j != j_sel - 1])
                jj = np.append(jj, j_sel - 1)
        else:
            jj = np.array([j_sel-1])

        # For each curve, set the points and colors.
        for j in jj:
            # Get the view limits.
            k_lo = view.k_lo[j]
            k_hi = view.k_hi[j]

            # Get the data within view.
            xj = sets.x[j][k_lo:k_hi+1]
            yj = sets.y[j][k_lo:k_hi+1]

            # Find all valid points in view.
            is_x_fin = np.isfinite(xj) if not view.xlg \
                    else np.isfinite(xj) & (xj > 0)
            is_y_fin = np.isfinite(yj) if not view.ylg \
                    else np.isfinite(yj) & (yj > 0)
            mm_fin = (is_x_fin & is_y_fin).nonzero()[0]
            # EPS added because of tolerance problems resulting in none valid.
            is_x_in = (xj[mm_fin] >= view.x_lo_lin - EPS) \
                    & (xj[mm_fin] <= view.x_hi_lin + EPS)
            is_y_in = (yj[mm_fin] >= view.y_lo_lin - EPS) \
                    & (yj[mm_fin] <= view.y_hi_lin + EPS)
            nn_in = (is_x_in & is_y_in).nonzero()[0]
            mm_valid = mm_fin[nn_in]

            # Skip if no valid points were found.
            if len(mm_valid) == 0:
                continue

            # Get the coordinates of the dots to set to True. First dot is 0;
            # last dot is Cols - 1. Whole-value subcolumns refer to the middle
            # of the subcolumn. So, the edge of the subcolumns is -0.5.
            xj = xj[mm_valid] if not view.xlg else np.log10(xj[mm_valid])
            yj = yj[mm_valid] if not view.ylg else np.log10(yj[mm_valid])
            if x_span > 0:
                C = (Cols - 1)*(xj - view.x_lo)/x_span
            else:
                C = 0.5*(Cols - 1)
            if y_span > 0:
                R = (Rows - 1)*(view.y_hi - yj)/y_span
            else:
                R = 0.5*(Rows - 1)
            C = np.clip(np.round(C).astype(int), 0, Cols - 1)
            R = np.clip(np.round(R).astype(int), 0, Rows - 1)

            # Map locations to the expanded canvas.
            self.dots[R, C] = True

            # Store the color indices. A more complex method of selecting the
            # color of the data set which occupies more of a character actually
            # results in some undesirable visual artifacts, such as z-fighting
            # between data sets.
            if sets.J > 1:
                c = C//self.subcols
                r = R//self.subrows
                self.colors[r, c] = j + 1

        # Convert the matrix of ones and zeros to character values.
        if self.uni: # Braille
            self.chars[:, :] = (0x2800
                    +    self.dots[0::4, ::2] +   8*self.dots[0::4, 1::2]
                    +  2*self.dots[1::4, ::2] +  16*self.dots[1::4, 1::2]
                    +  4*self.dots[2::4, ::2] +  32*self.dots[2::4, 1::2]
                    + 64*self.dots[3::4, ::2] + 128*self.dots[3::4, 1::2])
        else:
            asci = np.array([0x20, 0x60, 0x2D, 0x27, 0x2E, 0x21, 0x3A, 0x7C])
            self.chars[:, :] = asci[
                    self.dots[::3] + 2*self.dots[1::3] + 4*self.dots[2::3]]

    def draw_chars(self, view, label=None, j_label=0,
            modified=False, use_esc=True): # Canvas method
        """
        Render the canvas to the terminal, including the view or label strings
        and not including the cursor, ghost cursor, or associated strings.

        Parameters
        ----------
        view : View, default None
            Object holding the x and y min and max values of the view.
        label : str, default None
            String label.
        j_label : int, default 0
            Color index for the label.
        modified : bool, default False
            Flag that the current data sets have been modified from their
            original values. This is used to affect the color of the sides of
            the canvas box in order to signal to the user that the plotted data
            is modified.
        use_esc : bool, default True
            Flag to use ANSI escape sequences. This only matters when the plot
            function also uses the this function in a limited terminal.
        """

        # Move the terminal cursor up to the top of the border. The rest
        # position of the terminal cursor is the beginning of the line right
        # below the outline box. So, moving to the top of the box does not
        # require a leftward move. Using the rows_last variable, this operation
        # is able to handle the transition in terminal screen sizes correctly.
        if use_esc:
            draw_str = RESET
            if self.rows_last is not None:
                draw_str += CSI + str(self.rows_last + 2) + ARROW_UP
            self.rows_last = self.rows
        else:
            draw_str = ""

        # Draw the top border, which can be a zoom indicator.
        draw_str += chr(self.border["tl"])
        if ((view.x_lo > view.x_min) or (view.x_hi < view.x_max)) and use_esc:
            # Get the bar's first and last column numbers.
            x_full_span = view.x_max - view.x_min # width of data
            col_a = round(self.cols*(view.x_lo - view.x_min)/x_full_span)
            col_b = round(self.cols*(view.x_hi - view.x_min)/x_full_span)

            # Limit the column values.
            col_a = max(0, col_a)
            col_b = min(self.cols - 1, col_b)
            col_a = min(col_b, col_a)

            # Add the segment before the view region.
            if col_a > 0:
                draw_str += self.frgnd + str(self.gray) + "m"
                draw_str += chr(self.border["h"]) * col_a
                draw_str += RESET

            # Add the view region.
            draw_str += chr(self.border["h"]) * (col_b - col_a + 1)

            # Add the segment after the view region.
            if col_b < self.cols - 1:
                draw_str += self.frgnd + str(self.gray) + "m"
                draw_str += chr(self.border["h"]) * (self.cols - 1 - col_b)
                draw_str += RESET
        else:
            draw_str += chr(self.border["h"]) * self.cols
        draw_str += chr(self.border["tr"])
        sys.stdout.write(draw_str + "\n")

        # Define where to redraw, and update the last chars and colors matrices.
        if (self.chars_last is None) or (self.colors_last is None) \
                or not use_esc:
            self.deltas[:, :] = True
            self.chars_last = self.chars.copy()
            self.colors_last = self.colors.copy()
        else:
            self.deltas[:, :] = (self.chars != self.chars_last) \
                    | ((self.colors != self.colors_last) \
                    & (self.chars != self.blank))
            self.chars_last[:, :] = self.chars
            self.colors_last[:, :] = self.colors

        # Define the formatting for the modified state of the data.
        if modified and use_esc:
            mod_pre = self.frgnd + str(self.gray) + "m"
        else:
            mod_pre = ""
        mod_post = RESET if modified and use_esc else ""

        # Draw each row of the canvas.
        for row in range(self.rows):
            # Initialize the row string with the left border.
            draw_str = mod_pre
            draw_str += chr(self.border["vl"]) if row == view.row_zero \
                    else chr(self.border["v"])
            draw_str += mod_post
            draw_str += BOLD if use_esc and Config.bold else ""
            col_last = -1 # column of the last write
            last_color = 0 # the last foreground color

            # Draw this row.
            for col in range(self.cols):
                # Skip where there is no delta.
                if not self.deltas[row, col]:
                    continue

                # Jump to the new character location.
                if col > col_last + 1:
                    draw_str += CSI + str(col - col_last - 1) + ARROW_RT
                col_last = col

                # Get this color and character.
                this_char = self.chars[row, col]
                this_color = self.colors[row, col]

                # Switch to the current color for non-blank characters.
                if (this_color != last_color) and (this_char != self.blank) \
                        and use_esc:
                    color_idx = (this_color - 1) % len(self.darks)
                    color_value = self.darks[color_idx]
                    draw_str += self.frgnd + str(color_value) + "m"
                    last_color = this_color

                # Add the canvas character.
                draw_str += chr(this_char)

            # Jump to the last character location.
            margin = (self.cols - 1) - col_last
            if margin > 0:
                if use_esc:
                    draw_str += CSI + str(margin) + ARROW_RT
                else:
                    draw_str += " " * margin

            # End the row string with a format reset and the right border. Bold
            # box drawing characters tend to gain some separation and not
            # produce a continuous line. This is why the format must be reset
            # before drawing the border.
            draw_str += RESET if use_esc else ""
            draw_str += mod_pre
            draw_str += chr(self.border["vr"]) if row == view.row_zero \
                    else chr(self.border["v"])
            draw_str += mod_post
            sys.stdout.write(draw_str + "\n")

        # Reinitialize the draw string.
        draw_str = chr(self.border["bl"])

        # Build the view string.
        if self.info_mode in [0, 1, 3, 7]:
            # Initialize the view string and length.
            view_str = ""
            view_len = 0

            # Build and append the x string.
            x_lo_lin = view.x_lo if not view.xlg else 10**view.x_lo
            x_hi_lin = view.x_hi if not view.xlg else 10**view.x_hi
            x_str = "X:" + ftostr(x_lo_lin) + "," + ftostr(x_hi_lin)
            if len(x_str) + 2 <= self.view_space:
                view_len += len(x_str) + 2
                if view.xlg and use_esc:
                    x_str = self.frgnd + str(self.gray) + "m" \
                            + x_str + RESET
                view_str += " " + x_str + " "

            # Build and append the y string.
            y_lo_lin = view.y_lo if not view.ylg else 10**view.y_lo
            y_hi_lin = view.y_hi if not view.ylg else 10**view.y_hi
            y_str = "Y:" + ftostr(y_lo_lin) + "," + ftostr(y_hi_lin)
            if view_len + len(y_str) + 1 <= self.view_space:
                view_len += len(y_str) + 1
                if view.ylg and use_esc:
                    y_str = self.frgnd + str(self.gray) + "m" \
                            + y_str + RESET
                view_str += y_str + " "

            # Append filler.
            if view_len < self.view_space:
                gap = self.view_space - view_len
                view_str = view_str + chr(self.border["h"]) * gap

            # Append to the draw string.
            draw_str += view_str

        # Build the cursor and metrics filler strings.
        if self.info_mode in [0, 1, 4]:
            draw_str += chr(self.border["h"]) * self.cursor_space
        if self.info_mode in [0, 2, 5]:
            draw_str += chr(self.border["h"]) * self.metrics_space

        # Build the label string.
        if self.info_mode in [0, 2, 6, 7]:
            if label is not None:
                # Initialize the label string and length.
                label_str = ""
                label_len = 0

                # Append the label.
                label_len = min(len(label) + 2, self.label_space)
                label_str = label[:label_len - 2]
                if (j_label != 0) and use_esc:
                    color_idx = (j_label - 1) % len(self.lites)
                    color_value = self.lites[color_idx]
                    label_str = self.frgnd + str(color_value) + "m" \
                            + label_str + RESET
                label_str = " " + label_str + " "

                # Prepend filler.
                if label_len < self.label_space:
                    gap = self.label_space - label_len
                    label_str = chr(self.border["h"]) * gap + label_str

                # Append to the draw string.
                draw_str += label_str
            else:
                # Apply filler.
                draw_str += chr(self.border["h"]) * self.label_space

        # Finish the draw string.
        draw_str += chr(self.border["br"])

        # Write the string and flush the buffer.
        sys.stdout.write(draw_str + "\n")
        sys.stdout.flush()

    def draw_cursor(self, sets, view, cursor): # Canvas method
        """
        This function only erases the cursor (and ghost cursor) form its old
        position and redraws the cursor (and ghost cursor) at its new position.
        It does not redraw the entire canvas.

        Parameters
        ----------
        sets : Sets
            Object holding the lists of x and y data.
        view : View, default None
            Object holding the x and y min and max values of the view.
        cursor : Cursor
            Object holding the cursor's x value, jump size and limit, array of x
            indices, and index of currently-selected data set.
        """

        def add_column(canvas, col, col_last, show_cursor=True, dark_bar=False):
            # Skip if the column is out of bounds.
            if (col < 0) or (col >= canvas.cols):
                return "", col_last

            # Initialize.
            draw_str = RESET
            if dark_bar:
                draw_str += self.frgnd + str(self.gray) + "m"
            last_char = canvas.blank # the last character.
            last_color = 0 # the last foreground color

            # Move to the top of the column.
            draw_str += CSI + str(canvas.rows) + ARROW_UP
            if col > col_last:
                draw_str += CSI + str(col - col_last) + ARROW_RT
            elif col < col_last:
                draw_str += CSI + str(col_last - col) + ARROW_LT

            # Draw the column.
            for row in range(canvas.rows):
                # Get this character and color.
                this_char = canvas.chars[row, col]
                this_color = canvas.colors[row, col] \
                        if (this_char != canvas.blank) \
                        else cursor.j_sel

                # Reset the format.
                if (this_char == canvas.blank) \
                        and (last_char != canvas.blank): # falling edge
                    draw_str += RESET # Remove bold format.
                    last_color = 0 # Track the color reset.
                    if dark_bar:
                        draw_str += self.frgnd + str(self.gray) + "m"
                elif (this_char != canvas.blank) \
                        and (last_char == canvas.blank): # rising edge
                    draw_str += BOLD if Config.bold else "" # Make bold.
                    last_color = 0 # Track the color reset.

                # Switch to the current color.
                if this_color != last_color:
                    color_idx = (this_color - 1) % len(self.darks)
                    if dark_bar or not show_cursor:
                        color_value = self.darks[color_idx]
                    else:
                        color_value = self.lites[color_idx]
                    draw_str += self.frgnd + str(color_value) + "m"

                # Add the canvas character.
                if (this_char != canvas.blank) or not show_cursor:
                    draw_str += chr(this_char)
                else:
                    draw_str += chr(canvas.border["v"])

                # Move left and down.
                draw_str += CSI + ARROW_LT + CSI + ARROW_DN

                # Update the last values.
                last_char = this_char
                last_color = this_color

            return draw_str, col

        # -----------------------------------------------
        # Erase the old ghost and current cursor columns.
        # -----------------------------------------------

        # Get the current and last cursor columns.
        col_cur, _ = self.column(view, cursor.x_cur)
        col_cur_last = self.col_cur_last
        if cursor.x_gho is not None:
            col_gho, _ = self.column(view, cursor.x_gho)
        else:
            col_gho = None
        col_gho_last = self.col_gho_last

        # Initialize the draw string.
        draw_str = CSI + ARROW_UP # Move up to the info bar.
        col_last = -1

        # Erase the last ghost cursor, if there was one and it is not the same
        # as the current ghost cursor.
        if col_gho_last is not None:
            if ((col_gho is not None) and (col_gho_last != col_gho)) \
                    or col_gho is None:
                col_str, col_last = add_column(self, col_gho_last, col_last,
                        show_cursor=False, dark_bar=False)
                draw_str += col_str

        # Erase the last cursor, if there was one and it is not the same as the
        # current cursor.
        if (col_cur_last is not None) and (col_cur_last != col_cur):
            col_str, col_last = add_column(self, col_cur_last, col_last,
                    show_cursor=False, dark_bar=False)
            draw_str += col_str

        # ----------------------------------------------
        # Draw the new ghost and current cursor columns.
        # ----------------------------------------------

        # Draw ghost cursor, if there is one.
        if cursor.x_gho is not None:
            col_str, col_last = add_column(self, col_gho, col_last,
                    show_cursor=True, dark_bar=True)
            draw_str += col_str

        # Draw the current cursor.
        col_str, col_last = add_column(self, col_cur, col_last,
                show_cursor=True, dark_bar=False)
        draw_str += col_str

        # Save the last positions.
        self.col_cur_last = col_cur
        self.col_gho_last = col_gho

        # Reset format and move to the beginning of the info bar.
        draw_str += RESET
        if col_last > 0:
            draw_str += CSI + str(col_last) + ARROW_LT
        col_last = 0

        # ------------------
        # Draw the info bar.
        # ------------------

        # Build the view skip string.
        if self.info_mode in [0, 1, 3]:
            draw_str += CSI + str(self.view_space) + ARROW_RT

        # Build the cursor string.
        if self.info_mode in [0, 1, 4]:
            # Initialize the cursor string.
            cursor_str = ""

            # If only one data set is selected, append the x index.
            n_str = ""
            if cursor.j_sel != 0:
                n_str += f" n:{cursor.k_cur[cursor.j_sel-1]}"
            elif cursor.J == 1:
                n_str += f" n:{cursor.k_cur[0]}"
            if len(cursor_str) + len(n_str) + 1 <= self.cursor_space:
                cursor_str += n_str + " "

            # Append the cursor x coordinate.
            vxl = view.x_lo if not view.xlg else 10**view.x_lo
            vxh = view.x_hi if not view.xlg else 10**view.x_hi
            x = cursor.x_cur if not view.xlg else 10**cursor.x_cur
            x_str = "x:" + ftostr(x, sigfigs(x, vxh - vxl))
            if len(cursor_str) + len(x_str) + 1 <= self.cursor_space:
                cursor_str += x_str + " "

            # Append the cursor y coordinate or range.
            vyl = view.y_lo if not view.ylg else 10**view.y_lo
            vyh = view.y_hi if not view.ylg else 10**view.y_hi
            yl = cursor.y_min if not view.ylg else 10**cursor.y_min
            yh = cursor.y_max if not view.ylg else 10**cursor.y_max
            y_str = "y:" + ftostr(yl, sigfigs(yl, vyh - vyl))
            if (not np.isnan(yl)) and (yl != yh):
                y_str += "," + ftostr(yh, sigfigs(yh, vyh - vyl))
            if len(cursor_str) + len(y_str) + 1 <= self.cursor_space:
                cursor_str += y_str + " "

            # Wrap the cursor string in color.
            cursor_len = len(cursor_str)
            if cursor.j_sel > 0:
                color_idx = (cursor.j_sel - 1) % len(self.lites)
                color_value = self.lites[color_idx]
                cursor_str = self.frgnd + str(color_value) + "m" \
                        + cursor_str + RESET

            # Append filler.
            if cursor_len < self.cursor_space:
                gap = self.cursor_space - cursor_len
                cursor_str += chr(self.border["h"]) * gap

            # Append the cursor string to the info bar.
            draw_str += cursor_str

        # Build the metrics string.
        if (self.info_mode in [0, 2, 5]) and (cursor.x_gho is not None):
            # Initialize the metrics string.
            metrics_str = ""

            # If many data sets are selected,
            if (cursor.j_sel == 0) and (cursor.J > 1):
                # Append the change in x.
                dx = cursor.x_cur - cursor.x_gho
                dx_str = "\u03B4x:" + ftostr(dx, sigfigs(dx, dx))
                if len(metrics_str) + len(dx_str) + 2 <= self.metrics_space:
                    metrics_str += " " + dx_str + " "
            else: # or just one data set is selected,
                # Append the change in indices.
                k_cur = cursor.k_cur[cursor.j_sel - 1]
                k_gho = cursor.k_gho[cursor.j_sel - 1]
                dn_str = "\u03B4n:" + str(k_cur - k_gho)
                if len(metrics_str) + len(dn_str) + 2 <= self.metrics_space:
                    metrics_str += " " + dn_str + " "

                # Append the change in x.
                dx = cursor.x_cur - cursor.x_gho
                dx_str = "\u03B4x:" + ftostr(dx, sigfigs(dx, dx))
                if len(metrics_str) + len(dx_str) + 1 <= self.metrics_space:
                    metrics_str += dx_str + " "

                # Append the change in y.
                yj = sets.y[cursor.j_sel - 1]
                dy = yj[k_cur] - yj[k_gho]
                dy_str = "\u03B4y:" + ftostr(dy, sigfigs(dy, dy))
                if len(metrics_str) + len(dy_str) + 1 <= self.metrics_space:
                    metrics_str += dy_str + " "

                # Append the mean of y.
                yj_sel = yj[k_gho:k_cur+1] if k_gho < k_cur \
                        else yj[k_cur:k_gho+1]
                kk_fin = np.isfinite(yj_sel).nonzero()[0]
                ym = np.mean(yj_sel[kk_fin])
                ym_str = "\u03BC:" # Greek mu
                ym_str += ftostr(ym, sigfigs(ym, ym))
                if len(metrics_str) + len(ym_str) + 1 <= self.metrics_space:
                    metrics_str += ym_str + " "

                # Append the standard deviation of y.
                ys = np.std(yj_sel[kk_fin])
                ys_str = "\u03C3:" # Green sigma
                ys_str += ftostr(ys, sigfigs(ys, ys))
                if len(metrics_str) + len(ys_str) + 1 <= self.metrics_space:
                    metrics_str += ys_str + " "

            # Wrap the metrics string in color.
            metrics_len = len(metrics_str)
            if cursor.j_sel > 0:
                color_idx = (cursor.j_sel - 1) % len(self.lites)
                color_value = self.lites[color_idx]
                metrics_str = self.frgnd + str(color_value) + "m" \
                        + metrics_str + RESET

            # Append filler.
            if metrics_len < self.metrics_space:
                gap = self.metrics_space - metrics_len
                metrics_str += chr(self.border["h"]) * gap

            # Append the metrics string to the info bar.
            draw_str += metrics_str

        # Write the draw string and flush.
        sys.stdout.write(draw_str + "\n")
        sys.stdout.flush()


class View:
    """
    Attributes
    ----------
    x_min : float
        Minimum valid x (linear or log scale).
    x_max : float
        Maximum valid x (linear or log scale).
    y_min : float
        Minimum valid y (linear or log scale).
    y_max : float
        Maximum valid y (linear or log scale).
    k_min : int np.ndarray
        Indices of minimum valid x.
    k_max : int np.ndarray
        Indices of maximum valid x.
    x_span_min : float
        Minimum span of x in zoom.

    x_lo : float
        Minimum valid x in view (linear or log scale).
    x_hi : float
        Maximum valid x in view (linear or log scale).
    y_lo : float
        Minimum valid y in view (linear or log scale).
    y_hi : float
        Maximum valid y in view (linear or log scale).
    k_lo : int np.ndarray
        Indices of minimum valid x in view (or near).
    k_hi : int np.ndarray
        Indices of maximum valid x in view (or near).

    x_lo_lin : float
        Left-most edge of view in linear scaling.
    x_hi_lin : float
        Right-most edge of view in linear scaling.
    y_lo_lin : float
        Bottom edge of view in linear scaling.
    y_hi_lin : float
        Top edge of view in linear scaling.

    row_zero : int
        Row index of y = 0.
    xlg : bool
        Flag for x-axis logarithmic scaling.
    ylg : bool
        Flag for y-axis logarithmic scaling.

    Notes
    -----
    The view and the cursor maintain indices into the x-axis arrays in order to
    minimize the search space when moving the cursor or changing the view.
    Consequently, these indices should not land on points which cannot be
    plotted, like non-finite values, and they should actually serve to represent
    the relevant search space.

    It would be nice to use the NumPy function "searchsorted" because it would
    in theory be more efficient given it relies on a binary search algorithm.
    However, it is not used because it does not correctly handle NaNs or
    infinities, unfortunately.

    The current view could have the following types of x-data ranges:

        1:  ----|---------------|----     continuous
        2:  ----|----       ----|----     gap in the middle
        3:  ----|----           |         end of valid data in view
        4:      |           ----|----     start of valid data in view
        5:  ----|----           |  --     gap ends after view
        6:  --  |           ----|----     gap starts before view
        7:  --  |               |  --     gap beyond view
        8:  --  |               |         end of valid data before view
        9:      |               |  --     start of valid data after view

    The first row of the x data is simple and standard: the data is defined for
    the full view. The second row includes values near the edges of the view,
    but is missing values in the middle. The next two rows (3 and 4) end or
    start somewhere within the view. This means the view indices do not extend
    to the edges of the view. The fifth and sixth rows have no values defined
    near one of the edges of the view. The seventh row has no values defined
    within the view but does have values defined outside of the view. A similar
    issue exists with the last two rows. In the first six cases, the view
    indices should identify valid x values closest to and within the view edges.
    In the last three cases, since there are no valid values within the view and
    we still wish for the indices to be useful, the indices should represent x
    values closest to the view edges. This requires that the data check at the
    beginning guarantee there are some valid values in each row of the x data.

    In all cases, the view indices should refer to valid values and the minimum
    indices should always be less than or equal to the maximum indices. Note, it
    is possible for the minimum and maximum indices to be equal.

    The cursor indices should represent the valid values of each row of x
    closest to the cursor position. This does not mean the x value corresponding
    to the cursor index is within the range of x values of the view. It does
    mean that the cursor index will be within the range of the view indices.
    Note, something within view is always closer to the center than something
    outside the view.

    If logarithmic scaling is used on the x axis, all of the view and cursor x
    values should be in logarithmic scaling as well. The data itself, however,
    should not be. The original data needs to remain unaltered and uncopied.
    Therefore, when checking whether x-axis values are within the view, it is
    more efficient to convert the view x values to linear scaling rather than to
    convert all the data x values to logarithmic scaling. It also means that no
    check must be performed on the data x values to see if they are positive
    before calculating the logarithm.
    """

    def __init__(self, sets, canvas, xlg, ylg, ea=False): # View method
        """
        This function initializes the view, which in the beginning should be of
        all the data. So, the x and y view limits should be the x and y data
        limits.

        Parameters
        ----------
        sets : Sets
            Object holding the lists of x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        xlg : bool
            Flag specifying if the x axis should be plotted with logarithmic
            scaling.
        ylg : bool
            Flag specifying if the y axis should be plotted with logarithmic
            scaling.
        ea : bool, default False
            Flag to apply equal axis scaling to the x and y axes. Because the
            appearance of proportionality is affected by the particular font
            chosen and the settings of the terminal emulator being used, the
            effective aspect ratio of the characters can be set with the
            itrm.Config class.
        """

        # Data limits
        self.x_min = None   # minimum valid x (linear or log scale)
        self.x_max = None   # maximum valid x (linear or log scale)
        self.y_min = None   # minimum valid y (linear or log scale)
        self.y_max = None   # maximum valid y (linear or log scale)
        self.k_min = np.zeros(sets.J, dtype=int) # indices of minimum valid x
        self.k_max = np.zeros(sets.J, dtype=int) # indices of maximum valid x
        self.x_span_min = None # minimum span of x in zoom

        # Data representation
        self.row_zero = -1  # row index of y = 0
        self.xlg = xlg      # flag for x-axis logarithmic scaling
        self.ylg = ylg      # flag for y-axis logarithmic scaling

        # Set the data limits.
        self.set_limits(sets)

        # Apply axis scaling.
        if ea:
            x_scale = (canvas.cols*Config.ar)/(self.x_max - self.x_min)
            y_scale = canvas.rows/(self.y_max - self.y_min)
            if x_scale < y_scale:
                y_scale = x_scale
                y_span = canvas.rows/y_scale
                y_mid = (self.y_max + self.y_min)*0.5
                self.y_min = y_mid - y_span*0.5
                self.y_max = y_mid + y_span*0.5
            elif y_scale < x_scale:
                x_scale = y_scale
                x_span = (canvas.cols*Config.ar)/x_scale
                x_mid = (self.x_max + self.x_min)*0.5
                self.x_min = x_mid - x_span*0.5
                self.x_max = x_mid + x_span*0.5

        # Copy data limits to the view limits.
        self.x_lo = self.x_min
        self.x_hi = self.x_max
        self.y_lo = self.y_min
        self.y_hi = self.y_max
        self.k_lo = self.k_min.copy()
        self.k_hi = self.k_max.copy()

        # Get the view edges.
        self.x_lo_lin = None
        self.x_hi_lin = None
        self.y_lo_lin = None
        self.y_hi_lin = None
        self.update_x_edges(canvas)
        self.update_y_edges(canvas)

    def set_limits(self, sets): # View method
        """
        Find the min and max of the x-axis data, the corresponding indices of
        those limits for each data set, and the min and max of the y-axis data.

        Parameters
        ----------
        sets : Sets
            Object holding the lists of x and y data.
        """

        # Initialize the limits.
        self.x_min = np.inf
        self.x_max = -np.inf
        self.y_min = np.inf
        self.y_max = -np.inf
        self.x_span_min = np.inf # minimum step size of x

        # For each row of data, expand the limits.
        for j in range(sets.J):
            # Find the valid x values by index.
            is_xj_fin = np.isfinite(sets.x[j]) if not self.xlg \
                else np.isfinite(sets.x[j]) & (sets.x[j] > 0)
            kk_valid = is_xj_fin.nonzero()[0]

            # Check for no valid x values.
            if len(kk_valid) == 0:
                raise ValueError(f"Set {j} has no valid x values.")

            # Find the minimum step size in x.
            if len(kk_valid) == 1:
                dxj_min = 0.0
            else:
                dx = np.diff(sets.x[j][kk_valid]) if not self.xlg \
                        else np.diff(np.log10(sets.x[j][kk_valid]))
                dxj_min = max(dx.min(), EPS)
            self.x_span_min = min(self.x_span_min, dxj_min)

            # Save the indices of the minimum and maximum.
            self.k_min[j] = kk_valid[0] # requires monotonicity
            self.k_max[j] = kk_valid[-1] # requires monotonicity

            # Expand the x-axis limits.
            xj_min = sets.x[j][self.k_min[j]]
            xj_max = sets.x[j][self.k_max[j]]
            if self.xlg:
                xj_min = np.log10(xj_min)
                xj_max = np.log10(xj_max)
            self.x_min = min(self.x_min, xj_min) # (linear or log scale)
            self.x_max = max(self.x_max, xj_max) # (linear or log scale)

            # Find the valid points by index.
            is_yj_fin = np.isfinite(sets.y[j]) if not self.ylg \
                else np.isfinite(sets.y[j]) & (sets.y[j] > 0)
            kk_valid = (is_xj_fin & is_yj_fin).nonzero()[0]

            # Check for no valid points.
            if len(kk_valid) == 0:
                continue

            # Expand the y-axis limits.
            yj_min = np.min(sets.y[j][kk_valid])
            yj_max = np.max(sets.y[j][kk_valid])
            if self.ylg:
                yj_min = np.log10(yj_min)
                yj_max = np.log10(yj_max)
            self.y_min = min(self.y_min, yj_min) # (linear or log scale)
            self.y_max = max(self.y_max, yj_max) # (linear or log scale)

    def reset(self, sets, canvas, cursor): # View method
        """
        This function makes note of the preexisting relative zoom and position
        of the view and relative position of the cursor. It then recalculates
        the limits of the data and applies the prior relative zoom and position
        of the view and relative position of the cursor.

        Parameters
        ----------
        sets : Sets
            Object holding the lists of x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        cursor : Cursor
            Object holding the cursor's x value, jump size and limit, array of x
            indices, and index of currently-selected data set.
        """

        # Save the original relative position and zoom (linear or log scale).
        x_span = self.x_hi - self.x_lo
        x_range = self.x_max - self.x_min
        rel_zoom = x_span/x_range
        x_center = (self.x_hi + self.x_lo)/2
        rel_pan = (x_center - self.x_min)/x_range

        # Save the original relative cursor position.
        rel_cursor = (cursor.x_cur - self.x_min)/x_range

        # Recalculate the data limits.
        self.set_limits(sets)

        # Restore the original relative position and zoom.
        x_range = self.x_max - self.x_min
        x_center = rel_pan * x_range + self.x_min
        x_span = rel_zoom * x_range
        self.x_lo = x_center - x_span/2
        self.x_hi = x_center + x_span/2
        self.limit_x() # Limit x_lo and x_hi.

        # Update the edges of the view.
        self.update_x_edges(canvas)

        # Update the view indices by starting with the data limits
        # and zooming in.
        self.k_lo[:] = self.k_min[:]
        self.k_hi[:] = self.k_max[:]
        self.zoom_in_indices(sets) # Updates k_lo and k_hi.

        # Update the y-axis of the view.
        self.clamp_y(sets, canvas, cursor)

        # Restore the original relative cursor position.
        cursor.x_cur = rel_cursor * x_range + self.x_min

    def update_x_edges(self, canvas): # View method
        """
        Calculate the edges of the view's x-axis. This adds a small margin in
        order to help with finite-precision comparisons when performing view
        calculations.

        Parameters
        ----------
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        """

        # Get total numbers of subrows and subcolumns.
        Cols = canvas.subcols * canvas.cols

        # Get the span of x and y values in view.
        x_span = self.x_hi - self.x_lo # (linear or log scale)

        # Get the view's limits (linear or log scaling).
        x_margin = x_span * 0.5/(Cols - 1) # (linear or log scale)
        x_lo = self.x_lo - x_margin
        x_hi = self.x_hi + x_margin

        # Get the view's limits in linear scaling. These are needed to compare
        # with the original linear data values in each data set.
        self.x_lo_lin = x_lo if not self.xlg else 10**x_lo
        self.x_hi_lin = x_hi if not self.xlg else 10**x_hi

    def update_y_edges(self, canvas): # View method
        """
        Calculate the edges of the view's y-axis. This adds a small margin in
        order to help with finite-precision comparisons when performing view
        calculations.

        Parameters
        ----------
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        """

        # Get total numbers of subrows and subcolumns.
        Rows = canvas.subrows * canvas.rows

        # Get the span of x and y values in view.
        y_span = self.y_hi - self.y_lo # (linear or log scale)

        # Get the view's limits (linear or log scaling).
        y_margin = y_span * 0.5/(Rows - 1) # (linear or log scale)
        y_lo = self.y_lo - y_margin
        y_hi = self.y_hi + y_margin

        # Get the view's limits in linear scaling. These are needed to compare
        # with the original linear data values in each data set.
        self.y_lo_lin = y_lo if not self.ylg else 10**y_lo
        self.y_hi_lin = y_hi if not self.ylg else 10**y_hi

    def center(self, sets, canvas, cursor): # View method
        """
        This function centers the view about the cursor's x position. It ensures
        the view is within the data limits. It recalculates the edges of the
        view and recalculates the x-axis view indices.

        Parameters
        ----------
        sets : Sets
            Object holding the lists of x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        cursor : Cursor
            Object holding the cursor's x value, jump size and limit, array of x
            indices, and index of currently-selected data set.
        """

        # Set the view to center on the cursor.
        x_span = self.x_hi - self.x_lo # (linear or log scale)
        self.x_lo = cursor.x_cur - x_span/2 # (linear or log scale)
        self.x_hi = self.x_lo + x_span # (linear or log scale)

        # Limit the view to the data limits.
        self.limit_x() # Limit x_lo and x_hi.

        # Get the view edges.
        self.update_x_edges(canvas)

        # Adjust the indices.
        self.pan_indices(sets, cursor)

    def zoom(self, zoom_factor, sets, canvas, cursor): # View method
        """
        This function changes the view by zooming in or out. It ensures the view
        is within the data limits. It recalculates the edges of the view and
        recalculates the x-axis view indices.

        Parameters
        ----------
        zoom_factor : float
            Factor by which to scale the current span of x-axis values. Values
            less than 1 will result in zooming in. Values greater than 1 will
            result in zooming out.
        sets : Sets
            Object holding the lists of x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        cursor : Cursor
            Object holding the cursor's x value, jump size and limit, array of x
            indices, and index of currently-selected data set.
        """

        # Get new view limits. (linear or log scale)
        x_span = self.x_hi - self.x_lo
        rel_position = (cursor.x_cur - self.x_lo)/x_span
        new_rel_position = 0.33*(0.5) + 0.67*rel_position
        x_span *= zoom_factor
        x_lo = cursor.x_cur - new_rel_position * x_span
        x_hi = x_lo + x_span

        # Prevent zoom in from panning.
        if zoom_factor < 1:
            if x_lo < self.x_lo:
                x_lo = self.x_lo
                x_hi = x_lo + x_span
            if x_hi > self.x_hi:
                x_hi = self.x_hi
                x_lo = x_hi - x_span

        # Save the new limits.
        self.x_lo = x_lo
        self.x_hi = x_hi

        # Limit the view to the data limits.
        self.limit_x() # Limit x_lo and x_hi.

        # Get the view edges.
        self.update_x_edges(canvas)

        # Adjust the indices.
        if zoom_factor < 1:
            self.zoom_in_indices(sets)
        elif zoom_factor > 1:
            self.zoom_out_indices(sets)

    def limit_x(self): # View method
        """
        Limit the x-axis values of the view. This simply ensures that the view's
        x-axis values do not exceed the data's x-axis values. It does not relate
        to the view indices at all. The view object properties are changed in
        place and no return value is given.
        """

        # Get the desired span of x values.
        x_span = self.x_hi - self.x_lo # (linear or log scale)

        # Ensure the view is not too zoomed in.
        if x_span < self.x_span_min:
            x_center = (self.x_hi + self.x_lo)/2 # (linear or log scale)
            self.x_lo = x_center - self.x_span_min/2 # (linear or log scale)
            self.x_hi = x_center + self.x_span_min/2 # (linear or log scale)

        # Ensure the view does not exceed the data limits.
        if self.x_lo < self.x_min:
            self.x_lo = self.x_min
            self.x_hi = min(self.x_lo + x_span, self.x_max)
        elif self.x_hi > self.x_max:
            self.x_hi = self.x_max
            self.x_lo = max(self.x_hi - x_span, self.x_min)

    def clamp_y(self, sets, canvas, cursor): # View method
        """
        This function calculates the min and max y-axis values in view, the
        y-axis edges of the view, and the canvas row in which a y value of zero
        exists.

        Parameters
        ----------
        sets : Sets
            Object holding the lists of x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        cursor : Cursor
            Object holding the cursor's x value, jump size and limit, array of x
            indices, and index of currently-selected data set.
        """

        # Initialize the y limits.
        y_min = np.inf
        y_max = -np.inf

        # Search each row of (x, y).
        jj = np.arange(sets.J) if cursor.j_sel == 0 \
                else np.array([cursor.j_sel - 1])
        for j in jj:
            # Get the view limits.
            k_lo = self.k_lo[j]
            k_hi = self.k_hi[j]

            # Get the data within view.
            xj_view = sets.x[j][k_lo:k_hi+1]
            yj_view = sets.y[j][k_lo:k_hi+1]

            # Find all valid points in view.
            is_x_fin = np.isfinite(xj_view) if not self.xlg \
                    else np.isfinite(xj_view) & (xj_view > 0)
            is_y_fin = np.isfinite(yj_view) if not self.ylg \
                    else np.isfinite(yj_view) & (yj_view > 0)
            mm_fin = (is_x_fin & is_y_fin).nonzero()[0]
            is_x_in = (xj_view[mm_fin] > self.x_lo_lin) \
                    & (xj_view[mm_fin] < self.x_hi_lin)
            nn_in = (is_x_in).nonzero()[0]
            mm_valid = mm_fin[nn_in]

            # Skip adjusting the limits if no valid points were found.
            if len(mm_valid) == 0:
                continue

            # Get the limits of y within the view.
            yj_min = yj_view[mm_valid].min()
            yj_max = yj_view[mm_valid].max()

            # Expand the overall min and max.
            y_min = min(y_min, yj_min) # ignores NaNs
            y_max = max(y_max, yj_max) # ignores NaNs

        # Check for no valid values.
        # A finite range is needed for scaling the plot.
        if y_min == np.inf:
            y_min = 0.0 if not self.ylg else 1.0
            y_max = 0.0 if not self.ylg else 1.0

        # Check for no range, which can happen with valid values.
        if y_min == y_max:
            y_min -= EPS
            y_max += EPS

        # Scale to logarithmic.
        if self.ylg:
            y_min = np.log10(y_min)
            y_max = np.log10(y_max)

        # Save the view's y-axis minimum and maximum.
        self.y_lo = y_min
        self.y_hi = y_max

        # Get the view edges.
        self.update_y_edges(canvas)

        # Update the zero row, which can change y_lo and y_hi.
        self.update_row_zero(canvas)

    def zoom_in_indices(self, sets): # View method
        """
        Update the arrays of indices of the view's x min and max by searching
        within the prior subset of view x values. The view object properties are
        changed in place and no return value is given.

        Parameters
        ----------
        sets : Sets
            Object containing the x and y data.

        Notes
        -----
        It is not possible to zoom in on a region without some valid x values in
        at least one of the rows because zooming centers on the cursor which
        will only latch onto valid x values in the rows of interest, whether one
        specific row or all of them.

        The view indices for each data set serve to increase efficiency in
        finding valid values when changing the view or moving the cursor. The
        low and high indices should mark either the limits of valid data within
        the view or the nearest valid values on either side of the view. The
        following shows some possible scenarios where the vertical bars mark the
        edges of the view and the pluses mark the indices of the view:

                    |               |       (old view)
            1:  --------|+-----+|-------    continuous
            2:  --------|+--+   |  -----    gap within new view
            3:  -----+  |       |  +----    gap within old view
            4:  --+     |       |    +--    gap surrounding old view
            5:  --+     |       |           end of valid data
            6:          |       |    +--    start of valid data

        In all cases, the indices of the previous view provide the search space
        for the indices of the new view.
        """

        # Adjust the indices for each data set.
        for j in range(sets.J):
            # Get the old low and high indices.
            k_lo = self.k_lo[j]
            k_hi = self.k_hi[j]

            # Find all valid x values within the new view
            # by searching within the old view.
            xj_view = sets.x[j][k_lo:k_hi+1] # (M,) where M = k_hi - k_lo + 1
            is_fin = np.isfinite(xj_view) if not self.xlg \
                    else np.isfinite(xj_view) & (xj_view > 0) # (M,)
            is_in = (self.x_lo_lin < xj_view) & (xj_view < self.x_hi_lin)
            kk_valid = (is_fin & is_in).nonzero()[0] + k_lo # (N,) where N <= M

            # Update the view indices.
            if len(kk_valid) != 0:
                self.k_lo[j] = kk_valid[0] # requires monotonicity
                self.k_hi[j] = kk_valid[-1] # requires monotonicity
                continue

            # If no valid values were within the new view, get the indices of
            # all valid values outside the new view but within the old view.
            # There must be valid values in the old view's range of indices.
            is_less = xj_view <= self.x_lo_lin
            is_more = xj_view >= self.x_hi_lin
            kk_less = (is_fin & is_less).nonzero()[0] + k_lo
            kk_more = (is_fin & is_more).nonzero()[0] + k_lo

            # Find the new minimum index.
            if len(kk_less) != 0: # some values less than new view
                self.k_lo[j] = kk_less[-1] # right-most
            else: # no values less than new view (some must be greater)
                self.k_lo[j] = kk_more[0] # left-most

            # Find the new maximum index.
            if len(kk_more) != 0: # some values more than new view
                self.k_hi[j] = kk_more[0] # left-most
            else: # no values more than new view (some must be lesser)
                self.k_hi[j] = kk_less[-1] # right-most

    def zoom_out_indices(self, sets): # View method
        """
        Update the arrays of indices of the view's x min and max by searching
        outside the prior subset of view x values. The view object properties
        are changed in place and no return value is given.

        Parameters
        ----------
        sets : Sets
            Object containing the x and y data.

        Notes
        -----
        It is not guaranteed that the old view indices will be within the old
        view. However, they will always mark the best places to start searching
        for the new view. The view indices for each data set serve to increase
        efficiency in finding valid values when changing the view or moving the
        cursor. The low and high indices should mark either the limits of valid
        data within the view or the nearest valid values on either side of the
        view.

        The following are the actions to take given some possible scenarios,
        where the vertical bars mark the edges of the new view and the pluses
        mark the old min and max indices:

            0:        |       |         (old view)
            1:  ---|--+-------+--|---   search left of min and right of max
            2:  ---|--+--+     --|---   search left of min and right of max
            3:  ---|--+--+       | --   search left of min and right of max
            4:  ---|--     +--+--|---   search left of min and right of max
            5:  ---|-+         +-|---   search left of min and right of max
            6:  ---|-+           |      search left of min and right of max
            7:     |           +-|---   search left of min and right of max
            8:  ---|-+           | +-   search left of min and reuse min as max
            9:  -+ |           +-|---   reuse max as min and search right of max
            10: -+ |             |      reuse old indices
            11:    |             | +-   reuse old indices
            12: -+ |             | +-   reuse old indices

        So, we see that the min and max indices should not be treated
        independently. If the x values corresponding to the old indices are both
        within the new view, search left and right. If just the min is within
        the new view, search left and use the old min for the new max. If just
        the max is within the new view, search right and use the old max for the
        new min. If neither is within the view, reuse the old indices (i.e., do
        nothing).
        """

        # Adjust the indices for each data set.
        for j in range(sets.J):
            # Get the data limits.
            k_min = self.k_min[j]
            k_max = self.k_max[j]

            # Get the old view limits.
            k_lo = self.k_lo[j]
            k_hi = self.k_hi[j]
            xk_lo = sets.x[j][k_lo] # (linear scale)
            xk_hi = sets.x[j][k_hi] # (linear scale)

            # Get the left search space, if the x position of the old low index
            # is within the new view.
            if self.x_lo_lin <= xk_lo <= self.x_hi_lin:
                xj_left = sets.x[j][k_min:k_lo+1] # all valid points to the left
                is_fin = np.isfinite(xj_left) if not self.xlg \
                        else np.isfinite(xj_left) & (xj_left > 0)
                is_in = self.x_lo_lin <= xj_left
                kk_left = (is_fin & is_in).nonzero()[0] + k_min

            # Get the right search space, if the x position of the old high
            # index is within the new view.
            if self.x_lo_lin <= xk_hi <= self.x_hi_lin:
                xj_right = sets.x[j][k_hi:k_max+1] # all valid to the right
                is_fin = np.isfinite(xj_right) if not self.xlg \
                        else np.isfinite(xj_right) & (xj_right > 0)
                is_in = xj_right <= self.x_hi_lin
                kk_right = (is_fin & is_in).nonzero()[0] + k_hi

            # Update the minimum and maximum indices.
            if (self.x_lo_lin <= xk_lo) and (xk_hi <= self.x_hi_lin):
                self.k_lo[j] = kk_left[0] # requires monotonicity
                self.k_hi[j] = kk_right[-1] # requires monotonicity
            elif self.x_lo_lin <= xk_lo <= self.x_hi_lin: # left
                self.k_hi[j] = self.k_lo[j] # reuse min as new max
                self.k_lo[j] = kk_left[0] # requires monotonicity
            elif self.x_lo_lin <= xk_hi <= self.x_hi_lin: # right
                self.k_lo[j] = self.k_hi[j] # reuse max as new min
                self.k_hi[j] = kk_right[-1] # requires monotonicity

    def pan_indices(self, sets, cursor): # View method
        """
        Update the arrays of indices of the view's x min and max by searching
        left or right of the prior view indices. The view object properties are
        changed in place and no return value is given.

        Parameters
        ----------
        sets : Sets
            Object containing the original x and y data.
        cursor : Cursor
            Object holding the cursor's x value, jump size and limit, array of x
            indices, and index of currently-selected data set.

        Notes
        -----
        Panning always centers the view about the cursor position, which by this
        point will already have an updated array of indices. It is not
        guaranteed that there will be valid x values in every data set within
        the new view. It is, however, guaranteed that the new cursor index will
        be within the range of values of the new view indices for each row of x.
        This is due to them sharing the same criteria: valid values of x closest
        to the view.

        The goal here is to efficiently find the indices of the new view for
        each row of x. The indices should mark the range of all valid values
        within view, the range of the gap surrounding the view when no valid
        values are within view, or the last valid values before the view or
        first valid values after the view.

        If the cursor index is within the new view, we know the view is not a
        gap. If the cursor index is outside the view, we can search before and
        after the view indices for valid values. We can use the data limits to
        check if there should be valid values before or after the cursor index.

        The cursor index is a good place to start. Whether the cursor index is
        within view or not, the lower view index must be to the left of the
        cursor index and the higher view index must be to the right of the
        cursor index.
        """

        # Adjust the indices for each data set.
        for j in range(sets.J):
            # Get the data limits.
            k_min = self.k_min[j]
            k_max = self.k_max[j]

            # Get the cursor index.
            k_cur = cursor.k_cur[j]
            x_cur = sets.x[j][k_cur] # (linear scale)

            # Get the left search space from the cursor.
            xj_left = sets.x[j][k_min:k_cur+1] # all points to the left
            is_left_fin = np.isfinite(xj_left) if not self.xlg \
                    else np.isfinite(xj_left) & (xj_left > 0)

            # Get the right search space from the cursor.
            xj_right = sets.x[j][k_cur:k_max+1] # all points to the right
            is_right_fin = np.isfinite(xj_right) if not self.xlg \
                    else np.isfinite(xj_right) & (xj_right > 0)

            # Get the indices inside or outside the view
            if self.x_lo_lin <= x_cur <= self.x_hi_lin: # inside
                is_in = self.x_lo_lin <= xj_left
                kk_left = (is_left_fin & is_in).nonzero()[0] + k_min
                is_in = xj_right <= self.x_hi_lin
                kk_right = (is_right_fin & is_in).nonzero()[0] + k_cur
                self.k_lo[j] = kk_left[0]
                self.k_hi[j] = kk_right[-1]
            elif (x_cur < self.x_lo_lin) or (self.x_hi_lin < x_cur): # outside
                kk_left = (is_left_fin).nonzero()[0] + k_min
                kk_right = (is_right_fin).nonzero()[0] + k_cur
                self.k_lo[j] = kk_left[-1]
                self.k_hi[j] = kk_right[0]

    def update_row_zero(self, canvas): # View method
        """
        Find the row where the y-axis value is zero. The result of this function
        will be used to draw a mark on either side of the canvas where the y
        values reach zero. This mark will not necessarily visually center on
        exactly the zero position. To achieve that, the scale of the view would
        have to be adjusted. However, such and adjustment can lead to unwanted
        jitter as the user cycles through various data sets, even if they have
        approximately the same limits.

        Parameters
        ----------
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        """

        Rows = canvas.subrows * canvas.rows
        y_span = self.y_hi - self.y_lo
        if y_span > 0:
            R = (Rows - 1)*(self.y_hi - 0)/y_span
            row_zero = R//canvas.subrows
        else:
            row_zero = -1
        if (row_zero < 0) or (row_zero >= canvas.rows):
            row_zero = -1
        self.row_zero = row_zero


class Cursor:
    """
    Attributes
    ----------
    x_cur : float
        Cursor x position (linear or log scale).
    k_cur : (J,) np.ndarray(int)
        Indices of x near cursor (might not be in view).
    jump_size : float
        Change in x across one character column (linear or log scale).
    y_min : float
        Minimum of y values in cursor column.
    y_max : float
        Maximum of y values in cursor column.
    J : int
        Number of data sets.
    j_sel : int
        Index of selected data set (0 for all).
    x_gho : float
        Ghost cursor x position (linear or log scale).
    k_gho : (J,) np.ndarray(int)
        Indices of x near ghost cursor (might not be in view).
    labels : None, str, list, or tuple
        The set from which the current label is selected.
    label : None or str
        The current label.
    j_label : int
        Integer value of label color.
    """

    def __init__(self, sets, canvas, view, labels): # Cursor method
        """
        Position the cursor in the middle of the x-axis range of values, define
        the render column number and get the indices for each row of x.

        Parameters
        ----------
        sets : Sets
            Object containing the original x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        view : View
            Object holding the current x and y view limits as well as the x and
            y-axis logarithmic scaling flags and the view's x-axis limit
            indices.
        labels : None, str, list, or tuple
            The set from which the current label is selected.
        """

        # Initialize the properties.
        self.x_cur = (view.x_hi + view.x_lo)/2 # midpoint (linear or log scale)
        self.k_cur = np.zeros(sets.J, dtype=int)
        self.jump_size = 0
        self.y_min = None
        self.y_max = None
        self.J = sets.J
        self.j_sel = 0
        self.x_gho = None
        self.k_gho = None
        self.labels = labels
        self.label = None
        self.j_label = 0

        # Align the cursor position with the data.
        self.align(sets, canvas, view)

        # Set the cursor jump size (linear or log scale).
        self.set_jump_size(canvas, view)

        # Select the current label.
        self.select_label()

    def align(self, sets, canvas, view): # Cursor method
        """
        Align the cursor position (based on x_cur) with the closest x value.

        Parameters
        ----------
        sets : Sets
            Object containing the original x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns.
        view : View
            Object holding the current x and y view limits as well as the x and
            y-axis logarithmic scaling flags and the view's x-axis limit
            indices.
        """

        # Align the cursor position with the nearest column center in the center
        # of the view. Whole-value columns or subcolumns refer to the middle of
        # the column or subcolumn. So, the left-most edge of all columns has an
        # index value of -0.5.
        _, x_cur = canvas.column(view, self.x_cur)

        # Get the indices of the closest x values to x_cur.
        x_closest = 0 # x value closest to x_cur
        dst_min = np.inf # minimum distance to x_cur
        for j in range(self.J):
            # Find the closest x value of this whole row.
            ka = view.k_min[j]
            kb = view.k_max[j]
            xj = sets.x[j][ka:kb+1]
            is_fin = np.isfinite(xj) if not view.xlg \
                    else np.isfinite(xj) & (xj > 0) # (K,)
            mm_valid = is_fin.nonzero()[0] # (M,) where M <= K
            xj_valid = xj[mm_valid]
            dst = np.abs(xj_valid - x_cur) if not view.xlg \
                    else np.abs(np.log10(xj_valid) - x_cur) # (M,)
            m_cur = mm_valid[dst.argmin()]
            self.k_cur[j] = m_cur + ka

            # Check if the closest x on this row is closest overall.
            xj_closest = xj[m_cur] if not view.xlg else np.log10(xj[m_cur])
            dst = abs(x_cur - xj_closest)
            if dst < dst_min:
                dst_min = dst
                x_closest = xj_closest

        # Set the new x_cur with the closest x.
        self.x_cur = x_closest # (linear or log scale)

    def move(self, jump_factor, sets, canvas, view): # Cursor method
        """
        Move the cursor and its indices to the new jump position. At this point,
        the view has not been adjusted. The new cursor position is not
        guaranteed to be within the current view. The cursor object properties
        are changed in place and no return value is given.

        Parameters
        ----------
        jump_factor : float
            Positive or negative multiplier to be multiplied by the current
            cursor jump size. The sign indicates a right or left motion.
        sets : Sets
            Object containing the original x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns. Used for centering the x
            position to the center of a column.
        view : View
            Object holding the current x and y view limits as well as the x and
            y-axis logarithmic scaling flags and the view's x-axis limit
            indices.

        Returns
        -------
        out : bool
            Flag that the cursor is outside the view.
        """

        # Get the target cursor position.
        dx = jump_factor*self.jump_size # (linear or log scale)
        x_new = self.x_cur + dx # new target position (linear or log scale)
        _, x_new = canvas.column(view, x_new)

        # Get new cursor position in linear scaling.
        x_new_lin = x_new if not view.xlg else 10**x_new

        # Find the x value to the right or left.
        dst_min = np.inf # minimum distance to x_new
        for j in range(sets.J):
            # Get the search space.
            if dx > 0: # rightward
                if x_new > view.x_hi:
                    k_a = view.k_hi[j]
                    k_b = view.k_max[j]
                    if k_a > k_b:
                        k_a = self.k_cur[j] + 1
                else:
                    k_a = self.k_cur[j] + 1
                    k_b = view.k_hi[j]
                    if k_a > k_b:
                        k_b = view.k_max[j]
            elif dx < 0: # leftward
                if x_new < view.x_lo:
                    k_a = view.k_min[j]
                    k_b = view.k_lo[j]
                    if k_a > k_b:
                        k_b = self.k_cur[j] - 1
                else:
                    k_a = view.k_lo[j]
                    k_b = self.k_cur[j] - 1
                    if k_a > k_b:
                        k_a = view.k_min[j]

            # Get the current cursor position in linear scaling.
            x_cur_lin = sets.x[j][self.k_cur[j]]

            # Find the best match within the search space.
            xj = sets.x[j][k_a:k_b+1]
            is_fin = np.isfinite(xj) if not view.xlg \
                    else np.isfinite(xj) & (xj > 0)
            is_beyond = xj > x_cur_lin if dx > 0 else xj < x_cur_lin
            mm = (is_fin & is_beyond).nonzero()[0]
            if len(mm) == 0:
                self.k_cur[j] = k_b if dx > 0 else k_a
                continue
            dst = np.abs(xj[mm] - x_new_lin) if not view.xlg \
                    else np.abs(np.log10(xj[mm]) - x_new)
            n = dst.argmin()
            self.k_cur[j] = mm[n] + k_a

            # Save the closest match to x_new.
            if (self.j_sel == 0) and (dst[n] < dst_min):
                dst_min = dst[n]
                x_cur = sets.x[j][self.k_cur[j]]
                self.x_cur = x_cur if not view.xlg else np.log10(x_cur)
            elif self.j_sel - 1 == j:
                dst_min = dst[n]
                x_cur = sets.x[j][self.k_cur[j]]
                self.x_cur = x_cur if not view.xlg else np.log10(x_cur)

        # Check if the new position is outside the view.
        out = (self.x_cur < view.x_lo) or (self.x_cur > view.x_hi)
        return out

    def cycle_selection(self, dj): # Cursor method
        """
        Cycle which data set is selected.

        Parameters
        ----------
        dj : int
            Change to the data-set selection index.
        """

        if self.J > 1:
            self.j_sel = (self.j_sel + dj) % (self.J + 1)
        else:
            self.j_sel = 0
        self.select_label()

    def select_label(self): # Cursor method
        """ Select a label from labels based on the current data-set selection
        index. """

        # Define labels if none where provided.
        if self.labels is None:
            if self.J == 1:
                self.labels = ""
            else:
                self.labels = [str(self.J) + " sets"]
                for j in range(self.J):
                    self.labels.append("Set " + str(j+1) + "/" + str(self.J))

        # Select a label from the set of labels.
        if isinstance(self.labels, str):
            self.label = self.labels if self.labels != "" else None
            self.j_label = 0
        elif len(self.labels) == self.J + 1:
            self.label = self.labels[self.j_sel]
            self.j_label = self.j_sel
        elif len(self.labels) == self.J:
            if self.j_sel == 0:
                self.label = str(self.J) + " sets"
            else:
                self.label = self.labels[self.j_sel - 1]
            self.j_label = self.j_sel
        else:
            if self.j_sel == 0:
                self.label = str(self.J) + " sets"
            elif self.j_sel <= len(self.labels):
                self.label = self.labels[self.j_sel - 1]
            else:
                self.label = self.labels[self.j_sel - 1]
                self.label = "Set " + str(self.j_sel) + "/" + str(self.J)
            self.j_label = self.j_sel

    def set_jump_size(self, canvas, view): # Cursor method
        """
        Get the change in x (linear or logarithmic scaling) per canvas column.

        Parameters
        ----------
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns. Used for centering the x
            position to the center of a column.
        view : View
            Object holding the current x and y view limits as well as the x and
            y-axis logarithmic scaling flags and the view's x-axis limit
            indices.
        """

        # The first and last points are centered on the first and last dots.
        x_span = view.x_hi - view.x_lo
        width = canvas.cols - 1/canvas.subcols
        self.jump_size = x_span/width

    def y_span(self, sets, canvas, view): # Cursor method
        """
        Calculate the span of y-axis values within the column of the cursor
        position.

        Parameters
        ----------
        sets : Sets
            Object containing the original x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns. Used for centering the x
            position to the center of a column.
        view : View
            Object holding the current x and y view limits as well as the x and
            y-axis logarithmic scaling flags and the view's x-axis limit
            indices.
        """

        # Get the cursor position.
        _, x_center = canvas.column(view, self.x_cur)

        # Get the left and right edges of the cursor column.
        x_left = x_center - self.jump_size/2 # (linear or log scale)
        x_right = x_center + self.jump_size/2 # (linear or log scale)
        x_left_lin = x_left if not view.xlg else 10**x_left
        x_right_lin = x_right if not view.xlg else 10**x_right

        # Initialize the y limits.
        y_min = np.inf
        y_max = -np.inf

        # Define the list of data sets over which to iterate.
        jj = np.arange(sets.J) if (self.j_sel == 0) \
                else np.array([self.j_sel-1])

        # Search the selected sets.
        for j in jj:
            # Get the view limits.
            k_lo = view.k_lo[j]
            k_hi = view.k_hi[j]

            # Get the data within view.
            xj_view = sets.x[j][k_lo:k_hi+1]
            yj_view = sets.y[j][k_lo:k_hi+1]

            # Find all valid points in view.
            is_x_fin = np.isfinite(xj_view) if not view.xlg \
                    else np.isfinite(xj_view) & (xj_view > 0)
            is_y_fin = np.isfinite(yj_view) if not view.ylg \
                    else np.isfinite(yj_view) & (yj_view > 0)
            mm_valid = (is_x_fin & is_y_fin).nonzero()[0]
            if len(mm_valid) > 1:
                is_x_in = (xj_view[mm_valid] >= x_left_lin) \
                        & (xj_view[mm_valid] <= x_right_lin)
                nn_in = (is_x_in).nonzero()[0]
                mm_valid = mm_valid[nn_in]

            # Skip if no valid points were found.
            if len(mm_valid) == 0:
                continue

            # Get the limits of y within the view.
            yj_min = yj_view[mm_valid].min()
            yj_max = yj_view[mm_valid].max()
            if view.ylg:
                yj_min = np.log10(yj_min)
                yj_max = np.log10(yj_max)

            # Expand the overall min and max.
            y_min = min(y_min, yj_min)
            y_max = max(y_max, yj_max)

        # Provide default values if no valid values where found.
        if np.isinf(y_min) or np.isinf(y_max):
            y_min = np.nan
            y_max = np.nan

        # Save the values.
        self.y_min = y_min
        self.y_max = y_max

    def reset(self, sets, canvas, view): # Cursor method
        """
        Align the cursor with the data, recalculate the jump size, and get the
        span of y-axis values within the column of the cursor position.

        Parameters
        ----------
        sets : Sets
            Object containing the original x and y data.
        canvas : Canvas
            Object holding the size of the canvas in rows and columns as well as
            the number of subrows and subcolumns. Used for centering the x
            position to the center of a column.
        view : View
            Object holding the current x and y view limits as well as the x and
            y-axis logarithmic scaling flags and the view's x-axis limit
            indices.
        """

        # Remove the ghost cursor.
        self.x_gho = None
        self.k_gho = None

        # Realign the cursor to the data, define the jump size, and the span of
        # y values at the cursor.
        self.align(sets, canvas, view)
        self.set_jump_size(canvas, view)
        self.y_span(sets, canvas, view)

# ------------------------------------------------------------------------------
# Progress bar and bar chart
# ------------------------------------------------------------------------------

class Progress:
    """
    Output a simple progress bar with percent complete to the terminal. When k
    equals K - 1, the progress bar will complete and start a new line.
    """

    def __init__(self, K, cols=1):
        """
        Initialize the progress bar.

        Parameters
        ----------
        K : int
            Final index value of k plus 1.
        cols : int, default 1
            Desired width of the full string, including the percent complete,
            the bar, and the clock if greater than 1 or fraction of window
            columns if less than 1.
        """

        # Define the max value of k + 1 and the initial time.
        self.K = K
        self.t_init = time.perf_counter()
        self.t_last = self.t_init

        # Get the terminal size.
        term_cols, _ = term_size()
        self.use_esc = is_term()

        # Convert a fractional cols to columns.
        if cols <= 1:
            cols = max(round(term_cols * cols), 18)

        # Define the bar width.
        self.bar_width = cols - 5 - 12

    def update(self, k):
        """
        Update the progress bar (actually print it).

        Parameters
        ----------
        k : int
            Index which should grow monotonically from 0 to K - 1.
        """

        # Skip this call if the bar is not done but not enough time has passed.
        t_now = time.perf_counter()
        if (k + 1 < self.K) and (t_now - self.t_last < 0.2):
            return
        self.t_last = t_now

        # Get the ratio.
        ratio = max(0.0, min(self.K - 1.0, (k + 1)/self.K))

        # Get the clock string.
        t_show = t_now - self.t_init
        if k + 1 == self.K:
            clk_str = "  "
        else:
            t_show = 0.0 if ratio <= 0 else t_show*(1 - ratio)/ratio
            clk_str = " -"
        hours = int(t_show/3600)
        minutes = int((t_show - hours*3600)//60)
        seconds = t_show % 60
        clk_str += f"{hours:02d}:{minutes:02d}:{seconds:04.1f}"

        # Build the progress bar.
        draw_str = HIDE_CURSOR if self.use_esc else ""
        draw_str += f"\r{int(100*ratio):3d}% "
        draw_str += fill_bar(self.bar_width*ratio, self.bar_width, self.use_esc)
        if self.use_esc:
            draw_str += RESET
        draw_str += f"{clk_str}"
        if self.use_esc:
            draw_str += SHOW_CURSOR
        if k + 1 >= self.K:
            draw_str += "\n"

        # Write the bar.
        sys.stdout.write(draw_str)
        sys.stdout.flush()


def bars(x, labels=None, cols=1):
    """
    Create a bar graph of the data in x using the labels for each element
    of x.

    Parameters
    ----------
    x : float array like
        Set of values to plot as a bar graph.
    labels : string list, default None
        List of strings. This should be the same length as x.
    cols : int, default 1
        Desired number of columns if greater than 1 or fraction of window
        columns if less than 1.
    """

    # Get the terminal size.
    term_cols, _ = term_size()
    use_esc = is_term() # necessary to use color

    # Convert a fractional cols to columns.
    if cols <= 1:
        cols = max(round(term_cols * cols), 18)

    # Get the width of labels.
    label_width = 0
    if labels is not None:
        label_width = len(max(labels, key=len))

    # Get the max width of the printed bar length.
    x_width = 0
    for i in range(len(x)):
        x_str = f"{x[i]:g}"
        x_width = max(x_width, len(x_str))

    # Adjust the total width to make room for labels.
    width = max(1, cols - label_width - x_width - 3)

    # Define the vertical bar string.
    vert_bar = chr(0x2502) if Config.uni else "|"
    reset = RESET if use_esc else ""

    # For each value of x, print the bar.
    draw_str = ""
    span = max(max(x), 1)
    if labels is None:
        for i in range(len(x)):
            draw_str += vert_bar
            draw_str += fill_bar(width * x[i]/span, width, use_esc, False)
            draw_str += f" {x[i]:g}"
            draw_str += reset + "\n"
    else:
        for i in range(len(x)):
            if labels is not None:
                n_spc = label_width - len(labels[i])
                draw_str += " " * n_spc + labels[i] + " "
            draw_str += vert_bar
            draw_str += fill_bar(width * x[i]/span, width, use_esc, False)
            draw_str += f" {x[i]:g}"
            draw_str += reset + "\n"

    # Write the bars.
    sys.stdout.write(draw_str)
    sys.stdout.flush()


def fill_bar(n, N, use_esc, fill_empty=True):
    """ Get the string of a fill bar with n out of N cells filled. The cells
    which are not filled will be colored dark. """

    # Define the Unicode characters.
    uh = chr(0x2501) # box drawings heavy horizontal
    ul = chr(0x2578) # box drawings heavy left  "- "
    ur = chr(0x257A) # box drawings heavy right " -"

    # Round n when it is close to an integer.
    if (n % 1 < 0.1) or (n % 1 > 0.9):
        n = round(n)

    # Define the before, middle, and after strings.
    more = (n % 1 > 0.5)
    if Config.uni and use_esc:
        b = uh
        if not more:
            m = Config.frgnd + str(Config.gray) + "m" + ur
        else:
            m = ul + Config.frgnd + str(Config.gray) + "m"
        a = uh
    elif Config.uni and not use_esc:
        b = uh
        m = " " if not more else ul
        a = " "
    elif not Config.uni and use_esc:
        b = "="
        if not more:
            m = "-" + Config.frgnd + str(Config.gray) + "m"
        else:
            m = "=" + Config.frgnd + str(Config.gray) + "m"
        a = "-"
    else:
        b = "="
        m = "-" if not more else "="
        a = " "

    # Get the component lengths.
    nb = min(int(n), N)
    na = max(0, N - int(n) - 1)
    nm = max(0, N - nb - na)

    # Build the bar string.
    if fill_empty:
        fill_str = b*nb + m*nm + a*na
    else:
        fill_str = b*nb

    return fill_str

# ------------------------------------------------------------------------------
# Tables
# ------------------------------------------------------------------------------

def table(matrix, head=None, left=None, width=10, sep="  "):
    """
    Print a table to the terminal.

    Parameters
    ----------
    matrix : list of lists of values
        Table of values.
    head : list of strings, default []
        List of header labels.
    left : list of strings, default []
        List of left-most column labels.
    width : int, default 10
        Width in characters of each cell.
    sep : string, default "  "
        String separating columns.
    """

    # -----------------
    # Check the inputs.
    # -----------------

    # Check the type of matrix.
    if isinstance(matrix, (str, float, int)):
        matrix = [[matrix]]
    elif isinstance(matrix, list):
        is_2d = False
        for n, datum in enumerate(matrix):
            if isinstance(datum, np.ndarray):
                is_2d = True
                matrix[n] = datum.tolist()
            elif isinstance(datum, list):
                is_2d = True
        if not is_2d:
            matrix = [matrix]
    elif isinstance(matrix, np.ndarray):
        matrix = matrix.tolist()
        if not isinstance(matrix[0], list):
            matrix = [matrix]
    else:
        raise TypeError("heat: matrix must be a list!")

    # Check the type of head.
    if head is None:
        head = []
    elif isinstance(head, (str, float, int)):
        head = [head]
    elif isinstance(head, np.ndarray):
        head = head.tolist()
    elif not isinstance(head, list):
        raise TypeError("heat: head must be a list!")

    # Check the type of left.
    if left is None:
        left = []
    elif isinstance(left, (str, float, int)):
        left = [left]
    elif isinstance(left, np.ndarray):
        left = left.tolist()
    elif not isinstance(left, list):
        raise TypeError("heat: left must be a list!")

    # Check that width is within 3 to 30.
    if width < 6:
        width = 6
    elif width > 30:
        width = 30

    # -------------
    # Print header.
    # -------------

    def f2str(num, width=6):
        """
        Convert a floating-point number, num, to a string, keeping the total
        width in characters equal to width.
        """

        # Ensure width is not less than 6, and check if padding should not be
        # used (i.e., width was negative).
        if width < 0:
            width = -width
            skip_padding = True
        else:
            skip_padding = False
        width = max(6, width)

        # Make num non-negative but remember the minus.
        if num < 0:
            sw = 1
            s = "-"
            num = -num
            ei = int(np.floor(np.log10(num))) # integer exponent
        elif num > 0:
            sw = 0
            s = ""
            ei = int(np.floor(np.log10(num))) # integer exponent
        else:
            sw = 0
            s = ""
            ei = 0

        # Build number string without leading spaces.
        if ei >= 4:     # 10000 to inf
            precision = width - 2 - len(str(ei)) - sw
            f_str = s + f"{num*(10**(-ei)):.{precision}g}"
            if "." in f_str:
                f_str = f_str.rstrip("0").rstrip(".")
            f_str += f"e{ei}"
        elif ei >= 0:   # 1 to 10-
            precision = width - 2 - ei - sw
            f_str = s + f"{num:.{precision}f}"
            if "." in f_str:
                f_str = f_str.rstrip("0").rstrip(".")
        elif ei >= -3:  # 0.001 to 1-
            precision = width - 2 - sw
            f_str = s + f"{num:.{precision}f}"
            if "." in f_str:
                f_str = f_str.rstrip("0").rstrip(".")
        else:           # -inf to 0.001-
            precision = width - 3 - len(str(-ei)) - sw
            f_str = s + f"{num*(10**(-ei)):.{precision}g}"
            if "." in f_str:
                f_str = f_str.rstrip("0").rstrip(".")
            f_str += f"e{ei:d}"

        # Add leading spaces for padding.
        if not skip_padding:
            f_str = " "*(width - len(f_str)) + f_str

        return f_str

    def fixed_width_string(C, width=6):
        """
        Convert a string or numeric value, C, to a string, keeping the total
        width in characters equal to width.
        """

        if isinstance(C, str):
            L = len(C)
            if L > width:
                L = width - 3
                return C[:L] + "..."
            elif L == width:
                return C
            else:
                return " "*(width-L) + C
        elif isinstance(C, float):
            return f2str(C, width)
        else:
            return f2str(float(C), width)

    # Define the horizontal and vertical bars.
    if Config.uni:
        horz_bar = chr(0x2500)
        vert_bar = chr(0x2502)
    else:
        horz_bar = "-"
        vert_bar = "|"

    # Print the header.
    if len(head) > 0:
        row_str = ""
        if len(left) > 0:
            row_str += " "*width + " " + vert_bar + " "
        for n_col, val in enumerate(head):
            if n_col > 0:
                row_str += sep
            row_str += fixed_width_string(val, width)
        sys.stdout.write(row_str + "\n")

        row_str = ""
        if len(left) > 0:
            row_str += horz_bar*width + " " + vert_bar + " "
        for n_col in range(len(head)):
            if n_col > 0:
                row_str += sep
            row_str += horz_bar*width
        sys.stdout.write(row_str + "\n")

    # -------------
    # Print matrix.
    # -------------

    for n_row, vals in enumerate(matrix):
        row_str = ""
        if len(left) > n_row:
            row_str += fixed_width_string(left[n_row], width)
            row_str += " " + vert_bar + " "
        elif len(left) > 0:
            row_str += horz_bar*width + " " + vert_bar + " "
        for n_col, val in enumerate(vals):
            if n_col > 0:
                row_str += sep
            row_str += fixed_width_string(val, width)
        sys.stdout.write(row_str + "\n")

# ------------------------------------------------------------------------------
# Matrix plotting functions
# ------------------------------------------------------------------------------

def heat(matrix, uni=None):
    """
    Create a surface plot using the input matrix. The rows are printed in
    reverse order.

    Parameters
    ----------
    matrix : (rows,cols) np.ndarray
        Matrix of values to plot as a heat map.
    uni : bool, default None
        Flag to use Unicode characters. If None, use Config.uni.

    Notes
    -----
    This function uses the 24 shades of gray at the end of the 8-bit color
    table. Although there are 6 more "shades" of gray including true black and
    true white between color codes 16 and 231, these do not fit into the
    uniform spacing of the 24. True white makes a larger leap leap from the
    rest of all the grays (17) than the usual interval (10) among the 24.
    Therefore, given the slight benefit and the increased complexity, the 6
    additional grays were not included.
    """

    # Get the terminal size.
    term_cols, _ = term_size()
    use_esc = is_term() # necessary to use color

    # Scale the matrix.
    m_min = np.min(matrix)
    m_max = np.max(matrix)
    M = np.round((matrix - m_min)/(m_max - m_min)*23).astype(int)
    rows, cols = M.shape

    # Stop if the terminal window is not wide enough.
    if cols > term_cols:
        raise ValueError("The terminal window is too small for "
                + f"this heat map: {cols} > {term_cols}")

    # Decide whether to use Unicode characters.
    if (uni is None) or not isinstance(uni, bool):
        uni = Config.uni

    # Print the matrix.
    draw_str = ""
    if uni:
        if use_esc:
            for row in range(0, rows - rows % 2, 2):
                for col in range(cols):
                    draw_str += "\x1b[48;5;" + str(M[row, col] + 232) + "m"
                    draw_str += "\x1b[38;5;" + str(M[row+1, col] + 232) + "m"
                    draw_str += chr(0x2584) # lower half block
                draw_str += RESET + "\n"
            if rows % 2 == 1:
                for col in range(cols):
                    draw_str += "\x1b[48;5;" + str(M[-1, col] + 232) + "m"
                draw_str += RESET + "\n"
        else:
            for row in range(0, rows - rows % 2, 2):
                for col in range(cols):
                    if (M[row, col] < 12) and (M[row+1, col] < 12):
                        draw_str += " "
                    elif (M[row, col] < 12) and (M[row+1, col] >= 12):
                        draw_str += chr(0x2584) # lower half block
                    elif (M[row, col] >= 12) and (M[row+1, col] < 12):
                        draw_str += chr(0x2580) # upper half block
                    else:
                        draw_str += chr(0x2588) # full block
                draw_str += "\n"
            if rows % 2 == 1:
                for col in range(cols):
                    if M[row, col] < 12:
                        draw_str += " "
                    else:
                        draw_str += chr(0x2580) # upper half block
                draw_str += "\n"
    else:
        if use_esc:
            for row in range(rows):
                for col in range(cols):
                    draw_str += "\x1b[48;5;" + str(M[row, col] + 232) + "m  "
                draw_str += RESET + "\n"
        else:
            for row in range(rows):
                for col in range(cols):
                    if M[row, col] < 12:
                        draw_str += "  "
                    else:
                        draw_str += "[]"
                draw_str += "\n"

    # Write the matrix.
    sys.stdout.write(draw_str)
    sys.stdout.flush()


def spy(matrix):
    """
    Print the sparsity of a matrix.
    """

    # Get the terminal size.
    term_cols, _ = term_size()
    term_width = term_cols*2 if Config.uni else term_cols//2

    # Stop if the terminal window is not wide enough.
    I, J = matrix.shape
    if J > term_width:
        raise ValueError("The terminal window is too small for "
                + f"this heat map: {J} > {term_width}")

    # Convert matrix to zeros and ones.
    M = (np.abs(matrix) > EPS).astype(int)

    # Convert the large matrix to a smaller matrix of character values.
    if Config.uni:
        II = math.ceil(I/4)*4
        JJ = math.ceil(J/2)*2
        MM = np.zeros((II, JJ), dtype=int)
        for i in range(I): # This method supports sparse matrices.
            for j in range(J):
                MM[i, j] = M[i, j]
        chars = (0x2800 + MM[0::4, ::2] +  8*MM[0::4, 1::2]
                +  2*MM[1::4, ::2] +  16*MM[1::4, 1::2]
                +  4*MM[2::4, ::2] +  32*MM[2::4, 1::2]
                + 64*MM[3::4, ::2] + 128*MM[3::4, 1::2])
    else: # stars
        chars = 0x20*np.ones((I, 2*J+1), dtype=int)
        chars[:, 1:-1:2] += 0xA*M

    # Draw the plot.
    draw_str = ""
    rows, cols = chars.shape
    for row in range(rows):
        for col in range(cols):
            draw_str += chr(chars[row, col])
        draw_str += "\n"

    # Write the matrix.
    sys.stdout.write(draw_str)
    sys.stdout.flush()
