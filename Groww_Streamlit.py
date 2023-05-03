# Run the following command prompt in your terminal
#print("
import psycopg2
import pandas as pd
import streamlit as st
import datetime
import time

# Set the title of the app
st.title("Transaction History app!")
st.header("Welcome to my Groww Transaction")
st.subheader("Please enter your transaction information below")


def create_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="nava_services",
        port="5432",
        user="postgres", #navnath
        password="postgres")
    return conn

conn = create_connection()
cursor = conn.cursor()

with st.form(key='columns_in_form'):
    c1 , c2 = st.columns(2)

    with c1:
        # Create a form to collect data from the user
        share_name = st.text_input("Enter the share name")
        price_per_share = st.number_input("Enter the price per share", min_value=0.0)
        shares = st.number_input("Enter the number of shares", min_value=0)
        total_price = price_per_share * shares

    with c2:
        order_type = st.selectbox("Select the order type", ["buy", "sell"])
        date_of_transaction = st.date_input("Enter the date of transaction")

    submitButton = st.form_submit_button("Submit")

def process_request():
    with st.spinner(f'We are processing...!'):
        time.sleep(10)
    st.success("Data inserted successfully!")
    

if submitButton:
    cursor.execute("SET search_path to navnath") 

    # Insert data into the Postgres database
    cursor.execute("INSERT INTO groww(share_name,price_per_share,shares,total_price,order_type,date_of_transaction) VALUES (%s, %s, %s, %s, %s, %s)",
            (share_name, price_per_share, shares, total_price, order_type, date_of_transaction))
    conn.commit()
    process_request()

cursor.execute("SET search_path to navnath")
cursor.execute("select serial_id,share_name,price_per_share,shares,total_price,order_type,date_of_transaction from groww order by serial_id")
data = cursor.fetchall()


# Convert the rows to a pandas DataFrame
df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

#print(df.columns)

# Set the 'Name' column as the index
df = df.set_index('serial_id')

#print(df.info())

# Display the DataFrame
st.dataframe(df)

#st.table(data)
cursor.close()
conn.close()

st.write("**Nava Services** is the leading resource for comprehensive data, research and insights spanning the Indian capital markets.", unsafe_allow_html=True)
st.markdown('<span style="colour:red"> Navnath Nagorao Bhoskar </span>', unsafe_allow_html=True)
