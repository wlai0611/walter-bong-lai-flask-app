import connexion

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

@app.route("/")
def home():
    return "Endpoints are online. :)"

if __name__ == "__main__":
    app.run(port=5000)