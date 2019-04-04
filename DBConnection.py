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

            cursor.execute("CREATE TABLE `listings`.`address` ("
                           "`id` INT NOT NULL AUTO_INCREMENT,"
                           "`uni_id` INT NOT NULL,"
                           "`address` VARCHAR(255) NOT NULL,"
                           "PRIMARY KEY (`id`));")

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

        cursor.execute("SELECT * FROM indexes;")

        if cursor.rowcount == 0:
            self.getIndexes()

        db.close()

    def getIndexes(self):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        values = []

        cursor.execute("SELECT listing_id FROM listing WHERE uni_id=1;")
        result = cursor.fetchall()

        for record in result:
            values.append(record[0])

        cursor.execute("INSERT INTO indexes VALUES (1, '" + str(values) + "');")

        values = []

        cursor.execute("SELECT listing_id FROM listing WHERE uni_id=2;")
        result = cursor.fetchall()

        for record in result:
            values.append(record[0])

        cursor.execute("INSERT INTO indexes VALUES (2, '" + str(values) + "');")

        values = []

        cursor.execute("SELECT listing_id FROM listing WHERE uni_id=3;")
        result = cursor.fetchall()

        for record in result:
            values.append(record[0])

        cursor.execute("INSERT INTO indexes VALUES (3, '" + str(values) + "');")

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
        preferred = cursor.fetchall()[0]

        db.close()
        return preferred

    def setPreferred(self):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        cursor.execute("SELECT * FROM preferred;")
        preferred = cursor.fetchall()

        cursor.execute("SELECT searched_roomtype, COUNT(searched_roomtype) AS occ FROM history GROUP BY searched_roomtype ORDER BY occ DESC LIMIT 1;")
        preferred_roomtype = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(searched_sqft) FROM history")
        preferred_sqft = int(cursor.fetchone()[0])

        cursor.execute("SELECT searched_washroom, COUNT(searched_washroom) AS occ FROM history GROUP BY searched_washroom ORDER BY occ DESC LIMIT 1;")
        preferred_washroom = cursor.fetchone()[0]

        cursor.execute("SELECT searched_parking, COUNT(searched_parking) AS occ FROM history GROUP BY searched_parking ORDER BY occ DESC LIMIT 1;")
        preferred_parking = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(searched_price) FROM history")
        preferred_price = int(cursor.fetchone()[0])

        if len(preferred) > 0:
            cursor.execute("CREATE TABLE preferred_new LIKE preferred;")
            cursor.execute("RENAME TABLE preferred TO preferred_old, preferred_new TO preferred;")
            cursor.execute("DROP TABLE preferred_old;")

        cursor.execute("INSERT INTO preferred VALUES ('" + preferred_roomtype + "', " + str(preferred_sqft) + ", '" + preferred_washroom + "', '" + preferred_parking + "', " + str(preferred_price) + ");")

        db.close()

    def preferredListings(self, uni=None):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()

        preferred = self.getPreferred()

        query = "SELECT listing_id, room_type, sqft, washroom, parking, price, address FROM listing WHERE"

        if uni == 'uoit':
            query += " uni_id=1"
        elif uni == 'utsc':
            query += " uni_id=2"
        elif uni == 'utm':
            query += " uni_id=3"

        if not query.endswith("WHERE"):
            query += " AND"

        if preferred[0] == 'F-SW':
            query += " room_type LIKE '%F-SW%'"
        elif preferred[0] == 'F-SHW':
            query += " room_type LIKE '%F-SHW%'"
        elif preferred[0] == 'UF-SW':
            query += " room_type LIKE '%UF-SW%'"
        elif preferred[0] == 'UF-SHW':
            query += " room_type LIKE '%UF-SHW%'"

        if not query.endswith("WHERE"):
            if query.endswith("AND"):
                query += ""
            else:
                query += " AND"

        query += " sqft*1.1>=" + str(preferred[1]) + " AND sqft*0.9<=" + str(preferred[1])

        if not query.endswith("WHERE"):
            if query.endswith("AND"):
                query += ""
            else:
                query += " AND"

        if preferred[3] == "Yes":
            query += " parking LIKE '%Yes%'"
        elif preferred[3] == "No":
            query += " parking LIKE '%No%'"

        if not query.endswith("WHERE"):
            if query.endswith("AND"):
                query += ""
            else:
                query += " AND"

        query += " price*1.1>=" + str(preferred[4]) + " AND price*0.9<=" + str(preferred[4]) + ";"

        cursor.execute(query)
        preferred_listings = cursor.fetchall()

        db.close()
        return preferred_listings

    def getListings(self, university, room, washroom, parking, price, size):
        db = MySQLdb.connect("localhost", "root", "", "listings")

        cursor = db.cursor()
        uni_id = 0
        room_type = ""
        searched_parking = ""
        searched_washroom = ""
        indexes = []
        result = []

        if university == '' and room == '' and washroom == '' and not parking:
            return self.depthFirst()

        cursor.execute("SELECT listing_id, room_type, sqft, washroom, parking, price, address FROM listing;")
        values = cursor.fetchall()

        if university == 'uoit':
            uni_id = 1
        elif university == 'utsc':
            uni_id = 2
        elif university == 'utm':
            uni_id = 3

        if not university == '':
            cursor.execute("SELECT listing_indexes FROM indexes WHERE uni_id=" + str(uni_id) + ";")
            str1 = cursor.fetchall()[0][0]
            str2 = str1.replace("[", "")
            numbers = str2.replace("]", "")
            indexes = [int(s) for s in numbers.split(',')]
        else:
            cursor.execute("SELECT listing_id FROM listing;")
            str1 = cursor.fetchall()
            for item in str1:
                indexes.append(item[0])
            print(indexes)

        if room == 'furnished' and washroom == 'separate':
            room_type = "F-SW"
            searched_washroom = "separate"
        elif room == 'furnished' and washroom == 'shared':
            room_type = "F-SHW"
            searched_washroom = "shared"
        elif room == 'unfurnished' and washroom == 'separate':
            room_type = "UF-SW"
            searched_washroom = "separate"
        elif room == 'unfurnished' and washroom == 'shared':
            room_type = "UF-SHW"
            searched_washroom = "shared"
        elif room == '' and washroom == 'separate':
            searched_washroom = "separate"
        elif room == '' and washroom == 'shared':
            searched_washroom = "shared"

        if parking:
            searched_parking = "Yes"
        elif not parking:
            searched_parking = "No"


        for value in indexes:
            #print(values[value-1])
            if room == '':
                if washroom == '':
                    if not parking:
                        if int(values[value-1][2]) <= int(size) and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])
                    elif parking:
                        if values[value-1][4] == searched_parking and int(values[value-1][2]) <= int(size) and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])

                elif washroom == 'separate' or washroom == 'shared':
                    if not parking:
                        if int(values[value-1][2]) <= int(size) and values[value-1][3] == washroom.capitalize() and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])
                    elif parking:
                        if values[value-1][4] == searched_parking and int(values[value-1][2]) <= int(size) and values[value-1][3] == washroom.capitalize() and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])

            elif room == 'furnished':
                if washroom == '':
                    if not parking:
                        if values[value-1][1].startswith('F-') and int(values[value-1][2]) <= int(size) and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])
                    elif parking:
                        if values[value-1][1].startswith('F-') and values[value-1][4] == searched_parking and int(values[value-1][2]) <= int(size) and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])

                elif washroom == 'separate' or washroom == 'shared':
                    if not parking:
                        if values[value-1][1] == room_type and int(values[value-1][2]) <= int(size) and values[value-1][3] == washroom.capitalize() and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])
                    elif parking:
                        if values[value-1][1] == room_type and values[value-1][4] == searched_parking and int(values[value-1][2]) <= int(size) and values[value-1][3] == washroom.capitalize() and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])

            elif room == 'unfurnished':
                if washroom == '':
                    if not parking:
                        if values[value-1][1].startswith('UF-') and int(values[value-1][2]) <= int(size) and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])
                    elif parking:
                        if values[value-1][1].startswith('UF-') and values[value-1][4] == searched_parking and int(values[value-1][2]) <= int(size) and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])

                elif washroom == 'separate' or washroom == 'shared':
                    if not parking:
                        if values[value-1][1] == room_type and int(values[value-1][2]) <= int(size) and values[value-1][3] == washroom.capitalize() and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])
                    elif parking:
                        if values[value-1][1] == room_type and values[value-1][4] == searched_parking and int(values[value-1][2]) <= int(size) and values[value-1][3] == washroom.capitalize() and int(values[value-1][5]) <= int(price):
                            result.append(values[value-1])

        print(result)
        history = []

        cursor.execute("SELECT * FROM history;")
        temp_hist = cursor.fetchall()

        for record in temp_hist:
            history.append(list(record))

        search_history = [room_type, size, searched_washroom, searched_parking, price]

        if len(history) >= 30:
            history.pop(0)

            for record in history:
                record[0] -= 1

            search_history.insert(0, 30)

            history.append(search_history)

            cursor.execute("CREATE TABLE history_new LIKE history;")
            cursor.execute("RENAME TABLE history TO history_old, history_new TO history;")
            cursor.execute("DROP TABLE history_old;")

            for record in history:
                cursor.execute("INSERT INTO history VALUES (" + str(record[0]) + ", '" + record[1] + "', " + str(record[2]) + ", '" + record[3] + "', '" + record[4] + "', " + str(record[5]) + ");")

        else:
            index = 0

            if len(history) > 0:
                index = history[len(history)-1][0] + 1

            search_history.insert(0, index)
            history.append(tuple(search_history))

            cursor.execute("CREATE TABLE history_new LIKE history;")
            cursor.execute("RENAME TABLE history TO history_old, history_new TO history;")
            cursor.execute("DROP TABLE history_old;")

            for record in history:
                cursor.execute("INSERT INTO history VALUES (" + str(record[0]) + ", '" + record[1] + "', " + str(record[2]) + ", '" + record[3] + "', '" + record[4] + "', " + str(record[5]) + ");")

        db.close()
        self.setPreferred()
        return result

