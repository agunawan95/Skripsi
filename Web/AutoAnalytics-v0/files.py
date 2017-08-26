import database
import datetime
import os


class Files(database.Database):

    data = None
    msg = ""

    def user_file(self, id):
        sql = "SELECT * FROM files WHERE owner = " + str(id)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def add_file(self, name, owner, location):
        today = datetime.datetime.now()
        sql = "INSERT INTO files VALUES(default, '" + name + "', " + str(owner) + ", '" + str(today) + "', '" + location + "')"
        if self.cur.execute(sql):
            self.con.commit()
            return True
        else:
            return False

    def load_file(self, id):
        sql = "SELECT * FROM files WHERE id = " + str(id)
        self.cur.execute(sql)
        self.data = self.cur.fetchone()

    def get_data(self):
        return self.data

    def delete_file(self, upload_folder):
        if self.data is not None:
            basedir = os.getcwd()
            path = basedir + upload_folder + "/" + self.data['location']
            os.remove(path)

            sql = "DELETE FROM files WHERE id = " + str(self.data['id'])
            if self.cur.execute(sql):
                self.con.commit()
                return True
            else:
                self.msg = "Cannot Delete File Metadata on Server"
                return False

    def err_msg(self):
        return self.msg

    def search_file(self, id, query):
        sql = "SELECT * FROM files WHERE owner = " + str(id) + " AND name LIKE '%" + query + "%'"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def search_shareable_user(self, id_user, file):
        sql = "SELECT * FROM user WHERE id = " + str(id_user)
        self.cur.execute(sql)
        user = self.cur.fetchone()

        if user['auth'] == "admin":
            sql = "SELECT id, username FROM user WHERE id NOT IN (SELECT id_user FROM shared_files WHERE id_file = " + str(file) + ") AND admin = " + str(id_user)
        elif user['auth'] == 'user':
            sql = "SELECT id, username FROM user WHERE id NOT IN (SELECT id_user FROM shared_files WHERE id_file = " + str(file) + ") AND (admin = " + str(user['admin']) + " OR id = " + str(user['admin'])
        elif user['auth'] == 'root':
            sql = "SELECT id, username FROM user WHERE id NOT IN (SELECT id_user FROM shared_files WHERE id_file = " + str(file) + ") AND auth = 'admin'"

        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def share_detail(self, file):
        sql = "SELECT sf.id, u.username, DATE_FORMAT(sf.shared_at, '%W, %d %M %Y') as shared_at, sf.permission FROM user u JOIN shared_files sf ON sf.id_user = u.id WHERE sf.id_file = " + str(file)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def share_file(self, users, file, permission):
        if users is '':
            self.msg = "No User Selected"
            return False
        if permission is not 'r' and permission is not 'w':
            permission = 'r'
        today = str(datetime.datetime.now())
        users = str(users).strip().split(",")
        for user in users:
            sql = "INSERT INTO shared_files VALUES(default, " + user + ", " + str(file) + ", '" + today + "', '" + permission + "')"
            if self.cur.execute(sql):
                self.con.commit()
        return True

    def get_shared_file(self, id_user):
        sql = "SELECT f.location, f.name, f.id FROM shared_files sf JOIN files f ON f.id = sf.id_file WHERE sf.id_user = " + str(id_user)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def search_shared_file(self, id_user, query):
        sql = "SELECT f.location, f.name, f.id FROM shared_files sf JOIN files f ON f.id = sf.id_file WHERE sf.id_user = " + str(id_user) + " AND f.name LIKE '%" + query + "%'"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data