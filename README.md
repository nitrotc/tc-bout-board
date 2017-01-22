![Sample Board Image](https://github.com/nitrotc/tc-bout-board/blob/master/docs/board_sample.png)

## Introduction
"TC BOUT BOARD" was created to help wrestling teams hosting home meets display an active queue of matches or bouts. 
The application is designed to leverage an XGA resolution projector to display a dynamic bout board on a 
 gymnasium wall. It supports up to 6 mats running at any given time. Bout numbers are automatically generated in three 
 digit format based on the number of bouts scheduled for each mat.  Adjustments can be made for scratches and other
 adjustments to the schedule.  

## Features
- Multi-platform: Tested on Mac OSX, Windows and CentOS.
- No network needed: Will function in those crowded gymnasiums without WiFi.
- Separate admin window: Queue/schedule changes cleanly update in display window.
- Resizable board: What if I have a WXGA projector?  Should still work well.  

## Requirements
TC Bout Board is a python 2 application.  All you should need is python 2.7.12 to get this working.  To install python, 
download it from [Python.org](https://www.python.org/) and  follow the install instructions. 
- Python 2.7.12
- Tkinter installed with Python (should be included in your Python distro)
- An XGA resolution projector
- ***Optional:***  
Create an image file to put a logo on your bout board.
Image should be roughly 86x80 pixels in GIF format.  
Name the file bb_team_image.gif

## Install
- *If you are unfamiliar with installing python or python applications, try reading the windows install example here:*
   [tc-bout-board Windows Install](https://github.com/nitrotc/tc-bout-board/blob/master/docs/tc-bout-board-win-install.pdf)
- Install Python 2.7.12 environment that includes Tkinter.
- Create a directory called ./dzdtsoftware/tc_bout_board. You can put this in C:\, /opt, your home directory or wherever.
- Copy tc_bout_board.py and bb_team_image.gif from the ~app directory to the new directory.  

## Usage
The application consists of 2 windows.  An admin interface and the bout board display.  The admin interface is to 
be used on your main display of your laptop. All updates to the running board will be done there at the head table. 
The admin interface will have the same information as the bout board in addition to the the entire queue/schedule for 
each mat.

There are a few steps to getting the board up and running.  Typically, you would run the application, 
tell it how many matches are on each mat, "initialize the meet", display the board and add or remove bouts as
needed.
 1. Run TC Bout Board e.g. $ python /usr/local/dzdtsoftware/tc_bout_board/tc_bout_board.py
 2. From the "Get Started" menu, click "Setup Meet".
 3. In the "Information Area" select the number of mats running in your tournament.
 4. Use the spin-boxes to set the number of bouts you have scheduled for each mat.
 5. Click "Initialize Meet"
 6. From the "Get Started" menu, click "Display Board"  
 
**What do I do when a bout finishes?**
- Highlight the finished bout and click "Remove Match"
 
**What do I do if I need to add in a bout?**
- Say...bout 101a needs to be inserted above bout 101.
- "Add Match at Selection" inserts above the selected bout.
- Highlight the bout where you want to insert the new one.
- Type the bout number (up to 5 characters) in the box next to the "Add Match at Selection" button.
- Click the button.  
 
## License
TC BOUT BOARD is released under GNU General Public License
