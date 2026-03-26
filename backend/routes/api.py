from flask import Blueprint, request, jsonify, render_template
from models.image_classifier import classify_image
from utils.database import get_db_connection
import os
from PIL import Image, ImageDraw, ImageFont

api = Blueprint('api', __name__)

@api.route('/upload', methods=['GET'])
def upload_page():
    """
    Serve the HTML page for image upload.
    """
    return render_template('upload.html')

@api.route('/api/upload', methods=['POST'])
def upload_image():
    """
    Endpoint to upload an image, classify items, and return annotated image.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']

    # Ensure the 'temp' directory exists
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    image_path = f"{temp_dir}/{image.filename}"
    image.save(image_path)

    try:
        predictions = classify_image(image_path)

        # Map predictions to class labels
        class_labels = ['milk', 'eggs', 'cheese', 'butter', 'yogurt', 'juice', 'vegetables']  # Replace with your actual class labels
        results = {label: f"{prob * 100:.2f}%" for label, prob in zip(class_labels, predictions[0])}

        # Annotate the image
        annotated_image_path = f"{temp_dir}/annotated_{image.filename}"
        annotate_image(image_path, predictions[0], class_labels, annotated_image_path)

        os.remove(image_path)  # Clean up the original image
        return jsonify({"predictions": results, "annotated_image_url": f"/{annotated_image_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def annotate_image(image_path, predictions, class_labels, output_path):
    """
    Annotate the image with predictions and bounding boxes, then save it.
    """
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Example: Simulate bounding boxes (replace with actual coordinates if available)
    width, height = image.size
    box_height = height // len(class_labels)  # Divide the image into sections for each label

    font = ImageFont.load_default()

    for i, (label, prob) in enumerate(zip(class_labels, predictions)):
        # Simulate a bounding box
        top_left = (10, i * box_height)
        bottom_right = (width - 10, (i + 1) * box_height - 10)
        draw.rectangle([top_left, bottom_right], outline="red", width=3)

        # Add label and confidence score
        text = f"{label}: {prob * 100:.2f}%"
        text_position = (top_left[0] + 5, top_left[1] + 5)
        draw.text(text_position, text, fill="red", font=font)

    image.save(output_path)

@api.route('/recipes', methods=['GET'])
def get_recipes():
    """
    Endpoint to retrieve recipes based on classified items.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes ORDER BY confidence DESC')
    recipes = cursor.fetchall()
    conn.close()

    return jsonify({"recipes": [dict(recipe) for recipe in recipes]})