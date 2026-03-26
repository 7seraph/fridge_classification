# Backend for Fridge Image Classifier and Recipe Generator

## Overview
This backend application allows users to upload images of their fridge contents, classify the items using a pre-trained image classification model, and retrieve recipes based on the identified items. Recipes are ranked by confidence score.

## Features
- **Image Upload**: Upload images of fridge contents.
- **Image Classification**: Classify items in the image using a TensorFlow model.
- **Recipe Retrieval**: Retrieve recipes ranked by confidence score.
- **Database Integration**: Store and retrieve recipes from an SQLite database.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Pip
- Virtual Environment (optional but recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Initialization
1. Ensure the `data/` directory exists.
2. Run the following command to initialize the database:
   ```bash
   python utils/database.py
   ```

### Running the Application
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Access the API at `http://127.0.0.1:5000`.

## API Endpoints

### 1. `/api/upload` (POST)
- **Description**: Upload an image and classify items in the fridge.
- **Request**:
  - Form-data: `image` (file)
- **Response**:
  ```json
  {
      "predictions": [
          {"item": "milk", "confidence": 0.95},
          {"item": "eggs", "confidence": 0.89}
      ]
  }
  ```

### 2. `/api/recipes` (GET)
- **Description**: Retrieve recipes based on classified items.
- **Response**:
  ```json
  {
      "recipes": [
          {
              "id": 1,
              "name": "Omelette",
              "ingredients": "eggs, milk",
              "instructions": "Beat eggs, add milk, cook in a pan.",
              "confidence": 0.89
          }
      ]
  }
  ```

## Project Structure
```
backend/
├── app.py              # Main Flask application
├── models/             # Image classification model
│   └── image_classifier.py
├── routes/             # API endpoints
│   └── api.py
├── utils/              # Utility modules
│   └── database.py
├── data/               # SQLite database
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## Future Improvements
- Enhance the image classification model.
- Add more robust error handling.
- Expand the recipe database.

## License
This project is licensed under the MIT License.