from flask import Flask
from routes.form_routes import form_bp
from flask_cors import CORS
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    load_dotenv()

    # Register blueprints
    app.register_blueprint(form_bp, url_prefix='/form')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
