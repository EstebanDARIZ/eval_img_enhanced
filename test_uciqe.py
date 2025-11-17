import numpy as np
import os
import glob
import scipy


import time

from config import RAW_DATA_PATH, PROCESSED_DATA_PATH
from uciqe import uciqe, uciqe_mod, uciqe_dec


def evaluate_folder(folder_path):
    uciqe_scores = []
    uciqe_mod_scores = []
    uciqe_chro_scores = []
    uciqe_lum_scores = []
    uciqe_sat_scores = []

    img_paths = sorted(glob.glob(os.path.join(folder_path, "*.png")) +
                       glob.glob(os.path.join(folder_path, "*.jpg")) +
                       glob.glob(os.path.join(folder_path, "*.jpeg")))

    for img_path in img_paths:
        uciqe_score = uciqe(img_path)
        uciqe_mod_score = uciqe_mod(img_path)
        uciqe_chro_score, uciqe_lum_score, uciqe_sat_score = uciqe_dec(img_path)

        uciqe_scores.append(uciqe_score)
        uciqe_mod_scores.append(uciqe_mod_score)  
        uciqe_chro_scores.append(uciqe_chro_score)
        uciqe_lum_scores.append(uciqe_lum_score)
        uciqe_sat_scores.append(uciqe_sat_score)

    return np.mean(uciqe_scores), np.mean(uciqe_mod_scores), np.mean(uciqe_chro_scores), np.mean(uciqe_lum_scores), np.mean(uciqe_sat_scores)


if __name__ == "__main__":
    t0 = time.time()
    print("=== Evaluation Pipeline ===")

    print(f"RAW images folder: {RAW_DATA_PATH}")
    print(f"PROCESSED images folder: {PROCESSED_DATA_PATH}")

    # Compute for raw
    raw_uciqe, raw_uciqe_mod, raw_uciqe_chro, raw_uciqe_lum, raw_uciqe_sat = evaluate_folder(RAW_DATA_PATH)
    # Compute for processed
    proc_uciqe, proc_uciqe_mod, proc_uciqe_chro, proc_uciqe_lum, proc_uciqe_sat = evaluate_folder(PROCESSED_DATA_PATH)

    print("\n===== RESULTS =====")
    print(f"RAW:       UCIQE = {raw_uciqe:.3f},  UCIQE_mod = {raw_uciqe_mod:.3f}, UCIQE_chro = {raw_uciqe_chro:.3f}, UCIQE_lum = {raw_uciqe_lum:.3f}, UCIQE_sat = {raw_uciqe_sat:.3f}")
    print(f"PROCESSED: UCIQE = {proc_uciqe:.3f},  UCIQE_mod = {proc_uciqe_mod:.3f}, UCIQE_chro = {proc_uciqe_chro:.3f}, UCIQE_lum = {proc_uciqe_lum:.3f}, UCIQE_sat = {proc_uciqe_sat:.3f}")
    print("-----------------------------------")

    # Deltas
    delta_uciqe = proc_uciqe - raw_uciqe
    delta_uciqe_mod = proc_uciqe_mod - raw_uciqe_mod
    delta_uciqe_chro = proc_uciqe_chro - raw_uciqe_chro
    delta_uciqe_lum = proc_uciqe_lum - raw_uciqe
    delta_uciqe_sat = proc_uciqe_sat - raw_uciqe_sat
    # Deltas in %
    delta_uciqe_pct = (delta_uciqe / raw_uciqe) * 100 if raw_uciqe != 0 else 0
    delta_uciqe_mod_pct = (delta_uciqe_mod / raw_uciqe_mod) * 100 if raw_uciqe_mod != 0 else 0
    delta_uciqe_chro_pct = (delta_uciqe_chro / raw_uciqe_chro) * 100 if raw_uciqe_chro != 0 else 0
    delta_uciqe_lum_pct = (delta_uciqe_lum / raw_uciqe_lum) * 100 if raw_uciqe_lum != 0 else 0
    delta_uciqe_sat_pct = (delta_uciqe_sat / raw_uciqe_sat) * 100 if raw_uciqe_sat != 0 else 0
    # Printing results
    print(f"Δ UCIQE (↑ better): {delta_uciqe:.3f}  ({delta_uciqe_pct:+.3f}%)")
    print(f"Δ UCIQE_mod (↑ better): {delta_uciqe_mod:.3f}  ({delta_uciqe_mod_pct:+.3f}%)")  
    print(f"Δ UCIQE_chro (↑ better): {delta_uciqe_chro:.3f}  ({delta_uciqe_chro_pct:+.3f}%)")
    print(f"Δ UCIQE_lum (↑ better): {delta_uciqe_lum:.3f}  ({delta_uciqe_lum_pct:+.3f}%)")
    print(f"Δ UCIQE_sat (↑ better): {delta_uciqe_sat:.3f}  ({delta_uciqe_sat_pct:+.3f}%)")          
    print("#######################################")
    print('Duration = ', time.time() -  t0)       
