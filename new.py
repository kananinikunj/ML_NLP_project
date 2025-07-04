import pandas as pd
import numpy as np
import streamlit as st
import datetime
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings("ignore")

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import LabelEncoder

from sklearn.svm import LinearSVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score


st.set_page_config(layout="wide")


@st.cache_data()
def get_data():
    df = pd.read_csv("diamonds.csv")
    df = df.drop(['Unnamed: 0'], axis=1)
    return df
Data = get_data()

## Title
st.markdown("<h1 style='text-align: center; color: red;'>REPORT 📝</h1>", unsafe_allow_html=True)


## Greeting
now = datetime.datetime.now()
hour = now.hour
if hour < 12:
    greeting = "Good morning"
elif hour < 17:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"
st.write("{}!".format(greeting))
st.markdown("---")
#st.markdown("<h4 style='text-align: center;'>========================================================================================</h4>", unsafe_allow_html=True)

clarity_oder = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1', 'Ideal', 'Premium', 'Very Good', 'Good', 'Fair']
code1_s = [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5]
cut_mapping = dict(zip(['Ideal', 'Premium', 'Very Good', 'Good', 'Fair'], [2, 1, 3, 4, 5]))
color_mapping = dict(zip(['D', 'E', 'F', 'G', 'H', 'I', 'J'], range(7)))
clarity_mapping = dict(zip(['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1'], range(8)))


Data1 = Data
Data1['cut'] = Data1['cut'].map(cut_mapping)
Data1['color'] = Data1['color'].map(color_mapping)
Data1['clarity'] = Data1['clarity'].map(clarity_mapping)


le = LabelEncoder()

Data1['cut'] = le.fit_transform(Data1['cut'])
Data1['color'] = le.fit_transform(Data1['color'])
Data1['clarity'] = le.fit_transform(Data1['clarity'])

X=Data1.drop('price',axis=1)
y=Data1['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

Re = st.sidebar.selectbox("Select",("LinearSVR","KNeighborsRegressor","LinearRegression","RandomForestRegressor",
                                    "GradientBoostingRegressor","DecisionTreeRegressor"))

if Re == "LinearSVR":
    pipe1 = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LinearSVR(random_state = 42))])

    model = pipe1.fit(X_train, y_train)

    y_pred = model.predict(X_test)

elif Re == "KNeighborsRegressor":
    pipe2 = Pipeline([
        ('scaler', MinMaxScaler()),
        ('model', KNeighborsRegressor())])

    model = pipe2.fit(X_train, y_train)

    y_pred = model.predict(X_test)

elif Re == "LinearRegression":
    pipe3 = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LinearRegression())])

    model = pipe3.fit(X_train, y_train)

    y_pred = model.predict(X_test)

elif Re == "RandomForestRegressor":
    model = RandomForestRegressor(random_state = 42).fit(X_train, y_train)

    y_pred = model.predict(X_test)

elif Re == "GradientBoostingRegressor":
    model = GradientBoostingRegressor(random_state = 42).fit(X_train, y_train)

    y_pred = model.predict(X_test)

elif Re == "DecisionTreeRegressor":
    model = DecisionTreeRegressor(random_state = 42).fit(X_train, y_train)

    y_pred = model.predict(X_test)

result = st.sidebar.checkbox("Show Result Score")
a = mean_absolute_error(y_test, y_pred)
b = mean_absolute_percentage_error(y_test, y_pred)
c = mean_squared_error(y_test, y_pred)  # Default is squared=True
d = mean_squared_error(y_test, y_pred)**0.5  # Calculate RMSE manually
e = r2_score(y_test, y_pred) * 100
Table = {
  "Results": ["MAE", "MAPE", "MSE", "RMSE", "R2"],
  "Score": [a, b, c, d, e]
}
table = pd.DataFrame(Table)
if result:
    st.title(Re)
    st.table(table)

#Predication
pr = st.sidebar.checkbox("Predication")
if pr:
    col1, col2 = st.columns([1,1])
    c1 = col1.selectbox("Color",('D','E','F','G','H','I','J'))
    cl1 = col2.selectbox("Clarity",('IF','VVS1','VVS2','VS1','VS2','SI1','SI2','I1'))
    cu1 = col1.selectbox("Cut",('Ideal','Premium','Very Good','Good','Fair'))
    ca1 = col2.number_input("Carat")
    dp1 = col1.number_input("Depth")
    tb1 = col2.number_input("Table")
    x1 = col1.number_input("x")
    y1 = col2.number_input("y")
    z1 = col1.number_input("z")
    cut_encoded = cut_mapping[cu1]
    color_encoded = color_mapping[c1]
    clarity_encoded = clarity_mapping[cl1]

    st.button("Predict")


    new_data = pd.DataFrame([{
        'carat': ca1, 'cut': cut_encoded, 'color': color_encoded,
        'clarity': clarity_encoded, 'depth': dp1, 'table': tb1, 'x': x1, 'y': y1, 'z': z1
    }])

    pred = pd.concat([X_test.iloc[:0], new_data], ignore_index=True)

    #model = RandomForestRegressor(random_state=42).fit(X_train, y_train)
    y_pred = model.predict(pred)
    y_pred = round(y_pred[0],1)
    st.markdown(f"<h4 style='text-align: center;'>Price : ${y_pred}</h4>", unsafe_allow_html=True)
