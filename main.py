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

    img_paths = sorted(glob.glob(os.path.join(folder_path, "*.png")) +
                       glob.glob(os.path.join(folder_path, "*.jpg")) +
                       glob.glob(os.path.join(folder_path, "*.jpeg")))

    for img_path in img_paths:
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

    # Compute for raw
    raw_niqe, raw_uciqe, raw_brisque = evaluate_folder(RAW_DATA_PATH)
    # Compute for processed
    proc_niqe, proc_uciqe, proc_brisque = evaluate_folder(PROCESSED_DATA_PATH)

    print("\n===== RESULTS =====")
    print(f"RAW:       UCIQE = {raw_uciqe:.3f},  NIQE = {raw_niqe:.3f},  Brisque = {raw_brisque:.3f}")
    print(f"PROCESSED: UCIQE = {proc_uciqe:.3f},  NIQE = {proc_niqe:.3f},  Brisque = {proc_brisque:.3f}")
    print("-----------------------------------")

    # Deltas
    delta_niqe = raw_niqe - proc_niqe
    delta_uciqe = proc_uciqe - raw_uciqe
    delta_brisque = raw_brisque - proc_brisque
    # Deltas in %
    delta_niqe_pct = (delta_niqe / raw_niqe) * 100 if raw_niqe != 0 else 0
    delta_uciqe_pct = (delta_uciqe / raw_uciqe) * 100 if raw_uciqe != 0 else 0
    delta_brisque_pct = (delta_brisque / raw_brisque) * 100 if raw_brisque != 0 else 0

    # Printing results
    print(f"Δ UCIQE (↑ better): {delta_uciqe:.3f}  ({delta_uciqe_pct:+.2f}%)")
    print(f"Δ NIQE  (↓ better): {delta_niqe:.3f}  ({delta_niqe_pct:+.2f}%)")
    print(f"Δ Brisque (↓ better): {delta_brisque:.3f}  ({delta_brisque_pct:+.2f}%)")          
