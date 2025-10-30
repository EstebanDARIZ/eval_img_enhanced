import numpy as np
import os
import glob
from PIL import Image
import scipy
# Patch pour compatibilité imquality / libsvm
if not hasattr(scipy, "ndarray"):
    scipy.ndarray = np.ndarray
from imquality import brisque

from config import RAW_DATA_PATH, PROCESSED_DATA_PATH
from niqe import niqe  
from uciqe import uciqe  


def evaluate_folder(folder_path):
    niqe_scores = []
    uciqe_scores = []
    brisque_scores = []

    for img_path in glob.glob(os.path.join(folder_path, "*.png")):
        # Load grayscale for NIQE
        img = np.array(Image.open(img_path).convert('L'))
        niqe_score = niqe(img)
        uciqe_score = uciqe(img_path)
        img_rgb = np.array(Image.open(img_path).convert('RGB'))
        brisque_score = brisque.score(img_rgb)

        niqe_scores.append(niqe_score)
        uciqe_scores.append(uciqe_score)
        brisque_scores.append(brisque_score)    

    return np.mean(niqe_scores), np.mean(uciqe_scores), np.mean(brisque_scores)


if __name__ == "__main__":
    print("=== Evaluation Pipeline ===")

    print(f"RAW images folder: {RAW_DATA_PATH}")
    print(f"PROCESSED images folder: {PROCESSED_DATA_PATH}")

    # # Compute for raw
    # raw_niqe, raw_uciqe, raw_brisque = evaluate_folder(RAW_DATA_PATH)
    # # Compute for processed
    # proc_niqe, proc_uciqe, proc_brisque = evaluate_folder(PROCESSED_DATA_PATH)

    # print("\n===== RESULTS =====")
    # print(f"RAW:       UCIQE = {raw_uciqe:.3f},  NIQE = {raw_niqe:.3f},  Brisque = {raw_brisque:.3f}")
    # print(f"PROCESSED: UCIQE = {proc_uciqe:.3f},  NIQE = {proc_niqe:.3f},  Brisque = {proc_brisque:.3f}")
    # print("-----------------------------------")
    # print(f"Δ NIQE  (↓ better): {raw_niqe - proc_niqe:.3f}")
    # print(f"Δ UCIQE (↑ better): {proc_uciqe - raw_uciqe:.3f}")
    # print(f"Δ Brisque (↓ better): {raw_brisque - proc_brisque:.3f}")            
