import cv2
import numpy as np



def uciqe(img_path):
    img_bgr = cv2.imread(img_path)
    if img_bgr is None:
        raise ValueError(f"Image not found or unreadable: {img_path}")

    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    coe_metric = [0.4680, 0.2745, 0.2576]

    img_lum = img_lab[..., 0] / 255
    img_a = img_lab[..., 1] / 255
    img_b = img_lab[..., 2] / 255

    img_chr = np.sqrt(img_a ** 2 + img_b ** 2)
    img_sat = img_chr / np.sqrt(img_chr ** 2 + img_lum ** 2)
    aver_sat = np.mean(img_sat)
    aver_chr = np.mean(img_chr)
    var_chr = np.sqrt(np.mean(np.abs(1 - (aver_chr / img_chr) ** 2)))

    nbins = 256 if img_lum.dtype == 'uint8' else 65536
    hist, bins = np.histogram(img_lum, nbins)
    cdf = np.cumsum(hist) / np.sum(hist)

    ilow = np.where(cdf > 0.01)[0][0]
    ihigh = np.where(cdf >= 0.99)[0][0]
    tol = [(ilow - 1) / (nbins - 1), (ihigh - 1) / (nbins - 1)]
    con_lum = tol[1] - tol[0]

    quality_val = coe_metric[0] * var_chr + coe_metric[1] * con_lum + coe_metric[2] * aver_sat
    return quality_val