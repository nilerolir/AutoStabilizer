# Project: Nicolas Roa's Work
# Date: 08-02-2025
# Version: 1.4.4


# Imports for ImageJ and image processing
from ij import IJ                       								# Main functions of ImageJ (logging, opening images, etc.)
from ij.plugin import FolderOpener        								# Allows opening a folder as a sequence of images
from ij.process import ImageConverter    	 							# Image conversion between different formats
# Imports for date and time handling
from datetime import datetime             								# Formatting and manipulating dates and times
# Imports related to ImageJ preferences
import ij.Prefs                         								# Handling ImageJ preferences and settings
# Imports for interacting with the operating system
import os                               								# Operations with paths, directories, and files
import sys                             								 	# Access to system functions and parameters
# Imports for network connections
from java.net import URL  							# For making requests to web services and APIs
# Imports for data input/output operations
from java.io import BufferedReader, InputStreamReader, DataOutputStream # Handling streams for reading and writing data
# Imports for encoding operations
# Import for handling JSON data
from org.json import JSONObject         								# Creating and parsing JSON objects
# Imports for graphical interface and dialog handling
import javax.swing.JDialog as JDialog     								# Dialog component for modal windows
import java.awt.Dialog.ModalityType as ModalityType  					# Defines the modality type of dialogs
# Import for copying directories recursively
from shutil import copytree             								# Complete copy of one folder to another
# Imports for selecting files and directories through a dialog
import javax.swing.JFileChooser as JFileChooser  						# Component for opening file or directory selection dialogs
import codecs                           								# Handling files with specific encoding
# Additional Swing imports for building the GUI
from javax.swing import JPanel, JButton, JLabel, JTextField, BoxLayout, BorderFactory, SwingConstants
from javax.swing import JComboBox, JCheckBox, JScrollPane
# AWT imports for layout, font, and color settings
from java.awt import BorderLayout, FlowLayout, Font, Color, GridLayout, Insets, Dimension
from javax.swing import SwingUtilities   								# To ensure the GUI runs on the event dispatch thread
# Imports for window event handling
from java.awt.event import WindowAdapter   								# Adapter for window closing and other window events

# =============================================
# Global Variables
# =============================================
configuracion = {}  # Do not initialize here (loaded after the GUI)
iteracion_avance = 0
custom_plate_size = None   # New global variable to store the size entered in Edit

# ==========================================================================
# Graphical Interface
# ============================================================================
def setup_gui():
	"""
	Calls _build_gui and starts constructing the Graphical User Interface (GUI)
	on the Swing event thread to ensure thread safety.
	"""
	SwingUtilities.invokeLater(lambda: _build_gui())

# =====================================================
# Class for handling window events
# =======================================================
class MyWindowAdapter(WindowAdapter):
	def windowClosing(self, e):
		"""
		Logs the event of manual window closing.
		"""
		IJ.log("Program closed")

def _build_gui():
	"""
	Constructs the main window of the GUI.
	Sets up the dialog (JDialog), panels and adds the necessary components
	(folder selection, dropdown menu, checkboxes, and buttons).
	"""
	frame = JDialog(None, "AutoStabilizer - v1.4.4 - Configurations", ModalityType.APPLICATION_MODAL)
	frame.setSize(700, 350)  # GUI window
	frame.setLayout(BorderLayout())
	frame.setLocationRelativeTo(None)  # Center window
	# Window background: light gray (rgb(240,240,240))
	frame.getContentPane().setBackground(Color(240, 240, 240))
	# Add WindowListener to log when manually closed
	frame.addWindowListener(MyWindowAdapter())
		
	# Main panel with border and padding
	main_panel = JPanel()
	main_panel.setLayout(BoxLayout(main_panel, BoxLayout.Y_AXIS))
	main_panel.setBorder(BorderFactory.createCompoundBorder(
		BorderFactory.createLineBorder(Color(200, 200, 200)),
		BorderFactory.createEmptyBorder(15, 15, 15, 15)
	))
	main_panel.setBackground(Color(255, 255, 255))
	
	# Title
	lbl_title = JLabel("AutoStabilizer - v1.4.4 - Configurations", SwingConstants.CENTER)
	lbl_title.setFont(Font("Arial", Font.BOLD, 20))
	lbl_title.setForeground(Color(51, 51, 51))
	lbl_title.setBorder(BorderFactory.createEmptyBorder(0, 0, 20, 0))
	main_panel.add(lbl_title)
	
	# Panel for text fields and "Select" buttons
	input_panel = JPanel(GridLayout(2, 2, 10, 10))
	input_panel.setBorder(BorderFactory.createEmptyBorder(0, 0, 30, 0))
	
	# Working directory
	lbl_workdir = JLabel("Working directory:")
	lbl_workdir.setFont(Font("Arial", Font.PLAIN, 14))
	txt_workdir = JTextField(50)
	btn_workdir = JButton("Select", actionPerformed=lambda e: _select_folder(txt_workdir))
	btn_workdir.setFont(Font("Arial", Font.PLAIN, 12))
	btn_workdir.setPreferredSize(Dimension(80, 25))  # Adjust button size
	input_panel.add(lbl_workdir)
	input_panel.add(txt_workdir)
	input_panel.add(btn_workdir)
	
	# Folder to copy
	lbl_copyfolder = JLabel("Folder to copy:")
	lbl_copyfolder.setFont(Font("Arial", Font.PLAIN, 14))
	txt_copyfolder = JTextField(50)
	btn_copyfolder = JButton("Select", actionPerformed=lambda e: _select_folder(txt_copyfolder))
	btn_copyfolder.setFont(Font("Arial", Font.PLAIN, 12))
	btn_copyfolder.setPreferredSize(Dimension(80, 25))  # Adjust button size
	input_panel.add(lbl_copyfolder)
	input_panel.add(txt_copyfolder)
	input_panel.add(btn_copyfolder)
	
	main_panel.add(input_panel)
	
	# Panel for dropdown menu and "Custom" button
	main_panel.add(_build_gui_dropdown())
	
	# Panel for checkboxes
	checkbox_panel = JPanel(FlowLayout(FlowLayout.LEFT, 10, 10))
	lbl_config = JLabel("Configurations:")
	lbl_config.setFont(Font("Arial", Font.PLAIN, 14))
	lbl_config.setForeground(Color(85, 85, 85))
	
	# Creating checkboxes to modify parameters in Config.txt
	chk_debug = JCheckBox("Debug", actionPerformed=lambda e: _update_config_checkbox("Debug", chk_debug.isSelected()))
	chk_avance = JCheckBox("Avance", actionPerformed=lambda e: _update_config_checkbox("Avance", chk_avance.isSelected()))
	chk_visor = JCheckBox("Visor", actionPerformed=lambda e: _update_config_checkbox("Visor", chk_visor.isSelected()))
	chk_dev = JCheckBox("Dev", actionPerformed=lambda e: _update_config_checkbox("Dev", chk_dev.isSelected()))
	
	checkbox_panel.add(lbl_config)
	checkbox_panel.add(chk_debug)
	checkbox_panel.add(chk_avance)
	checkbox_panel.add(chk_visor)
	checkbox_panel.add(chk_dev)
	
	main_panel.add(checkbox_panel)
	
	# Button panel (Accept and Close)
	btn_panel = JPanel(FlowLayout(FlowLayout.RIGHT, 10, 10))
	btn_accept = JButton("Accept", background=Color(70, 130, 180), foreground=Color.WHITE)
	btn_accept.setFont(Font("Arial", Font.BOLD, 12))
	# Action: validate fields, start processing, and close the GUI.
	btn_accept.addActionListener(lambda e: (_on_accept(frame, txt_workdir.getText(), txt_copyfolder.getText()), frame.dispose()))
	btn_close = JButton("Close", background=Color(220, 53, 69), foreground=Color.WHITE)
	btn_close.setFont(Font("Arial", Font.BOLD, 12))
	# Action: log that the program was closed and close the window.
	btn_close.addActionListener(lambda e: (IJ.log("Program closed"), frame.dispose()))
	btn_panel.add(btn_accept)
	btn_panel.add(btn_close)
	
	frame.add(main_panel, BorderLayout.CENTER)
	frame.add(btn_panel, BorderLayout.SOUTH)
	frame.setVisible(True)

def _select_folder(text_field):
	"""
	Opens a dialog for the user to select a directory and updates the text field.
	
	Parameters:
		text_field (JTextField): Text field to be updated with the selected directory path.
	"""
	chooser = JFileChooser()
	chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
	if chooser.showOpenDialog(None) == JFileChooser.APPROVE_OPTION:
		selected_dir = chooser.getSelectedFile().getAbsolutePath()
		text_field.setText(selected_dir)
		IJ.log("Selected directory: {}".format(selected_dir))

def _build_gui_dropdown():
	"""
	Creates and returns a panel containing:
	  - A dropdown menu to select the culture plate size.
	  - A "Custom" button to open a personalized selection window.
	  
	Returns:
		JPanel: Panel containing both components.
	"""
	dropdown_panel = JPanel(FlowLayout(FlowLayout.LEFT, 10, 10))
	lbl_placa = JLabel("Culture plate size:")
	lbl_placa.setFont(Font("Arial", Font.PLAIN, 14))
	lbl_placa.setForeground(Color(85, 85, 85))
	sizes = ["1 x 1", "2 x 2", "3 x 2", "4 x 3", "8 x 6", "12 x 8", "Edit"]
	combo_sizes = JComboBox(sizes)
	combo_sizes.setFont(Font("Arial", Font.PLAIN, 12))
	combo_sizes.setBackground(Color(255, 255, 255))
	combo_sizes.setForeground(Color(51, 51, 51))
	combo_sizes.setBorder(BorderFactory.createLineBorder(Color(204, 204, 204)))

	# Listener to handle dropdown selection
	def on_size_selected(event):
		selected_item = combo_sizes.getSelectedItem()
		if selected_item == "Edit":
			_open_edit_window()  # Open edit window
		else:
			_update_plate_size(selected_item)  # Update plate size

	combo_sizes.addActionListener(on_size_selected)

	# "Custom" button that interacts with the selected option
	btn_custom = JButton("Custom", actionPerformed=lambda e: _open_custom_window(combo_sizes.getSelectedItem()))
	btn_custom.setFont(Font("Arial", Font.PLAIN, 12))
	btn_custom.setBackground(Color(40, 167, 69))
	btn_custom.setForeground(Color(255, 255, 255))
	dropdown_panel.add(lbl_placa)
	dropdown_panel.add(combo_sizes)
	dropdown_panel.add(btn_custom)
	return dropdown_panel


def _on_accept(frame, work_dir, copy_dir):
	"""
	Handles the Accept button action.
	
	Validates that both directories are provided, creates the folder structure in
	the working directory, updates the Config.txt file, copies the specified folder,
	loads the configuration, and starts image processing.
	
	Parameters:
		frame (JDialog): The current GUI window.
		work_dir (str): The working directory path.
		copy_dir (str): The folder path to be copied.
	"""
	if not work_dir or not copy_dir:
		IJ.log("Error: Select both directories.")
		return

	# Create folder structure
	workspace_path = setup_workspace(work_dir)
	if workspace_path:
		update_config(workspace_path)
		copy_to_input(os.path.join(workspace_path, "InputFolder"), copy_dir)

		# Close GUI and load configuration
		frame.dispose()
		global configuracion, iteracion_avance
		configuracion = load_config_file()
		iteracion_avance = 0  # Reset counter

		# Execute main logic
		start_program(configuracion)
		create_destination_folders(configuracion)
		process_images(configuracion)
		debug(configuracion, 'END OF PROGRAM.', '')
		
# ==============================================
# Adapter and window handling functions
# =============================================

class MyWindowAdapter(WindowAdapter):
	"""
	Window adapter that logs when the window is closed.
	Used to keep track of the manual closing event of the GUI.
	"""
	def windowClosing(self, e):
		IJ.log("Program closed")

# ========================================================
# Configuration and Copy Functions
# ========================================================
def setup_workspace(base_dir):
	workspace_path = os.path.join(base_dir, "Carpeta de trabajo AutoStabilizer")
	try:
		if not os.path.exists(workspace_path):
			os.makedirs(workspace_path)
			for subdir in ["LogFolder", "InputFolder", "OutputFolder"]:
				os.makedirs(os.path.join(workspace_path, subdir))
			IJ.log("Workspace created: {}".format(workspace_path))
		return workspace_path
	except Exception as e:
		IJ.log("Error creating workspace: {}".format(str(e)))
		return None

def update_config(workspace_path):
	try:
		with codecs.open("Config.txt", "r", "utf-8") as f:
			lines = f.readlines()

		replacements = {
			"LogFolder=": os.path.join(workspace_path, "LogFolder").replace("/", "\\\\"),
			"InputFolder=": os.path.join(workspace_path, "InputFolder").replace("/", "\\\\"),
			"OutputFolder=": os.path.join(workspace_path, "OutputFolder").replace("/", "\\\\")
		}

		updated_lines = []
		for line in lines:
			for key, value in replacements.items():
				if line.strip().startswith(key):
					line = "{}{}\n".format(key, value)
			updated_lines.append(line)

		with codecs.open("Config.txt", "w", "utf-8") as f:
			f.writelines(updated_lines)
			IJ.log("Config.txt updated.")
	except Exception as e:
		IJ.log("Error updating Config.txt: {}".format(str(e)))

def copy_to_input(dest_dir, source_dir):
	try:
		for item in os.listdir(source_dir):
			src_path = os.path.join(source_dir, item)
			if os.path.isdir(src_path):
				dest_path = os.path.join(dest_dir, item)
				copytree(src_path, dest_path)
				IJ.log("Folder copied: {}".format(item))
	except Exception as e:
		IJ.log("Error copying files: {}".format(str(e)))

def _update_config_checkbox(config_key, is_selected):
	"""
	Updates Config.txt when a checkbox is toggled.
	
	Parameters:
		config_key (str): Key in Config.txt (e.g., 'Debug', 'Avance', etc.).
		is_selected (bool): True if the checkbox is selected, False otherwise.
	"""
	try:
		with open("Config.txt", "r") as f:
			lines = f.readlines()
		
		updated_lines = []
		for line in lines:
			if line.strip().startswith(config_key + "="):
				line = "{}={}\n".format(config_key, str(is_selected))
			updated_lines.append(line)
		
		with open("Config.txt", "w") as f:
			f.writelines(updated_lines)
		IJ.log("Config.txt updated: {}={}".format(config_key, is_selected))
	except Exception as e:
		IJ.log("Error updating Config.txt: {}".format(str(e)))

# New function to update plate size
def _update_plate_size(plate_size):
	"""
	Updates the ReadFolders and CreateFolders variables in Config.txt based on the selected plate size.
	
	Parameters:
		plate_size (str): Selected plate size (e.g., "1 x 1", "2 x 2", etc.).
	"""
	try:
		# Extract the number of rows and columns
		rows, cols = map(int, plate_size.split(" x "))
		
		# Generate the folders
		folders = []
		for col in range(cols):
			for row in range(1, rows + 1):
				folder = "{}{:02d}".format(chr(65 + col), row)  # 65 is the ASCII code for 'A'
				folders.append(folder)
		folders_str = ",".join(folders)
		
		# Update the Config.txt file
		with open("Config.txt", "r") as f:
			lines = f.readlines()
		
		updated_lines = []
		for line in lines:
			if line.strip().startswith("ReadFolders="):
				line = "ReadFolders={}\n".format(folders_str)
			elif line.strip().startswith("CreateFolders="):
				line = "CreateFolders={}\n".format(folders_str)
			updated_lines.append(line)
		
		with open("Config.txt", "w") as f:
			f.writelines(updated_lines)
		IJ.log("Config.txt updated with plate size: {}".format(plate_size))
	except Exception as e:
		IJ.log("Error updating plate size: {}".format(str(e))

# New function to open the custom window

def _open_custom_window(selected_item):
	"""
	Opens a custom window based on the selected dropdown option.
	For any option, including "Edit", the same personalized selection window is opened.
	"""
	# If "Edit" is selected, use the value entered in the Edit window
	if selected_item == "Edit":
		global custom_plate_size
		if custom_plate_size is not None:
			plate_size = custom_plate_size
		else:
			IJ.log("Error: No custom size defined. Use the Edit option to enter it.")
			return
	else:
		plate_size = selected_item

	custom_frame = JDialog(None, "Custom Selection", ModalityType.APPLICATION_MODAL)
	custom_frame.setSize(400, 300)
	custom_frame.setLayout(BorderLayout())
	custom_frame.setLocationRelativeTo(None)  # Center window

	# Main panel
	main_panel = JPanel()
	main_panel.setLayout(BoxLayout(main_panel, BoxLayout.Y_AXIS))
	main_panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15))
	
	# Extract the number of rows and columns
	try:
		rows, cols = map(int, plate_size.split(" x "))
	except Exception as e:
		IJ.log("Incorrect plate format: {}".format(plate_size))
		return

	# Create checkboxes for each plate position
	checkboxes = []
	for col in range(cols):
		row_panel = JPanel(FlowLayout(FlowLayout.LEFT))
		for row in range(1, rows + 1):
			folder = "{}{:02d}".format(chr(65 + col), row)
			chk = JCheckBox(folder)
			checkboxes.append((folder, chk))
			row_panel.add(chk)
		main_panel.add(row_panel)

	# Add a scroll pane
	scroll_pane = JScrollPane(main_panel)
	scroll_pane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED)
	scroll_pane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED)

	# Save button
	btn_save = JButton("Save", actionPerformed=lambda e: _save_custom_selection(checkboxes, custom_frame))
	btn_save.setBackground(Color(70, 130, 180))
	btn_save.setForeground(Color(255, 255, 255))

	custom_frame.add(scroll_pane, BorderLayout.CENTER)
	custom_frame.add(btn_save, BorderLayout.SOUTH)
	custom_frame.setVisible(True)

# New function to save the custom selection
def _save_custom_selection(checkboxes, frame):
	"""
	Saves the custom selection to Config.txt.
	
	Parameters:
		checkboxes (list): List of tuples (folder, JCheckBox).
		frame (JDialog): Window that will be closed after saving.
	"""
	selected_folders = [folder for folder, chk in checkboxes if chk.isSelected()]
	folders_str = ",".join(selected_folders)
	try:
		with open("Config.txt", "r") as f:
			lines = f.readlines()
		
		updated_lines = []
		for line in lines:
			if line.strip().startswith("ReadFolders="):
				line = "ReadFolders={}\n".format(folders_str)
			elif line.strip().startswith("CreateFolders="):
				line = "CreateFolders={}\n".format(folders_str)
			updated_lines.append(line)
		
		with open("Config.txt", "w") as f:
			f.writelines(updated_lines)
		IJ.log("Config.txt updated with custom selection.")
		frame.dispose()
	except Exception as e:
		IJ.log("Error saving custom selection: {}".format(str(e)))

def _open_edit_window():
	"""
	Opens a window for manually editing the culture plate size.
	"""
	edit_frame = JDialog(None, "Edit Culture Plate", ModalityType.APPLICATION_MODAL)
	edit_frame.setSize(400, 200)
	edit_frame.setLayout(BorderLayout())
	edit_frame.setLocationRelativeTo(None)  # Center window

	# Main panel
	main_panel = JPanel()
	main_panel.setLayout(BoxLayout(main_panel, BoxLayout.Y_AXIS))
	main_panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15))

	# Title
	lbl_title = JLabel("Edit your culture plate", SwingConstants.CENTER)
	lbl_title.setFont(Font("Arial", Font.BOLD, 16))
	lbl_title.setForeground(Color(51, 51, 51))
	main_panel.add(lbl_title)

	# Example message
	lbl_example = JLabel("Example: 2 x 16", SwingConstants.CENTER)
	lbl_example.setFont(Font("Arial", Font.PLAIN, 12))
	lbl_example.setForeground(Color(85, 85, 85))
	lbl_example.setBorder(BorderFactory.createEmptyBorder(10, 0, 10, 0))
	main_panel.add(lbl_example)

	# Text field to enter the size
	txt_plate_size = JTextField(20)
	txt_plate_size.setFont(Font("Arial", Font.PLAIN, 12))
	txt_plate_size.setBorder(BorderFactory.createLineBorder(Color(204, 204, 204)))
	main_panel.add(txt_plate_size)

	# Save button
	btn_save = JButton("Save", actionPerformed=lambda e: _save_edit_plate_size(txt_plate_size.getText(), edit_frame))
	btn_save.setBackground(Color(70, 130, 180))
	btn_save.setForeground(Color.WHITE)
	btn_save.setFont(Font("Arial", Font.BOLD, 12))
	btn_panel = JPanel(FlowLayout(FlowLayout.CENTER, 10, 10))
	btn_panel.add(btn_save)

	edit_frame.add(main_panel, BorderLayout.CENTER)
	edit_frame.add(btn_panel, BorderLayout.SOUTH)
	edit_frame.setVisible(True)

def _save_edit_plate_size(plate_size, frame):
	"""
	Saves the manually entered plate size to Config.txt.
	
	Parameters:
		plate_size (str): Plate size entered by the user (e.g., "2 x 16").
		frame (JDialog): Window that will be closed after saving.
	"""
	try:
		global custom_plate_size
		custom_plate_size = plate_size  # Store the entered plate size for use in the Custom button
		# Validate the plate size format
		if "x" not in plate_size:
			IJ.log("Error: Incorrect format. Use '2 x 16' as an example.")
			return
		
		# Extract rows and columns
		rows, cols = map(int, plate_size.strip().split("x"))

		# Generate the folders
		folders = []
		for col in range(cols):
			for row in range(1, rows + 1):
				folder = "{}{:02d}".format(chr(65 + col), row)  # 65 is the ASCII code for 'A'
				folders.append(folder)
		folders_str = ",".join(folders)

		# Update the Config.txt file
		with open("Config.txt", "r") as f:
			lines = f.readlines()

		updated_lines = []
		for line in lines:
			if line.strip().startswith("ReadFolders="):
				line = "ReadFolders={}\n".format(folders_str)
			elif line.strip().startswith("CreateFolders="):
				line = "CreateFolders={}\n".format(folders_str)
			updated_lines.append(line)

		with open("Config.txt", "w") as f:
			f.writelines(updated_lines)
		IJ.log("Config.txt updated with plate size: {}".format(plate_size))
		frame.dispose()
	except Exception as e:
		IJ.log("Error updating plate size: {}".format(str(e))

def log(config, message):
	"""
	Logs a message to the log file defined in the configuration.

	Parameters:
		config (dict): Configuration dictionary that must contain the key 'LogFolder'.
		message (str): Message to log.

	Example:
		log(config, "Process started successfully.")
	"""
	log_folder = config.get('LogFolder')
	
	# Generates a file name with the current date in the format Log_AAAA_MM_DD.txt.
	log_file_name = "Log_%s.txt" % datetime.now().strftime("%Y_%m_%d")
	log_file_path = os.path.join(log_folder, log_file_name)
	
	try:
		# Create LogFolder if it does not exist
		if not os.path.exists(log_folder):
			os.makedirs(log_folder)
		with open(log_file_path, 'a') as log_file:
			log_file.write("%s || %s\n" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message))
	except IOError:
		print("%s || ERROR: Could not write to the log file." % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def validate_data(config):
	"""
	Verifies that the required keys are present and non-empty in the configuration dictionary.

	Parameters:
		config (dict): Configuration dictionary.

	Returns:
		None. (Exits the program with sys.exit(1) in case of missing or empty data.)

	Example:
		validate_data(configuration)
	"""
	# Define keys present in Config
	variables= ['LogFolder','InputFolder','OutputFolder','ReadFolders','CreateFolders','BrightFoldersPoint','Debug','Avance','Visor','Dev','ENDPOINT','PREDICTION_KEY']
	for variable in variables:
		if variable not in config or not config[variable]:
			print("\n%s || ERROR: The variable '%s' does not exist or contains no data." % (datetime.now(),variable))
			sys.exit(1)

def load_config_file():
	"""
	Reads the 'Config.txt' file, parses its lines, and returns a dictionary of parameters.

	Returns:
		dict: A dictionary containing the loaded configuration parameters.

	Example:
		configuration = load_config_file()
	"""
	config = {}

	# Open the configuration file
	ruta_config = 'Config.txt'
	try:
		with open(ruta_config, 'r') as archivo:
			for linea in archivo:   
				if '=' in linea:
					clave, valor = linea.split('=', 1)
					# Remove whitespace around key and value
					clave = clave.strip()
					valor = valor.strip()
					# Store in the dictionary
					config[clave] = valor
			validate_data(config)
			# if 'DEV' is enabled, overwrite values of 'ReadFolders' and 'BrightFoldersPoint'
			if config.get('Dev') == 'True':
				config.update({"BrightFoldersPoint": "POINT 00001\\BRIGHT,POINT 00002\\BRIGHT"})
				config.update({'ReadFolders':'A01'})
			return config
	except IOError:
		print('Error: could not find or open the file %s.' % (ruta_config))
		sys.exit(1)

def start_program(configuracion):
	"""
	Displays welcome messages, logs the start, and if debug mode is active, prints the configuration.

	Parameters:
		configuracion (dict): Configuration dictionary obtained from load_config_file().

	Example:
		start_program(configuration)
	"""	
	print("\n" * 15)
	separador = '*' * 50
	print('\n%s' % separador)
	print('%s' % ('**            WELCOME TO THE PROGRAM            **'))
	print('%s' % separador)
	print('Program start: %s' % datetime.now())
	log(configuracion, 'Program start.')
	if configuracion.get('Debug') == 'True':
		print('%s' % ('************** DEBUG MODE ENABLED ***************'))
		print('Current Configurations:\n')
		for clave, valor in configuracion.items():
			print('%-25s: %s' % (clave, valor))
	print('%s\n\n' % separador)

def create_destination_folders(configuracion): 
	"""
	Creates the output folders specified in the configuration if they do not already exist.

	Parameters:
		configuracion (dict): Configuration dictionary containing 'OutputFolder' and 'CreateFolders'.

	Example:
		create_destination_folders(configuration)
	"""
	outputFolder = configuracion.get('OutputFolder')
	if outputFolder:
		# List of new folder names
		folderNames = configuracion.get('CreateFolders').split(',')
		for newFolderName in folderNames:
			# Build the path of the new folder
			newDir = os.path.join(outputFolder, newFolderName)
			# Create the new directory if it does not exist
			if not os.path.exists(newDir):
				os.makedirs(newDir)
				debug(configuracion, 'Folder created: ', newDir)
			else:
				debug(configuracion, 'Folders already exist: ', newDir)

def debug(configuracion,mensaje,variable):
	"""
	Prints a message to the console if Debug mode is enabled and logs it.

	Parameters:
		configuracion (dict): Configuration dictionary, including the 'Debug' key ('True'/'False').
		mensaje (str): Base message to display.
		variable (str): Additional information to display with the message.

	Example:
		debug(configuration, "Directory to open:", directory)
	"""
	if configuracion.get('Debug') == 'True':
		print('%s || %s %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), mensaje, variable))
	log(configuracion, mensaje + variable)

def update_progress(folderNames,BrightNames):
	"""
	Increments a global counter to indicate processing progress and logs the percentage completed.

	Parameters:
		folderNames (list): List of folders to process.
		BrightNames (list): List of subfolders (e.g., 'BRIGHT').

	Example:
		update_progress(folderNames, BrightNames)
	"""
	global iteracion_avance
	if configuracion.get('Avance') == 'True':
		iteracion_avance = iteracion_avance + 1
		percentage = float(iteracion_avance) / (len(folderNames)*len(BrightNames)) * 100
		message = '%.2f%% completed.' % percentage
		debug(configuracion, message, '')

def check_image_orientation(configuracion,NewDire):
	"""
	Checks the orientation of the first image in the folder and determines if a flip is needed.

	Parameters:
		configuracion (dict): Configuration dictionary with API data (ENDPOINT, PREDICTION_KEY).
		NewDire (str): Path to the folder containing the image sequence.

	Returns:
		bool: True if a flip is required; False otherwise.

	Example:
		need_flip = check_image_orientation(configuration, folderPath)
	"""
	ruta_tiff=NewDire + '\\00000.TIFF'
	ruta_jpg=NewDire + '\\_TIFF_JPG.jpg'
	imagen = IJ.openImage(ruta_tiff)
	IJ.saveAs(imagen, 'JPG', ruta_jpg)
	imagen.close()
	flip_required = custom_vision_connection(configuracion,ruta_jpg)
	return flip_required
		
def custom_vision_connection(configuracion,ruta_jpg):
	"""
	Sends the image to the Custom Vision API, analyzes the JSON response, and determines the correct orientation.

	Parameters:
		configuracion (dict): Configuration with 'ENDPOINT', 'PREDICTION_KEY', etc.
		ruta_jpg (str): Path to the JPG image to be sent.

	Returns:
		bool: True if the image is inverted (tagged as 'Derecha') and probability is above the threshold;
			  False if correctly oriented ('Izquierda') with high probability;
			  None in case of error.

	Example:
		flip_required = custom_vision_connection(configuration, "C:/path/image.jpg")
	"""
	# API Configuration
	ENDPOINT = configuracion.get('ENDPOINT')
	PREDICTION_KEY = configuracion.get('PREDICTION_KEY')
	IMAGE_PATH = ruta_jpg
	
	# Check if the image exists
	if not os.path.exists(IMAGE_PATH):
		debug(configuracion, 'Input image does not exist: ', IMAGE_PATH)  # Fix: use comma to separate message and variable.
		return None

	# Read the image in binary
	with open(IMAGE_PATH, "rb") as image_file:
		image_data = image_file.read()
	
	# Create the HTTP connection
	url = URL(ENDPOINT)
	connection = url.openConnection()
	connection.setRequestMethod("POST")
	connection.setRequestProperty("Content-Type", "application/octet-stream")
	connection.setRequestProperty("Prediction-Key", PREDICTION_KEY)
	connection.setDoOutput(True)
	
	# Send the image data
	output_stream = DataOutputStream(connection.getOutputStream())
	output_stream.write(image_data)
	output_stream.flush()
	output_stream.close()
	
	# Read the API response
	response_code = connection.getResponseCode()
	if response_code == 200:
		debug(configuracion, "Connection to custom vision model successful.", "")
		reader = BufferedReader(InputStreamReader(connection.getInputStream()))
		response = ""
		line = reader.readLine()
		while line is not None:
			response += line
			line = reader.readLine()
		reader.close()

		# Parse the JSON response
		json_response = JSONObject(response)
		predictions = json_response.getJSONArray("predictions")

		# Confirm orientation
		for i in range(predictions.length()):
			prediction = predictions.getJSONObject(i)
			tag_name = prediction.getString("tagName")
			probability = prediction.getDouble("probability")
			if tag_name == 'Derecha' and probability > 0.7:
				debug(configuracion, 'Image requires orientation change as it is oriented from right to left. Probability:', "{0:.2f}%".format(probability * 100))
				return True
			elif tag_name == 'Izquierda' and probability > 0.7:
				debug(configuracion, 'Correct orientation. Probability:', "{0:.2f}%".format(probability * 100))
				return False
			else:
				debug(configuracion, 'Orientation inconclusive. Probability:', "{0:.2f}%".format(probability * 100))
		return None
	else:
		debug(configuracion, 'Error connecting to custom vision. Error code:', str(response_code))
		reader = BufferedReader(InputStreamReader(connection.getErrorStream()))
		error_response = []
		line = reader.readLine()
		while line is not None:
			error_response.append(line)
			line = reader.readLine()
		reader.close()
		debug(configuracion, 'Error type', str(error_response))
		return None

def flip_orientation(imp):
	"""
	Iterates through all frames in a stack and applies a horizontal flip.

	Parameters:
		imp (ImagePlus): Image object (stack) opened in ImageJ.

	Example:
		flip_orientation(imp)
	"""
	stack = imp.getStack()  # Access the video frames
	for i in range(1, stack.getSize() + 1):
		frame = stack.getProcessor(i)
		frame.flipHorizontal()  # Change orientation horizontally
	debug(configuracion, "Orientation change applied to the video.", "")

def process_images(configuracion):
	inputFolder = configuracion.get('InputFolder')
	if inputFolder:
		folderNames = configuracion.get('ReadFolders').split(',')
		for newFolderName in folderNames:
			BrightNames = configuracion.get('BrightFoldersPoint').split(',')
			for BrightName in BrightNames:
				# Normalize directory path to remove extra backslashes
				raw_new_dire = os.path.join(inputFolder, newFolderName, BrightName)
				NewDire = os.path.normpath(raw_new_dire)
				debug(configuracion, 'Directory to open: ', NewDire)
				if os.path.exists(NewDire):
					flip_required = check_image_orientation(configuracion, NewDire)
					imp = FolderOpener.open(NewDire)
					if imp:
						if configuracion.get('Visor') == 'True':
							imp.show()
						ij.Prefs.set("options.scaleConversions", True)
						ic = ImageConverter(imp)
						ic.setDoScaling(True)
						ic.convertToGray8()
						NombreVideo = BrightName[:11] + '.avi'
						# Normalize output path and create directory if needed
						output_path = os.path.normpath(os.path.join(configuracion.get('OutputFolder'), newFolderName, NombreVideo))
						out_dir = os.path.dirname(output_path)
						if not os.path.exists(out_dir):
							os.makedirs(out_dir)
						debug(configuracion, 'Directory where the avi file will be saved: ', output_path)
						if flip_required:
							flip_orientation(imp)
						IJ.run(imp, "AVI... ", "compression=None frame=7 save=[" + output_path + "]")
						debug(configuracion, 'File save completed: ', NombreVideo)
					else:
						error_message = 'ERROR: Could not open the image sequence from folder %s' % NewDire
						debug(configuracion, error_message, '')
				else:
					no_dir_message = 'Directory does not exist for %s\\%s.' % (newFolderName, BrightName)
					debug(configuracion, no_dir_message, '')
				update_progress(folderNames, BrightNames)

# =============================================
# Main Execution
# =============================================
# Only this runs at the start
if __name__ == "__main__":
	setup_gui()

# =============================================
# End of Program
# =============================================
