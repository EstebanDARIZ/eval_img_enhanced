#  Underwater Image Quality Evaluation Pipeline

This project provides a **pipeline for evaluating the quality of underwater images** before and after enhancement, using three no-reference image quality metrics:

- **UCIQE** – Underwater Color Image Quality Evaluation (↑ higher is better)  
- **NIQE** – Naturalness Image Quality Evaluator (↓ lower is better)  
- **BRISQUE** – Blind/Referenceless Image Spatial Quality Evaluator (↓ lower is better)

---

##  Installation

### 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate       

### 2. Install dependencies
pip install -r requirements.txt

---

##  Usage

### 1. Configure paths
Edit `config.py` to set the directories containing your images:

RAW_DATA_PATH = "images/raw"
PROCESSED_DATA_PATH = "images/processed"

### 2. Run the evaluation
python main.py

---

##  Technical Overview

- **UCIQE** measures color and contrast quality of underwater images (higher = better).  
- **NIQE** evaluates the naturalness and texture distortion of an image (lower = better).  
- **BRISQUE** estimates perceptual degradation without a reference image (lower = better).

The pipeline:
1. Iterates through all `.png` images in each folder.
2. Computes all three metrics for each image.
3. Returns the mean values for each dataset.
4. Displays the differences between **RAW** and **PROCESSED** image sets.

---

##  References

- **UCIQE**: Yang, M., et al. *"Underwater image quality evaluation metric based on colorfulness, sharpness, and contrast."* ICIP, 2015.  
- **NIQE**: Mittal, A., et al. *"Making a completely blind image quality analyzer."* IEEE Signal Processing Letters, 2013.  
- **BRISQUE**: Mittal, A., et al. *"No-reference image quality assessment in the spatial domain."* IEEE Transactions on Image Processing, 2012.

---

## 👨‍🔬 Author

Developed by **Esteban Dreau-Darizcuren**  

---
