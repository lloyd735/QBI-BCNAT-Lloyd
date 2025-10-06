#----------------HOW-TO-USE--------------------

# this function will let you open ANY 3D nii.gz file shaped (x,y,z) where z is the slice axis
# so you can use this for original breast images, cropped original, masks, etc. As long as they are shaped correctly (xyz)
# you can use keyboard left and right arrow to flip through 2D layers of the 3D image

# the only thing that needs to be changed is the line that calls nii.gz files.
# change the directory of the line nii = nib.load(r"directory_to_3D_image")

# I used anaconda prompt to actually run this visualization tool, but there are other ways too.
# my anaconda prompt:
#conda activate LABC
#D:
#cd "D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\My code"
#python "slice viewer.py"

#----------------END----------------------------

import nibabel as nib
import matplotlib
import numpy as np
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# Load File
#nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\nnUNet_raw_data_base\RESULTS_FOLDER\Prediction\Breast_0001.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\Elastix\Original\Breast_0001_0001.nii.gz")
#nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\Elastix\Original\Breast_0001_0000.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\nnUNet_raw_data_base\nnUNet_raw_data\Task789_LABC\imagesTs\Breast_0009_0000.nii.gz")
#nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\Elastix\Registered\Breast_0001_0001.nii.gz")
#nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\Elastix\Registered\Cropped\pre_cropped_0009.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\Elastix\Registered\Cropped\pre_cropped_0009_old.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\Elastix\Registered\Cropped\pre_cropped_0009.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\nnUNet_raw_data_base\nnUNet_raw_data\Task789_LABC\imagesTs\Breast_0001_0000.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\Elastix\Registered\Cropped\Breast_0009_0000_cropped.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\nnUNet_raw_data_base\nnUNet_raw_data\Task789_LABC\imagesTs\Breast_0009_0000.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\SampleISPY2Data\ISPY2 3D Image Arrays\Breast_0002_0000.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\SampleISPY2Data\ISPY2 3D Image Arrays\Experimental 10.3\Breast_0009_0003.nii.gz")
nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\SampleISPY2Data\ISPY2 3D Image Arrays\Experimental 10.5\Breast_0007_0000.nii.gz")
#nii = nib.load(r"D:\OneDrive - UW\QBI lab\BCNAT\Lloyd735\Janse Segmentation\nnUNet_raw_data_base\RESULTS_FOLDER\Prediction\Breast_0002.nii.gz")

data = nii.get_fdata()

# Start from the middle slice
slice_idx = data.shape[2] // 2

fig, ax = plt.subplots()
img = ax.imshow(data[:, :, slice_idx], cmap="gray")
ax.set_title(f"Slice {slice_idx}/{data.shape[2]-1}")
ax.axis("off")

def on_key(event):
    global slice_idx
    if event.key == "right":
        slice_idx = (slice_idx + 1) % data.shape[2]
    elif event.key == "left":
        slice_idx = (slice_idx - 1) % data.shape[2]
    else:
        return
    img.set_data(data[:, :, slice_idx])
    ax.set_title(f"Slice {slice_idx}/{data.shape[2]-1}")
    fig.canvas.draw_idle()

fig.canvas.mpl_connect("key_press_event", on_key)

plt.show(block=True)
