from app import create_app
import os
environment = os.getenv('FLASK_ENV', 'testing')

app = create_app(environment)

if __name__ == "__main__":
    app.run()
