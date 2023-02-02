import os
from tkinter import Tk, filedialog, messagebox

# defining a function for the task
def create_dirtree_without_files(src, dst):

	# getting the absolute path of the source
	# directory
	src = os.path.abspath(src)
	
	# making a variable having the index till which
	# src string has directory and a path separator
	src_prefix = len(src) + len(os.path.sep)
	
	# making the destination directory
	#os.makedirs(dst)
	
	# doing os walk in source directory
	for root, dirs, files in os.walk(src):
		for dirname in dirs:
		
			# here dst has destination directory,
			# root[src_prefix:] gives us relative
			# path from source directory
			# and dirname has folder names
			dirpath = os.path.join(dst, root[src_prefix:], dirname)
			print(dirpath)

			# making the path which we made by
			# joining all of the above three
			os.mkdir(dirpath)

def choose_2_paths():
    CUR_DIR = str(os.path.dirname(__file__))

    root = Tk() # pointing root to Tk() to use it as Tk() in program.
    root.withdraw() # Hides small tkinter window.
    root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
    messagebox.showinfo("Init names folder", "Please select the folder containing the CORRECT STRUCTURE")
    GOOD_NAMES_FILE = filedialog.askdirectory(initialdir=CUR_DIR) # Returns opened path as str
    if GOOD_NAMES_FILE == "":
        exit()

    root = Tk() # pointing root to Tk() to use it as Tk() in program.
    root.withdraw() # Hides small tkinter window.
    root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
    messagebox.showinfo("Bad names folder", "Please select the folder where you want the structure to be copied")
    BAD_NAMES_FILE = filedialog.askdirectory(initialdir=CUR_DIR) # Returns opened path as str
    if BAD_NAMES_FILE == "":
        exit()
    confirmation = messagebox.askokcancel(title="BEWARE", message=f"You are going to place into '{BAD_NAMES_FILE}' the files structure of '{GOOD_NAMES_FILE}'. Press 'OK' to continue or 'Cancel' to abort.")
    #Ask if operation should proceed; return true if the answer is ok
    if confirmation != True:
        exit()

    return [GOOD_NAMES_FILE, BAD_NAMES_FILE]

# calling the creation function
dirs = choose_2_paths()
init_dir = dirs[0]
target_dir = dirs[1]
create_dirtree_without_files(init_dir,
							target_dir)
