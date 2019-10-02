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

def add_customer(cust_id, cust_name, ph_no, wallet, cursor):
    q_add = ("INSERT INTO customer VALUES (%s, %s, %s, %s)")
    cursor.execute(q_add,(cust_id, cust_name, ph_no, wallet))
    if cursor.rowcount>0:
        return 1
    else :
        return 0

def detect_rfid_tag(rfid_id, cursor):
    q_detect = ("SELECT C_ID FROM rfid_link WHERE R_ID = %s")
    cursor.execute(q_detect,(rfid_id,))
    cust_id = cursor.fetchall()
    return cust_id[0][0]

def cust_detail(cust_id, cursor):
	cust = ("SELECT * FROM customer WHERE C_ID = %s")
	cursor.execute(cust,(cust_id,))
	customer_details = cursor.fetchall()
	return customer_details[0]

def find_customer_name(rfid_tag, cursor):
	cust = ("SELECT C_Name FROM customer, rfid_link WHERE rfid_link.R_ID = %s and rfid_link.C_ID = customer.C_ID")
	cursor.execute(cust,(rfid_tag,))
	customer_name = cursor.fetchall()
	return customer_name[0]

def find_customer_id(rfid_tag, cursor):
	cust = ("SELECT customer.C_ID FROM customer, rfid_link WHERE rfid_link.R_ID = %s and rfid_link.C_ID = customer.C_ID")
	cursor.execute(cust,(rfid_tag,))
	customer_id = cursor.fetchall()
	return customer_id[0][0]

def items_bought(c_id, cursor):
    items_query = ("SELECT I_Name, Price FROM items, customer, items_bought WHERE customer.C_ID = items_bought.Cust_ID and items_bought.Item_Name =items.I_Name and customer.C_ID = %s ")
    cursor.execute(items_query,(c_id,))
    items = cursor.fetchall()
    if cursor.rowcount > 0 :
        return items
    else :
        return 0

def items_bought_1(c_id, cursor):
    items_query = ("SELECT I_Name, Price FROM items, customer, items_bought WHERE customer.C_ID = items_bought.Cust_ID and items_bought.Item_Name =items.I_Name and customer.C_ID = 1 ")
    cursor.execute(items_query,(c_id,))
    items = cursor.fetchall()
    if cursor.rowcount > 0 :
        return items
    else :
        return 0

def items_bought_2(c_id, cursor):
    items_query = ("SELECT I_Name, Price FROM items, customer, items_bought WHERE customer.C_ID = items_bought.Cust_ID and items_bought.Item_Name =items.I_Name and customer.C_ID = 2 ")
    cursor.execute(items_query,(c_id,))
    items = cursor.fetchall()
    if cursor.rowcount > 0 :
        return items
    else :
        return 0

def display_items_bought(cust_id, cursor):
    items = items_bought(id,cursor)
    print items

    if items :
        print "Items in the cart are : "
        count = 0
        print "\tItem\tPrice"
        for i in items:
            count+=1
            print i[0],
            print "\t"
            print i[1]
    else :
        print "No items in cart"

def display_items_bought_1(cursor):
    items = items_bought_1(cursor)
    print items


    if items :
        print "Items in the cart are : "
        count = 0
        print "\tItem\tPrice"
        for i in items:
            count+=1
            print i[0],
            print "\t"
            print i[1]
    else :
        print "No items in cart"

def display_items_bought_2(cursor):
    items = items_bought_2(cursor)
    print items

    if items :
        print "Items in the cart are : "
        count = 0
        print "\tItem\tPrice"
        for i in items:
            count+=1
            print i[0],
            print "\t"
            print i[1]
    else :
        print "No items in cart"

def find_suggestion(item_bought, cursor):
    sugg = ("SELECT DISTINCT Suggested_Item FROM suggested_item WHERE Bought_Item = %s")
    cursor.execute(sugg,(item_bought,))

    suggested_items = cursor.fetchall()
    return suggested_items

def check_item(cust_id, item, cursor) :
    query_cart = ("SELECT * FROM items_bought WHERE Cust_ID = %s and Item_Name = %s")
    cursor.execute(query_cart,(cust_id, item))
    msg = cursor.fetchall()
    if not msg :
        return 1
    else :
        return 0

def add_item_to_cart(id, item,cursor):

    query_cart = ("INSERT INTO items_bought VALUES ( %s , %s )")
    cursor.execute(query_cart,(id, item))
    if cursor.rowcount>0:
        return 1
    else :
        return 0

def remove_item_from_cart(cust_id, item, cursor):
    q_remove = ("DELETE FROM items_bought WHERE Cust_ID = %s and Item_Name = %s")
    cursor.execute(q_remove,(cust_id, item))
#    print cursor.rowcount
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

def calculate_total(cust_id, cursor):
    items = items_bought(cust_id, cursor)
    total_cost = 0
    if items == 0:
        return 0
    else :
        for i in items :
            print i
            total_cost += int(i[1])
        return total_cost

def get_amount_in_wallet(cust_id, cursor):
    q_getwallet = ("SELECT Wallet_Amount FROM customer WHERE C_ID = %s")
    cursor.execute(q_getwallet,(cust_id,))
    wallet_amt = cursor.fetchall()
    return wallet_amt[0][0]

def deduct_amount(cust_id, cursor):
    cost = calculate_total(cust_id, cursor)
    wal_amt = get_amount_in_wallet(cust_id, cursor)
    remaining = wal_amt - cost
    q_updateWallet = ("UPDATE customer SET Wallet_Amount = %s WHERE C_ID = %s")
    cursor.execute(q_updateWallet,(remaining, cust_id))
    if cursor.rowcount > 0:
        print "Wallet updated"
        del_cart(cust_id, cursor)
        return 1
    else :
        print "Wallet not updated"
        return 0

def del_cart(cust_id, cursor):
    q_delCart = ("DELETE FROM items_bought WHERE Cust_ID = %s")
    cursor.execute(q_delCart,(cust_id,))
    if cursor.rowcount > 0:
        print "Cart Items deleted"
        return 1
    else :
        print "No items in cart"
        return 0


if __name__ == "__main__":
    con,cursor = establish_conn()
    print "Connection Established"
    id = find_customer_id(2,cursor)
    print id[0][0]
    wallet_balance = get_amount_in_wallet(id[0][0], cursor)
    deduct_amount(id[0][0],cursor)
    con.commit()
#Testing calculate total cost
"""
    id = find_customer_id(1,cursor)
    print id[0][0]
    cost = calculate_total(id[0][0], cursor)
    print "Amount in cart = " + str(cost)
"""
