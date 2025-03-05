#Proyecto: trabajo de Nicolas Roa
#Fecha: 03-02-2025
#Versión: 1.3


from ij import IJ						# Provee métodos para manipular y procesar imágenes en Fiji (ImageJ). Por ejemplo, IJ.openImage(), IJ.run(), IJ.saveAs().
from ij.plugin import FolderOpener		# Permite abrir una secuencia de imágenes (generalmente en formato TIFF o similar) como una pila (stack) de imágenes en ImageJ.
from ij.process import ImageConverter 	# Facilita la conversión de una imagen (o pila) a diferentes tipos, como 8 bits, 16 bits, etc.
from datetime import datetime			# Manejo de fechas y horas para el registro (log) y para mostrar información de inicio/fin del programa.
import ij.Prefs							# Acceso a preferencias de ImageJ, como la conversión de escala al cambiar el tipo de imagen.
import os								# Acceso al sistema de archivos para crear rutas, verificar existencia de carpetas, etc.
import sys								# Para detener la ejecución con sys.exit() si no se cumplen ciertas condiciones.

from java.net import URL, HttpURLConnection		
# Manejo de conexiones HTTP. Permite abrir conexiones (openConnection()) y configurar parámetros como método de petición, cabeceras, etc.
from java.io import BufferedReader, InputStreamReader, DataOutputStream		
# BufferedReader e InputStreamReader: Para leer la respuesta de la API de Custom Vision. 
# DataOutputStream: Para enviar datos binarios (en este caso, la imagen) a través de la conexión HTTP.

import base64							# Se utilizaría para codificar/decodificar información en base64. 
from org.json import JSONObject			# Parsear la respuesta en formato JSON de la API de Custom Vision y extraer valores (por ejemplo, predictions



def log(config, message):
	"""
	Registra un mensaje en el archivo de log definido en la configuración.

    Parámetros:
	config (dict): Diccionario con la configuración del sistema. Debe contener la clave 'LogFolder'.
    message (str): Mensaje a registrar en el archivo de log.

    Retorno:
        None. (Efecto colateral: Escribe en el archivo de log.)

    Ejemplo de uso:
        log(configuracion, "Proceso iniciado correctamente.")
    """
	log_folder = config.get('LogFolder')	
	# Obtiene del diccionario config la ubicación de la carpeta donde se almacenarán los archivos de log.
	log_file_name = "Log_%s.txt" % datetime.now().strftime("%Y_%m_%d")	
	# Genera un nombre de archivo con la fecha actual en formato Log_AAAA_MM_DD.txt.
	log_file_path = os.path.join(log_folder, log_file_name) 
	# Crea la ruta completa del archivo de log combinando la carpeta
	try:
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
		debug(configuracion, 'La imagen de entrada no existe'. IMAGE_PATH)
	
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
	"""
    Orquesta la lectura de carpetas, la determinación de orientación y la conversión de las pilas de imágenes a AVI.

    Parámetros:
    configuracion (dict): Diccionario con toda la configuración del programa.

    Retorno:
    None.

    Ejemplo de uso:
    procesamiento_imagenes(configuracion)
    """
	inputFolder = configuracion.get('InputFolder')
	if inputFolder:
		#Lista de carpetas a procesar
		folderNames = configuracion.get('ReadFolders').split(',')
		for newFolderName in folderNames:
			BrightNames = configuracion.get('BrightFoldersPoint').split(',')
			for BrightName in BrightNames:
				#Construir las rutas de las carpetas
				NewDire = os.path.join(inputFolder,newFolderName,BrightName)
				debug(configuracion,'Directorio a abrir: ',NewDire)
				#Abre la secuencia de imágenes como una pila
				if os.path.exists(NewDire):
					cambiar_orientacion = orientacion(configuracion,NewDire)
					imp = FolderOpener.open(NewDire)
					#Mostrar secuencia de imagenes
					if imp:
						if configuracion.get('Visor') == 'True':
							#abre ventana
							imp.show()
						# Establecer la opción "ScaleConversions" a True
						ij.Prefs.set("options.scaleConversions", True)
						# Convertir la imagen a 8 bits con escalado
						ic = ImageConverter(imp)
						ic.setDoScaling(True)
						ic.convertToGray8()
						#Crear nombre de video
						NombreVideo = BrightName[:11] + '.avi'
						#Construir ruta de destino
						output_path = os.path.join(configuracion.get('OutputFolder'),newFolderName,NombreVideo)
						debug(configuracion,'Directorio donde se grabara el archivo avi: ',output_path)
						#ejecuta cambio de orientación si corresponde
						if cambiar_orientacion:
							cambio_orientacion(imp)
						# Guardar la imagen como AVI
						IJ.run(imp, "AVI... ", "compression=None frame=7 save=[" + output_path + "]")
						debug(configuracion, 'Guardado de archivo finalizado: ', NombreVideo)
						#cierra ventana
						if configuracion.get('Visor') == 'True':
							imp.close()
					else:
						mensaje_error = 'ERROR: No se pudo abrir la secuencia de imagenes de la carpeta %s' % NewDire
						debug(configuracion, mensaje_error, '')
				else:
					mensaje_no_dir = 'No existe directorio para %s\\%s.' % (newFolderName, BrightName)
					debug(configuracion, mensaje_no_dir,'')
				#valida porcentaje
				avance(folderNames,BrightNames)


#Declaracion de varibles globales
configuracion = {}
iteracion_avance = 0

#llamado a funciones
configuracion = abre_archivo_config()
inicio_programa(configuracion)
creacion_carpetas_destino(configuracion)
procesamiento_imagenes(configuracion)

debug(configuracion, 'FIN DEL PROGRAMA.', '')