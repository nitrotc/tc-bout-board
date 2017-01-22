#!/usr/bin/env python
#
#     "TC BOUT BOARD" a wrestling Match Bout Board application for youth matches or tournaments
#     Copyright (C) 2016  Anthony Cetera
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os import system
from platform import system as platform
from Tkinter import *
import tkMessageBox

# Global Variables
meet = set([])

# Images
team_image = "bb_team_image.gif"

# Initialize bout board row text variables.  Global so they can be updated from both classes.
nw_text = []
od_text = []
dd_text = []
ith_text = []


class WrMat:
    """
    The WrMat class maintains the bout board data set.
    Each object is a mat number and a list of match numbers on that mat
    mat_bouts should always be added to the class as a list.
    """
    def __init__(self, mat_num, mat_bouts):
        self.mat_num = mat_num
        self.mat_bouts = mat_bouts

    def __str__(self):
        return str(self.mat_num) + "\n" + str(self.mat_bouts)

    def add_bout(self, bout_num):
        self.mat_bouts.append(bout_num)

    def finish_bout(self, bout_pos):
        self.mat_bouts.pop(bout_pos)

    def insert_bout(self, bout_pos, bout_num):
        self.mat_bouts.insert(bout_pos, bout_num)

    def get_mat_num(self):
        return self.mat_num

    def get_mat_bouts(self):
        return self.mat_bouts


def help_about():
    """
    Posts version and license information.
    """
    tkMessageBox.showinfo("About TC BOUT BOARD", "TC BOUT BOARD v1.0 Copyright (C) 2016 Anthony Cetera\n"
                                                 "This program comes with ABSOLUTELY NO WARRANTY;"
                                                 " for details click Help --> About\n\n"
                                                 "This is free software, and you are welcome to redistribute it"
                                                 "under certain conditions; "
                                                 "please check the beginning of the source code for license details.")


def get_mat(matnum):
    """
    Send in a mat number and get back the WrMat object containing that mat number.
    """
    global meet
    for eachmat in meet:
        if eachmat.get_mat_num() == matnum:
            return eachmat


def validate_match_spinbox(value):
    """
    Function checks that spinboxes contain integers between 1 and 99.
    First I tried making this a method in the Adminwin class but Pycharm complained.
    Made it static to avoid Pycharm error - I'm neurotic like that.
    """
    try:
        intval = int(value)
        if 0 < intval < 100:
            return True
        else:
            return False
    except ValueError:
        return False


def validate_insert_match(value):
    """
    Function checks limits the insert to 5 characters.
    """
    try:
        if len(value) < 6:
            return True
        else:
            return False
    except ValueError:
        return False


def update_grid(matnum):
    """
    StringVars for board grid labels are defined in class Boardwin.
    Function sets each of these stringvars based on the contents of the current WrMat match list.
    Function must be passed a mat number to update from.
    """
    curmat = get_mat(matnum)
    matboutlist = curmat.get_mat_bouts()

    try:
        nw_text[matnum].set(matboutlist[0])
    except IndexError:
        nw_text[matnum].set("*")

    try:
        od_text[matnum].set(matboutlist[1])
    except IndexError:
        od_text[matnum].set("*")

    try:
        dd_text[matnum].set(matboutlist[2])
    except IndexError:
        dd_text[matnum].set("*")

    try:
        ith_text[matnum].set(matboutlist[3])
    except IndexError:
        ith_text[matnum].set("*")


class Adminwin:
    """
    All administrative window functions are defined here.
    """
    def __init__(self, master):
        # Define the maximum number of mats the application will support
        # Update this if you want to try running more than 6 mats.  Not tested with integers > 6.
        self.maxmats = 6

        # Define lists needed to hold each listbox object
        # One needed for the mats, mat labels, and mat scrollbars
        self.mat = []
        self.matlabel = []
        self.sbmat = []

        # Define variables needed to start the additional board window
        self.board_window = None
        self.start_board_window = None
        # Establish that the bout board isn't running
        self.board_running = False

        # Define meet setup variables before initializing
        self.init_mat_num = None
        self.init_mat_optmenu = None
        self.init_mat_label = None
        self.init_button = None

        # Define list to hold spinboxes for match numbers
        self.match_num_spin = []
        self.match_spinner_label = []

        # Init cleanup flag
        # This is used to decide if we should cleanup the information frame after initializing the meet set.
        self.wipe_mat_optmenu = False

        # Set starting rows for mat grid
        mat_start_row = 0
        mat_button_row = 0

        # Deal with initial focus problem on OSX
        if platform() == 'Darwin':  # How Mac OS X is identified by Python
            system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        # Set up root of parent window as master
        self.master = master
        self.master.title("BOUT BOARD ADMIN")

        # Draw a frame in the grid for a border
        self.adminframe = Frame(self.master, bd=6, bg='gray90', relief=SUNKEN)
        self.adminframe.grid(column=0, row=0)
        self.adminframe.grid_rowconfigure(0, weight=1)
        self.adminframe.grid_columnconfigure(0, weight=1)

        # Menu block
        # Build menu for one time options
        self.menubar = Menu(self.master)
        self.init_menu = Menu(self.menubar, tearoff=0)
        self.init_menu.add_command(label="Setup Meet", command=self.draw_init_dialogs)
        self.init_menu.add_command(label="Show Board", command=self.start_board)
        self.menubar.add_cascade(label="Get Started", menu=self.init_menu)
        # Quit Menu
        self.quit_menu = Menu(self.menubar, tearoff=0)
        self.quit_menu.add_command(label="Close Board", command=self.stop_board)
        self.quit_menu.add_command(label="Quit!", command=self.adminframe.quit)
        self.menubar.add_cascade(label="Quit Menu", menu=self.quit_menu)
        # Help Menu
        self.help_menu = Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="About", command=help_about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        # Populate the menu bar with options above
        self.master.config(menu=self.menubar)

        # Build grid of up to 6 potential mats
        for i in range(self.maxmats):
            matnum = i + 1
            matcol = (i % 3) * 2
            matlabelrow = ((i // 3) * 2) + mat_start_row
            matrow = matlabelrow + 1
            scrollcol = matcol + 1
            self.matlabel.append(Label(self.adminframe, text="MAT " + str(matnum)))
            self.sbmat.append(Scrollbar(self.adminframe, orient=VERTICAL))
            self.mat.append(Listbox(self.adminframe, selectmode=SINGLE, yscrollcommand=self.sbmat[i].set))
            self.sbmat[i].config(command=self.mat[i].yview)
            self.matlabel[i].grid(sticky=(N, W), column=matcol, row=matlabelrow)
            self.mat[i].grid(sticky=(N, W), column=matcol, row=matrow)
            self.sbmat[i].grid(sticky=(N, S), column=scrollcol, row=matrow)

        # Draw interactive area
        self.interactframe = Frame(self.master, bd=6, bg='gray69', relief=SUNKEN)
        self.interactframe.grid(sticky=(E, W), column=0, columnspan=2, row=1)

        # Remove a match
        self.rm_button = Button(self.interactframe, text="Remove Match", command=self.rm_bout)
        self.rm_button.grid(sticky=W, column=0, row=mat_button_row)

        # Assign validation function to master for spinbox input validation
        # Each time a change is made inside the entry box of the spinner, the contents are evaluated against this.
        validate_insert_cmd = self.master.register(validate_insert_match)

        # Insert a match
        self.add_button = Button(self.interactframe, text="Add Match at Selection", command=self.add_bout)
        self.add_button.grid(column=0, row=mat_button_row + 1)
        self.add_dialog = Entry(self.interactframe, validate='all', validatecommand=(validate_insert_cmd, '%P'), bd=3)
        self.add_dialog.grid(column=2, row=mat_button_row + 1)

        # Draw information message area
        self.infoframe = Frame(self.master, bd=6, bg='gray69', relief=SUNKEN)
        self.infoframe.grid(sticky=(N, S), column=1, row=0)
        self.infoframe.grid_columnconfigure(0, minsize=200)
        self.infolabel = Label(self.infoframe, text="Information Area", fg='blue', relief=GROOVE)
        self.infospacer = Label(self.infoframe)
        self.infospacer.grid(column=1, row=0, padx=36)
        self.infolabel.grid(sticky=(E, W), column=0, row=0, columnspan=2)

    def cleanup_init(self):
        """
        This method destroys all the widgets that were created during the meet setup phase.
        However, we can also call this every time we need to redraw the bouts per mat spinners if the user
        selects a new number of mats.
        """
        if self.wipe_mat_optmenu:
            self.init_mat_optmenu.destroy()
            self.init_mat_label.destroy()
            self.wipe_mat_optmenu = False

        for count in range(len(self.match_num_spin)):
            self.match_spinner_label[count].destroy()
            self.match_num_spin[count].destroy()

        # wipe button because it doesn't seem to destroy after it's pushed down the grid
        self.init_button.destroy()

        # wipe lists that hold spinner widgets
        self.match_num_spin = []
        self.match_spinner_label = []

    def meet_init(self):
        """
        This function generates the meet set by iterating through each mat that the user chose a number of matches for.
        A WrMat object is added to the set one by one until the entire meet is stored.
        """
        global meet

        # wipe current meet.  meet should contain current set of WrMat objects.
        meet = set([])

        # Time to get the user input for the number of mats running today.
        mat_qty = self.init_mat_num.get()

        # Create each list of matches and add them to the meet.
        for count in range(mat_qty):
            mat_num = count + 1
            mat_bouts = self.match_num_spin[count].get()
            temp_bouts = list(range(mat_num * 100 + 1, mat_num * 100 + int(mat_bouts) + 1))
            temp_bouts_str = []
            for bout_num in temp_bouts:
                temp_bouts_str.append(str(bout_num))
            temp_mat = WrMat(mat_num, temp_bouts_str)
            meet.add(temp_mat)

        # Destroy all widgets associated with setting up a new board by calling the cleanup function.
        self.wipe_mat_optmenu = True
        self.cleanup_init()

        # Draw everything now that the meet set is created
        self.draw_lists()

    def draw_matchnum_spin(self, matsval):
        """
         Method generates spinboxes to input number of matches per mat.  Then, generates
         the list of match numbers from x01-x99.
        """
        # Assign validation function to master for spinbox input validation
        # Each time a change is made inside the entry box of the spinner, the contents are evaluated against this.
        validate_spin_cmd = self.master.register(validate_match_spinbox)

        # If number of mats changes we need to clear the existing spinboxes in the info frame
        # Also cleanup function should wipe the list containing the existing SB widgets
        # So check for widgets erase and redraw
        if self.match_num_spin:
            self.cleanup_init()

        # Create and draw the spinboxes based on the number of mats chosen.
        # These spinboxes allow the user to select the number of bouts per mat.
        for mat_num in range(1, matsval + 1):
            self.match_spinner_label.append(Label(self.infoframe, text="Number of bouts on MAT " + str(mat_num)))
            self.match_num_spin.append(Spinbox(self.infoframe,
                                               from_=1,
                                               to=99,
                                               width=6,
                                               validate='all',
                                               validatecommand=(validate_spin_cmd, '%P')))
            self.match_spinner_label[mat_num - 1].grid(column=0, row=mat_num + 1)
            self.match_num_spin[mat_num - 1].grid(column=1, row=mat_num + 1)

        # Button to init all values selected
        # Calls function to set up meet set and destroy init widgets.
        self.init_button = Button(self.infoframe, text="Initialize Meet", bg='red', command=self.meet_init)
        self.init_button.grid(column=0, row=self.maxmats + 2)

    def clear_listboxes(self):
        """
        Wipe the contents of the admin listboxes
        """
        for i in range(self.maxmats):
            self.mat[i].delete(0, END)

    def draw_init_dialogs(self):
        """
        Create a list from 1 to the maximum number of mats on the floor.
        This establishes the options for the Optionmenu of mats running this day
        """
        if tkMessageBox.askyesno("Initialize", "Board will reset.\nAre you sure?"):
            # Create a list to hold the Optionmenu choices for the number of mats running
            mat_opts_list = list(range(1, self.maxmats + 1))

            # Track a variable for when hte number of mats changes...as an integer.
            self.init_mat_num = IntVar()

            # Set the default to the 3rd value in the list.  Should always be the integer 3.
            self.init_mat_num.set(mat_opts_list[2])

            # Create the drop down menu.
            self.init_mat_label = Label(self.infoframe, text="Number of mats running today?")
            self.init_mat_optmenu = OptionMenu(self.infoframe,
                                               self.init_mat_num,
                                               *mat_opts_list,
                                               command=self.draw_matchnum_spin)
            self.init_mat_label.grid(column=0, row=1)
            self.init_mat_optmenu.grid(sticky=EW, column=1, row=1)

            # Check to see if list of spinners has values
            # If not, generate some spinners with the default value of the Optionmenu
            if not self.match_num_spin:
                self.draw_matchnum_spin(self.init_mat_num.get())

            # Clean up any running boards
            self.stop_board()

            # Clear listboxes as to not confuse the user after the selected a new setup
            self.clear_listboxes()

    def draw_lists(self):
        """
        Time to draw the listboxes in the admin window with the contents of the entire meet set
        We can also call this function to clear the boxes for a new init.
        Note: in that case it will not wipe the meet set but we will get a clean window.
        """
        global meet

        # Make sure boxes are cleared on subsequent runs
        self.clear_listboxes()

        # Iterate through each WrMat then iterate through the list of bouts in that mat object.
        # add each mat number to the list boxes.
        for temp_mat in meet:
            mn = temp_mat.get_mat_num() - 1
            for temp_bout in temp_mat.get_mat_bouts():
                self.mat[mn].insert(END, temp_bout)
            self.mat[mn].insert(END, "END of BOUTS")

    def rm_bout(self):
        """
        Iterate through all the list boxes and check for a selection.
        When a selection is found, delete the bout number from the listbox and remove the bout from the class.
        """
        for i in range(len(meet)):
            sel_bout = self.mat[i].curselection()
            # Check for a selection line number and that the line selected isn't the only one.
            if sel_bout and (self.mat[i].size() - 1) != sel_bout[0]:
                sel_bout_int = sel_bout[0]
                cur_mat = get_mat(i+1)
                cur_mat.finish_bout(sel_bout_int)
                self.mat[i].delete(sel_bout_int)
                # Make sure whatever the last selected position in listbox stays selected
                self.mat[i].selection_set(sel_bout_int)
                if self.board_running:
                    update_grid(i + 1)

    def add_bout(self):
        """
        Free form entry box to add bouts to the list.
        Currently only checks for duplicates on the same mat.
        """
        # Iterate through each admin listbox and check for a selection
        for i in range(len(meet)):
            matnum = i + 1
            duplicate = False
            sel_bout = self.mat[i].curselection()
            # Get value in entry box
            box_val = self.add_dialog.get()
            # Check for a selection and no blank values
            if sel_bout and box_val:
                sel_bout_int = sel_bout[0]
                cur_mat = get_mat(matnum)
                # Check for duplicates
                for check_dup in cur_mat.get_mat_bouts():
                    if check_dup == box_val:
                        duplicate = True
                if not duplicate:
                    # First update the mat object from the class WrMat with the new bout number
                    cur_mat.insert_bout(sel_bout_int, self.add_dialog.get())
                    # Keep the corresponding list box in sync
                    # by inserting the new bout into the box in the same position
                    self.mat[i].insert(sel_bout_int, self.add_dialog.get())
                    # Check to see if the board is being displayed by checking the flag
                    # If so, call out to redraw based on the mat queue that changed
                    if self.board_running:
                        update_grid(matnum)

    def start_board(self):
        """
        Leverage the TopLevel function to start a new window as a child of the root
        Because this is intended to run on an XGA projector, set the dimensions to 1024
        The board_running flag needs to be maintained if we want to make sure multiple windows don't get spawned.
        """
        if not self.board_running and meet:
            self.board_running = True
            self.board_window = Toplevel(self.master)
            self.board_window.geometry('1024x768')

            # Capture destroy events.  This makes it board_running flag consistent no matter how window is destroyed.
            self.board_window.protocol("WM_DELETE_WINDOW", self.stop_board)

            # Make root resizable
            self.board_window.rowconfigure(0, weight=1)
            self.board_window.columnconfigure(0, weight=1)

            # Boardwin class deals with all functions of the actual bout board display
            self.start_board_window = Boardwin(self.board_window)

    def stop_board(self):
        """
        If the board needs to close for some reason, this function destroys the top level window.
        """
        if self.board_running:
            self.board_window.destroy()
            self.board_running = False


class Boardwin:
    """
    This class is defined specifically to start a second window to draw the board.
    It is called as a child window in the Adminwin class with the TopLevel function.
    """
    def __init__(self, master):
        """
        The entire window is managed in __init__
        The board makes use of a corner image that can be customized to whatever is placed in bb_team_image.gif
        Otherwise, there are a few tunable parameters like fonts, colors and boarder type.
        ToDo - organize the tunables such that that the variables containing them are all in one place.
        """
        # "text" globals hold the actual values that will be in each row of the grid
        global meet, nw_text, od_text, dd_text, ith_text, team_image

        # Set up the child window
        self.master = master
        self.master.title("BOUT BOARD")

        # Make the root resizable by giving the columns and rows a weight
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Put a frame in the grid hold the bout board matrix
        self.boardframe = Frame(self.master, bd=6, relief=SUNKEN)
        self.boardframe.grid(sticky=N+S+E+W, column=0, row=0)

        # Determine number of mats for iterations of mats.
        self.active_mats = len(meet)

        # Number of columns is number of mats plus 1.  Again, for iterations of columns.
        max_x = len(meet) + 1

        # Board will always have 5 rows (Header, NW, OD, DD, ITH)
        max_y = 5

        # Initialize row Label variables
        self.header_row = []
        self.nw_label = []
        self.od_label = []
        self.dd_label = []
        self.ith_label = []

        # Formatting variables.  In this case only one just to set up the border around each grid box.
        bb_relief = RIDGE

        # Attempt to define a variable to render the corner image.
        # If the attempt fails, skip this altogether.
        try:
            corner_image = PhotoImage(file=team_image)
        except TclError:
            corner_image = None

        # Make all the columns resizable
        # The 1st column will maintain 2/3 the width of the other ones.
        for x in range(max_x):
            if x == 0:
                self.boardframe.columnconfigure(x, weight=2)
            else:
                self.boardframe.columnconfigure(x, weight=3)

        # Make all the rows resizable
        # The 1st row will be 2/3 the height of the other rows.
        for y in range(max_y):
            if y == 0:
                self.boardframe.rowconfigure(y, weight=2)
            else:
                self.boardframe.rowconfigure(y, weight=3)

        # Draw the first row of the grid
        # Create the column headers based on how many mats there are
        for mat_column in range(max_x):
            # Special handling of (0,0)
            # make it an image not text like the others
            if mat_column == 0:
                self.header_row.append(Label(self.boardframe, image=corner_image,
                                             bg='goldenrod', relief=bb_relief))
                self.header_row[0].image = corner_image
            # The rest of the columns will display the mat number
            else:
                self.header_row.append(Label(self.boardframe, text="MAT " + str(mat_column),
                                             font='Helvetica 42 bold', bg='goldenrod', relief=bb_relief))
            # Time to place the contents of the list instance into the first row of the grid
            self.header_row[mat_column].grid(sticky=N+S+E+W, column=mat_column, row=0)

        # Initialize the rest of the board with the following for loop
        for pos in range(max_x):
            # By setting up each list entry as a StringVar, changing them redraws the new value
            nw_text.append(StringVar())
            od_text.append(StringVar())
            dd_text.append(StringVar())
            ith_text.append(StringVar())

            if pos == 0:
                # Static row headers for column 0
                nw_text[pos].set("Now \nWrestling")
                od_text[pos].set("On \nDeck")
                dd_text[pos].set("Double \nDeck")
                ith_text[pos].set("In the \nHole")
            else:
                # update_grid will assign values to the newly assigned StringVar
                # Notice the function must be passed the mat number here indicated by a "pos"ition on the grid
                update_grid(pos)

            # Define formatting variables based on the column number being worked on
            if pos == 0:
                grid_color = 'goldenrod'
                grid_font = 'Helvetica 40 bold'
                # By setting the grid width, in characters, we insure the auto resize
                # won't shrink or grow the grid squares based on the contents
                # 9 is the number of characters in the word "Wrestling"
                grid_width = 9
            else:
                grid_color = 'light goldenrod'
                grid_font = 'Helvetica 60 bold'
                # By setting the grid width, in characters, we insure the auto resize
                # won't shrink or grow the grid squares based on the contents
                # 5 characters gives us room for a 5 character bout number
                grid_width = 5

            # As each column position is updated establish a label widget for the value
            # Now Wrestling
            self.nw_label.append(Label(self.boardframe, textvariable=nw_text[pos], height=2,
                                       font=grid_font, bg=grid_color, relief=bb_relief, width=grid_width))
            # On Deck
            self.od_label.append(Label(self.boardframe, textvariable=od_text[pos], height=2,
                                       font=grid_font, bg=grid_color, relief=bb_relief, width=grid_width))
            # Double Deck
            self.dd_label.append(Label(self.boardframe, textvariable=dd_text[pos], height=2,
                                       font=grid_font, bg=grid_color, relief=bb_relief, width=grid_width))
            # In the Hole
            self.ith_label.append(Label(self.boardframe, textvariable=ith_text[pos], height=2,
                                        font=grid_font, bg=grid_color, relief=bb_relief, width=grid_width))

            # Place each bout label on the grid
            self.nw_label[pos].grid(sticky=N + S + E + W, column=pos, row=1)
            self.od_label[pos].grid(sticky=N + S + E + W, column=pos, row=2)
            self.dd_label[pos].grid(sticky=N + S + E + W, column=pos, row=3)
            self.ith_label[pos].grid(sticky=N + S + E + W, column=pos, row=4)


def main():
    root = Tk()
    app1 = Adminwin(root)
    root.mainloop()
    try:
        root.destroy()
    except TclError:
        pass

if __name__ == '__main__':
    main()
