import connexion
from flask import render_template

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

@app.route("/")
def home():
    return "Endpoints are online. :)"

@app.route("/interface")
def interface():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(port=5000)