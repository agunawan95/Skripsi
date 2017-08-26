from flask import Flask, render_template, request, session, redirect, url_for, make_response, jsonify, abort, send_file
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import pandas as pd

# --------------------------------------------------------------------------------------
# ===================================== Helper Class ===================================
# --------------------------------------------------------------------------------------

import user
import files as fl
import enterprise

# ======================================================================================

# --------------------------------------------------------------------------------------
# ===================================== Configuration ==================================
# --------------------------------------------------------------------------------------

UPLOAD_FOLDER = '/upload'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "bluebutterfly"

from flask_cors import CORS, cross_origin
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


@app.context_processor
def utility_processor():
    def file_size(file_path):
        """
        this function will return the file size
        """
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return convert_bytes(file_info.st_size)
    return dict(filesize=file_size)

# ======================================================================================

# --------------------------------------------------------------------------------------
# ===================================== Error Pages ====================================
# --------------------------------------------------------------------------------------


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


# ======================================================================================

# --------------------------------------------------------------------------------------
# ====================================== Main Pages ====================================
# --------------------------------------------------------------------------------------

@app.route("/")
def home():
    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")
    session['page'] = 'home'
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    user_helper = user.User()
    err = False
    msg = ""
    if session.get('lock') is None:
        session['lock'] = False
    if session['lock'] is True:
        return redirect("/lock")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_helper.login(username, password):
            u = user_helper.get_data()
            session['login'] = True
            session['username'] = request.form["username"]
            session['id'] = u['id']
            session['auth'] = u['auth']
            return redirect("/")
        else:
            err = True
            msg = user_helper.err_msg()
    return render_template("login.html", err=err, msg=msg)


@app.route("/lock", methods=['GET', 'POST'])
def lock():
    user_helper = user.User()
    if request.method == "POST":
        password = request.form['password']
        username = session['username']
        if user_helper.login(username, password):
            session['lock'] = False
            return redirect("/")
    if session.get("username") is None:
        return redirect("/login")
    session['lock'] = True
    return render_template("lock.html")


@app.route("/users", methods=['GET', 'POST'])
def users():
    user_helper = user.User()

    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    err = 0
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        auth = ''
        admin = 0
        if session['auth'] == 'root':
            auth = 'admin'
        elif session['auth'] == 'admin':
            auth = 'user'
            admin = session['id']
        if confirm is not password:
            err = 1
            msg = "Confirm Password Incorrect"
        if user_helper.add_user(username, password, auth, admin):
            if auth == "admin":
                # Add Enterprise Data
                name = request.form['enterprise-name']
                address = request.form['enterprise-address']
                email = request.form['enterprise-email']
                phone = request.form['enterprise-phone']
                filesize = request.form['enterprise-filesize']
                user_limit = request.form['enterprise-user']
                enterprise_helper = enterprise.Enterprise()

                u = user_helper.get_by_username(username)

                if enterprise_helper.add_enterprise(name, address, email, phone, filesize, user_limit, u['id']):
                    msg = "Success"
                    return redirect("/users")
            msg = "Success"
            return redirect("/users")
        else:
            err = 1
            msg = user_helper.err_msg()
    all_user = None
    if session['auth'] == 'root':
        all_user = user_helper.get_all_admin()
    elif session['auth'] == 'admin':
        all_user = user_helper.get_enterprise_user(session['id'])
    session['page'] = 'users'
    return render_template("user.html", users=all_user, err=err, msg=msg)


@app.route("/users/s", methods=['POST'])
def user_search_redirect():
    search = request.form['search']
    if search == '':
        return redirect("/users")
    return redirect("/users/s/" + str(search))


@app.route("/users/s/<query>")
def users_search(query=None):
    user_helper = user.User()

    err = 0
    msg = ''

    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    if query is None:
        return redirect("/users")

    users = None
    if session['auth'] == 'root':
        users = user_helper.search_admin(query)
    elif session['auth'] == 'admin':
        users = user_helper.search_user(query, session['id'])

    return render_template("user.html", users=users, err=err, msg=msg)


@app.route("/files/s", methods=['POST'])
def file_search_redirect():
    search = request.form['search']
    if search == '':
        return redirect("/files")
    return redirect("/files/s/" + str(search))


@app.route("/files/s/<query>")
def files_search(query=None):
    file_helper = fl.Files()

    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    if query is None:
        return redirect("/users")

    user_files = file_helper.search_file(session['id'], query)

    return render_template("file.html", files=user_files)


@app.route("/files", methods=['GET', 'POST'])
def files():
    session['page'] = 'files'

    user_helper = user.User()
    file_helper = fl.Files()

    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    user_file = file_helper.user_file(session['id'])

    return render_template("file.html", files=user_file)


@app.route("/share")
def shared_with_me():
    session['page'] = 'files'

    file_helper = fl.Files()

    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")
    user_shared_file = file_helper.get_shared_file(session['id'])
    return render_template("share.html", files=user_shared_file)


@app.route("/share/s", methods=['POST'])
def share_search_redirect():
    session['page'] = 'files'
    search = request.form['search']
    if search == '':
        return redirect("/share")
    return redirect("/share/s/" + str(search))


@app.route("/share/s/<query>")
def share_search(query=None):
    session['page'] = 'files'
    file_helper = fl.Files()

    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    if query is None:
        return redirect("/share")

    user_files = file_helper.search_shared_file(session['id'], query)

    return render_template("share.html", files=user_files)


@app.route("/project/add")
def add_project():
    session['page'] = 'project'
    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")
    return render_template("add_project.html")

# ======================================================================================

# --------------------------------------------------------------------------------------
# ======================================= Services =====================================
# --------------------------------------------------------------------------------------


@app.route("/api/user/<id>", methods=['GET', 'PUT', 'DELETE'])
def api_user(id=None):
    user_helper = user.User()

    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    id_session = session['id']
    user_helper.load_user(id_session)
    data = user_helper.get_data()
    if request.method == 'GET':
        if data['auth'] == 'user':
            abort(404)

        if id is not None:
            res = user_helper.load_user(id)
            if res is False:
                abort(404)
            if res['auth'] == 'root':
                abort(403)
            if res['auth'] == 'admin':
                enterprise_helper = enterprise.Enterprise()
                res['enterprise'] = enterprise_helper.get_enterprise_by_user(res['id'])
            return jsonify(res)
        else:
            return jsonify({"err": "Must Have ID"})

    if request.method == 'DELETE':
        if user_helper.delete_user(id):
            return jsonify({"err": 0, "msg": "Success"})
        else:
            return jsonify({"err": 1, "msg": user_helper.err_msg()})

    if request.method == 'PUT':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        user_helper.change_username(id, username)

        if password != '':
            if password == confirm:
                if not user_helper.change_password(id, password):
                    return jsonify({"err": 1, "msg": user_helper.err_msg()})
            else:
                return jsonify({"err": 1, "msg": "Detected Password Change but Wrong Confirmation Password"})

        user_helper.load_user(id)
        data = user_helper.get_data()

        if data['auth'] == 'admin':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            filesize = request.form['filesize']
            user_limit = request.form['user_limit']

            enterprise_helper = enterprise.Enterprise()

            if not enterprise_helper.update_enterprise(data['id'], name, address, email, phone, filesize, user_limit):
                return jsonify({"err": 1, "msg": enterprise_helper.error_msg()})

        return jsonify({"err": 0, "msg": "Success"})


@app.route("/api/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({
                "err": 1,
                "msg": "No File Part " + str(request.files)
            })
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return jsonify({
                "err": 1,
                "msg": "No Selected File"
            })
        if file and allowed_file(file.filename):
            file_helper = fl.Files()
            user_helper = user.User()
            user_helper.load_user(session['id'])
            user_data = user_helper.get_data()
            filename = secure_filename(file.filename)
            basedir = os.getcwd()
            if not os.path.exists(basedir + app.config['UPLOAD_FOLDER'] + "/" + user_data['home_folder']):
                os.makedirs(basedir + app.config['UPLOAD_FOLDER'] + "/" + user_data['home_folder'])
            if not os.path.exists(basedir + app.config['UPLOAD_FOLDER'] + "/" + user_data['home_folder'] + "/files"):
                os.makedirs(basedir + app.config['UPLOAD_FOLDER'] + "/" + user_data['home_folder'] + "/files")
            if not os.path.exists(basedir + app.config['UPLOAD_FOLDER'] + "/" + user_data['home_folder'] + "/project"):
                os.makedirs(basedir + app.config['UPLOAD_FOLDER'] + "/" + user_data['home_folder'] + "/project")
            target = basedir + app.config['UPLOAD_FOLDER'] + "/" + user_data['home_folder'] + "/files"
            file.save(os.path.join(target, filename))
            file_helper.add_file(filename, session['id'], user_data['home_folder'] + "/files/" + filename)
            return jsonify({
                "err": 0,
                "msg": "Upload File Success",
                "filename": file.filename
            })
        else:
            return jsonify({
                "err": 1,
                "msg": "Extension not Allowed"
            })


@app.route("/api/download/<id>", methods=['GET'])
def download(id=None):
    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    # Add Security File Owner

    file_helper = fl.Files()
    file_helper.load_file(id)
    data = file_helper.get_data()
    basedir = os.getcwd()
    path = basedir + app.config['UPLOAD_FOLDER'] + "/" + data['location']
    return send_file(path, as_attachment=True)


@app.route("/api/file/<id>", methods=['DELETE'])
def file_api(id=None):
    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    file_helper = fl.Files()
    if request.method == 'DELETE':
        file_helper.load_file(id)
        if file_helper.delete_file(app.config['UPLOAD_FOLDER']):
            return jsonify({"err": 0, "msg": "Success"})
        else:
            return jsonify({"err": 0, "msg": file_helper.err_msg()})


@app.route("/api/shareable/<id_file>")
def shareable_file(id_file=None):
    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    file_helper = fl.Files()

    file_helper.load_file(id_file)
    f = file_helper.get_data()
    if f['owner'] is not session['id']:
        abort(403)

    data = file_helper.search_shareable_user(session['id'], id_file)
    return jsonify(data)


@app.route("/api/share/detail/<id_file>")
def share_detail(id_file=None):
    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    file_helper = fl.Files()

    file_helper.load_file(id_file)
    f = file_helper.get_data()
    if f['owner'] is not session['id']:
        abort(403)

    data = file_helper.share_detail(id_file)
    return jsonify(data)


@app.route("/api/share", methods=['POST'])
def share():
    users = request.form['users']
    id = request.form['id_file']
    permission = request.form['permission']

    if session.get("login") is None:
        return redirect("/login")
    if session.get("lock") is True:
        return redirect("/lock")

    file_helper = fl.Files()

    file_helper.load_file(id)
    f = file_helper.get_data()
    if f['owner'] is not session['id']:
        abort(403)

    if file_helper.share_file(users, id, permission):
        return jsonify({"err": 0, "msg": "Success"})
    else:
        return jsonify({"err": 1, "msg": file_helper.err_msg()})


@app.route("/coba/<id>", methods=['PUT', 'DELETE'])
def coba(id=None):
    if request.method == 'DELETE':
        msg = "Delete " + str(id)
        return jsonify({"msg": msg})
    if request.method == 'PUT':
        msg = "PUT "
        username = request.form['username']
        password = request.form['password']
        msg = msg + "Username: " + username + "Password: " + password + "ID: " + id
        return jsonify({"msg": msg})
    return jsonify({"msg": "Meong"})

# ======================================================================================

# --------------------------------------------------------------------------------------
# ===================================== Other Access ===================================
# --------------------------------------------------------------------------------------


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ======================================================================================

if __name__ == '__main__':
    app.run(debug=True)
