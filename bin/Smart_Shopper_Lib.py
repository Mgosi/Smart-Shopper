"""
    Description : Library For Smart_Shopper

"""
import sys
import mysql.connector

config = {
	'user': 'root',
	'password': 'root123',
	'database': 'smart_shopper',
}


def establish_conn():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    return cnx, cursor

def find_customer_name(rfid_tag, cursor):
	cust = ("SELECT C_Name FROM customer, rfid_link WHERE rfid_link.R_ID = %s and rfid_link.C_ID = customer.C_ID")
	cursor.execute(cust,(rfid_tag,))
	customer_name = cursor.fetchall()
	return customer_name

def find_customer_id(rfid_tag, cursor):
	cust = ("SELECT customer.C_ID FROM customer, rfid_link WHERE rfid_link.R_ID = %s and rfid_link.C_ID = customer.C_ID")
	cursor.execute(cust,(rfid_tag,))
	customer_id = cursor.fetchall()
	return customer_id

def items_bought(cust_id, cursor):
    items_query = ("SELECT I_Name, Price FROM items, customer, items_bought WHERE customer.C_ID = %s and customer.C_ID = items_bought.Cust_ID and items_bought.Item_Name =items.I_Name ")
    cursor.execute(items_query,(cust_id,))
    items = cursor.fetchall()
    if items == []:
        return 0
    else :
        return items

def display_items_bought(cust_id, cursor):
    items = items_bought(id,cursor)
    if items :
        print "Items in the cart are : "
        count =0
        for i in items:
            count+=1
            print "Item "+str(count)+": ",
            print i[0],
            print "Price "+str(count)+": ",
            print i[1]
    else :
        print "No items in cart"

def find_suggestion(item_bought, cursor):
    sugg = ("SELECT DISTINCT RHS_Item FROM store_rules WHERE LHS_Item = %s")
    cursor.execute(sugg,(item_bought,))

    suggested_items = cursor.fetchall()
    return suggested_items

def add_item_to_cart(id, item,cursor):

    query_cart = "INSERT INTO items_bought VALUES ( %s , %s )"
    cursor.execute(query_cart,(id, item))
    if cursor.rowcount>0:
        return 1
    else :
        return 0

def remove_item_from_cart(cust_id, item, cursor):
#    q = ("SELECT * FROM items_bought")
#    cursor.execute(q)
    q_remove = ("DELETE FROM items_bought WHERE Cust_ID = %s and Item_Name = %s")
    cursor.execute(q_remove,(cust_id, item))
    print cursor.rowcount
    if cursor.rowcount > 0:
        return 1
    else :
        return 0

def add_to_suggested_list(r_no, lhs, rhs, conf, cursor):
    q_suggested = ("INSERT INTO suggested_item VALUES (%s, %s, %s, %s)")
    cursor.execute(q_suggested,(r_no, lhs, rhs, conf))
    if cursor.rowcount > 0:
        return 1
    else :
        return 0

def del_suggested_list(cursor):
    q_del_sugg = ("DELETE FROM suggested_item")
    cursor.execute(q_del_sugg)

if __name__ == "__main__":
    con,cursor = establish_conn()
    print "Connection Established"
