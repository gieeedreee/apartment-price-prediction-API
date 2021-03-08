# apartment-price-prediction-API
# Introduction

This is the second part of project where collected data (scraped from website www.domoplius.lt) is trained, tested, linear regression model is saved and created an API using Flask.
Model predicts apartment price in Lithuania. Flask application is connected to the PostgreSQL database hosted by Heroku and the model's inputs and outputs are inserted into one table.
Application is deployed  to Heroku and is accessible by following links:

 * for main page - https://capstone241.herokuapp.com
 
 * for predictions - https://capstone241.herokuapp.com/predict
 
 * for 10 last predictions - https://capstone241.herokuapp.com/select
 
"/predict" (POST method) accepts json type inputs with features and returns predicted prices.

Input sample: 

 {"features": 

 [{"Area": 32, "Room": 1, "Year": 2020, "Flat_floor": 1, "Total_floor": 4, "City": "Vilnius"}, 
 {"Area": 32, "Room": 1, "Year": 2020, "Flat_floor": 1, "Total_floor": 4, "City": "Kaunas"}, 
 {"Area": 32, "Room": 1, "Year": 2020, "Flat_floor": 1, "Total_floor": 4, "City": "Klaipeda"}]}

Output:

 {"predicted_price": [110086.77605950236, 54602.422311458955, 49125.371590929775]}
