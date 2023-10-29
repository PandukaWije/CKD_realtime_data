import streamlit as st
import pandas as pd
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('water-quality-monitor-1d632-firebase-adminsdk-f3rew-15cf7b5342.json')

try:
    # Initialize the app with a service account, granting admin privileges
    app = firebase_admin.get_app()
    ref = db.reference(app=app, path='/')
except ValueError as e:
    if str(e) == "The default Firebase app does not exist. Make sure to initialize the SDK by calling initialize_app().":
        # Initialize the Firebase app if it doesn't exist
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://water-quality-monitor-1d632-default-rtdb.firebaseio.com/'
        })
        app = firebase_admin.get_app()
        ref = db.reference(app=app, path='/')

st.title('Sensor Data')
st.subheader('Latest Readings')

if st.button('Start Streaming'):
    try:
        while True:
            # Get latest data
            latest_data = ref.get()

            pH_values = list(latest_data.values())[0]
            status_values = list(latest_data.values())[1]
            TDS_values = list(latest_data.values())[2]
            temperature_values = list(latest_data.values())[3]
            turbidity_values = list(latest_data.values())[4]

            # Extract sensor values
            pH_values_last_key, pH = pH_values.popitem()
            status_last_key, status = status_values.popitem()
            TDS_last_key, TDS = TDS_values.popitem()
            temperature_last_key, temperature = temperature_values.popitem()
            turbidity_last_key, turbidity = turbidity_values.popitem()

            # Create a DataFrame with the latest data
            columns = ['pH', 'TDS', 'Temperature', 'Turbidity', 'Status']
            table_data = pd.DataFrame(data=[[pH, TDS, temperature, turbidity, status]], columns=columns)

            # Display the updated DataFrame using st.empty()
            table_container = st.empty()
            table_container.dataframe(table_data)

            # Wait 1 sec
            time.sleep(1)

    except KeyboardInterrupt:
        st.write('Stopped streaming')
