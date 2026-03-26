import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Load the pre-trained model
MODEL_PATH = "c:/Users/Kevin Tran/Desktop/big projects/backend/data/fridge_model.h5"  # Replace with the actual path to your model
model = load_model(MODEL_PATH)

def preprocess_image(image_path):
    """
    Preprocess the image to the format required by the model.
    """
    image = Image.open(image_path).convert('RGB')
    image = image.resize((224, 224))  # Resize to model's input size
    image_array = np.array(image) / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

def classify_image(image_path):
    """
    Classify the image and return predictions.
    """
    processed_image = preprocess_image(image_path)
    predictions = model.predict(processed_image)
    return predictions

if __name__ == "__main__":
    # Example usage
    test_image_path = "path_to_test_image.jpg"  # Replace with an actual image path
    predictions = classify_image(test_image_path)
    print("Predictions:", predictions)