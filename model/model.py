import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

data = pd.read_csv("../data/cleaned_data.csv")
data.drop(['Unnamed: 0', 'Price_m2'], axis=1, inplace=True)

df_features = data.drop(["Price_eur"], 1)
num_features = df_features.drop(["City"], 1)

# Encoding categorical data
encoder = OneHotEncoder(drop='first', sparse=False)
enc_df = pd.DataFrame(encoder.fit_transform(data[['City']]))

# Scaling numeric data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(num_features)

# Joining scaled and encoded data
features = np.concatenate([scaled_data, enc_df], axis=-1,)
label = data['Price_eur']

X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=10)

# Prediction with Linear Regression
clf = LinearRegression()
clf.fit(X_train, y_train)
predicted = clf.predict(X_test)
expected = y_test


# Saving model to file
with open("clf.pkl", "wb") as f:
    pickle.dump(clf, f)

with open("encoder.pkl", "wb") as ohe:
    pickle.dump(encoder, ohe)

with open("scaler.pkl", "wb") as sc:
    pickle.dump(scaler, sc)
