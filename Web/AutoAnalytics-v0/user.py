import database
import hashlib
import pymysql


class User(database.Database):

    err = 0
    msg = ''
    data = None

    def login(self, username, password):
        sql = "SELECT * FROM user WHERE username = '" + username + "' AND password = '" + password + "'"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        self.data = data
        if self.cur.rowcount > 0:
            self.msg = "Success"
            return True
        if username == "" and password == "":
            self.msg = "Username and Password is Required"
            return False
        if username == "":
            self.msg = "Username is Required"
            return False
        if password == "":
            self.msg = "Password is Required"
            return False
        self.msg = "Wrong Username or Password"
        return False

    def err_msg(self):
        return self.msg

    def get_data(self):
        return self.data

    def get_users(self):
        sql = "SELECT * FROM user WHERE auth <> 'root'"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def get_all_admin(self):
        sql = "SELECT * FROM user WHERE auth = 'admin'"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def get_enterprise_user(self, id):
        sql = "SELECT * FROM user WHERE auth <> 'root' AND admin = " + str(id)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def add_user(self, username, password, auth, admin):
        if username == "" and password == "":
            self.msg = "Username and Password is Required"
            return False
        if username == "":
            self.msg = "Username is Required"
            return False
        if password == "":
            self.msg = "Password is Required"
            return False
        if auth == "":
            self.msg = "Authentication Level is Required"
            return False
        sql = "SELECT * FROM user WHERE username = '" + username + "'"
        self.cur.execute(sql)
        if self.cur.rowcount > 0:
            self.msg = "Username Already Exist"
            return False
        hash_object = hashlib.sha3_256(str(username).encode("utf-8"))
        hex = hash_object.hexdigest()
        home_folder = hex[0:30]
        sql = "INSERT INTO user VALUES(default, '" + username + "', '" + password + "', '" + home_folder + "', '" + auth + "', " + str(admin) + ")"
        if self.cur.execute(sql):
            self.con.commit()
            self.msg = "Success"
            return True
        else:
            self.msg = "Cannot Add New User to Database"
            return False

    def load_user(self, id):
        sql = "SELECT * FROM user WHERE id = " + str(id)
        self.cur.execute(sql)
        if self.cur.rowcount > 0:
            self.data = self.cur.fetchone()
            res = {
                "id": self.data['id'],
                "username": self.data['username'],
                "home_folder": self.data['home_folder'],
                "auth": self.data['auth']
            }
            return res
        else:
            return False

    def delete_user(self, id):
        sql = "DELETE FROM user WHERE id = " + str(id)
        if self.cur.execute(sql):
            self.con.commit()
            self.msg = "Success"
            return True
        else:
            self.msg = "Cannot Delete User From Database"
            return False

    def change_password(self, id, password):
        sql = "UPDATE user SET password = '" + password + "' WHERE id = " + str(id)
        if self.cur.execute(sql):
            self.con.commit()
            self.msg = "Success"
            return True
        else:
            self.msg = "Cannot Change User Password To Database"
            return False

    def change_username(self, id, username):
        sql = "UPDATE user SET username = '" + username + "' WHERE id = " + str(id)
        if username != '':
            if self.cur.execute(sql):
                self.con.commit()
                self.msg = "Success"
                return True
            else:
                self.msg = "No Data Affected"
                return False
        else:
            self.msg = "Username Must Have Value"
            return False

    def search_admin(self, query):
        sql = "SELECT * FROM user WHERE username LIKE '%" + query + "%' AND auth = 'admin'"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def search_user(self, query, id):
        sql = "SELECT * FROM user WHERE username LIKE '%" + query + "%' AND admin = " + str(id)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def get_by_username(self, username):
        sql = "SELECT * FROM user WHERE username = '" + username + "'"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data