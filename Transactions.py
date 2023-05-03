import psycopg2
import pandas as pd
import streamlit as st
import datetime
import time
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

# Connect to the database
def create_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="nava_services",
        port="5432",
        user="postgres", #navnath
        password="postgres")
    return conn

conn = create_connection()

# Create a cursor object to execute queries
cursor = conn.cursor()

def Market_Transaction():
    # Set the app title
    st.set_page_config(page_title="Market Transaction App", page_icon="https://navaserivces.com/Market Transaction")

    # Create the sidebar menu
    menu = ['Home','Groww', 'Zerodha', 'Nava Services']
    choice = st.sidebar.selectbox("Select a page",menu)

    def process_request():
        with st.spinner(f"Firing up the database engines....get ready for takeoff...!"):
            time.sleep(10)
            st.success("Connection established successfully...!")

    # Show the appropriate page based on user choice
    if choice == 'Home':
        st.title('Transaction History app!')
        st.write('This is a simple application built with Streamlit that allows users to input transactional data and store it in a database.')
        # https://www.nseindia.com/assets/images/logo_nifty50.png

    elif choice == 'Groww':
        st.header("Welcome to my Groww Transaction")
        st.subheader("Please enter your transaction information below")

        with st.form(key='columns_in_form'):
            c1 , c2 = st.columns(2)

            with c1:
                # Create a form to collect data from the user
                share_name = st.selectbox("Enter the share name", ["Ambuja Cements", "Bajaj Finserv", "Bajaj Holdings and Investments","HDFC Bank","Indian Oil Corporation","Indraprastha Gas","Mahindra & Mahindra","Mahindra & Mahindra Financial Services","Mahindra Holidays and Resorts India","Motherson International","NCC","NMDC","Orient Cement","Power Finance Corporation","Quick Heal Technologies","REC Limited","Steel Authority of India","Tata Coffee","Tata Consumer Products","Tata Steel","The Federal Bank","The Indian Hotels Company","Welspun India"])
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

        st.subheader("View Groww Transactions Data")

        # Convert the rows to a pandas DataFrame
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

        print(df.columns)

        # Set the 'Name' column as the index
        df = df.set_index('serial_id')
        # Display the DataFrame
        st.dataframe(df)

        # Query the table and get the total number of records
        cursor.execute("SELECT COUNT(*) FROM groww")
        result = cursor.fetchone()
        total_records = result[0]

        # Display the total number of records in Streamlit with bold font
        st.header(f"Total groww records: **{total_records}**")

        
        cursor.execute("select distinct share_name, COUNT(share_name) as Transactions from groww group by share_name order by Transactions desc")
        data = cursor.fetchall()
        st.subheader("Number of Transactions of Shares")
        #Convert the rows to a pandas DataFrame
        dfunique = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

        print(dfunique.columns)

        # Display the DataFrame
        st.dataframe(dfunique)

        # Create the bar chart using plotly express
        fig = px.bar(dfunique, x="share_name", y="transactions")

# Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        cursor.execute('''
        SELECT share_name,
        SUM(CASE WHEN order_type = 'buy' THEN 1 ELSE 0 END) AS buy_count,
        SUM(CASE WHEN order_type = 'sell' THEN 1 ELSE 0 END) AS sell_count
        FROM groww
        GROUP BY share_name 
        ORDER BY share_name
        ''')

        data = cursor.fetchall()

        dfunique = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

        #print(df.columns)

        # Display the DataFrame
        st.dataframe(dfunique)



        sharecounts = df['share_name'].value_counts()
        fig = px.pie(sharecounts, values=sharecounts.values, names=sharecounts.index)
        st.plotly_chart(fig)

        counts = df['order_type'].value_counts()
        fig = px.pie(counts, values=counts.values, names=counts.index)
        st.plotly_chart(fig)

        #st.table(data)
        cursor.close()
        conn.close()

        st.write("**Nava Services** is the leading resource for comprehensive data, research and insights spanning the Indian capital markets.", unsafe_allow_html=True)
        st.markdown('<span style="colour:red"> Navnath Nagorao Bhoskar </span>', unsafe_allow_html=True)

    elif choice == 'Zerodha':
        st.header("Welcome to my Zerodha Transactions ")
        st.subheader("Please enter your transaction information below")

        with st.form(key='columns_in_form'):
            c1 , c2 = st.columns(2)

            with c1:
                # Create a form to collect data from the user
                share_name = st.selectbox("Enter the share name", ["Bajaj Finserv", "Bandhan Bank", "Indian Oil Corporation","Indraprastha Gas","Mahindra & Mahindra","Motherson International","NMDC","NTPC","Orient Cement","Power Finance Corporation","Quick Heal Technologies","REC Limited","Steel Authority of India","Tata Coffee","Tata Steel","The Federal Bank","The Indian Hotels Company","Welspun India"])
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
            cursor.execute("INSERT INTO zerodha(share_name,price_per_share,shares,total_price,order_type,date_of_transaction) VALUES (%s, %s, %s, %s, %s, %s)",
            (share_name, price_per_share, shares, total_price, order_type, date_of_transaction))
            conn.commit()
            
        cursor.execute("SET search_path to navnath")
        cursor.execute("select serial_id,share_name,price_per_share,shares,total_price,order_type,date_of_transaction from zerodha order by serial_id")
        data = cursor.fetchall()
        st.subheader("View Zerodha Transactions Data")
        #Convert the rows to a pandas DataFrame
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

        #print(df.columns)

        # Set the 'Name' column as the index
        df = df.set_index('serial_id')

        # print(df.info())

        # Display the DataFrame
        st.dataframe(df)

        # Query the table and get the total number of records
        cursor.execute("SELECT COUNT(*) FROM zerodha")
        result = cursor.fetchone()
        total_records = result[0]

        # Display the total number of records in Streamlit with bold font
        st.header(f"Total zerodha records: **{total_records}**")

        cursor.execute("select distinct share_name from zerodha order by share_name")
        data = cursor.fetchall()
        st.subheader("View Unique Shares of Zerodha")
        #Convert the rows to a pandas DataFrame
        dfunique = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

        #print(df.columns)

        # Display the DataFrame
        st.dataframe(dfunique)

        cursor.execute("select distinct share_name, COUNT(share_name) as Transactions from zerodha group by share_name order by Transactions desc")
        data = cursor.fetchall()
        st.subheader("Number of Transactions of Shares")
        #Convert the rows to a pandas DataFrame
        dfunique = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

        print(dfunique.columns)

        # Display the DataFrame
        st.dataframe(dfunique)

        # Create the bar chart using plotly express
        fig = px.bar(dfunique, x="share_name", y="transactions")

# Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        sharecounts = df['share_name'].value_counts()
        fig = px.pie(sharecounts, values=sharecounts.values, names=sharecounts.index)
        st.plotly_chart(fig)

        counts = df['order_type'].value_counts()
        fig = px.pie(counts, values=counts.values, names=counts.index)
        st.plotly_chart(fig)

        #st.table(data)
        cursor.close()
        conn.close()

        st.markdown('<span style="colour:royalblue"> </span>',unsafe_allow_html=True)
        st.write("**Nava Services** is the leading resource for comprehensive data, research and insights spanning the Indian capital markets.")
        st.write("Navnath Nagorao Bhoskar")

    elif choice == 'Sensex':
        st.title('Add Sensex Data')
        with st.form(key='columns_in_form'):
            c1, c2 = st.columns(2)

            with c1:
                date_input = st.date_input("Enter a date")
            
            with c2:
                day_input = st.selectbox("Select a Day from dropdown",["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])

        #with st.form(key1='columns_in_form'):
            c3, c4 = st.columns(2)
            with c3:
                open_input = st.number_input("Enter a Open Value")

            with c4:
                high_input = st.number_input("Enter a High Value")

        #with st.form(key2='columns_in_form'):
            c5, c6 = st.columns(2)
            with c5:
                low_input = st.number_input("Enter a Low Value")

            with c6:
                close_input = st.number_input("Enter a Close Value")

        #with st.form(key3='columns_in_form'):
            c7, c8 = st.columns(2)
            with c7:
                day_change_input = st.number_input("Enter a Day Change Value")

            with c8:
                day_changeper_input = st.number_input("Enter a Day Change Percent Value")

            #Add a button to submit the data to the database

            if st.form_submit_button("Submit"):
                cursor.execute("INSERT INTO sensex(Date, Day, Open, High, Low, Close, Day_Change, Change_Prct) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(date_input,day_input,open_input,high_input,low_input,close_input,day_change_input,day_changeper_input))
                mydb.commit()
                process_request()

        st.title("View Sensex Data")
        # Retrive nifty50 data from the database
        # Example query - select all rows from a table
        query = 'SELECT Sensex_id, Date, Day, Open, High, Low, Close, Day_Change, Change_Prct FROM sensex'
        cursor.execute(query)

        # Fetch the data returned by the SQL query using the curser
        data = cursor.fetchall()

        # Create a Dataframe from the data
        df = pd.DataFrame(list(data),columns=[desc[0] for desc in cursor.description])

        df=df.set_index('Sensex_id')

        # Format negative values
        df['Day_Change'] = df['Day_Change'].apply(lambda x: '-{:,.2f}'.format(abs(x)) if x < 0 else '{:,.2f}'.format(x))
        df['Change_Prct'] = df['Change_Prct'].apply(lambda x: '-{:,.2f}'.format(abs(x)) if x < 0 else '{:,.2f}'.format(x))

        #print(df.columns)

        # Display the DataFrame with column names
        st.write(df)

        # Close the cursor and connection

        cursor.close()
        mydb.close()
        
    
    elif choice == 'View Nifty50 Data':
        st.title("View Nifty50 Data")
        # Retrive nifty50 data from the database
        # Example query - select all rows from a table
        query = 'SELECT Nifty_id, Date, Day, Open, High, Low, Close, Day_Change, Change_Prct FROM nifty_50'
        cursor.execute(query)

        # Fetch the data returned by the SQL query using the curser
        data = cursor.fetchall()

        # Create a Dataframe from the data
        df = pd.DataFrame(list(data),columns=[desc[0] for desc in cursor.description])

        df=df.set_index('Nifty_id')

        # Format negative values
        df['Day_Change'] = df['Day_Change'].apply(lambda x: '-{:,.2f}'.format(abs(x)) if x < 0 else '{:,.2f}'.format(x))
        df['Change_Prct'] = df['Change_Prct'].apply(lambda x: '-{:,.2f}'.format(abs(x)) if x < 0 else '{:,.2f}'.format(x))

        #print(df.columns)

        # Display the DataFrame with column names
        st.write(df)

        # Close the cursor and connection

        cursor.close()
        mydb.close()

# Run the app
if __name__=='__main__':
    Market_Transaction()
