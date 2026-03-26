from flask import Flask
from routes.api import api

app = Flask(
    __name__,
    template_folder="c:/Users/Kevin Tran/Desktop/big projects/frontend/templates",
    static_folder="c:/Users/Kevin Tran/Desktop/big projects/temp"
)

# Register Blueprints
app.register_blueprint(api)

# Import routes
# from routes import ...

if __name__ == "__main__":
    app.run(debug=True)