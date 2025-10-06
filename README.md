# Pipeline for testing Janse Model with ISPY2
This repo contains the code and information needed to run the said pipeline from preprocessing to running inference and visualization.
Manual below follows windows + WSL setup. I think the only difference for mac or linux VM users would be doing both steps A and B on the same os, instead of doing A on windows and B on wsl.

# Table of Contents
A. Setting up Windows environment: kernals, files, folders, model weight, etc.
B. Setting up Linux environment: kernals, pytorch library modification
C. Running preprocessing
D. Running inference
E. Visualization

# A. Windows Environment Setup
1. Clone Janse git repo into windows PC. Check that the model weights are ~100mb, not 1kB.
2. Download ISPY2 data into your windows PC. Preserve the original file structure.
3. Need to hand-build file on windows folders. Choose a rootdirectory that is going to be your workspace and create a folder named nnUNet_raw_data_base.
   
   Hand build file folders as shown below. Any file you see below that ends with an extension is coming from the cloned Janse git repo.
   
   
   C:/rootdirectory/nnUNet_raw_data_base/
   ├── nnUNet_raw_data
       ├── Task789_LABC   
          ├── imagesTr
          ├── imagesTs
          └── labelsTr
   ├── RESULTS_FOLDER
       ├──Prediction
           ├── postprocessing.json
           ├── plans.pkl
       ├── nnUNet
           ├── 3d_fullres
               ├── Task789_LABC
                   ├── nnUNetTrainerV2__nnUNetPlansv2.1
                       ├── plans.pkl
                       ├── postprocessing.json
                       ├── fold_0
                           ├── debug.json
                           ├── model_best_model.MODEL
                           ├── model_best_model.pkl
                           ├── model_final_checkpoint.model.MODEL
                           ├── model_final_checkpoint.model.pkl
                           ├── postprocessing.json

# B. Setting up wsl environment. I used ubuntu. 
IMPORTANT: IF YOURE NOT RUNNING INFERENCE, SKIP THIS STEP AND GO TO SECTION C
   
   a. Need to install CUDA + Pytorch + nnUNet on wsl. Then set up environment variables so wsl can find file locations.
     Do:
         Go to this link, find section "Installation". https://github.com/MIC-DKFZ/nnUNet/tree/nnunetv1
         Complete section 1,2,3,4 under installation.
   
   b. Need to edit nnunet source code.
       Find all occurences of torch.load() across the entire nnunet source code. For each occurence, add the parameter 'weights_only=False' into torch.load().
       FYI, I think I found 3 or 4 occurences of torch.load().
      
# C. Running preprocessing
1. Open Preprocessing_sample_crop 10.5 test.ipynb downloaded from this git repo.
2. Make a python kernal that has all the packages specified in the first cell of the notebook.
3. From this point on, you can run the notebook without any changes except changing directories to your own.
    I would recommend making a Test folder similar to how the notebook has. Location of the test folder can be anywhere, just make sure you change directories in the notebook.
4. Once you are done running the notebook (completed dataset.json) you need to copy some things to the right location.
   if you saved dataset.json under "nnUNet_raw_data_base\nnUNet_raw_data\Task789_LABC\" then no need to copy.
   if you saved that json somewhere else, copy to the location specified above.

   we need to have cropped image files copied over to imagesTs folder. Shown below.
   
   C:/rootdirectory/nnUNet_raw_data_base/
   ├── nnUNet_raw_data
       ├── Task789_LABC   
          ├── imagesTs
               ├──"Patient_0001_0000.nii.gz"
               ├──"Patient_0001_0001.nii.gz"
                 ....
               ├──"Patient_0009_0005.nii.gz"

   # D. Running inference.
   open wsl. running the code below will save results in the RESULTS>Prediction folder. Took less than a minute for 9 patients on RTX 4080 cuda 12.9

   nnUNet_predict   -i "$nnUNet_raw_data_base/nnUNet_raw_data/Task789_LABC/imagesTs"   -o "$RESULTS_FOLDER/Prediction"   -t 789 -m 3d_fullres

   # E. Visualization
      once you have the predictions you can use your own tools to visualizee .nii.gz files or you can use mine from the repo. Just change directories appropriately.
     If you want to visualize a 3D image use slice viewer.py. If you want to overlay a mask and an image use slice viewer_mask overlay.py

