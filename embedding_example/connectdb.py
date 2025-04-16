import psycopg2 , psycopg2.extras
from config import connection_credentials

def connect():
    connection = None
    crsr = None
    try :
        params = connection_credentials()
        print("Connecting to PostgreSQL Database ...")
        connection = psycopg2.connect(**params)                 # Connecting to PostgreSQL

        crsr = connection.cursor()          # Creating a cursor

        return crsr , connection

    except(Exception , psycopg2.DatabaseError) as error :
        print(error)