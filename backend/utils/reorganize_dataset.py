import os
import shutil

# Path to the dataset directory
data_dir = "c:/Users/Kevin Tran/Desktop/big projects/backend/data/Refrigerator_Contents_7_Classes_Dataset/Refrigerator_Contents_7_Classes_Dataset"
output_dir = "c:/Users/Kevin Tran/Desktop/big projects/backend/data/Refrigerator_Contents_7_Classes_Dataset/organized_dataset"

# List of classes (based on dataset description)
classes = ["Banana", "Bread", "Eggs", "Milk", "Potato", "Spinach", "Tomato"]

# Create output directories for each class
os.makedirs(output_dir, exist_ok=True)
for class_name in classes:
    os.makedirs(os.path.join(output_dir, class_name), exist_ok=True)

# Reorganize images into class folders
for filename in os.listdir(data_dir):
    for class_name in classes:
        if class_name.lower() in filename.lower():
            src_path = os.path.join(data_dir, filename)
            dest_path = os.path.join(output_dir, class_name, filename)
            shutil.move(src_path, dest_path)
            break

print("Dataset reorganization complete. Organized dataset is located at:", output_dir)