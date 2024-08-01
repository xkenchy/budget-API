from flask import Flask
from routes.form_routes import form_bp
from flask_cors import CORS



def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(form_bp, url_prefix='/form')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
