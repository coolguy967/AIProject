import MySQLdb
import random
import re


class Database:

    university = ["UTSC", "UTM", "UOIT"]

    room_type = {"F-SW" : 550, "F-SHW" : 500, "UF-SW" : 450, "UF-SHW" : 400}

    street = [["Military Trail", "Conlins Road", "Mirrow Court", "Gladys Road", "Bobmar Road"],
              ["Sawmill Valley Drive", "Snow Bunting Court", "Kingbird Court", "Belvedere Crescent", "Stonemason Crescent"],
              ["Dalhousie Crescent", "Niagra Drive", "McGill Court", "Secretariat Place", "Woodbine Place"]]

    def __init__(self):

        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        cursor.execute("SELECT * FROM listing;")

        if cursor.rowcount == 0:

            for i in range(10000):

                type = random.choice(list(self.room_type.keys()))

                price = str(self.room_type[type])

                sqft = random.randint(110, 240)

                washroom = ""

                if type == "F-SW":
                    washroom = "Separate"
                elif type == "F-SHW":
                    washroom = "Shared"
                elif type == "UF-SW":
                    washroom = "Separate"
                elif type == "UF-SHW":
                    washroom = "Shared"

                parking = random.choice(["Yes", "No"])

                if parking == "Yes":
                    price += "50"

                uni = random.choice(self.university)

                address = ""
                id = 0

                if uni == "UOIT":
                    address = str(random.randint(200, 1000)) + " " + random.choice(self.street[2]) + " Oshawa, ON"
                    id = 1

                    if address == cursor.execute("SELECT address FROM listing WHERE address = '" + address + "';"):
                        address = str(random.randint(200, 1000)) + " " + random.choice(self.street[2]) + " Oshawa, ON"

                elif uni == "UTSC":
                    address = str(random.randint(200, 1000)) + " " + random.choice(self.street[0]) + " Scarborough, ON"
                    id = 2

                    if address == cursor.execute("SELECT address FROM listing WHERE address = '" + address + "';"):
                        address = str(random.randint(200, 1000)) + " " + random.choice(self.street[0]) + " Scarborough, ON"

                elif uni == "UTM":
                    address = str(random.randint(200, 1000)) + " " + random.choice(self.street[1]) + " Mississauga, ON"
                    id = 3

                    if address == cursor.execute("SELECT address FROM listing WHERE address='" + address + "';"):
                        address = str(random.randint(200, 1000)) + " " + random.choice(self.street[1]) + " Mississauga, ON"

                '''query = "INSERT INTO listing (room_type, sqft, washroom, parking, price, address) VALUES ('" + type + "', '" + str(sqft) + "', '" + washroom + "', '" + parking + "', '" + price + "', '" + address + "');"'''

                query = "INSERT INTO address (uni_id, address) VALUES (" + str(id) + ", '" + address + "');"

                cursor.execute(query)

        cursor.execute("SELECT * FROM listing;")

        if cursor.rowcount == 0:

            cursor.execute("SELECT * FROM address;")

            addressses = cursor.fetchall()

            for i in range(10000):

                type = random.choice(list(self.room_type.keys()))

                price = self.room_type[type]

                sqft = random.randint(110, 240)

                washroom = ""

                if type == "F-SW":
                    washroom = "Separate"
                elif type == "F-SHW":
                    washroom = "Shared"
                elif type == "UF-SW":
                    washroom = "Separate"
                elif type == "UF-SHW":
                    washroom = "Shared"

                parking = random.choice(["Yes", "No"])

                if parking == "Yes":
                    price += 50

                cursor.execute("SELECT address FROM address WHERE id=" + str(i+1) + ";")
                str1 = cursor.fetchone()
                str2 = str(str1)
                str3 = str2.replace("('", "")
                address = str3.replace("',)", "")

                cursor.execute("SELECT uni_id FROM address WHERE id=" + str(i+1) + ";")
                id = int(re.search(r'\d+', str(cursor.fetchone())).group())

                query = "INSERT INTO listing (uni_id, room_type, sqft, washroom, parking, price, address) VALUES (" + str(id) + ", '" + type + "', " + str(sqft) + ", '" + washroom + "', '" + parking + "', " + str(price) + ", '" + address + "');"

                cursor.execute(query)

        db.close()

    def depthFirst(self):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        nodes = []

        cursor.execute("SELECT listing_id, room_type, sqft, washroom, parking, price, address  FROM listing INNER JOIN university WHERE listing.uni_id = university.uni_id AND university.uni_id=1;")
        temp = cursor.fetchall()

        for record in temp:
            nodes.append(list(record))

        cursor.execute("SELECT listing_id, room_type, sqft, washroom, parking, price, address FROM listing INNER JOIN university WHERE listing.uni_id = university.uni_id AND university.uni_id=2;")
        temp = cursor.fetchall()

        for record in temp:
            nodes.append(list(record))

        cursor.execute("SELECT listing_id, room_type, sqft, washroom, parking, price, address FROM listing INNER JOIN university WHERE listing.uni_id = university.uni_id AND university.uni_id=3;")
        temp = cursor.fetchall()

        for record in temp:
            nodes.append(list(record))

        db.close()

        return tuple(nodes)

    def breadthFirst(self, uni_id, room, washroom, parking, price):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        cursor.execute("SELECT listing_id, room_type, sqft, washroom, parking, price, address FROM listings WHERE uni_id=" + uni_id + ";")
        goal = cursor.fetchall()

        cursor.execute("SELECT uni_id FROM university WHERE uni_id=1;")
        current = cursor.fetchone()

        cursor.execute("SELECT uni_id FROM university WHERE uni_id=2;")
        current = cursor.fetchone()

        cursor.execute("SELECT uni_id FROM university WHERE uni_id=3;")
        current = cursor.fetchone()

        cursor.execute("SELECT listing_id, room_type, sqft, washroom, parking, price, address FROM listing INNER JOIN university WHERE listing.uni_id = university.uni_id AND university.uni_id=1;")
        nodes = cursor.fetchall()

        if nodes == goal:
            db.close()
            return nodes

        cursor.execute("SELECT * FROM listing INNER JOIN university WHERE listing.uni_id = university.uni_id AND university.uni_id=2;")
        nodes = cursor.fetchall()

        if nodes == goal:
            db.close()
            return nodes

        cursor.execute("SELECT * FROM listing INNER JOIN university WHERE listing.uni_id = university.uni_id AND university.uni_id=3;")
        nodes = cursor.fetchall()

        if nodes == goal:
            db.close()
            return nodes

    def getPreferred(self):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        cursor.execute("SELECT * FROM preferred;")
        preferred = cursor.fetchall()

        db.close()
        return preferred

    def setPreferred(self, room_type, sqft, washroom, parking, price):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        cursor.execute("SELECT * FROM preferred;")
        preferred = cursor.fetchall()

        print("test")

        if len(preferred) > 0:
            cursor.execute("CREATE TABLE preferred_new LIKE preferred;")
            print("test")
            cursor.execute("RENAME TABLE preferred TO preferred_old, preferred_new TO preferred;")
            print("test")
            cursor.execute("DROP TABLE preferred_old;")

        print("test")

        cursor.execute("INSERT INTO preferred VALUES ('" + room_type + "', " + str(sqft) + ", '" + washroom + "', '" + parking + "', " + str(price) + ");")

        db.close()

    def preferredListings(self):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        preferred = self.getPreferred()

        cursor.execute("SELECT * from listings WHERE room_type=" + preferred[0] + " AND (sqft*1.1)>=" + str(preferred[1]) + " AND (sqft*0.9)<=" + preferred[1] + " AND washroom=" + preferred[2] + " AND parking=" + preferred[3] + " AND (price*1.1)>=" + preferred[4] + " AND (price*0.9)<=" + str(preferred[4]) + ";")
        preferred_listings = cursor.fetchall()

        db.close()
        return preferred_listings

    def getListings(self, university, room, washroom, parking, price, size):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        room_type = ""
        searched_parking = ""
        searched_washroom = ""

        if university == '' and room == '' and washroom == '' and not parking:
            return self.depthFirst()

        query = "SELECT listing_id, room_type, sqft, washroom, parking, price, address FROM listing WHERE"

        if university == 'uoit':
            query += " uni_id=1"
        elif university == 'utsc':
            query += " uni_id=2"
        elif university == 'utm':
            query += " uni_id=3"

        if not query.endswith("WHERE"):
            query += " AND"

        if room == 'furnished' and washroom == 'separate':
            room_type = "F-SW"
            searched_washroom = "separate"
            query += " room_type LIKE '%F-SW%'"
        elif room == 'furnished' and washroom == 'shared':
            room_type = "F-SHW"
            searched_washroom = "shared"
            query += " room_type LIKE '%F-SHW%'"
        elif room == 'unfurnished' and washroom == 'separate':
            room_type = "UF-SW"
            searched_washroom = "separate"
            query += " room_type LIKE '%UF-SW%'"
        elif room == 'unfurnished' and washroom == 'shared':
            room_type = "UF-SHW"
            searched_washroom = "shared"
            query += " room_type LIKE '%UF-SHW%'"
        elif room == '' and washroom == 'separate':
            room_type = "Not Specified"
            searched_washroom = "separate"
            query += " room_type LIKE '%SW'"
        elif room == '' and washroom == 'shared':
            room_type = "Not Specified"
            searched_washroom = "shared"
            query += " room_type LIKE '%SHW'"
        elif room == 'furnished' and washroom == '':
            searched_washroom = "Not Specified"
            query += " room_type LIKE 'F%'"
        elif room == 'unfurnished' and washroom == '':
            searched_washroom = "Not Specified"
            query += " room_type LIKE 'UF%'"
        elif room == '' and washroom == '':
            room_type = "Not Specified"
            searched_washroom = "Not Specified"

        if not query.endswith("WHERE"):
            if query.endswith("AND"):
                query += ""
            else:
                query += " AND"

        if parking:
            searched_parking = "Yes"
            query += " parking LIKE '%Yes%'"
        elif not parking:
            searched_parking = "No"
            query += " parking LIKE '%No%'"

        if not query.endswith("WHERE"):
            if query.endswith("AND"):
                query += ""
            else:
                query += " AND"

        query += " price<=" + str(price) + " AND sqft<=" + str(size) + ";"

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.execute("SELECT * FROM history;")
        history = list(cursor.fetchall())

        search_history = [room_type, size, searched_washroom, searched_parking, price]

        if len(history) >= 30:
            history.pop()

            for record in history:
                list(record)[0] -= 1

            search_history.insert(0, 30)

            history.append(tuple(search_history))

            print("test2")

            cursor.execute("CREATE TABLE history_new LIKE history;")
            print("test2")
            cursor.execute("RENAME TABLE history TO history_old, history_new TO history;")
            print("test2")
            cursor.execute("DROP TABLE history_old;")
            print("test2")

            for record in history:
                cursor.execute("INSERT INTO history VALUES (" + str(record[0]) + ", '" + record[1] + "', " + str(record[2]) + ", '" + record[3] + "', '" + record[4] + "', " + str(record[5]) + ");")

        else:
            index = 0

            if len(history) > 0:
                index = history[len(history)-1][0] + 1

            search_history.insert(0, index)
            history.append(tuple(search_history))

            print("test3")

            cursor.execute("CREATE TABLE history_new LIKE history;")
            print("test3")
            cursor.execute("RENAME TABLE history TO history_old, history_new TO history;")
            print("test3")
            cursor.execute("DROP TABLE history_old;")
            print("test3")

            for record in history:
                cursor.execute("INSERT INTO history VALUES (" + str(record[0]) + ", '" + record[1] + "', " + str(record[2]) + ", '" + record[3] + "', '" + record[4] + "', " + str(record[5]) + ");")

        cursor.execute("SELECT * FROM preferred;")
        preferred = cursor.fetchone()

        cursor.execute("SELECT searched_roomtype, COUNT(searched_roomtype) AS occ FROM history GROUP BY searched_roomtype ORDER BY occ DESC LIMIT 1;")
        preferred_roomtype = cursor.fetchone()[0]
        print(preferred_roomtype)

        cursor.execute("SELECT AVG(searched_sqft) FROM history")
        preferred_sqft = int(cursor.fetchone()[0])
        print(preferred_sqft)

        cursor.execute("SELECT searched_washroom, COUNT(searched_washroom) AS occ FROM history GROUP BY searched_washroom ORDER BY occ DESC LIMIT 1;")
        preferred_washroom = cursor.fetchone()[0]
        print(preferred_washroom)

        cursor.execute("SELECT searched_parking, COUNT(searched_parking) AS occ FROM history GROUP BY searched_parking ORDER BY occ DESC LIMIT 1;")
        preferred_parking = cursor.fetchone()[0]
        print(preferred_parking)

        cursor.execute("SELECT AVG(searched_price) FROM history")
        preferred_price = int(cursor.fetchone()[0])
        print(preferred_price)

        db.close()
        self.setPreferred(preferred_roomtype, preferred_sqft, preferred_washroom, preferred_parking, preferred_price)
        return result

