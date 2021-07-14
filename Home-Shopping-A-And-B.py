
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n10464948
#    Student name: Samuel Robinson
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#


#-----Assignment Description-----------------------------------------#
#
#  Stay at Home Shopping
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for simulating an online shopping experience. See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#


#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these functions
# only.  You can import other functions provided they are standard
# ones that come with the default Python/IDLE implementation and NOT
# functions from modules that need to be downloaded and installed
# separately.  Note that not all of the imported functions below are
# needed to successfully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import some standard Tkinter functions. (You WILL need to use
# some of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#


#--------------------------------------------------------------------#
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will try to hide its
#      identity from the web server. This can sometimes be used
#      to prevent the server from blocking access to Python
#      programs. However we do NOT encourage using this option
#      as it is both unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message above about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#


#--------------------------------------------------------------------#
#
# A function to open a local HTML document in your operating
# system's default web browser.  (Note that Python's "webbrowser"
# module does not guarantee to open local files, even if you use a
# 'file://..." URL). The file to be opened must be in the same folder
# as this module.
#
# Since this code is platform-dependent we do NOT guarantee that it
# will work on all systems.
#
def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import isfile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not isfile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))

#
#--------------------------------------------------------------------#


#-----Student's Solution---------------------------------------------#
#

# Please be advised that ebay's online webpage updates quickly! To find
# specific items you may need to scroll down the official webpage.

# 1. Initialize variables.
# 1a. Setup colours for the frames of the GUI and the HTML divs.
# bg refers to the background, whereas fg refers to the foreground (text).
header_bg = "#6DAFFE" # Light-blue.
header_fg = "#FFFFFF" # White.
main_bg = "#FFFFFF" # Light-blue
widget_bg = "#EDF6FF" # Very light-blue.
widget_title_bg = "#DBEDFF" # Very light-blue, slightly more saturation.
footer_fg = "#FFFFFF" # White.
footer_bg = "#437FC7" # Dark-blue.
# 1b. Setup colours exclusively for the HTML divs.
photo_box_fg = "#000000" # Black.
number_label_bg = "#FE6D6D;" # Light-red.
container_fg = "#000000" # Black.
# 1c. Setup diffirent typefaces for the GUI.
small_font = "Arial", 9, "normal"
small_bold_font = "Arial", 9, "bold"
large_font = "Arial", 20, "italic"
# 1d. Setup variables to remember the details of the brand and selected bundle.
brand_name = "Poly Deliver"
bundle = ""
url_source = ""
host = ""
image1 = ""
name1 = ""
cost1 = ""
image2 = ""
name2 = ""
cost2 = ""
image3 = ""
name3 = ""
cost3 = ""
image4 = ""
name4 = ""
cost4 = ""
image5 = ""
name5 = ""
cost5 = ""
# 1e. Setup a list to rememebr the name and cost of each item inside the cart.
cart_name_collation = []
cart_cost_collation = []
# 1f. Establish a file name for receiving exported product images.
html_image_display = 'Product-Images.html'

#2. Analyse the date of bundles within each online or offline webpage.
def list_items_in_bundle():
    # 2a. Reference the variables from 1d for editing.
    global bundle, url_source, host
    global image1, image2, image3, image4, image5
    global name1, name2, name3, name4, name5
    global cost1, cost2, cost3, cost4, cost5
    # 2b. Assign a variable to remember the first five items in each extraction.
    first_five_items = ""
    # 2c. Establish regular expressions (regex) to find specific page elements.
    # .*? matches every character throughout a text or up to a given point.
    # This method can be more reliable but often has more steps to run.
    amazon_image_regex = "<img.*?>"
    amazon_name_regex = "<div[A-Za-z0-9\"-=> ]+\n +(.*?)\n +<\/div>"
    amazon_cost_regex = "<span[a-z0-9-=' ]+ >([$0-9.]*)<\/span><\/span>"
    ebay_image_regex = "<img.*?>"
    ebay_name_regex = "<h3.*?<\/span>(.*?)<\/h3>"
    ebay_cost_regex = "<span[a-z-_=\" ]+>([A-Z0-9$,. ]+)<"
    # 2d. Perform an online extraction for Ebay.
    try:
        if bundle_selection.get() == 1:
            # 2d-a. Clear the bundle list to display new products.
            empty_bundle_list()
            # 2d-b. Set basic information about the bundle.
            bundle = "Computers & Tablets"
            url_source = "https://www.ebay.com.au/b/Computers-Tablets-Network-Hardware/58058/bn_1843425?rt=nc&_sop=10"
            host = "Ebay"
            # 2d-c. Open and decode the webpage using 8-bit unicode.
            webpage = urlopen(url_source)
            webpage_bytes = webpage.read().decode("UTF-8")
            # 2d-d. Extract the chunk of the page containing the image gallery.
            start_mark = '<ul class="b-list__items_nofooter">'
            end_mark = '<div class="b-pagination">'
            start_position = webpage_bytes.find(start_mark)
            end_position = webpage_bytes.find(end_mark)
            extract_main = webpage_bytes[start_position: end_position]
            # 2d-e. Extract the first five list items.
            # Increment the start and end positions to find each instance,
            # place the index slices into variables to gather their data.
            start_mark = '<li class'
            end_mark = '</li>'
            start_position = extract_main.find(start_mark) - 1
            end_position = extract_main.find(end_mark) - 1
            for list_items in range(5):
                if start_position != -1 or end_position != -1: # if existent.
                    start_position = extract_main.find(start_mark,\
                                                 start_position + 1)
                    end_position = extract_main.find(end_mark, end_position + 1)
                first_five_items += extract_main[start_position: end_position\
                                                 + len(end_mark)]
            # 2d-f. Find each HTML tag containing images, names, and costs.
            image_extraction = findall(ebay_image_regex, first_five_items)
            name_extraction = findall(ebay_name_regex, first_five_items)
            cost_extraction = findall(ebay_cost_regex, first_five_items)
            # 2d-g. Destructure the result and place each item inside a list.
            image1, image2, image3, image4, image5 = image_extraction
            name1, name2, name3, name4, name5 = name_extraction
            cost1, cost2, cost3, cost4, cost5 = cost_extraction
            # 2d-h. Insert the five products into the bundle_list.
            # In a list 0.0 refers to a line's number and character index.
            bundle_list.config(state = "normal") # Allow widget modifications.
            bundle_list.insert(1.0, "\u25CF " + name1 + " - " + cost1 + "\n")
            bundle_list.insert(2.0, "\u25CF " + name2 + " - " + cost2 + "\n")
            bundle_list.insert(3.0, "\u25CF " + name3 + " - " + cost3 + "\n")
            bundle_list.insert(4.0, "\u25CF " + name4 + " - " + cost4 + "\n")
            bundle_list.insert(5.0, "\u25CF " + name5 + " - " + cost5)
            bundle_list.config(state = "disable") # Prevent widget modifcations.
    # 2e. Opening the URL or extracting data failed, display an error message.
    except Exception:
        print("Cannot analyse bundle 1!")
        bundle_list.config(state="normal") # Enable widget editing.
        bundle_list.insert(1.0,\
                        "\u274C An error occured, sorry for the inconvenience.")
        bundle_list.config(fg = "red")
        bundle_list.config(state = "disabled") # Disable widget editing.

    # 2f. Perform an online extraction for Amazon.
    try:
        if bundle_selection.get() == 2:
            # 2f-a. Clear the bundle list to display new products.
            empty_bundle_list()
            # 2f-b. Set basic information about the bundle.
            bundle = "Baby Product"
            url_source = "https://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products"
            host = "Amazon"
            # 2f-c. Open and decode the webpage using 8-bit unicode.
            webpage = urlopen(url_source)
            webpage_bytes = webpage.read().decode("UTF-8")
            # 2f-d. Extract the chunk of the page containing the image gallery.
            start_mark = '<div id="zg_pageInfo" initialload="true" page="1">'
            end_mark = '<div class="a-row a-spacing-top-mini">'
            start_position = webpage_bytes.find(start_mark)
            end_position = webpage_bytes.find(end_mark)
            extract_main = webpage_bytes[start_position: end_position]
            # 2f-e. Extract the first five list items.
            # Increment the start and end positions to find each instance,
            # place the index slices into variables to gather their data.
            start_mark = '<li class'
            end_mark = '</li>'
            start_position = extract_main.find(start_mark) - 1
            end_position = extract_main.find(end_mark) - 1
            for list_items in range(5):
                if start_position != -1 or end_position != -1: # if existent.
                    start_position = extract_main.find(start_mark,\
                                                 start_position + 1)
                    end_position = extract_main.find(end_mark, end_position + 1)
                first_five_items += extract_main[start_position: end_position\
                                                 + len(end_mark)]
            # 2f-f. Find each HTML tag containing images, names, and costs.
            image_extraction = findall(amazon_image_regex, first_five_items)
            name_exctration = findall(amazon_name_regex, first_five_items)
            cost_exctraction = findall(amazon_cost_regex, first_five_items)
            # 2f-g. Destructure the result and place each item inside a list.
            image1, image2, image3, image4, image5 = image_extraction
            name1, name2, name3, name4, name5 = name_exctration
            cost1, cost2, cost3, cost4, cost5 = cost_exctraction
            # 2f-h. Insert the five products into the bundle_list.
            # In a list 0.0 refers to a line's number and character index.
            bundle_list.config(state = "normal") # Allow widget modifications.
            bundle_list.insert(1.0, "\u25CF " + name1 + " - " + cost1 + "\n")
            bundle_list.insert(2.0, "\u25CF " + name2 + " - " + cost2 + "\n")
            bundle_list.insert(3.0, "\u25CF " + name3 + " - " + cost3 + "\n")
            bundle_list.insert(4.0, "\u25CF " + name4 + " - " + cost4 + "\n")
            bundle_list.insert(5.0, "\u25CF " + name5 + " - " + cost5)
            bundle_list.config(state = "disable") # Prevent widget modifcations.
    # 2g. Opening the URL or extracting data failed, display an error message.
    except Exception:
        print("Cannot analyse bundle 2!")
        bundle_list.config(state="normal") # Enable widget editing.
        bundle_list.insert(1.0,\
                        "\u274C An error occured, sorry for the inconvenience.")
        bundle_list.config(fg = "red")
        bundle_list.config(state = "disabled") # Disable widget editing.
        
    # 2h. Perform an offline extraction for Ebay.
    try:
        if bundle_selection.get() == 3:
            # 2h-a. Clear the bundle list to display new products.
            empty_bundle_list()
            # 2h-b. Set basic information about the bundle.
            bundle = "Vitamins & Food Supplements"
            url_source = "https://www.ebay.com.au/b/Vitamins-Dietary-Supplements/180959/bn_7203371?rt=nc&_sop=10"
            host = "Ebay (Local)"
            # 2h-c. Open with read mode, default buffering, and 8-bit unicode.
            webpage = open("Ebay-Vitamins-And-Food-Supplements.html", "r", -1,\
                           "UTF-8").read()
            # 2h-d. Extract the chunk of the page containing the image gallery.
            start_mark = '<ul class="b-list__items_nofooter">'
            end_mark = '<div class="b-pagination">'
            start_position = webpage.find(start_mark)
            end_position = webpage.find(end_mark)
            extract_main = webpage[start_position: end_position]
            # 2h-e. Extract the first five list items.
            # Increment the start and end positions to find each instance,
            # place the index slices into variables to gather their data.
            start_mark = '<li class'
            end_mark = '</li>'
            start_position = extract_main.find(start_mark) - 1
            end_position = extract_main.find(end_mark) - 1
            for list_items in range(5):
                if start_position != -1 or end_position != -1: # if existent.
                    start_position = extract_main.find(start_mark,\
                                                 start_position + 1)
                    end_position = extract_main.find(end_mark, end_position + 1)
                first_five_items += extract_main[start_position: end_position\
                                                 + len(end_mark)]
            # 2h-f. Find each HTML tag containing images, names, and costs.
            image_extraction = findall(ebay_image_regex, first_five_items)
            name_extraction = findall(ebay_name_regex, first_five_items)
            cost_extraction = findall(ebay_cost_regex, first_five_items)
            # 2h-g. Destructure the result and place each item inside a list.
            image1, image2, image3, image4, image5 = image_extraction
            name1, name2, name3, name4, name5 = name_extraction
            cost1, cost2, cost3, cost4, cost5 = cost_extraction
            # 2h-h. Insert the five products into the bundle_list.
            # In a list 0.0 refers to a line's number and character index.
            bundle_list.config(state = "normal") # Allow widget modifications.
            bundle_list.insert(1.0, "\u25CF " + name1 + " - " + cost1 + "\n")
            bundle_list.insert(2.0, "\u25CF " + name2 + " - " + cost2 + "\n")
            bundle_list.insert(3.0, "\u25CF " + name3 + " - " + cost3 + "\n")
            bundle_list.insert(4.0, "\u25CF " + name4 + " - " + cost4 + "\n")
            bundle_list.insert(5.0, "\u25CF " + name5 + " - " + cost5)
            bundle_list.config(state = "disable") # Prevent widget modifcations.
    # 2i. Opening the URL or extracting data failed, display an error message.
    except Exception:
        print("Cannot analyse bundle 3!")
        bundle_list.config(state="normal") # Enable widget editing.
        bundle_list.insert(1.0,\
                        "\u274C An error occured, sorry for the inconvenience.")
        bundle_list.config(fg = "red")
        bundle_list.config(state = "disabled") # Disable widget editing.
        
    # 2j. Perform an offline extraction for Amazon.
    try:
        if bundle_selection.get() == 4:
            # 2j-a. Clear the bundle list to display new products.
            empty_bundle_list()
            # 2j-b. Set basic information about the bundle.
            bundle = "Video Game"
            url_source = "https://www.amazon.com/best-sellers-video-games/zgbs/videogames"
            host = "Amazon (Local)"
            # 2j-c. Open with read mode, default buffering, and 8-bit unicode.
            webpage = open("Amazon-Video-Games.html", "r", -1, "UTF-8").read()
            # 2j-d. Extract the chunk of the page containing the image gallery.
            start_mark = '<div id="zg_pageInfo" initialload="true" page="1">'
            end_mark = '<div class="a-row a-spacing-top-mini">'
            start_position = webpage.find(start_mark)
            end_position = webpage.find(end_mark)
            extract_main = webpage[start_position: end_position]
            # 2j-e. Extract the first five list items.
            # Increment the start and end positions to find each instance,
            # place the index slices into variables to gather their data.
            start_mark = '<li class'
            end_mark = '</li>'
            start_position = extract_main.find(start_mark) - 1
            end_position = extract_main.find(end_mark) - 1
            for list_items in range(5):
                if start_position != -1 or end_position != -1: # if existent.
                    start_position = extract_main.find(start_mark,\
                                                 start_position + 1)
                    end_position = extract_main.find(end_mark, end_position + 1)
                first_five_items += extract_main[start_position: end_position\
                                                 + len(end_mark)]
            # 2j-f. Find each HTML tag containing images, names, and costs.
            image_extraction = findall(amazon_image_regex, first_five_items)
            name_exctration = findall(amazon_name_regex, first_five_items)
            cost_exctraction = findall(amazon_cost_regex, first_five_items)
            # 2j-g. Destructure the result and place each item inside a list.
            image1, image2, image3, image4, image5 = image_extraction
            name1, name2, name3, name4, name5 = name_exctration
            cost1, cost2, cost3, cost4, cost5 = cost_exctraction
            # 2j-h. Insert the five products into the bundle_list.
            # In a list 0.0 refers to a line's number and character index.
            bundle_list.config(state = "normal") # Allow widget modifications.
            bundle_list.insert(1.0, "\u25CF " + name1 + " - " + cost1 + "\n")
            bundle_list.insert(2.0, "\u25CF " + name2 + " - " + cost2 + "\n")
            bundle_list.insert(3.0, "\u25CF " + name3 + " - " + cost3 + "\n")
            bundle_list.insert(4.0, "\u25CF " + name4 + " - " + cost4 + "\n")
            bundle_list.insert(5.0, "\u25CF " + name5 + " - " + cost5)
            bundle_list.config(state = "disable") # Prevent widget modifcations.
    # 2k. Opening the URL or extracting data failed, display an error message.
    except Exception:
        print("Cannot analyse bundle 4!")
        bundle_list.config(state="normal") # Enable widget editing.
        bundle_list.insert(1.0,\
                        "\u274C An error occured, sorry for the inconvenience.")
        bundle_list.config(fg = "red")
        bundle_list.config(state = "disabled") # Disable widget editing.

# 3. Setup a HTML document to display the product imagess in a specific bundle.
def create_html(brand, category, url, host, photo1, label1, photo2, label2,\
                photo3, label3, photo4, label4, photo5, label5):
    # 3a. Open the webpage in write mode using an 8-bit unicode character set.
    html_file = open(file=html_image_display, mode="w", encoding="UTF-8")
    # 3b. Generate a HTML file.
    # Using a doc string retains the formatting of the code and reduces the need
    # to use write functions and newline characters. Despite using literal
    # positioning I have kept the doc string indented to improve readability.

    # The file uses a basic header, main, and footer structure. Inside the main
    # div there is a photo gallery which displays images like instant film.

    # All of the global variables assigned to remember the section colours and
    # bundle data are inserted into the write function, only internal CSS
    # commands end in a semicolon.
    
    html_file.write("""\
    <!doctype html>
    <html lang="en">

    <!-- Webpage Properties -->
    <head>
    <meta charset="UTF-8">
    <meta name="author" content="Samuel Robinson">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Product Images</title>
    
    <!-- Internal CSS Styles -->
    <style>
    *{ /* Apply properties to every element on the webpage */
            margin: 0px; /* Remove default margins to fit all elements */
            box-sizing: border-box; /* Measurements include padding and borders */
            overflow-x: hidden; /* Remove the scrollbar for the x-axis */
    }
    body{
            font-family: Arial, Helvetica, sans-serif;
    }
    header{
            height: 12vh; /* Percentage of viewport height */
            width: 100vw; /* Percentage of viewport width */
            margin: auto;
            padding-left: 32px;
            font-style: italic;
            color: """ + header_fg + ";" """
            background-color: """ + header_bg + ";" """
    }
    header img{
            float: left; /* The left and right location of an element */
    }
    header h1{
            position: absolute; /* Placed at parent element */
            left: 20px;
    }
    main{
            height: auto;
            min-height: calc(100vh - 12vh - 48px); /* Subtract header and footer height */
            width: 100vw; /* Percentage of viewport width */
            padding-top: 20px;
            background-color: """ + main_bg + ";" """
    }
    #container{
            height: auto;
            width: 80%;
            padding: 16px 24px 24px 24px; /* Top, right, bottom, left */
            margin: 0px auto 20px auto; /* Top, right, bottom, left */
            text-align: center;
            background-color: """ + widget_title_bg + ";" """
    }
    #container h2{
            color: """ + container_fg + ";" """
            opacity: 60%;
    }
    #container h4{
            color: """ + container_fg + ";" """
            opacity: 60%;
    }    
    #gallery-container{
            height: 90%;
            width: 100%;
            margin: 16px auto 0px auto; /* Top, right, bottom, left */
            padding: 16px;
            background-color: """ + widget_bg + ";" """
    }
    #photo-box{
            display: inline-block; /* Occupy space within the tag */
            width: 260px;
            overflow: hidden; /* Remove any scrollbars */
            margin: 12px;
            padding-top: 20px;
            text-align: justify; /* Fill a div with equal gaps between words */
            box-shadow: 3px 3px 15px 0px rgba(0,0,0,0.2); /* x, y, blur, spread, (rgba) */
    }
    #photo-box p{
            display: block; /* Start on a new line and fill a div's width */
            position: relative; /* Placed near its original location */
            padding: 8px;
            font-size: 13px;
            color: """ + photo_box_fg + ";" """
            opacity: 60%;
    }
    #photo{
            height: 220px;
            width: 100%;
            margin: 0 auto;
    }
    #photo img{
            display: block; /* Start on a new line and fill a div's width */
            height: 100%;
            width: 100%;
            object-fit: contain; /* Shrink the image to keep its aspect ratio */
    }
    #number-label{
            position: absolute; /* Placed at parent element */
            height: 28px;
            width: 40px;
            clip-path: polygon(0% 0%, 75% 0%, 100% 50%, 75% 100%, 0% 100%);
            /* Shape, (three or more relative percentage points) */
            margin-top: -20px; /* Reference padding-top from photo-box */
            text-align: center;
            background-color: """ + number_label_bg + ";" """
    }
    #number-label h5{
            /* p tags conflict with photo-box p tags, thus h5 is used instead */
            line-height: 28px; /* Reference height from number-label */
            font-size: 14px;
            font-weight: normal; /* Give the font a standard thickness. */
            color: """ + header_fg + ";" """
    }
    footer{
            width: 100vw; /* Percentage of viewport width */
            padding: 16px;
            text-align: center;
            color: """ + footer_fg + ";" """
            background-color: """ + footer_bg + ";" """
    }
    .verticalAlign{
            position: relative; /* Placed near its original location */
            top: 50%; /* Move vertically to the centre of an element */
            transform: translateY(-50%); /* Compensate for the movement */
    }
    @media all and (min-width: 640px) { /* If screen is > 640px resize list-item */
      .list-item {
        width: 50%;
      }
    }
    @media all and (min-width: 960px) { /* If screen is > 960px resize list-item */
      .list-item {
        width: 33.3%;
      }
    }
    .list{
            display: flex; /* Start on a new line and fill an element's space */
            flex-wrap: wrap; /* Move overflowing flex items to a new line */
    }
    .list-item{
            display: flex; /* Start on a new line and fill an element's space */
            width 100%;
            padding: 6px;
    }
    </style>
    </head>

    <!-- Webpage Contents -->
    <body>
    <header>
    <!-- Logo design courtesy of wwww.freelogodesign.org -->
    <img class='verticalAlign' src='Logo.gif' alt='Logo' height=64 width=64>
    <h1 class='verticalAlign'>""" + brand + """</h1>
    </header>

    <main>
    <!-- Generic content box -->
    <div id='container'>
    <h2>""" + category + """ Bundle</h2>
    <h4>Source Webpage: <a href='""" + url + """'>""" + host + """</a></h4>

    <!-- Image gallery -->
    <div id=gallery-container>
    <ul class="list">
    <!-- Product 1 -->
    <li class="list-item">
    <div id=photo-box>
    <div id=number-label><h5>#1</h5></div>
    <div id=photo>""" + photo1 + """</div><p><b>""" + label1 + """</b></p></div>
    </li>
    <!-- Product 2 -->
    <li class="list-item">
    <div id=photo-box>
    <div id=number-label><h5>#2</h5></div>
    <div id=photo>""" + photo2 + """</div><p><b>""" + label2 + """</b></p></div>
    </li>
    <!-- Product 3 -->
    <li class="list-item">
    <div id=photo-box>
    <div id=number-label><h5>#3</h5></div>
    <div id=photo>""" + photo3 + """</div><p><b>""" + label3 + """</b></p></div>
    </li>
    <!-- Product 4 -->
    <li class="list-item">
    <div id=photo-box>
    <div id=number-label><h5>#4</h5></div>
    <div id=photo>""" + photo4 + """</div><p><b>""" + label4 + """</b></p></div>
    </li>
    <!-- Product 5 -->
    <li class="list-item">
    <div id=photo-box>
    <div id=number-label><h5>#5</h5></div>
    <div id=photo>""" + photo5 + """</div><p><b>""" + label5 + """</b></p></div>
    </li>
    </ul>
    <!-- gallery-container end -->
    </div>
    
    <!-- container end -->
    </div>
    </main>

    <footer>
    <p>&copy; 2020 Samuel Robinson. Images may be subject to copyright.</p>
    </footer>
    
    </body>
    
    </html>""")
    print("Generated a HTML file for displaying bundle images.")
    # 3c. Safely close the file to prevent umexpected errors.
    html_file.close()
    # 3d. Attempt to open the generated HTML file using a web browser.
    open_html_file(html_image_display)

# 4. Create a HTML file to display the images in the product bundle.
def display_product_images():
    # 4a. Attempt to display bundle data.
    # As long as a bundle is chosen users can see bundle data anytime.
    try:
        # 4c. Test if bundle data is blank.
        if "" not in (bundle, url_source, host, image1, name1, image2, name2,\
                    image3, name3, image4, name4, image5, name5):
            # 4e. For each selection generate a HTML file with the bundle data.
            if bundle_selection.get() == 1:
                create_html(brand_name, bundle, url_source, host, image1, name1,\
                    image2, name2, image3, name3, image4, name4, image5, name5)
            elif bundle_selection.get() == 2:     
                create_html(brand_name, bundle, url_source, host, image1, name1,\
                    image2, name2, image3, name3, image4, name4, image5, name5)
            elif bundle_selection.get() == 3:     
                create_html(brand_name, bundle, url_source, host, image1, name1,\
                    image2, name2, image3, name3, image4, name4, image5, name5)
            else: # bundle_selection equals 4.
                create_html(brand_name, bundle, url_source, host, image1, name1,\
                    image2, name2, image3, name3, image4, name4, image5, name5)
        #  4d. Bundle selection or data is blank, display an error message.
        else:
            print("Cannot export images, some bundle data is blank!")
            empty_bundle_list() # Clear the bundle list to display error messages.
            bundle_list.config(state="normal") # Enable widget editing.
            bundle_list.insert(1.0,\
                        "\u274C Please select a product bundle to begin.")
            bundle_list.config(fg = "red")
            bundle_list.config(state = "disabled") # Disable widget editing.
    # 4b. Bundle selection or data is blank, display an error message.
    except Exception:
        print("Cannot export images, some bundle data is blank!")
        empty_bundle_list() # Clear the bundle list to display error messages.
        bundle_list.config(state="normal") # Enable widget editing.
        bundle_list.insert(1.0,\
                        "\u274C Please select a product bundle to begin.")
        bundle_list.config(fg = "red")
        bundle_list.config(state = "disabled") # Disable widget editing.

# 5. Add items from the bundle_list to the cart_list and collation lists.
def add_to_cart():
    # 5a. Reference the variables from 1e for editing.
    global cart_name_collation, cart_cost_collation
    # 5b. Test if the product names within bundle data are not blank.
    # It's not necessary to test for prices as names suffice for both.
    if "" not in (name1, name2, name3, name4, name5):
        # 5d. Add each unique bundle to the cart.
        cart_list.config(state = "normal") # Enable widget editing.
        if name1 not in cart_name_collation\
           and name2 not in cart_name_collation\
           and name3 not in cart_name_collation\
           and name4 not in cart_name_collation\
           and name5 not in cart_name_collation:
            cart_list.insert(END, "\u25CF " + name1 + "\n")
            cart_list.insert(END, "\u25CF " + name2 + "\n")
            cart_list.insert(END, "\u25CF " + name3 + "\n")
            cart_list.insert(END, "\u25CF " + name4 + "\n")
            cart_list.insert(END, "\u25CF " + name5 + "\n")
            cart_name_collation += (name1, name2, name3, name4, name5)
            cart_cost_collation += (cost1, cost2, cost3, cost4, cost5)
            print("Addeded the unique product bundle to the cart.")
        # 5e. The products are already in the cart, display an error message.
        else:
            print("The products are already in the cart!")
            empty_bundle_list()
            bundle_list.config(state="normal") # Enable widget editing.
            bundle_list.insert(1.0,\
                "\u274C The products you requested are already in the cart.")
            bundle_list.config(fg = "red")
            bundle_list.config(state = "disabled") # Disable widget editing.
        cart_list.config(state = "disable") # Disable widget editing.
    else:
        # 5c. Bundle data is blank, display an error message.
        print("Cannot add the bundle to the cart, some names are blank!")
        empty_bundle_list() # Clear the bundle list to display error messages.
        bundle_list.config(state="normal") # Enable widget editing.
        bundle_list.insert(1.0, "\u274C Please select a product bundle to begin.")
        bundle_list.config(fg = "red")
        bundle_list.config(state = "disabled") # Disable widget editing.

# 6. Clear all contents from the bundle_list.
def empty_bundle_list():
    bundle_list.config(fg = "black") # Reset the font colour after events.
    bundle_list.config(state = "normal") # Enable widget editing.
    bundle_list.delete("1.0", "end") # Delete text from lines 1 to end (5).
    bundle_list.config(state = "disabled") # Disable widget editing.
##    print("Emptied the bundle list and reset its text colour.")

# 7. Clear all contents from the cart_list and both collation lists.
def empty_cart():
    # 7a. Reference the variables from 1d and 1e for editing.
    global image1, image2, image3, image4, image5
    global cart_name_collation, cart_cost_collation
    # 7b. Remove all list items from the cart_list
    # The cart can always be emptied regardless of its contents.
    cart_list.config(state="normal") # Enable widget editing.
    cart_list.delete("1.0", "end") # Delete text from lines 1 to end (5).
    cart_list.config(state="disabled") # Disable widget editing.
    # 7c. Remove all list items from both collation lists.
    cart_name_collation = []
    cart_cost_collation = []
    print("Emptied the cart and reset bundle data.")

# 8. Add the names and costs of each item in the cart to a database.
def submit_order():
    # 8a. Reference the variables from 1e for editing.
    global cart_name_collation, cart_cost_collation
    # 8b. Test if both collation lists are not blank.
    if "" not in cart_name_collation and cart_cost_collation:
        # 8d. Attempt to clear and modify the database, and erase lists.
        try:
            # 8f. Connect to the database. 
            connection = connect("Orders.db")
            # 8g. Attatch a cursor to perform commands.
            database = connection.cursor()
            # 8h. Clear the table to prevent duplicate items.
            database.execute("""DELETE FROM CustomerOrders""")
            # 8i. Setup a counter to remember the iteration of the loop.
            index = -1 # An index always equals n-1, thus [3] equals position 2.
            # 8j. Insert the name and cost of products into appropriate columns.
            for products in range(len(cart_name_collation)):
                index += 1
                syntax_free_name = cart_name_collation[index].replace("'", "")
                database.execute("""
                INSERT INTO CustomerOrders(Product, Price)
                VALUES('""" + syntax_free_name + """', '""" +\
                                 cart_cost_collation[index] + """')
                """)
            # 8k. Write all changes to the database.
            connection.commit()
            # 8l. Safely close the database to prevent any unexpected errors.
            connection.close()
            print("Product information was written to the database.")
            # 8m. Display a confirmation message in the bundle_list.
            empty_bundle_list()
            bundle_list.config(state="normal") # Enable widget editing.
            bundle_list.insert(1.0,\
                            "\u2713 Your order was received, happy shopping!")
            bundle_list.config(fg = "green")
            bundle_list.config(state = "disabled") # Disable widget editing.
            # 8n. Clear all contents from the cart_list.
            cart_list.config(state="normal") # Enable widget editing.
            cart_list.delete("1.0", "end") # Delete text from lines 1 to end (5).
            cart_list.config(state="disabled") # Disable widget editing.
            # 8o. Clear all contents from both collation lists.
            cart_name_collation = []
            cart_cost_collation = []
        # 8e. If the data couldn't be written display an error message.
        except Exception:
            print("Cannot write product names and costs to the database.")
            empty_bundle_list() # Clear the bundle list to display error messages.
            bundle_list.config(state="normal") # Enable widget editing.
            bundle_list.insert(1.0,\
                        "\u274C An error occured, sorry for the inconvenience.")
            bundle_list.config(fg = "red")
            bundle_list.config(state = "disabled") # Disable widget editing.
    # 8c. If no products were added to the cart display an error message.
    else:
        print("Cannot submit order, the cart is empty!")
        empty_bundle_list() # Clear the bundle list to display error messages.
        bundle_list.config(state="normal") # Enable widget editing.
        bundle_list.insert(1.0,\
            "\u274C Please add a product bundle to the cart before submitting.")
        bundle_list.config(fg = "red")
        bundle_list.config(state = "disabled") # Disable widget editing.

# 9. Create the root window for the graphical user interface (GUI).
root_window = Tk()
root_window.title("Warehouse Communication App")
root_window.resizable(width=False, height=False)

# 10. Establish a variable to remember the state of each radio button.
bundle_selection = IntVar()

# 11. Create and place each frame in the root window.
# 11a. Setup and place the header frame.
header_frame = Frame(root_window, width=640, height=90, padx=12, pady=12,\
                     bg=header_bg)
header_frame.grid(column=0, row=0, sticky="W")
header_frame.grid_propagate(False) # Should the frame resize to its widgets?
# 11b. Setup and place the left body frame.
left_body_frame = Frame(root_window, width=224, height=376, padx=12, pady=12,\
                        bg=main_bg)
left_body_frame.grid(column=0, row=1, sticky="w")
left_body_frame.grid_propagate(False)
# 11c. Setup and place the right body frame.
right_body_frame = Frame(root_window, width=416, height=376,\
                    padx=12, pady=12, bg=main_bg)
right_body_frame.grid(column=0, row=1, sticky="e")
right_body_frame.grid_propagate(False)
# 11d. Setup and place the live stock frame.
live_stock_frame = LabelFrame(left_body_frame, text="New shipments",\
                    font=(small_bold_font), width=200, height=75, bg=widget_bg)
live_stock_frame.grid(column = 0, row=0, padx=0, pady=8)
live_stock_frame.grid_propagate(False)
# 11e. Setup and place the old stock frame.
old_stock_frame = LabelFrame(left_body_frame, text = "Inventory",\
                    font=(small_bold_font), width=200, height=75, bg=widget_bg)
old_stock_frame.grid(column=0, row=1, padx=0, pady=8)
old_stock_frame.grid_propagate(False)
# 11f. Setup and place the item frame.
bundle_frame = Frame(right_body_frame)
bundle_frame.grid(column=1, row=0, pady=8)
# 11g. Setup and place the cart frame.
cart_frame = Frame(right_body_frame)
cart_frame.grid(column=1, row=1, padx=0, pady=8)
cart_scroll_frame = Frame(cart_frame, bg="orange")
cart_scroll_frame.grid(column=0, row=1, sticky="e", pady=8)
# 11h. Setup and place the footer frame.
footer_frame = Frame(root_window, width=640, height=45, padx=12, pady=12,\
                    bg=footer_bg)
footer_frame.grid(column=0, row=5)
footer_frame.grid_propagate(False)

# 12. Create and place each widget inside the previous frames.
# 12a. Setup and place the store title.
store_title = Label(header_frame, text=brand_name, font=(large_font),\
                    bg=header_bg, fg=header_fg)
store_title.grid(column=1, row=0, padx=12)
# 12b. Setup and place the store logo.
logo_canvas = Canvas(header_frame, width=64, height=64, bg=header_bg,\
                     highlightthickness=0)
logo_canvas.grid(column=0, row=0)
logo_photo = PhotoImage(file="Logo.gif")
logo_canvas.create_image(0, 0, image=logo_photo, anchor=NW)
# 12c. Setup and place the bundle 1 selection radio button.
bundle_selection1 = Radiobutton(live_stock_frame, text="Computers & tablets",\
    font=(small_font), bg=widget_bg, activebackground=widget_bg, cursor="hand2",\
    value=1, variable=bundle_selection, command=list_items_in_bundle,\
    tristatevalue="a")
bundle_selection1.grid(column=0, row=0, sticky="w")
# 12d. Setup and place the bundle 2 selection radio button.
bundle_selection2 = Radiobutton(live_stock_frame, text="Baby products",\
    font=(small_font), bg=widget_bg, activebackground=widget_bg, cursor="hand2",\
    value=2, variable=bundle_selection, command=list_items_in_bundle,\
    tristatevalue="a")
bundle_selection2.grid(column=0, row=1, sticky="w")
# 12e. Setup and place the bundle 3 selection radio button.
bundle_selection3 = Radiobutton(old_stock_frame, text="Vitamins & food supplements",\
    font=(small_font), bg=widget_bg, activebackground=widget_bg, cursor="hand2",\
    value=3, variable=bundle_selection, command=list_items_in_bundle,\
    tristatevalue="a")
bundle_selection3.grid(column=0, row=2, sticky="w")
# 12f. Setup and place the bundle 4 selection radio button.
bundle_selection4 = Radiobutton(old_stock_frame, text="Video games",\
    font=(small_font), bg=widget_bg, activebackground=widget_bg, cursor="hand2",\
    value=4, variable=bundle_selection, command=list_items_in_bundle,\
    tristatevalue="a")
bundle_selection4.grid(column=0, row=3, sticky="w")
# 12g. Setup and place the display images button.
display_images_button = Button(left_body_frame, text="Show bundle images",\
    font=(small_font), width=18, bg=widget_bg, activebackground=widget_bg,\
    cursor="hand2", command=display_product_images)
display_images_button.grid(column=0, row=3, padx=8, pady=8)
# 12h. Setup and place the add to cart button.
add_to_cart_button = Button(left_body_frame, text="Add bundle to cart",\
    font=(small_font), width=18, bg=widget_bg, activebackground=widget_bg,\
    cursor="hand2", command=add_to_cart)
add_to_cart_button.grid(column=0, row=4, padx=8, pady=8)
# 12i. Setup and place the empty cart button.
empty_cart_button = Button(left_body_frame, text="Empty cart",\
    font=(small_font), width=18, bg=widget_bg, activebackground=widget_bg,\
    cursor="hand2", command=empty_cart)
empty_cart_button.grid(column=0, row=5, padx=8, pady=8)
# 12j. Setup and place the submit order button.
submit_order_button = Button(left_body_frame, text="Submit order",\
    font=(small_font), width=18, bg=widget_bg, activebackground=widget_bg,\
    cursor="hand2", command=submit_order)
submit_order_button.grid(column=0, row=6, padx=8, pady=8)
# 12k. Setup and place the bundle title.
bundle_title_label = Label(bundle_frame, text="Bundle products",\
    font=(small_bold_font), width=55, height=1, bg=widget_title_bg)
bundle_title_label.grid(column=0, row=0, sticky="w")
# 12l. Setup and place the bundle list.
bundle_list = ScrolledText(bundle_frame, font=(small_font), width=53, height=9,\
    wrap=WORD, bg=widget_bg)
bundle_list.grid(column=0, row=1, sticky="w")
bundle_list.config(state="disable") # Initially disable widget editing.
# 12m. Setup and place the cart title.
cart_title_label = Label(cart_frame, text="Cart", font=(small_bold_font),\
                    width=55, height=1, bg=widget_title_bg)
cart_title_label.grid(column=0, row=0, sticky="w")
cart_scrollbar = Scrollbar(cart_frame, orient=VERTICAL)
# 12n. Setup and place the cart list.
cart_list = ScrolledText(cart_frame, font=(small_font), width=53, height=9,\
                         wrap=WORD, bg=widget_bg)
cart_list.grid(column=0, row=1, sticky="w")
cart_list.config(state="disable") # Initially disable widget editing.
# 12o. Setup and place the copyright statement.
copyright_label = Label(footer_frame,\
    text="\u00A9 2020 Samuel Robinson.",\
    font=(small_bold_font), width=87, bg=footer_bg, fg=footer_fg)
copyright_label.grid(column=0, row=0, columnspan=1)

# 13. Make the window update periodically, this is a vital function for the GUI.
root_window.mainloop()

#
#--------------------------------------------------------------------#
