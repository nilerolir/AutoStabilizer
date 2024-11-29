# AutoStabilizer
The repository will contain a macro developed for Python in Jython for ImageJ/FIJI that corrects unwanted movements in live-cell microscopy videos. This processing facilitates advanced analyses, such as particle image velocimetry (PIV). The repository will include the macro, detailed documentation, and usage examples.
# Image Stabilization Macro for Microscopy Videos in ImageJ/FIJI
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
   Specify the directory containing your input videos and the folder for the processed results. Before running the code, create three folders in Documents or another destination location: `Log`, `To_be_processed`, and `Processed`. Additionally, the images to be processed should be in .tif format; copy all the images to be processed into the `To_be_processed` folder.
4. **Run the macro:**  
   The script will automatically process all videos, correcting objective movements.
---
## 🧪 **Example Use Case**
- **Input:**  
 The macro by default supports 6 simultaneous experiments in the format `{A01, A02, A03, B01, B02, B03}`. For the macro to function, the file names can later be modified directly in the code as needed.

This code was developed to work with 6-well multi-well plates, with data extracted from the Muvicyte live-cell imaging acquisition system. This explains the organization of the Input folders. Inside each folder, following the format A01 and so on, create subfolders named `{POINT 00001, POINT 00002, …, POINT 000010}`. Within each POINT folder, create a subfolder named BRIGHT containing all the images from the experiment conducted or the registered point of interest.

The macro will not throw an error if fewer POINT folders are present than those specified in the code. If there are more, it will simply not analyze them unless modifications are made in the code.

When working with images locally obtained from the Muvicyte live-cell microscopy acquisition system, the steps can be reduced to copying all the experiment folders into the `To_be_processed` folder..
---
- **Output:**  
  Stabilized videos ready for advanced analysis with the same organization of imput foldes are in `Processed` folder.
---
## 📄 **Config.txt**
- Open a text editor such as `Notepad` and create a text file named `Config.txt`.
- Define the following parameters without spaces or special characters:
  - LogFolder=C:\Users\Your-user\Documents\Log  
  - InputFolder=C:\Users\Your-user\Documents\To_be_processed
  - OutputFolder=C:\Users\Your-user\Documents\Processed
  - Debug=True  
  - Avance=True  
  - Visor=False  
- Save the text file in the (`/Fiji.app/`) folder
---
## 🤝 **Contributions**
Contributions are welcome! If you find bugs or have suggestions for improvement, feel free to open an *issue* or submit a *pull request*.
---
## 📫 **Contact**
Author: **Nicolás Roa**  
Email: [nilerolirl@gmail.com](mailto:nilerolir@gmail.com)  
