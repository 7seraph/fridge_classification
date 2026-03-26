import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Paths
model_path = "../data/fridge_model.h5"
data_dir = "c:/Users/Kevin Tran/Desktop/big projects/backend/data/Refrigerator_Contents_7_Classes_Dataset/organized_dataset"

# Load the trained model
model = load_model(model_path)

# Data generator for testing
test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    data_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(test_generator)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

# Predict on test data
predictions = model.predict(test_generator)
print("Sample Predictions:")
for i, pred in enumerate(predictions[:5]):
    print(f"Image {i+1}: {pred}")