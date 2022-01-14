import connexion
from flask import render_template,request
import numpy as np
import pickle
import re
import base64
import io
from PIL import Image

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

#LOCAL_CACHE2 = {}
#LOCAL_CACHE2["loaded_model"] = pickle.load(open("./model/model.pkl","rb"))

@app.route("/")
def home():
    return "Endpoints are online. :)"

@app.route("/interface")
def interface():
    return render_template("home.html")

@app.route("/pictureDemo", methods = ["POST"])
def picture():
    
    #pickle.dump(request.values["imageBase64"],open("C:\\Users\\Walter\\Desktop\\datascience\\byteString.pickle","wb"))
    #https://medium.com/csmadeeasy/send-and-receive-images-in-flask-in-memory-solution-21e0319dcc1
    
    #https://stackoverflow.com/questions/44172643/python-flask-request-json-returns-none-type-instead-of-json-dictionary
    
    canvasImageAsString = request.values["imageBase64"]
    noHeader = canvasImageAsString.split(",")[1]
    validCharsOnly = re.sub("[^a-zA-Z0-9/+]+", "",noHeader)
    missing_padding = len(validCharsOnly) % 4
    if missing_padding:
        validCharsOnly += "=" * (4 - missing_padding)

    imgDecoded = base64.b64decode(validCharsOnly)
    imageFile = io.BytesIO()
    imageFile.write(imgDecoded)
    image = Image.open(imageFile)

    imgarr = np.array(image)
    swapColorAndHeight = np.swapaxes(imgarr,0,2) 
    swapHeightAndWidth =  np.swapaxes(swapColorAndHeight,1,2)
    layerWithDrawing = swapHeightAndWidth[3]
    return str(layerWithDrawing[layerWithDrawing>0])

if __name__ == "__main__":
    app.run(port=5000,debug=True)