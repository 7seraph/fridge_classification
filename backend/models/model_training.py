import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Paths
data_dir = "c:/Users/Kevin Tran/Desktop/big projects/backend/data/Refrigerator_Contents_7_Classes_Dataset/organized_dataset"
annotations_path = "c:/Users/Kevin Tran/Desktop/big projects/backend/data/annotations.json"

# Load bounding box annotations
with open(annotations_path, "r") as f:
    annotations = json.load(f)

# Data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

def data_generator_with_bboxes(generator):
    """
    Custom data generator to include bounding box annotations.
    """
    while True:
        images, labels = next(generator)
        bboxes = []
        for filename in generator.filenames:
            image_id = os.path.basename(filename)
            bboxes.append(annotations[image_id]["bbox"])  # Assuming bbox is in [x1, y1, x2, y2] format
        yield images, [labels, np.array(bboxes)]

train_generator_with_bboxes = data_generator_with_bboxes(train_generator)
val_generator_with_bboxes = data_generator_with_bboxes(val_generator)

# Build the model
def build_model(input_shape, num_classes):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def build_model_with_bboxes(input_shape, num_classes):
    """
    Build a model that predicts both class probabilities and bounding boxes.
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes + 4, activation='sigmoid')  # num_classes for class probabilities, 4 for bounding boxes
    ])
    model.compile(
        optimizer='adam',
        loss={
            'class_probs': 'categorical_crossentropy',
            'bboxes': 'mean_squared_error'
        },
        metrics={
            'class_probs': 'accuracy',
            'bboxes': 'mse'
        }
    )
    return model

# Model training
input_shape = (224, 224, 3)
num_classes = len(train_generator.class_indices)
model = build_model_with_bboxes(input_shape, num_classes)

history = model.fit(
    train_generator_with_bboxes,
    epochs=10,
    validation_data=val_generator_with_bboxes,
    steps_per_epoch=len(train_generator),
    validation_steps=len(val_generator)
)

# Save the model
model.save("c:/Users/Kevin Tran/Desktop/big projects/backend/data/fridge_model_with_bboxes.h5")
print("Model training complete. Saved as fridge_model_with_bboxes.h5")
