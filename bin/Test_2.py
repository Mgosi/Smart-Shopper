import mysql.connector
import sys
import Smart_Shopper_Lib_Tester as SSL
import Apriori_for_Smart_Shopper as AS
config = {
	'user': 'root',
	'password': 'root123',
	'database': 'smart_shopper',
}

def get_customers(cursor):
	query = ("SELECT * FROM customer")
	cursor.execute(query)
	cust = cursor.fetchall()

	for each in cust:
		print each[0], each[1]

	print "In get_customers function with customers"
	return cust

def find_customer(rfid_tag, cursor):
	print "hi"
	print rfid_tag
	cust = ("SELECT C_Name FROM customer, rfid_link WHERE rfid_link.R_ID = 2 and rfid_link.C_ID = customer.C_ID")
	cursor.execute(cust,(rfid_tag))
	customer_name = cursor.fetchone()
	return customer_name


if __name__ == "__main__":

	con, cursor = SSL.establish_conn()
	rfid_id = "1E007935194B"
	cust_id = SSL.detect_rfid_tag(rfid_id, cursor)
	cust_detail = SSL.cust_detail(cust_id, cursor)
	item = 'Milk'
	sugg_item = SSL.find_suggestion(item, cursor)
	print sugg_item


	con.close()
