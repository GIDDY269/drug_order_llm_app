import pyodbc
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from schema import CreateScrapeSchema
from dotenv import load_dotenv
import os

load_dotenv()

database = os.environ.get('DATABASE')
server = os.environ.get('SERVER')


#create a connection with database
def create_sql_connection():
    print('CREATING SQL CONNECTION')
    connection_string = 'Driver={SQL Server};' + f'Server={server};Database={database};Trusted_Connection=yes;'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    return connection,cursor



def sql_table():
    print('CREATING SQL DATABASE TALE')
    Create_table = '''
        CREATE TABLE DRUG_ORDER_CHATBOT (
            Id INT PRIMARY KEY IDENTITY(1,1),
            name VARCHAR(MAX),
            section VARCHAR(MAX),
            category VARCHAR(MAX),
            image VARCHAR(MAX),
            price VARCHAR(MAX),
            description VARCHAR(MAX)
        )
        '''

    try:
        cnxn,cursor = create_sql_connection()
        cursor.execute(Create_table)
        cnxn.commit()

    except pyodbc.Error as e:
        # Check if the error is due to the table already existing (error code 2714)
        if e.args[0] == '42S01' and 'already an object named' in str(e):
            print("Table DRUG_ORDER_CHATBOT already exists. Using existing table.")
        else:
            raise  # Re-raise the exception if it's not the expected one

    finally:
        cnxn.close()


def insert_data(data):
    print('INSERTING DATA INTO TABLE')
    cnxn,cursor = create_sql_connection()
    try:
        # Construct and execute the insert query
        insert_query = f"INSERT INTO [DRUG_ORDER_CHATBOT] ({', '.join(data.keys())}) VALUES ({', '.join(['?']*len(data.values()))})"
        cursor.execute(insert_query,list(data.values()))
        cnxn.commit()
    finally:
        cnxn.close()







