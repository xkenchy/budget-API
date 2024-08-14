import os
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

    # Root endpoint for ELB health check
    @app.route('/')
    def index():
        return "Hello, this is the root endpoint. The application is running."

    return app

# This is the WSGI application callable that Elastic Beanstalk will look for
application = create_app()

if __name__ == '__main__':
    # Use environment variable for port, default to 8080 for Elastic Beanstalk
    port = int(os.getenv('PORT', 8080))

    # Bind to 0.0.0.0 to make the app accessible externally in Elastic Beanstalk
    application.run(host='0.0.0.0', port=port, debug=True)
