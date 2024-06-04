from app import create_app
from config import config
from app.models.ModelVideo import db
from flask_migrate import Migrate

app = create_app(config['development'])
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
