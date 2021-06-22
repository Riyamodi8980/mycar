from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_Car_v3_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = float(request.form['Year'])
        Kms_Driven=float(request.form['Kms_Driven'])
        Mileage=float(request.form['mileage'])
        Engine=float(request.form['engine'])
        Max_power=float(request.form['max_power'])
        Torque=float(request.form['torque'])
        Seats=float(request.form['seats'])
        Year=2020-Year
        
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
                Fuel_Type_LPG=0     
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
            Fuel_Type_LPG=0 
        elif(Fuel_Type_Petrol=='LPG'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_LPG=1   
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_LPG=0
            
        
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Trustmark_Dealer=0
        elif(Seller_Type_Individual=='Trustmark Dealer'):
            Seller_Type_Individual=0
            Seller_Type_Trustmark_Dealer=1
        else:
            Seller_Type_Individual=0
            Seller_Type_Trustmark_Dealer=0
            
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
            
        Owner=request.form['owner']
        if(Owner=='Test Drive Car'):
            owner_Fourth=0
            owner_Second=0
            owner_Test=1
            owner_Third=0
        elif(Owner=='Second Owner'):
            owner_Fourth=0
            owner_Second=1
            owner_Test=0
            owner_Third=0 
        elif(Owner=='Third Owner'):
            owner_Fourth=0
            owner_Second=0
            owner_Test=0
            owner_Third=1
            
        elif(Owner=='Fourth & Above Owner'): 
            owner_Fourth=1
            owner_Second=0
            owner_Test=0
            owner_Third=0
        else:
            owner_Fourth=0
            owner_Second=0
            owner_Test=0
            owner_Third=0
            
        print([Kms_Driven,Mileage,Engine,Max_power,Torque,Seats,Year,Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Seller_Type_Individual,Seller_Type_Trustmark_Dealer,Transmission_Mannual,owner_Fourth,owner_Second,owner_Test,owner_Third],'\n\n\n')
        prediction=model.predict([[Kms_Driven,Mileage,Engine,Max_power,Torque,Seats,Year,Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Seller_Type_Individual,Seller_Type_Trustmark_Dealer,Transmission_Mannual,owner_Fourth,owner_Second,owner_Test,owner_Third]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

