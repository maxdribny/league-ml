from flask import Flask
from routes import register_routes

app = Flask(__name__)

# Register all routes
register_routes(app)


@app.route("/")
def home():
    return "League of Legends ML App"


if __name__ == "__main__":
    app.run(debug=True)
