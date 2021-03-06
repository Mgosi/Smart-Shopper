import serial
import Smart_Shopper_Lib_Tester as SSL
import Apriori_for_Smart_Shopper as AS
arduino_milk = serial.Serial('COM4', 9600, timeout=.5)
arduino_grape = serial.Serial('COM5', 9600, timeout=.5)
def readRFID():
	c=1
	while True:
		if c == 1:
			print "Waiting for input from Arduino..."
		c = c+1
		data_milk = arduino_milk.readline()[:-2]
		data_grape = arduino_grape.readline()[:-2]
		found = 0
		if data_milk :#the last bit gets rid of the new-line chars
			found = 1
			print "Milk detected"
			item = 'Milk'
			rfid_id = data_milk[:12]
		elif data_grape :
			found = 2
			print "Jam Detected"
			item = 'Jam'
			rfid_id = data_grape[:12]


		added = 0
		if found:
			try :
				con, cursor = SSL.establish_conn()
				cust_id = SSL.detect_rfid_tag(rfid_id, cursor)

				print "--------------------------------------------------------"
				print "Customer ID = ",
				print cust_id
				print "RFID Tag = ",
				print rfid_id
				print "Item detected : " + item
				print "                ------"
				try :
#					SSL.display_items_bought(cust_id, cursor)
					if SSL.check_item(cust_id, item, cursor):
						print "Adding Item"
						if SSL.add_item_to_cart(cust_id, item, cursor) :

							added = 1
							wallet_amt = SSL.get_amount_in_wallet(cust_id,cursor)
							total_cost = SSL.calculate_total(cust_id, cursor)
							balance = wallet_amt-total_cost
							if balance < 0 :
								print "Insuficient balance in wallet"
								SSL.remove_item_from_cart(cust_id, item, cursor)
								added = 0
							if added :
								con.commit()
								print item + " added to Cart"
						else :
							print "Error. Item not added. "
					else :
						print "Item already in cart"
						if SSL.remove_item_from_cart(cust_id, item, cursor) :
							con.commit()
							added = 0
							print item + " deleted from cart"
						else :
							print "Error. Item not removed"

				except :
					print "something went wrong with adding or removing"
			except :
				print "Wrong"
			print "                ------"
			if added :
				try :
					AS.Apriori()
				except :
					print "error in Apriori"
				try :
					sugg_item = SSL.find_suggestion(item, cursor)
					print "Item Bought : " + item
					for s_item in sugg_item:
						print "Item Suggested : " + s_item[0]
				except :
					print "Error in Suggestion"
			print "--------------------------------------------------------"
			c=1

if __name__ == '__main__':
	readRFID()
