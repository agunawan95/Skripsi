import database


class Enterprise(database.Database):

    msg = ""

    def add_enterprise(self, name, address, email, phone, filesize, user_limit, admin):
        sql = "INSERT INTO enterprise VALUES (default, '" + name + "', '" + address + "', '" + email + "', '" + phone + "', " + str(filesize) + ", " + str(user_limit) + ", " + str(admin) + ")"
        res = self.cur.execute(sql)
        if res:
            self.con.commit()
        return res

    def get_enterprise_by_user(self, id):
        sql = "SELECT * FROM enterprise WHERE admin = " + str(id)
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data

    def update_enterprise(self, id, name, address, email, phone, filesize, user_limit):
        sql = "UPDATE enterprise SET name = '" + name + "', address = '" + address + "', email = '" + email + "', phone = '" + phone + "', filesize_limit = " + str(filesize) + ", user_limit = " + str(user_limit) + " WHERE admin = " + str(id)
        if self.cur.execute(sql):
            self.con.commit()
            return True
        else:
            self.msg = "No Change Have Made!"
            return False

    def error_msg(self):
        return self.msg
