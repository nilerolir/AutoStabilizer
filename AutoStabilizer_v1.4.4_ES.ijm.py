#Proyecto: trabajo de Nicolas Roa
#Fecha: 08-02-2025
#Versión: 1.4.4


# Importaciones para ImageJ y procesamiento de imágenes
from ij import IJ                       								# Funciones principales de ImageJ (logging, apertura de imágenes, etc.)
from ij.plugin import FolderOpener        								# Permite abrir una carpeta como secuencia de imágenes
from ij.process import ImageConverter    	 							# Conversión de imágenes entre distintos formatos
# Importaciones para manejo de fechas y tiempos
from datetime import datetime             								# Formateo y manipulación de fechas y horas
# Importaciones relacionadas a las preferencias de ImageJ
import ij.Prefs                         								# Manejo de las preferencias y configuraciones de ImageJ
# Importaciones para interacción con el sistema operativo
import os                               								# Operaciones con rutas, directorios y archivos
import sys                             								 	# Acceso a funciones y parámetros del sistema
# Importaciones para realizar conexiones de red
from java.net import URL  							# Para realizar peticiones a servicios web y APIs
# Importaciones para operaciones de entrada/salida de datos
from java.io import BufferedReader, InputStreamReader, DataOutputStream # Manejo de streams para lectura y escritura de datos
# Importaciones para operaciones de codificación
# Importación para manejar datos en formato JSON
from org.json import JSONObject         								# Creación y análisis de objetos JSON
# Importaciones para la interfaz gráfica y manejo de diálogos
import javax.swing.JDialog as JDialog     								# Componente de diálogo para ventanas modales
import java.awt.Dialog.ModalityType as ModalityType  					# Define el tipo de modalidad de los diálogos
# Importación para copiar directorios de forma recursiva
from shutil import copytree             								# Copia completa de una carpeta a otra
# Importaciones para seleccionar archivos y directorios mediante un diálogo
import javax.swing.JFileChooser as JFileChooser  						# Componente para abrir diálogos de selección de archivos o directorios
import codecs                           								# Manejo de archivos con codificación específica
# Importaciones adicionales de Swing para construir la GUI
from javax.swing import JPanel, JButton, JLabel, JTextField, BoxLayout, BorderFactory, SwingConstants
from javax.swing import JComboBox, JCheckBox, JScrollPane
# Importaciones de AWT para configuraciones de layouts, fuentes y colores
from java.awt import BorderLayout, FlowLayout, Font, Color, GridLayout, Insets, Dimension
from javax.swing import SwingUtilities   								# Para asegurar que la GUI se ejecute en el hilo de eventos
# Importaciones para manejo de eventos en la ventana
from java.awt.event import WindowAdapter   								# Adaptador para eventos de cierre y otros eventos de ventana

# =============================================
# Variables Globales
# =============================================
configuracion = {}  # No inicializar aquí (se carga después de la GUI)
iteracion_avance = 0
custom_plate_size = None   # Nueva variable global para almacenar el tamaño ingresado en Edit

# ==========================================================================
# Interfaz Gráfica
# ============================================================================
def setup_gui():
	"""
	 Llama a _build_gui e inicia la construcción de la interfaz gráfica (GUI) 
	 en el hilo de eventos de Swing para garantizar la seguridad de hilos.
	"""
	SwingUtilities.invokeLater(lambda: _build_gui())

# =====================================================
# Clase para manejar eventos de ventana
# =======================================================
class MyWindowAdapter(WindowAdapter):
	def windowClosing(self, e):
		"""
		LLeva un registro del evento de cierre manual de la ventana.
		"""
		IJ.log("Programa cerrado")

def _build_gui():
	"""
	Construye la ventana principal de la interfaz gráfica.
	Configura el diálogo (JDialog), los paneles y agrega los componentes necesarios
	(selección de directorios, menú desplegable, casillas de verificación y botones).
	"""
	frame = JDialog(None, "AutoStabilizer - v1.4.4 - Configuraciones", ModalityType.APPLICATION_MODAL)
	frame.setSize(700, 350)  # Ventana GUI
	frame.setLayout(BorderLayout())
	frame.setLocationRelativeTo(None)  # Centrar ventana
	# Fondo de la ventana: gris claro (rgb(240,240,240))
	frame.getContentPane().setBackground(Color(240, 240, 240))
	# Agregar WindowListener para registrar log al cerrar manualmente
	frame.addWindowListener(MyWindowAdapter())
		
	# Panel principal con borde y padding
	main_panel = JPanel()
	main_panel.setLayout(BoxLayout(main_panel, BoxLayout.Y_AXIS))
	main_panel.setBorder(BorderFactory.createCompoundBorder(
		BorderFactory.createLineBorder(Color(200, 200, 200)),
		BorderFactory.createEmptyBorder(15, 15, 15, 15)
	))
	main_panel.setBackground(Color(255, 255, 255))
	
	# Título
	lbl_title = JLabel("AutoStabilizer - v1.4.4 - Configuraciones", SwingConstants.CENTER)
	lbl_title.setFont(Font("Arial", Font.BOLD, 20))
	lbl_title.setForeground(Color(51, 51, 51))
	lbl_title.setBorder(BorderFactory.createEmptyBorder(0, 0, 20, 0))
	main_panel.add(lbl_title)
	
	# Panel para las barras de escritura y botones "Seleccionar"
	input_panel = JPanel(GridLayout(2, 2, 10, 10))
	input_panel.setBorder(BorderFactory.createEmptyBorder(0, 0, 30, 0))
	
	# Directorio de trabajo
	lbl_workdir = JLabel("Directorio de trabajo:")
	lbl_workdir.setFont(Font("Arial", Font.PLAIN, 14))
	txt_workdir = JTextField(50)
	btn_workdir = JButton("Seleccionar", actionPerformed=lambda e: _select_folder(txt_workdir))
	btn_workdir.setFont(Font("Arial", Font.PLAIN, 12))
	btn_workdir.setPreferredSize(Dimension(80, 25))  # Ajustar tamaño del botón
	input_panel.add(lbl_workdir)
	input_panel.add(txt_workdir)
	input_panel.add(btn_workdir)
	
	# Carpeta a copiar
	lbl_copyfolder = JLabel("Carpeta a copiar:")
	lbl_copyfolder.setFont(Font("Arial", Font.PLAIN, 14))
	txt_copyfolder = JTextField(50)
	btn_copyfolder = JButton("Seleccionar", actionPerformed=lambda e: _select_folder(txt_copyfolder))
	btn_copyfolder.setFont(Font("Arial", Font.PLAIN, 12))
	btn_copyfolder.setPreferredSize(Dimension(80, 25))  # Ajustar tamaño del botón
	input_panel.add(lbl_copyfolder)
	input_panel.add(txt_copyfolder)
	input_panel.add(btn_copyfolder)
	
	main_panel.add(input_panel)
	
	# Panel para el menú desplegable y botón "Custom"
	main_panel.add(_build_gui_dropdown())
	
	# Panel para las casillas de selección
	checkbox_panel = JPanel(FlowLayout(FlowLayout.LEFT, 10, 10))
	lbl_config = JLabel("Configuraciones:")
	lbl_config.setFont(Font("Arial", Font.PLAIN, 14))
	lbl_config.setForeground(Color(85, 85, 85))
	
	# Creación de casillas de selección para modificar parámetros en Config.txt
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
	
	# Panel de botones (Aceptar y Cerrar)
	btn_panel = JPanel(FlowLayout(FlowLayout.RIGHT, 10, 10))
	btn_accept = JButton("Aceptar", background=Color(70, 130, 180), foreground=Color.WHITE)
	btn_accept.setFont(Font("Arial", Font.BOLD, 12))
	# Acción: valida campos, inicia procesamiento y cierra la GUI.
	btn_accept.addActionListener(lambda e: (_on_accept(frame, txt_workdir.getText(), txt_copyfolder.getText()), frame.dispose()))
	btn_close = JButton("Cerrar", background=Color(220, 53, 69), foreground=Color.WHITE)
	btn_close.setFont(Font("Arial", Font.BOLD, 12))
	# Acción: registra en log que el programa fue cerrado y cierra la ventana.
	btn_close.addActionListener(lambda e: (IJ.log("Programa cerrado"), frame.dispose()))
	btn_panel.add(btn_accept)
	btn_panel.add(btn_close)
	
	frame.add(main_panel, BorderLayout.CENTER)
	frame.add(btn_panel, BorderLayout.SOUTH)
	frame.setVisible(True)

def _select_folder(text_field):
	"""
	Abre un cuadro de diálogo para que el usuario seleccione un directorio y actualiza el campo de texto.
	
	Parámetros:
		text_field (JTextField): Campo de texto a actualizar con la ruta del directorio seleccionado.
	"""
	chooser = JFileChooser()
	chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
	if chooser.showOpenDialog(None) == JFileChooser.APPROVE_OPTION:
		selected_dir = chooser.getSelectedFile().getAbsolutePath()
		text_field.setText(selected_dir)
		IJ.log("Directorio seleccionado: {}".format(selected_dir))

def _build_gui_dropdown():
	"""
	Crea y retorna un panel que contiene:
	  - Un menú desplegable para seleccionar el tamano de la placa de cultivo.
	  - Un botón "Custom" para abrir una ventana de selección personalizada.
	  
	Retorno:
		JPanel: Panel conteniendo ambos componentes.
	"""
	dropdown_panel = JPanel(FlowLayout(FlowLayout.LEFT, 10, 10))
	lbl_placa = JLabel("Tamaño de placa de cultivo:")
	lbl_placa.setFont(Font("Arial", Font.PLAIN, 14))
	lbl_placa.setForeground(Color(85, 85, 85))
	sizes = ["1 x 1", "2 x 2", "3 x 2", "4 x 3", "8 x 6", "12 x 8", "Edit"]
	combo_sizes = JComboBox(sizes)
	combo_sizes.setFont(Font("Arial", Font.PLAIN, 12))
	combo_sizes.setBackground(Color(255, 255, 255))
	combo_sizes.setForeground(Color(51, 51, 51))
	combo_sizes.setBorder(BorderFactory.createLineBorder(Color(204, 204, 204)))

	# Listener para manejar la selección del menú desplegable
	def on_size_selected(event):
		selected_item = combo_sizes.getSelectedItem()
		if selected_item == "Edit":
			_open_edit_window()  # Abrir ventana de edición
		else:
			_update_plate_size(selected_item)  # Actualizar tamaño de placa

	combo_sizes.addActionListener(on_size_selected)

	# Botón "Custom" que interactúa con la opción seleccionada
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
	Maneja la acción del botón Aceptar.
	
	Valida que ambos directorios sean proporcionados, crea la estructura de carpetas en
	el directorio de trabajo, actualiza el archivo Config.txt, copia la carpeta indicada,
	carga la configuración y da inicio al procesamiento de imágenes.
	
	Parámetros:
		frame (JDialog): La ventana actual de la GUI.
		work_dir (str): Ruta del directorio de trabajo seleccionado.
		copy_dir (str): Ruta de la carpeta a copiar.
	"""
	if not work_dir or not copy_dir:
		IJ.log("Error: Selecciona ambos directorios.")
		return

	# Crear estructura de carpetas
	workspace_path = setup_workspace(work_dir)
	if workspace_path:
		update_config(workspace_path)
		copy_to_input(os.path.join(workspace_path, "InputFolder"), copy_dir)

		# Cerrar GUI y cargar la configuración del sistema
		frame.dispose()
		global configuracion, iteracion_avance
		configuracion = abre_archivo_config()
		iteracion_avance = 0  # Reiniciar contador

		# Ejecutar la lógica principal del programa
		inicio_programa(configuracion)
		creacion_carpetas_destino(configuracion)
		procesamiento_imagenes(configuracion)
		debug(configuracion, 'FIN DEL PROGRAMA.', '')
		
# ==============================================
# Funciones de adaptadores y manejo de ventana
# =============================================

class MyWindowAdapter(WindowAdapter):
	"""
	Adaptador de ventana que registra en el log cuando la ventana es cerrada.
	Se utiliza para llevar un registro del evento de cierre manual de la GUI.
	"""
	def windowClosing(self, e):
		IJ.log("Programa cerrado")

# ========================================================
# Funciones de Configuración y Copia
# ========================================================
def setup_workspace(base_dir):
	workspace_path = os.path.join(base_dir, "Carpeta de trabajo AutoStabilizer")
	try:
		if not os.path.exists(workspace_path):
			os.makedirs(workspace_path)
			for subdir in ["LogFolder", "InputFolder", "OutputFolder"]:
				os.makedirs(os.path.join(workspace_path, subdir))
			IJ.log("Workspace creado: {}".format(workspace_path))
		return workspace_path
	except Exception as e:
		IJ.log("Error creando workspace: {}".format(str(e)))
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
			IJ.log("Config.txt actualizado.")
	except Exception as e:
		IJ.log("Error actualizando Config.txt: {}".format(str(e)))

def copy_to_input(dest_dir, source_dir):
	try:
		for item in os.listdir(source_dir):
			src_path = os.path.join(source_dir, item)
			if os.path.isdir(src_path):
				dest_path = os.path.join(dest_dir, item)
				copytree(src_path, dest_path)
				IJ.log("Carpeta copiada: {}".format(item))
	except Exception as e:
		IJ.log("Error copiando archivos: {}".format(str(e)))

def _update_config_checkbox(config_key, is_selected):
	"""
	Actualiza el archivo Config.txt cuando se marca o desmarca una casilla de selección.
	
	Parámetros:
	config_key (str): Clave en el archivo Config.txt (ej. 'Debug', 'Avance', etc.).
	is_selected (bool): True si la casilla está marcada, False si no lo está.
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
		IJ.log("Config.txt actualizado: {}={}".format(config_key, is_selected))
	except Exception as e:
		IJ.log("Error actualizando Config.txt: {}".format(str(e)))

# Nueva función para actualizar el tamaño de la placa
def _update_plate_size(plate_size):
	"""
	Actualiza las variables ReadFolders y CreateFolders en Config.txt según el tamano de la placa seleccionada.
	
	Parámetros:
	plate_size (str): Tamano de la placa seleccionada (ej. "1 x 1", "2 x 2", etc.).
	"""
	try:
		# Extraer el número de filas y columnas
		rows, cols = map(int, plate_size.split(" x "))
		
		# Generar las carpetas
		folders = []
		for col in range(cols):
			for row in range(1, rows + 1):
				folder = "{}{:02d}".format(chr(65 + col), row)  # 65 es el código ASCII para 'A'
				folders.append(folder)
		folders_str = ",".join(folders)
		
		# Actualizar el archivo Config.txt
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
		IJ.log("Config.txt actualizado con tamano de placa: {}".format(plate_size))
	except Exception as e:
		IJ.log("Error actualizando tamano de placa: {}".format(str(e)))

# Nueva función para abrir la ventana personalizada

def _open_custom_window(selected_item):
    """
    Abre una ventana personalizada basada en la opción seleccionada en el menú desplegable.
    Para cualquier opción, incluida "Edit", se abre la misma ventana de selección personalizada.
    """
    # Si se selecciona "Edit", usar el valor ingresado en la ventana Edit
    if selected_item == "Edit":
        global custom_plate_size
        if custom_plate_size is not None:
            plate_size = custom_plate_size
        else:
            IJ.log("Error: No se ha definido un tamano personalizado. Usa la opción Edit para ingresarlo.")
            return
    else:
        plate_size = selected_item

    custom_frame = JDialog(None, "Selección Personalizada", ModalityType.APPLICATION_MODAL)
    custom_frame.setSize(400, 300)
    custom_frame.setLayout(BorderLayout())
    custom_frame.setLocationRelativeTo(None)  # Centrar ventana

    # Panel principal
    main_panel = JPanel()
    main_panel.setLayout(BoxLayout(main_panel, BoxLayout.Y_AXIS))
    main_panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15))
    
    # Extraer el número de filas y columnas
    try:
        rows, cols = map(int, plate_size.split(" x "))
    except Exception as e:
        IJ.log("Formato de placa incorrecto: {}".format(plate_size))
        return

    # Crear casillas para cada posición de la placa
    checkboxes = []
    for col in range(cols):
        row_panel = JPanel(FlowLayout(FlowLayout.LEFT))
        for row in range(1, rows + 1):
            folder = "{}{:02d}".format(chr(65 + col), row)
            chk = JCheckBox(folder)
            checkboxes.append((folder, chk))
            row_panel.add(chk)
        main_panel.add(row_panel)

    # Agregar un panel de desplazamiento
    scroll_pane = JScrollPane(main_panel)
    scroll_pane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED)
    scroll_pane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED)

    # Botón para guardar la selección
    btn_save = JButton("Guardar", actionPerformed=lambda e: _save_custom_selection(checkboxes, custom_frame))
    btn_save.setBackground(Color(70, 130, 180))
    btn_save.setForeground(Color(255, 255, 255))

    custom_frame.add(scroll_pane, BorderLayout.CENTER)
    custom_frame.add(btn_save, BorderLayout.SOUTH)
    custom_frame.setVisible(True)

# Nueva función para guardar la selección personalizada
def _save_custom_selection(checkboxes, frame):
	"""
	Guarda la selección personalizada en el archivo Config.txt.
	
	Parámetros:
	checkboxes (list): Lista de tuplas (folder, JCheckBox).
	frame (JDialog): Ventana que se cerrará después de guardar.
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
		IJ.log("Config.txt actualizado con selección personalizada.")
		frame.dispose()
	except Exception as e:
		IJ.log("Error guardando selección personalizada: {}".format(str(e)))

# Después de la función _save_custom_selection, agrega lo siguiente:

def _open_edit_window():
	"""
	Abre una ventana para editar manualmente el tamano de la placa de cultivo.
	"""
	edit_frame = JDialog(None, "Editar Placa de Cultivo", ModalityType.APPLICATION_MODAL)
	edit_frame.setSize(400, 200)
	edit_frame.setLayout(BorderLayout())
	edit_frame.setLocationRelativeTo(None)  # Centrar ventana

	# Panel principal
	main_panel = JPanel()
	main_panel.setLayout(BoxLayout(main_panel, BoxLayout.Y_AXIS))
	main_panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15))

	# Título
	lbl_title = JLabel("Edita tu placa de cultivo", SwingConstants.CENTER)
	lbl_title.setFont(Font("Arial", Font.BOLD, 16))
	lbl_title.setForeground(Color(51, 51, 51))
	main_panel.add(lbl_title)

	# Mensaje de ejemplo
	lbl_example = JLabel("Ejemplo: 2 x 16", SwingConstants.CENTER)
	lbl_example.setFont(Font("Arial", Font.PLAIN, 12))
	lbl_example.setForeground(Color(85, 85, 85))
	lbl_example.setBorder(BorderFactory.createEmptyBorder(10, 0, 10, 0))
	main_panel.add(lbl_example)

	# Campo de texto para ingresar el tamaño
	txt_plate_size = JTextField(20)
	txt_plate_size.setFont(Font("Arial", Font.PLAIN, 12))
	txt_plate_size.setBorder(BorderFactory.createLineBorder(Color(204, 204, 204)))
	main_panel.add(txt_plate_size)

	# Botón para guardar
	btn_save = JButton("Guardar", actionPerformed=lambda e: _save_edit_plate_size(txt_plate_size.getText(), edit_frame))
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
	Guarda el tamano de la placa ingresado manualmente en el archivo Config.txt.
	Parámetros:
		plate_size (str): Tamano de la placa ingresado por el usuario (ej. "2 x 16").
		frame (JDialog): Ventana que se cerrará después de guardar.
	"""
	try:
		global custom_plate_size
		custom_plate_size = plate_size  # Almacenar el tamaño ingresado para usarlo en el botón Custom
		# Validar el formato del tamaño de la placa
		if "x" not in plate_size:
			IJ.log("Error: Formato incorrecto. Usa '2 x 16' como ejemplo.")
			return
		
		# Extraer filas y columnas
		rows, cols = map(int, plate_size.strip().split("x"))

		# Generar las carpetas
		folders = []
		for col in range(cols):
			for row in range(1, rows + 1):
				folder = "{}{:02d}".format(chr(65 + col), row)  # 65 es el código ASCII para 'A'
				folders.append(folder)
		folders_str = ",".join(folders)

		# Actualizar el archivo Config.txt
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
		IJ.log("Config.txt actualizado con tamano de placa: {}".format(plate_size))
		frame.dispose()
	except Exception as e:
		IJ.log("Error actualizando tamano de placa: {}".format(str(e)))

def _on_accept(frame, work_dir, copy_dir):
	if not work_dir or not copy_dir:
		IJ.log("Error: Selecciona ambos directorios.")
		return

	# Crear estructura de carpetas
	workspace_path = setup_workspace(work_dir)
	if workspace_path:
		update_config(workspace_path)
		copy_to_input(os.path.join(workspace_path, "InputFolder"), copy_dir)

		# Cerrar GUI y cargar configuración
		frame.dispose()
		global configuracion, iteracion_avance
		configuracion = abre_archivo_config()
		iteracion_avance = 0  # Reiniciar contador

		# Ejecutar lógica principal
		inicio_programa(configuracion)
		creacion_carpetas_destino(configuracion)
		procesamiento_imagenes(configuracion)
		debug(configuracion, 'FIN DEL PROGRAMA.', '')

# =============================================
# Funciones de Ricardo
# =============================================

def log(config, message):
	"""
	Registra un mensaje en el archivo de log definido en la configuración.

	Parámetros:
	config (dict): Diccionario con la configuración del sistema. Debe contener la clave 'LogFolder'.
	message (str): Mensaje a registrar en el archivo de log.

	Retorno:
	None. (Efecto colateral: Escribe en el archivo de log.)

	Ejemplo de uso:
		log(config, "Proceso iniciado correctamente.")
	"""
	log_folder = config.get('LogFolder')
	
	# Genera un nombre de archivo con la fecha actual en formato Log_AAAA_MM_DD.txt.
	log_file_name = "Log_%s.txt" % datetime.now().strftime("%Y_%m_%d")
	log_file_path = os.path.join(log_folder, log_file_name)
	
	try:
		# Crear LogFolder si no existe
		if not os.path.exists(log_folder):
			os.makedirs(log_folder)
		with open(log_file_path, 'a') as log_file:
			log_file.write("%s || %s\n" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message))
	except IOError:
		print("%s || ERROR: No se pudo escribir en el archivo de log." % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def valida_datos(config):
	"""
	Verifica que las claves requeridas estén presentes y no sean vacías en el diccionario de configuración.

	Parámetros:
	config (dict): Diccionario con los valores de configuración.

	Retorno:
	None. (En caso de ausencia o valor vacío, finaliza el programa con sys.exit(1).)

	Ejemplo de uso:
		valida_datos(configuracion)
	"""
	# Definir Claves presentes en Config
	variables= ['LogFolder','InputFolder','OutputFolder','ReadFolders','CreateFolders','BrightFoldersPoint','Debug','Avance','Visor','Dev','ENDPOINT','PREDICTION_KEY']
	for variable in variables:
		if variable not in config or not config[variable]:
			print("\n%s || ERROR: La variable '%s' no existe o no contiene datos." % (datetime.now(),variable))
			sys.exit(1)

def abre_archivo_config():
	"""
	Lee el archivo 'Config.txt', parsea sus líneas y retorna un diccionario con los parámetros.

	Parámetros:
	(No recibe parámetros, utiliza ruta fija 'Config.txt'.)

	Retorno:
	dict: Diccionario con los valores de configuración cargados.

	Ejemplo de uso:
	configuracion = abre_archivo_config()
	"""
	config = {}

	# Abrir el archivo de configuración
	ruta_config = 'Config.txt'
	try:
		with open(ruta_config, 'r') as archivo:
			for linea in archivo:   
				if '=' in linea:
					clave, valor = linea.split('=', 1)
					# Eliminar espacios en blanco alrededor de clave y valor
					clave = clave.strip()
					valor = valor.strip()
					# Almacenar en el diccionario
					config[clave] = valor
			valida_datos(config)
			#si 'DEV' está habilitado, sobreescribe valores de 'ReadFolders' y 'BrightFoldersPoint'
			if config.get('Dev') == 'True':
				config.update({"BrightFoldersPoint": "POINT 00001\\BRIGHT,POINT 00002\\BRIGHT"})
				config.update({'ReadFolders':'A01'})
			return config
	except IOError:
		print('Error: no se encontro el archivo %s o no se pudo abrir.' % (ruta_config))
		sys.exit(1)

def inicio_programa(configuracion):
	"""
	Muestra mensajes de bienvenida, registra el inicio en el log y, si está activo el modo debug, imprime la configuración.

	Parámetros:
	configuracion (dict): Diccionario de configuración, obtenido de abre_archivo_config().

	Retorno:
	None.

	Ejemplo de uso:
	inicio_programa(configuracion)
	"""	
	print("\n" * 15)
	separador = '*' * 50
	print('\n%s' % separador)
	print('%s' % ('**            BIENVENIDO AL PROGRAMA            **'))
	print('%s' % separador)
	print('Inicio del programa: %s' % datetime.now())
	log(configuracion, 'Inicio del programa.')
	if configuracion.get('Debug') == 'True':
		print('%s' % ('************** MODO DEBUG ACTIVADO ***************'))
		print('Configuraciones Actuales:\n')
		for clave, valor in configuracion.items():
			print('%-25s: %s' % (clave, valor))
	print('%s\n\n' % separador)

def creacion_carpetas_destino(configuracion): 
	"""
	Crea las carpetas de salida especificadas en la configuración si no existen.

	Parámetros:
	configuracion (dict): Diccionario de configuración. Debe contener las claves 'OutputFolder' y 'CreateFolders'.

	Retorno:
	None.

	Ejemplo de uso:
	creacion_carpetas_destino(configuracion)
	"""
	outputFolder = configuracion.get('OutputFolder')
	if outputFolder:
		# Lista de nombres de las nuevas carpetas
		folderNames = configuracion.get('CreateFolders').split(',')
		for newFolderName in folderNames:
			# Construir la ruta de la nueva carpeta
			newDir = os.path.join(outputFolder, newFolderName)
			# Crear el nuevo directorio si no existe
			if not os.path.exists(newDir):
				os.makedirs(newDir)
				debug(configuracion, 'Carpeta creada: ', newDir)
			else:
				debug(configuracion, 'Las carpetas ya se encuentra creadas con anterioridad: ', newDir)

def debug(configuracion,mensaje,variable):
	"""
	Imprime un mensaje en consola si el modo Debug está activado y lo registra en el log.

	Parámetros:
	configuracion (dict): Diccionario de configuración, que incluye la clave 'Debug' ('True'/'False').
	mensaje (str): Mensaje base a mostrar.
	variable (str): Información adicional para mostrar junto al mensaje.

	Retorno:
	None. (Efecto colateral: imprime por consola y escribe en el log.)

	Ejemplo de uso:
	debug(configuracion, "Directorio a abrir:", NewDire)
	"""
	if configuracion.get('Debug') == 'True':
		print('%s || %s %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), mensaje, variable))
	log(configuracion, mensaje + variable)

def avance(folderNames,BrightNames):
	"""
	Incrementa un contador global para indicar el progreso del procesamiento y registra el porcentaje completado.

	Parámetros:
	folderNames (list): Lista de carpetas a procesar.
	BrightNames (list): Lista de subcarpetas (ej. 'BRIGHT').

	Retorno:
	None. (Efecto colateral: imprime el porcentaje de progreso por consola y en el log.)

	Ejemplo de uso:
	avance(folderNames, BrightNames)
	"""
	global iteracion_avance
	if configuracion.get('Avance') == 'True':
		iteracion_avance = iteracion_avance + 1
		porcentaje = float(iteracion_avance) / (len(folderNames)*len(BrightNames)) * 100
		mensaje = '%.2f%% completado.' % porcentaje
		debug(configuracion, mensaje, '')

def orientacion(configuracion,NewDire):
	"""
	Verifica la orientación de la primera imagen en la carpeta y decide si se requiere un cambio de orientación.

	Parámetros:
	configuracion (dict): Diccionario de configuración, que incluye datos para la conexión a la API (ENDPOINT, PREDICTION_KEY).
	NewDire (str): Ruta de la carpeta que contiene la secuencia de imágenes.

	Retorno:
	bool: True si se requiere cambio de orientación; False en caso contrario.
	(En caso de error o falta de conclusividad, devuelve None o no hace cambio.)

	Ejemplo de uso:
   	necesita_flip = orientacion(configuracion, rutaCarpeta)
	"""
	ruta_tiff=NewDire + '\\00000.TIFF'
	ruta_jpg=NewDire + '\\_TIFF_JPG.jpg'
	imagen = IJ.openImage(ruta_tiff)
	IJ.saveAs(imagen, 'JPG', ruta_jpg)
	imagen.close()
	cambiar_orientacion = conexion_custom_vision(configuracion,ruta_jpg)
	return cambiar_orientacion
		
def conexion_custom_vision(configuracion,ruta_jpg):
	"""
	Envía la imagen a la API de Custom Vision, analiza la respuesta JSON y determina la orientación correcta.

	Parámetros:
	configuracion (dict): Configuración con 'ENDPOINT', 'PREDICTION_KEY', etc.
	ruta_jpg (str): Ruta al archivo JPG que se enviará al servicio.

	Retorno:
	bool: True si la imagen está invertida (etiquetada como 'Derecha') y la probabilidad es mayor al umbral.
	False si está correctamente orientada ('Izquierda') con alta probabilidad.
	None o no retorna nada en caso de error.

	Ejemplo de uso:
	flip_necesario = conexion_custom_vision(configuracion, "C:/ruta/imagen.jpg")
	"""
	# Configuración de la API
	ENDPOINT = configuracion.get('ENDPOINT')
	PREDICTION_KEY = configuracion.get('PREDICTION_KEY')
	IMAGE_PATH = ruta_jpg
	
	# Verificar si la imagen existe
	if not os.path.exists(IMAGE_PATH):
		debug(configuracion, 'La imagen de entrada no existe: ', IMAGE_PATH)  # Fix: use comma to separate message and variable.
		return None

	# Leer la imagen en binario
	with open(IMAGE_PATH, "rb") as image_file:
		image_data = image_file.read()
	
	# Crear la conexión HTTP
	url = URL(ENDPOINT)
	connection = url.openConnection()
	connection.setRequestMethod("POST")
	connection.setRequestProperty("Content-Type", "application/octet-stream")
	connection.setRequestProperty("Prediction-Key", PREDICTION_KEY)
	connection.setDoOutput(True)
	
	# Enviar los datos de la imagen
	output_stream = DataOutputStream(connection.getOutputStream())
	output_stream.write(image_data)
	output_stream.flush()
	output_stream.close()
	
	# Leer la respuesta de la API
	response_code = connection.getResponseCode()
	if response_code == 200:
		debug(configuracion, "Conexion a modelo custom vision correcta.", "")
		reader = BufferedReader(InputStreamReader(connection.getInputStream()))
		response = ""
		line = reader.readLine()
		while line is not None:
			response += line
			line = reader.readLine()
		reader.close()

		# Parsear el JSON de la respuesta
		json_response = JSONObject(response)
		predictions = json_response.getJSONArray("predictions")

		# Confirma orientacion
		for i in range(predictions.length()):
			prediction = predictions.getJSONObject(i)
			tag_name = prediction.getString("tagName")
			probability = prediction.getDouble("probability")
			if tag_name == 'Derecha' and probability > 0.7:
				debug(configuracion, 'Imagen requiere cambio de orientacion debido a que se encuentra orientada de derecha a izquierda. Probabilidad:', "{0:.2f}%".format(probability * 100))
				return True
			elif tag_name == 'Izquierda' and probability > 0.7:
				debug(configuracion, 'Orientacion correcta. Probabilidad:', "{0:.2f}%".format(probability * 100))
				return False
			else:
				debug(configuracion, 'Orientacion no concluyente. Probabilidad:', "{0:.2f}%".format(probability * 100))
		return None
	else:
		debug(configuracion, 'Error de conexion a custom vision. Codigo de error:', str(response_code))
		reader = BufferedReader(InputStreamReader(connection.getErrorStream()))
		error_response = []
		line = reader.readLine()
		while line is not None:
			error_response.append(line)
			line = reader.readLine()
		reader.close()
		debug(configuracion, 'Tipo de error', str(error_response))
		return None

def cambio_orientacion(imp):
	"""
	Recorre todos los fotogramas de una pila (stack) y aplica un flip horizontal para invertir la orientación.

	Parámetros:
	imp (ImagePlus): Objeto de imagen (pila) abierto en ImageJ.

	Retorno:
	None. (Efecto colateral: Modifica la pila en memoria.)

	Ejemplo de uso:
	cambio_orientacion(imp)
	"""
	stack = imp.getStack()  # Acceder a los cuadros del video
	for i in range(1, stack.getSize() + 1):
		frame = stack.getProcessor(i)
		frame.flipHorizontal()  # Cambiar orientación horizontalmente
	debug(configuracion, "Cambio de orientacion realizado en el video.", "")

def procesamiento_imagenes(configuracion):
	inputFolder = configuracion.get('InputFolder')
	if inputFolder:
		folderNames = configuracion.get('ReadFolders').split(',')
		for newFolderName in folderNames:
			BrightNames = configuracion.get('BrightFoldersPoint').split(',')
			for BrightName in BrightNames:
				# Normalize directory path to remove extra backslashes
				raw_new_dire = os.path.join(inputFolder, newFolderName, BrightName)
				NewDire = os.path.normpath(raw_new_dire)
				debug(configuracion, 'Directorio a abrir: ', NewDire)
				if os.path.exists(NewDire):
					cambiar_orientacion = orientacion(configuracion, NewDire)
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
						debug(configuracion, 'Directorio donde se grabara el archivo avi: ', output_path)
						if cambiar_orientacion:
							cambio_orientacion(imp)
						IJ.run(imp, "AVI... ", "compression=None frame=7 save=[" + output_path + "]")
						debug(configuracion, 'Guardado de archivo finalizado: ', NombreVideo)
					else:
						mensaje_error = 'ERROR: No se pudo abrir la secuencia de imagenes de la carpeta %s' % NewDire
						debug(configuracion, mensaje_error, '')
				else:
					mensaje_no_dir = 'No existe directorio para %s\\%s.' % (newFolderName, BrightName)
					debug(configuracion, mensaje_no_dir, '')
				avance(folderNames, BrightNames)

# =============================================
# Ejecución Principal
# =============================================
# Solo esto se ejecuta al inicio
if __name__ == "__main__":
	setup_gui()

# =============================================
# Fin del Programa
# =============================================

