# Macro-v1.3 Documentation

**Author:** Nicolás Roa  
**Date:** 05/03/2025

## 1. Overview

This code aims to streamline the processing of microscopy images for cell migration experiments, obtained from the Cell culture Muvicyte system. The macro allows receiving images from a folder called `InputFolder`, where image stacks are stored with the following structure: `Well (A01)\POINT (0001)\Bright (stack)\images`. This structure supports a wide configuration of wells, points of interest, and their corresponding microscopy image stacks. 

The system immediately orients the migration direction of all loaded image stacks from left to right using the `Custom Vision -- Azure -- Microsoft` system. Additionally, it processes the image stacks in the Bright folder, converting them into `AVI` format videos.

## 2. ImageJ/Fiji Software Installation

1. Go to [https://imagej.net/software/fiji/downloads](https://imagej.net/software/fiji/downloads) and download the FIJI version for your operating system.

2. Alternatively, go to [https://imagej.net/ij/download.html](https://imagej.net/ij/download.html) and download the ImageJ version for your operating system. However, the Macro-v1.3- is designed for FIJI. The steps are very similar, but there may be inaccuracies.

3. Extract the downloaded .zip archive:
   - **Windows:** Right-click > "Extract All..."
   - **Mac OS:** Double-click the .zip file
   - **Linux:** Right-click > "Extract Here."

4. No installation is required for the downloaded file, but it can be used as is. Place it on your computer as follows:
   - **Windows or Linux:** Place the extracted directory "fiji-<win64, win32, linux64, or linux32 (depending on your installation)>" in any folder where you have read and write permissions (e.g., your Desktop or Documents folder).
   - **Mac OS:** Place the extracted directory "fiji-macosx" in your Documents folder (do not place it in the "Applications" folder to avoid issues caused by Mac OS's "path randomization").

5. Run FIJI:
   - **Windows:** Navigate to the "fiji-win<64 or 32>" directory, then enter the "Fiji.app" directory and double-click the "ImageJ-win<64 or 32>.exe" file.
   - **Mac OS:** Navigate to the "fiji-macosx" directory and double-click the "FIJI.app" icon.
   - **Linux:** Navigate to the "fiji-linux64" directory, then enter the "Fiji.app" directory and double-click the "ImageJ-linux64" file.

6. In FIJI, go to the menu entry "Help > Update..." and wait for the next dialog box to finish, showing a progress bar with "Checksummer." An "ImageJ Updater" window will appear.

7. Click "Manage Update Sites" in the "ImageJ Updater" window, which will display a list of update sites.

8. Scroll through the list and select the update site named "TurboReg" and "MultiStackReg." Additional information can be found in the following GitHub repository: [https://github.com/miura/MultiStackRegistration](https://github.com/miura/MultiStackRegistration)

9. Click "Close" to close the list.

10. Click "Apply Changes" in the "ImageJ Updater."

11. Wait for the installation to finish and for the software to prompt you to restart.

12. Close FIJI and restart it as described above.

## 3. Macro-v1.3 Installation

1. Download the macro "Macro-v1.3--v1.3" from the following GitHub repository:  
   [https://github.com/nilerolir/AutoStabilizer/tree/main/Code/AutoStabilizer-v1.3-](https://github.com/nilerolir/AutoStabilizer/tree/main/Code/AutoStabilizer-v1.3-)

2. Extract the files `Config.txt` and `Macro-v1.3-.ijm.py` from the `AutoStabilizer-v1.3-` folder as shown in Figure 2A,B. Then, copy the `Config.txt` file to the ImageJ/Fiji root directory and the `Macro-v1.3-.ijm.py` file to the Macros folder in the ImageJ/Fiji directory as shown in Figure 2C.

3. Before running the code, create a working folder in Documents or another target location, for example, `AutoStabilizer Working Folder`. Inside this folder, create the following subfolders: `Log`, `InputFolder`, and `OutputFolder` as shown in Figure 3A. Copy images into the `InputFolder` as shown in Figure 3B.

4. Copy the paths of the `Log`, `InputFolder`, and `OutputFolder` folders into the `Config.txt` file as shown in Figure 4.

5. In ImageJ/Fiji, follow these steps: Once ImageJ/Fiji is open, select `Plugins > Macros > Run > Macro-v1.3-` as shown in Figure 5A,B.

6. You can view the macro's execution in real-time from the ImageJ/Fiji macro editor console, as shown in Figure 5C. To do this, follow these steps: Once ImageJ/Fiji is open, select `Plugins > Macros > Edit > Macro-v1.3-`.

## 4. Figures and Attachments

### Figure 1: Path or location of a TIFF image stack folder for a time sequence corresponding to position 1 of well A01 during a prostate cancer cell (PC3) migration experiment.

![media/image1.png](https://github.com/nilerolir/AutoStabilizer/blob/main/Code/AutoStabilizer-v1.3-/Images/Fig%201.png)

### Figure 2: Steps to follow for the installation of the Macro-v1.3- code. Decompression of the RAR file (2A). Configuration file `Config.txt` and `Macro-v1.3-.ijm.py` after decompression of the RAR file (2B). ImageJ/FIJI root directory where the `Config.txt` file and the `Macro-v1.3-.ijm.py` file will be copied into the Macros folder (2C).

![media/image2.png](https://github.com/nilerolir/AutoStabilizer/blob/main/Code/AutoStabilizer-v1.3-/Images/Fig%202.png)

### Figure 3: AutoStabilizer Working Folder. Important folders: To use the code, you need to create a working folder containing the following subfolders with the default names `InputFolder`, `LogFolder`, and `OutputFolder`. It is recommended to work on the local C drive (3A). `InputFolder`: Place the data to be analyzed in the `InputFolder`. In this case, there is a 6-well plate with two rows and three columns (3B). Data registration per well: Each well can contain one or more records to be analyzed. Each position has a set of images to analyze (3C). Image stack per position and per well: For this example, there is a 96-frame image stack named BRIGHT (3D). `LogFolder`: Once the program is executed, a log will be recorded containing the actions performed by the program, such as the start and end of the program, folder creation, and progress percentage, among others (3E). `OutputFolder`: This folder stores the results of the code execution; if the folders are not created, the corresponding folders for the wells in the `InputFolder` will be created (3F). Results in the `OutputFolder`: The result of the code execution is an AVI video corresponding to the position contained in each well. The results follow the same organization as the `InputFolder` (3G).

![media/image3.png](https://github.com/nilerolir/AutoStabilizer/blob/main/Code/AutoStabilizer-v1.3-/Images/Fig%203.png)

### Figure 4: Configuration file `Config.txt`: The `Config.txt` configuration file contains a series of important parameters for the script's operation. Among these parameters are the locations of the working subfolders `{InputFolder, LogFolder, OutputFolder}`, as well as `{ReadFolders, CreateFolders}` which contain the subfolders `{A01, A02, A03, B01, B02, B03}`, and `{BrightFoldersPoint}`, which contains the subfolders `{POINT 00001/BRIGHT, POINT 00002/BRIGHT, ....}` and the execution variables: `Debug`, `Progress`, `Viewer`, and `Dev`. Meanwhile, `ENDPOINT` corresponds to the Custom Vision credential, an AI service that, after training for computer vision, discriminates the migration direction of the cell edge in this case of a prostate cancer cell line (PC3).

![media/image4.PNG](https://github.com/nilerolir/AutoStabilizer/blob/main/Code/AutoStabilizer-v1.3-/Images/Fig%204.PNG)

### Figure 5: Execution of the Macro-v1.3- code. Once ImageJ/Fiji is open, select `Plugins > Macros > Run > Macro-v1.3-` (5A). Macro window in the ImageJ/Fiji root directory with the Macro-v1.3- code (5B). Macro execution and editing console in ImageJ/Fiji: The code is built in Jython. Once the code is executed (by pressing Run), a welcome message will appear in the console, naming all the variables registered in the `Config.txt` configuration file dictionary (5C). Text file with the same information printed in the macro editing window, located in the `LogFolder` (5D).

![media/image5.PNG](https://github.com/nilerolir/AutoStabilizer/blob/main/Code/AutoStabilizer-v1.3-/Images/Fig%205.png)
