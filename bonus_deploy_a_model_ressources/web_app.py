from flask import Flask, request
from sklearn.externals import joblib

model = None

app = Flask(__name__)

def load_model():
    global model
    with open("model.sav", 'rb') as file:
        model = joblib.load(file)

@app.route('/')
def home():
    return "Check out our brand new model ! ;-)"

@app.route('/predict', methods=['POST'])
def get_prediction():
    if request.method == "POST":
        data = request.get_json() # get data posted as json
        data = np.array(data)[np.newaxis, :] # shape (4,) to (1,4)
        prediction = model.predict(data)
    return str(prediction[0])

if __name__ == '__main__':
    load_model()  # load model at the beginning once only
    app.run(host='0.0.0.0', port=80)