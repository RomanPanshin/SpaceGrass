import mysql.connector

def insert_data_into_database(AllFuel, All_Oxi, All_cost, day, Fly_Dist, sp_for_client):
    mydb = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO fuel_data (AllFuel, All_Oxi, All_cost, day, Fly_Dist, SP_for_Client) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (AllFuel, All_Oxi, All_cost, day, Fly_Dist, sp_for_client)
    mycursor.execute(sql, values)
    mydb.commit()
    mycursor.close()
    mydb.close()

