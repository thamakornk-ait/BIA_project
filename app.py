from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import pickle
app = Flask(__name__)
model = joblib.load('model_with_feature-selection_one-hot/model_with_downsampling/best_random_forest_model.pkl')
@app.route('/')
#comment
def home():
    return render_template('homepage.html')

@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        LIMIT_BAL = request.form['limit_balance']
        SEX  = request.form['sex']
        EDUCATION_3 = request.form['education']
        marriage = request.form['marriage']
        if marriage =='0':
            MARRIAGE_1 = 0
            MARRIAGE_3 = 0
        elif marriage == '1':
            MARRIAGE_1 = 1
            MARRIAGE_3 = 0
        elif marriage == '2':
            MARRIAGE_1 = 0
            MARRIAGE_3 = 0
        elif marriage == '3':
            MARRIAGE_1 = 0
            MARRIAGE_3 = 1
        PAY_0 = request.form['pay0']
        BILL_AMT1 = request.form['bii_amt0']
        PAY_AMT1 = request.form['pay_amt1']
        PAY_AMT2 = request.form['pay_amt2']
        PAY_AMT3 = request.form['pay_amt3']
        PAY_AMT4 = request.form['pay_amt4']
        PAY_AMT5 = request.form['pay_amt5']
        PAY_AMT6 = request.form['pay_amt6']

        scaler = pickle.load(open('model_with_feature-selection_one-hot/model_with_downsampling/scaler.pkl', 'rb'))
        [LIMIT_BAL, BILL_AMT1, PAY_AMT1, PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6]  \
            = scaler.transform([[LIMIT_BAL, BILL_AMT1, PAY_AMT1, PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6]])[0]
        

        data = {
            'LIMIT_BAL': float(LIMIT_BAL),
            'SEX': SEX,
            'EDUCATION_3': EDUCATION_3,
            'MARRIAGE_1': MARRIAGE_1,
            'MARRIAGE_3': MARRIAGE_3,
            'PAY_0': PAY_0,
            'BILL_AMT1': float(BILL_AMT1),
            'PAY_AMT1': float(PAY_AMT1),
            'PAY_AMT2': float(PAY_AMT2),
            'PAY_AMT3': float(PAY_AMT3),
            'PAY_AMT4': float(PAY_AMT4),
            'PAY_AMT5': float(PAY_AMT5),
            'PAY_AMT6': float(PAY_AMT6)
        }
        
        X = pd.DataFrame(data, index=[0])
        ypred = model.predict(X)
        preds = model.predict_proba(X)

        print("Prediction:", ypred)
        print("Percentage of default %.2f"%(preds[0][1]*100)+"%")

        detection_caught = False
        if ypred == 1:
            detection_caught = True

        if detection_caught:
            return jsonify({'message': 'Detection caught!'})
        else:
            return render_template('detection.html', detection_caught=detection_caught)
    return render_template('detection.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
