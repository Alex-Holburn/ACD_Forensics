############################################################################################
# Program/Script Title: ACD_Version.py
#
# Program/Script Version: 1.0
#
# Program/Script Purpose: The purpose of this script is to examine a user-specified
#                         Logix 5000 Project File, and extract the IDE version, last
#                         edit timestamp, and Project Name for end-user analysis.
#                         This analysis is typically in the form of rapid version control
#                         in production environments or keeping vendors in check.
#
# Program/Script Author: Alex Holburn https://www.alexholburn.com
#
# License: MIT License. Copyright 2021, Alex Holburn https://www.alexholburn.com
#
############################################################################################

# -----------------------------------BEGIN LIBRARY IMPORTS---------------------------------

import os
import time
import tkinter as main
import tkinter.filedialog
import webbrowser
from platform import system
from PIL import ImageTk, Image

# -----------------------------------END LIBRARY IMPORTS-----------------------------------

# -----------------------------------BEGIN VARIABLE DECLARATIONS---------------------------

operating_system = system()
dirName = os.path.dirname(__file__)  # Current directory
utilityImage = os.path.join(dirName, r'resources\ACD_Forensics_Text.png')
icoImage = os.path.join(dirName, r'resources\icon.ico')  # .ico image path
logoImage = os.path.join(dirName, r'resources\AlexHolburnLogo.png')  # logo image for shameless self promotion

fileIdentifier = 'This file was generated by the RSLogix 5000 software.'  # String that identifies a Logix 5000 project.
versionHeader = 'V E R S I O N   I N F O R M A T I O N :'  # String that identifies the Logix 5000 Version information.


# -----------------------------------BEGIN FUNCTION DEFINITIONS----------------------------

def extract_between(string, delim_1, delim_2):  # The purpose of this function is to extract the middle of a string.
    pos_delim_1 = string.find(delim_1)  # Find the position of the 1st delimiter.
    if pos_delim_1 == -1:  # Validate the string
        return ""

    pos_delim_2 = string.rfind(delim_2)  # Find the position of the 2nd delimiter.
    if pos_delim_2 == -1:
        return ""  # Validate the string

    adjusted_pos_delim_1 = pos_delim_1 + len(delim_1)  # Find the start position of the second slice of the string.
    if adjusted_pos_delim_1 >= pos_delim_2:  # Validate the processed string.
        return ""
    return string[adjusted_pos_delim_1:pos_delim_2]  # Return the processed string.


def extract_before(string, delim):  # Extract the part of a string before a delimiter
    pos_delim = string.find(delim)  # Find the position of the delimiter.
    if pos_delim == -1:  # Validate the string
        return ""
    return string[0:pos_delim]  # Return the processed string.


def extract_after(string, delim):  # Extract the part of a string after a delimiter.
    pos_delim = string.rfind(delim)  # Find the position of the delimiter
    if pos_delim == -1:
        return ""  # Validate the string
    adjusted_pos_delim = pos_delim + len(delim)  # Find the start position of the second slice of the string.
    if adjusted_pos_delim >= len(string):
        return ""  # Validate the string
    return string[adjusted_pos_delim:]  # Return the processed string.


def static_description_text():  # Function to paint static description text.
    description1 = main.Label(root, text='This utility is used to identify IDE version information '
                                         'from a Logix 5000 Project File [.ACD]. This information',
                              fg='black', font=('Segoe', 8))
    canvas1.create_window(275, 50, window=description1)

    description2 = main.Label(root, text='is typically used for version control in a production environment. '
                                         'In addition to the version control aspects,',
                              fg='black', font=('Segoe', 8))
    canvas1.create_window(275, 66, window=description2)

    description3 = main.Label(root, text='the utility can also be used '
                                         'to rapidly automate Logix 5000 Project initial forensic analysis.',
                              fg='black', font=('Segoe', 8))
    canvas1.create_window(275, 82, window=description3)


def static_status_text():  # Function to paint static status text.
    status1 = main.Label(root, text='Program Status:', fg='black', bg='White', font=('Segoe', 8,))
    canvas1.create_window(52, 186, window=status1)

    status2 = main.Label(root, text='Waiting for user input.', fg='black', bg='White', font=('Segoe', 8,))
    canvas1.create_window(67, 210, window=status2)


def browse_file():  # Define the file dialog with all files and .L5X extensions. Also updates selected file text.
    global target_acd  # Used as a global variable to get the filepath out of the function. Should update this to OOP.

    target_file = main.filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                  filetype=(("Logix 5000 Project", "*.ACD"), ("All Files", "*.*")))

    selected_file = main.Label(root, text=target_file, fg='black', bg='white', font=('Segoe', 8))
    canvas1.create_window(215, 117, window=selected_file)

    target_acd = target_file


def browse_button():  # Generates the browse button, on click, this guy calls browse_file.
    browse_file_button = main.Button(text='Select .ACD File', command=browse_file, )
    canvas1.create_window(475, 117, window=browse_file_button)


def check_logix5000_project():  # Check to see if the target file is a Logix 5000 Project.
    with open(target_acd, encoding='cp437') as file:  # use cp437 encoding because rockwell binaries are strange.
        acdfile = file.readlines()

    for line in acdfile:  # Checks each line in the project file for the Logix 5000 project string.
        if fileIdentifier in line:
            return True  # Returns 'True' if string found

    return False  # Returns 'False' if string not found, it's really only here if debug is needed.


def find_version_header():  # Find the Version Header information of the last project save.
    global version_info_line
    with open(target_acd, encoding='cp437') as acdFile:  # use cp437 encoding because rockwell binaries are strange.
        for num, line in enumerate(acdFile, 1):  # check each line for our version header text.
            if versionHeader in line:
                version_info_line = num - 4  # 4 is a magic number because Rockwell's format skipped a new line char.

                if versionHeader in line:
                    break


def find_version_info():  # We extract the version info string with this.
    global version_info_string
    acdfile = open(target_acd, encoding='cp437')  # use cp437 encoding because rockwell binaries are strange.
    lines = acdfile.readlines()  # read all of the lines in the file
    version_info_string = lines[version_info_line]
    acdfile.close()  # close the file for efficiency


def analyze_file():  # Saves the file to a location of the users choice, and kicks off the analysis.
    files = [('Text File', '*.txt'), ('All Files', '*.*')]
    file = main.filedialog.asksaveasfile(filetypes=files, defaultextension=files)  # We create the output text file here

    general_modified_date = 'File System Last Detected Edit: ' + time.ctime(os.path.getmtime(target_acd))

    if check_logix5000_project():  # Check if the root is "RSLogix5000Content".

        status3 = main.Label(root, text='File Type Check Status: OK (Logix5000 Project).', fg='black',
                             bg='White',
                             font=('Segoe', 8,))
        canvas1.create_window(130, 226, window=status3)

        find_version_header()
        find_version_info()

        status4 = main.Label(root, text='Generating AOI Analysis.',
                             fg='black', bg='White', font=('Segoe', 8,))
        canvas1.create_window(75, 242, window=status4)

        acd_name = 'ACD Name: ' + target_acd  # grab the filename/path for the analysis output
        acd_year = 'Last Edit Year: ' + version_info_string[0:4]  # grab the year of the last acd edit
        acd_month = 'Last Edit Month: ' + version_info_string[5:7]  # grab the month of the last acd edit
        acd_day = 'Last Edit Day: ' + version_info_string[8:10]  # grab the day of the last acd edit
        acd_hour = 'Last Edit Hour: ' + version_info_string[11:13]  # grab the hour of the last acd edit
        acd_minute = 'Last Edit Minute: ' + version_info_string[14:16]  # grab the minute of the last acd edit
        acd_second = 'Last Edit Minute: ' + version_info_string[17:19]  # grab the second of the last acd edit
        acd_millisecond = 'Last Edit Millisecond: ' + version_info_string[20:23]  # grab the msec of the last acd edit
        acd_major_version = 'Logix 5000 Major Version: ' + version_info_string[34:36]  # grab the major version
        acd_minor_version = 'Logix 5000 Minor Version: ' + version_info_string[37:42]  # grab the minor version
        acd_build_number = 'Logix 5000 Build Number: ' + version_info_string[43:51]  # grab the build number

        # Begin Generation of the AOI Analysis Text File
        analysis_file = file
        analysis_file.write("********************************************************* \n")
        analysis_file.write("Automated Analysis Performed By ACD Forensics Version 1.0 \n")
        analysis_file.write("********************************************************* \n")
        analysis_file.write("\n")
        analysis_file.write("********************************************* \n")
        analysis_file.write("***********General ACD Information*********** \n")
        analysis_file.write("********************************************* \n")
        analysis_file.write("\n")
        analysis_file.write(acd_name + "\n")
        analysis_file.write("\n")
        analysis_file.write(acd_major_version + "\n")
        analysis_file.write(acd_minor_version + "\n")
        analysis_file.write(acd_build_number + "\n")
        analysis_file.write("\n")
        analysis_file.write(acd_year + "\n")
        analysis_file.write(acd_month + "\n")
        analysis_file.write(acd_day + "\n")
        analysis_file.write(acd_hour + "\n")
        analysis_file.write(acd_minute + "\n")
        analysis_file.write(acd_second + "\n")
        analysis_file.write(acd_millisecond + "\n")
        analysis_file.write("\n")
        analysis_file.write("********************************************* \n")
        analysis_file.write("**********General File Information*********** \n")
        analysis_file.write("********************************************* \n")
        analysis_file.write("\n")
        analysis_file.write(general_modified_date + "\n")
        analysis_file.write("\n")

        status5 = main.Label(root, text='ACD Analysis Complete, Please Exit.',
                             fg='black', bg='White', font=('Segoe', 8,))
        canvas1.create_window(101, 258, window=status5)

    else:
        status3 = main.Label(root, text='File Type Check Status: FAIL (Logix5000 Project).', fg='black',
                             bg='White',
                             font=('Segoe', 8,))
        canvas1.create_window(134, 226, window=status3)

        status4 = main.Label(root, text='Process Aborted.', fg='black', bg='White', font=('Segoe', 8,))
        canvas1.create_window(56, 242, window=status4)


def analyze_button():  # Generates the analyze button, on click this guy calls analyze_file.
    analyze_file_button = main.Button(text='Analyze File', command=analyze_file, )
    canvas1.create_window(275, 155, window=analyze_file_button)


def callback(url):  # callback function. This guy lets us use URLs in an application.
    webbrowser.open_new(url)


# -----------------------------------END FUNCTION DEFINITIONS------------------------------

root = main.Tk()

# Set The Icon
root.iconbitmap(icoImage)

# Paint the canvas
canvas1 = main.Canvas(root, width=550, height=400)
canvas1.winfo_toplevel().title("ACD Forensics Version 1.0")
canvas1.pack()

# Create Status Box
canvas1.create_rectangle(10, 175, 540, 300, fill="white")

# Create Selected Filepath Box
canvas1.create_rectangle(10, 105, 425, 128, fill="white")

# Paint The Utility Logo
loadUtilityLogo = loadLogo = ImageTk.PhotoImage(Image.open(utilityImage))
canvas1.create_image(275, 25, image=loadLogo)

# Generate the Static Text
static_description_text()

# Generate Buttons and Option Radio Selections
browse_button()
analyze_button()

# Generate Static Status Text
static_status_text()

# Shameless Self Marketing (Psssst, I'm looking for a job in ICS cybersecurity!)
loadLogo = ImageTk.PhotoImage(Image.open(logoImage))
canvas1.create_image(250, 360, image=loadLogo)

link1 = main.Label(root, text="https://alexholburn.com/", fg="blue", font=('Segoe', 8, 'underline'), cursor="hand2")
link1.pack()
link1.bind("<Button-1>", lambda e: callback("https://alexholburn.com/"))

# Loop so the window appears
root.mainloop()
