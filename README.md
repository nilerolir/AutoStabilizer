# 1. AutoStabilizer
The repository will contain a macro developed for Python in Jython for ImageJ/FIJI that aims to streamline the processing of microscopy images for cell migration experiments, obtained from the Cell culture Muvicyte system. The macro allows receiving images from a folder called `InputFolder`, where image stacks are stored with the following structure: `Well (A01)\POINT (0001)\Bright (Stack)\images`. This structure supports a wide configuration of wells, points of interest, and their corresponding microscopy image stacks. The system immediately orients the migration direction of all loaded image stacks from left to right using the `Custom Vision -- Azure -- Microsoft` system. Additionally, it processes the image stacks in the Bright folder, converting them into `AVI` format videos. This processing facilitates advanced analyses, such as particle image velocimetry (PIV). The repository will include the macro, detailed documentation, and usage examples.

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

## 3. Macro-v1.3 Installation

1. Download the macro "Macro-v1.4.4" from this repository.   

2. Extract the files `Config.txt` and `AutoStabilizer_v1.4.4_.ijm.py`, figure 1A. Then, copy the `Config.txt` file to the ImageJ/Fiji root directory as shown in figure 1B and the `AutoStabilizer_1.4.4_ijm.py` file to the Macros folder in the ImageJ/Fiji directory as shown in Figure 1C.
   
3. To execute this code follow the steps below: Once ImageJ/Fiji is open select Plugins > Macros > Run > AutoStabilizer_v1.4.4_EN_.ijm.py as shown in figure 2.

4. Once the code is executed, a configuration window will open as shown in figure 3. 

In `Working directory` you can select the location of your working directory, which by default will be called `Work folder AutoStabilizer` with three subfolders `LogFolder, InputFolder, OutputFolder` as shown in Figure 4A. Also, in `Folder to copy` you can select some folder with many microscopy images stored in the form: `Pocillo (A01)\POINT (0001)\Brigth (Stack)\Images` as shown in figure 4B, C, D.



Translated with DeepL.com (free version)

5. Before running the code, create a working folder in Documents or another target location, for example, `AutoStabilizer Working Folder`. Inside this folder, create the following subfolders: `Log`, `InputFolder`, and `OutputFolder` as shown in Figure 3A. Copy images into the `InputFolder` as shown in Figure 3B.

6. Copy the paths of the `Log`, `InputFolder`, and `OutputFolder` folders into the `Config.txt` file as shown in Figure 4.

7. In ImageJ/Fiji, follow these steps: Once ImageJ/Fiji is open, select `Plugins > Macros > Run > Macro-v1.3-` as shown in Figure 5A,B.

8. You can view the macro's execution in real-time from the ImageJ/Fiji macro editor console, as shown in Figure 5C. To do this, follow these steps: Once ImageJ/Fiji is open, select `Plugins > Macros > Edit > Macro-v1.3-`.



---
## 🚀 **Key Features**
- **Automatic motion correction:** Leverages ImageJ plugins like `TurboReg` and `MultiStackReg`.
- **Standardized outputs:** Generates stabilized videos ready for quantitative analysis.
- **Use macro-tool interface:** Simple configuration tailored to various video types.
---
## 🖥️ **Requirements**
- **Required software:**
  - [FIJI/ImageJ](https://imagej.net/software/fiji/) (latest version recommended).
  - Plugins:
    - [TurboReg](https://imagej.net/plugins/turboreg)
    - [MultiStackReg](https://imagej.net/plugins/multistackreg)
- **Operating systems:** Windows, macOS, or Linux.
- **Necessary files:** The macro (`AutoStabilicer.ijm.py`) and an configuration file (`Config.txt`).
---
## 🔧 **Installation**
1. **Download the file:**  
   Obtain the `AutoStabilicer.ijm.py` file from this repository.
2. **Place it in FIJI:**  
   Save the file in FIJI’s macros folder (`/macros/`).
3. **Verify plugins:**  
   Ensure `TurboReg` and `MultiStackReg` are installed.
---
## 🛠️ **How to Use**
1. **Open FIJI:**  
   Launch FIJI/ImageJ software.
2. **Load the macro:**  
   From the menu, select `Plugins > Macros > Run` and choose `AutoStabilicer.ijm.py`.
3. **Configure the macro:**  
   Specify the directory containing your input videos and the folder for the processed results. Before running the code, create three folders in Documents or another destination location: `Log`, `InputFolder`, and `OutputFolder`. Additionally, the images to be processed should be in .tif format; copy all the images to be processed into the `InputFolder` folder.
4. **Run the macro:**  
   The script will automatically process all videos, correcting objective movements.
---
## 🧪 **Example Use Case**
- **Input:**  
 The macro by default supports 6 simultaneous experiments in the format `{A01, A02, A03, B01, B02, B03}`. For the macro to function, the file names can later be modified directly in the code as needed.

This code was developed to work with 6-well multi-well plates, with data extracted from the Muvicyte live-cell imaging acquisition system. This explains the organization of the Input folders. Inside each folder, following the format A01 and so on, create subfolders named `{POINT 00001, POINT 00002, …, POINT 000010}`. Within each POINT folder, create a subfolder named BRIGHT containing all the images from the experiment conducted or the registered point of interest.

The macro will not throw an error if fewer POINT folders are present than those specified in the code. If there are more, it will simply not analyze them unless modifications are made in the code.

When working with images locally obtained from the Muvicyte live-cell microscopy acquisition system, the steps can be reduced to copying all the experiment folders into the `InputFolder` folder..
---
- **Output:**  
  Stabilized videos ready for advanced analysis with the same organization of imput foldes are in `Processed` folder.
---
## 📄 **Config.txt**
The configuration file Config.txt contains a number of important parameters for script operation. Among these are the locations of the working folders `{InputFolder, LogFolder, OutputFolder}`, `{ReadFolders, CreateFolders}` containing the subfolders `{A01,A02,A03,B01,B02,B03}` in both cases, `{BrightFoldersPoint}` containing the subfolders `{POINT 00001/BRIGHT,POINT 00002/BRIGHT, . ..}` and execution variables `{Debug, Advance, Viewer, Dev}`.

---
## License
El contenido general de este proyecto se encuentra bajo licencia Creative Commons Attribution 3.0 Unported, y el código asociado se encuetra bajo licencia GNU General Public License v3.0.
The general content of this project is licensed under the Creative Commons Attribution 3.0 Unported license, and the asociated source code is licensed under the GNU General Public License v3.0. 

## 🤝 **Contributions**
Contributions are welcome! If you find bugs or have suggestions for improvement, feel free to open an *issue* or submit a *pull request*.
---
## 📫 **Contact**
Author: **Nicolás Roa**  
Email: [nilerolirl@gmail.com](mailto:nilerolir@gmail.com)  
