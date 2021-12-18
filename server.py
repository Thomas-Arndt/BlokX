from flask_app import app
from flask_app.controllers import controller_routes


if __name__=="__main__":
    app.run(debug=False)