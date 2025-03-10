# AutoStabilizer_v1.4.4 Documentation

**Author**: Nicolás Roa  
**Date**: March 10, 2025  

---

## Overview

AutoStabilizer_v1.4.4 is a code developed for ImageJ/Fiji in jython (python) that streamlines the processing of microscopy images for cell migration experiments obtained from the Cell Culture Muvicyte system. The code organizes images in a folder called `InputFolder`, where image stacks follow this structure:
```
Well (A01)\POINT (0001)\Bright (Stack)\Images
```
```
AutoStabilizer Working Folder/  
  ├── LogFolder  
  ├── InputFolder  
  └── OutputFolder  
```
This setup supports multiple well configurations, points of interest, and their corresponding microscopy image stacks. The system automatically orients all loaded image stacks from left to right using `Custom Vision – Azure – Microsoft`. Additionally, the code converts image stacks from the Bright folder into `AVI` format videos.

When executed in ImageJ or Fiji, an interactive user interface appears, allowing for intuitive configuration of key parameters via a configuration file. This code is available in both Spanish (ES) and English (EN), differing only in the language of the reports and interface. This processing facilitates advanced analyses, such as particle image velocimetry (PIV).

---

## ImageJ/Fiji Installation

1. Download FIJI for your operating system from: [https://imagej.net/software/fiji/downloads](https://imagej.net/software/fiji/downloads).
2. Alternatively, download ImageJ from: [https://imagej.net/ij/download.html](https://imagej.net/ij/download.html). However, this code is optimized for FIJI.
3. Extract the downloaded `.zip` file:
   - **Windows**: Right-click > "Extract All..."
   - **Mac OS**: Double-click the `.zip` file
   - **Linux**: Right-click > "Extract Here"
4. **No installation required**: Simply place the extracted folder in a suitable location:
   - **Windows/Linux**: Store the extracted `fiji-<win64, win32, linux64, linux32>` directory in a writable location (e.g., Desktop, Documents).
   - **Mac OS**: Store `fiji-macosx` in the Documents folder (not "Applications" to avoid path randomization issues).
5. **Run FIJI**:
   - **Windows**: Navigate to `fiji-win<64 or 32>` > `Fiji.app` and double-click `ImageJ-win<64 or 32>.exe`.
   - **Mac OS**: Open `fiji-macosx` and double-click `FIJI.app`.
   - **Linux**: Open `fiji-linux64` > `Fiji.app` and double-click `ImageJ-linux64`.
---

## Code Installation & Usage

1. Download `AutoStabilizer_v1.4.4_.ijm.py` from the repository.
2. Extract the files `Config.txt` and `AutoStabilizer_v1.4.4_.ijm.py`:
   - Copy `Config.txt` to the ImageJ/Fiji root directory.
   - Copy `AutoStabilizer_v1.4.4_.ijm.py` to the macros folder inside ImageJ/Fiji.
3. Open ImageJ/Fiji and navigate to:
   - `Plugins > Macros > Run > AutoStabilizer_v1.4.4_.ijm.py`
4. A user interface will appear with the following options:
   - **Select working directory**: Creates a folder called `AutoStabilizer Working Folder` with subfolders `InputFolder`, `LogFolder`, and `OutputFolder`.
   - **Select data to copy to `InputFolder`**.
   - **Select culture plate size**: Affects only `OutputFolder`, not `InputFolder`.
   - **Custom button**: Configures which wells to analyze without affecting Points per well.

### Configuration Variables
- `Debug`: Enables execution messages in the LOG file (`LogFolder`).
- `Avance`: Displays execution progress percentage.
- `Visor`: Opens/closes images during processing (increases resource usage).
- `Dev`: Runs a test mode analyzing fewer images for quick verification.

Once settings are saved, they remain unchanged unless manually edited in `Config.txt`. Execution logs are stored in `LogFolder`, and processed videos (`AVI` format) appear in `OutputFolder` following the same structure as `InputFolder`.

---

## Figures & Attachments

### Figure 1: Running AutoStabilizer_v1.4.4
![media/image1.png](https://github.com/nilerolir/AutoStabilizer/blob/main/Images/AutoStabilizer_images_figures_1.png)

- Copy `Config.txt` to ImageJ/Fiji root (Fig. 1A).
- Copy `AutoStabilizer_v1.4.4_.ijm.py` to the macros folder (Fig. 1B).
- Open ImageJ/Fiji and run `Plugins > Macros > Run > AutoStabilizer_v1.4.4_.ijm.py` (Fig. 1C).
- Open the corresponding `.ijm.py` code (Fig. 1D).

### Figure 2: User Interface Overview
![media/image2.png](https://github.com/nilerolir/AutoStabilizer/blob/main/Images/AutoStabilizer_images_figures_2.png)

- **Select working directory** (Fig. 2A).
- **Choose data to copy to `InputFolder`** (Fig. 2A).
- **Set culture plate size** (Fig. 2B).
- **Customize well selection** via "Custom" button (Fig. 2C).
- **Configuration Variables** if they are marked they are considered active, otherwise they are inactive(Fig. 2D)

### Figure 3: AutoStabilizer Working Folder
![media/image3.png](https://github.com/nilerolir/AutoStabilizer/blob/main/Images/AutoStabilizer_images_figures_3.png)

- **Folders created**: `InputFolder`, `LogFolder`, `OutputFolder` (Fig. 3A). **InputFolder**: Stores raw data (Fig. 3B).
- **Data per well**: Multiple records per well (Fig. 3C).
- **Image stacks**: Example with 96-frame "BRIGHT" stack (Fig. 3D).
- **LogFolder**: Stores execution logs (Fig. 3E).
- **OutputFolder**: Contains results (Fig. 3F, 3G).

---

## 🧪 **Example Use Case**

**Input:**  
```
Well (A01)/  
  ├── POINT (00001)/  
  │   └── Bright/  
  │       └── Images.tif  
  └── POINT (00002)/  
      └── Bright/  
          └── Images.tif  
```

- The code by default supports 6 simultaneous experiments in the format `{A01, A02, A03, B01, B02, B03}`. For the code to function, the file names can later be modified directly in the code as needed.

- This code was developed to work with 6-well multi-well plates, with data extracted from the Muvicyte live-cell imaging acquisition system. This explains the organization of the Input folders. Inside each folder, following the format A01 and so on, create subfolders named `{POINT 00001, POINT 00002, …, POINT 000010}`. Within each POINT folder, create a subfolder named BRIGHT containing all the images from the experiment conducted or the registered point of interest.

- The code will not throw an error if fewer POINT folders are present than those specified in the code. If there are more, it will simply not analyze them unless modifications are made in the code.

- When working with images locally obtained from the Muvicyte live-cell microscopy acquisition system, the steps can be reduced to copying all the experiment folders into the `InputFolder` folder..

**Output:**  

- Stabilized videos ready for advanced analysis with the same organization of imput foldes are in `Processed` folder.
```
OutputFolder/  
  └── Well (A01)/  
      └── POINT (00001)/  
          └── Video_Stabilized.avi 
```


### Logs:  
- Execution logs in `LogFolder` with timestamps, errors, and configurations. 

---

## 📄 Configuration File (**Config.txt**) 
The configuration file Config.txt contains a number of important parameters for script operation.

**Key parameters**:  
- Paths: `InputFolder`, `LogFolder`, `OutputFolder`.  
- Subfolders: `ReadFolders`, `CreateFolders` (e.g., `A01, B02`).  
- Image stacks: `BrightFoldersPoint` (e.g., `POINT 00001/Bright`).  
- Flags: `Debug`, `Progress`, `Viewer`, `Dev`.  

---

## Troubleshooting  
- **Missing plugins**: Install via Fiji’s update manager.  
- **Path errors**: Ensure folders have write permissions.  
- **Test mode**: Use `Dev` for quick validation.

---

> **Note**: For visual guides (e.g., folder structures, interface screenshots), refer to the original documentation. Images are omitted here but marked with placeholders like

---

## License
This project is licensed under **Creative Commons Attribution 3.0 Unported**, while the associated code is under **GNU General Public License v3.0**.

---

## Contributions
Contributions are welcome! Report issues or submit pull requests to improve the project.

---

## Contact
**Author**: Nicolás Roa  
📧 [nilerolirl@gmail.com](mailto:nilerolir@gmail.com)
