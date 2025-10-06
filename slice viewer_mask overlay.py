#----------------HOW TO USE-----------------

# Essentially the same as slice viewer.py. Only differnce is that the mask specified in pred_path will be overlayed above the file from baseline_path

# ---------------END-----------------------

import nibabel as nib
import matplotlib
matplotlib.use("TkAgg")   # ensure GUI backend
import matplotlib.pyplot as plt
import numpy as np

# --- Load baseline (MRI) ---
baseline_path = r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\nnUNet_raw_data_base\nnUNet_raw_data\Task789_LABC\imagesTs\Breast_0006_0001.nii.gz"
baseline_path = r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\SampleISPY2Data\ISPY2 3D Image Arrays\Breast_0009_0001.nii.gz"
baseline_path = r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\SampleISPY2Data\ISPY2 3D Image Arrays\Experimental 10.3\Breast_0002_0000.nii.gz"
baseline_path = r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\nnUNet_raw_data_base\nnUNet_raw_data\Task789_LABC\imagesTs\Breast_0002_0000.nii.gz"
baseline_path = r"D:\OneDrive - UW\QBI lab\Testing Space\Cropped original\Breast_0002_0002.nii.gz"
baseline = nib.load(baseline_path).get_fdata()

# --- Load prediction (segmentation mask) ---
# Replace this with your actual prediction NIfTI file
pred_path = r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\nnUNet_raw_data_base\RESULTS_FOLDER\Prediction\Breast_0006.nii.gz"
pred_path = r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\SampleISPY2Data\ISPY2 3D Image Arrays\Experimental 10.4\Breast_0002_breast_mask.nii.gz"
pred_path = r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\nnUNet_raw_data_base\RESULTS_FOLDER\Prediction\Breast_0002.nii.gz"
pred_path = r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\SampleISPY2Data\ISPY2 3D Image Arrays\Experimental 10.4\Breast_0002_tumor_ROI_nonec.nii.gz"
pred_path = r"D:\OneDrive - UW\QBI lab\Testing Space\Breast_0002_tumor_ROI_nonec.nii.gz"

pred = nib.load(pred_path).get_fdata()

# --- check shapes match ---
if baseline.shape != pred.shape:
    raise ValueError(f"Shape mismatch: baseline {baseline.shape}, prediction {pred.shape}")

# --- Start from the middle slice ---
slice_idx = baseline.shape[2] // 2

fig, ax = plt.subplots()
ax.axis("off")

# baseline grayscale
img_base = ax.imshow(baseline[:, :, slice_idx], cmap="gray")

# build RGBA red mask
overlay = np.zeros(baseline[:, :, slice_idx].shape + (4,), dtype=np.float32)
mask_slice = pred[:, :, slice_idx] > 0
overlay[mask_slice, 0] = 1.0  # Red channel
overlay[mask_slice, 1] = 0.0  # Green
overlay[mask_slice, 2] = 0.0  # Blue
overlay[mask_slice, 3] = 0.4  # Alpha (transparency)

img_pred = ax.imshow(overlay)

ax.set_title(f"Slice {slice_idx}/{baseline.shape[2]-1}")

def on_key(event):
    global slice_idx, overlay
    if event.key == "right":
        slice_idx = (slice_idx + 1) % baseline.shape[2]
    elif event.key == "left":
        slice_idx = (slice_idx - 1) % baseline.shape[2]
    else:
        return
    img_base.set_data(baseline[:, :, slice_idx])

    # update overlay
    overlay = np.zeros(baseline[:, :, slice_idx].shape + (4,), dtype=np.float32)
    mask_slice = pred[:, :, slice_idx] > 0
    overlay[mask_slice, 0] = 1.0
    overlay[mask_slice, 3] = 0.4
    img_pred.set_data(overlay)

    ax.set_title(f"Slice {slice_idx}/{baseline.shape[2]-1}")
    fig.canvas.draw_idle()

fig.canvas.mpl_connect("key_press_event", on_key)
plt.show(block=True)