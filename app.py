from flask import Flask, render_template, request
import numpy as np
import pickle
import os

print("Current Working Directory:", os.getcwd())
print("Files in Current Directory:", os.listdir())

app = Flask(__name__)

path_to_file = 'MedicalInsuranceCost.pkl'
model = pickle.load(open(path_to_file, 'rb'))



@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        age = float(request.form['age'])

        gender = request.form['gender']
        if (gender == 'male'):
            gender_male = 1
            gender_female = 0
        else:
            gender_male = 0
            gender_female = 1

        smoker = request.form['smoker']
        if (smoker == 'yes'):
            smoker_yes = 1
            smoker_no = 0
        else:
            smoker_yes = 0
            smoker_no = 1

        bmi = float(request.form['bmi'])
        children = int(request.form['children'])

        region = request.form['region']
        if (region == 'northwest'):
            region_northwest = 1
            region_southeast = 0
            region_southwest = 0
            region_northeast = 0
        elif (region == 'southeast'):
            region_northwest = 0
            region_southeast = 1
            region_southwest = 0
            region_northeast = 0
        elif (region == 'southwest'):
            region_northwest = 0
            region_southeast = 0
            region_southwest = 1
            region_northeast = 0
        else:
            region_northwest = 0
            region_southeast = 0
            region_southwest = 0
            region_northeast = 1
    


        values = np.array([[age,gender_male,smoker_yes,bmi,children,region_northwest,region_southeast,region_southwest]])
        prediction = model.predict(values)
        # prediction = round(prediction[0],2)
        prediction = "%.2f" % round(prediction[0], 2)


        return render_template('result.html', prediction_text='Medical insurance charge is {}'.format(prediction))

if __name__ == "__main__":
    app.run(debug=True)