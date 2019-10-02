cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
q_add = ("INSERT INTO customer VALUES (%s, %s, %s, %s)")
cursor.execute(q_add,(cust_id, cust_name, ph_no, wallet))
