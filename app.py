import os
import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "123456789"
db = "webdb.db"


def create_db():
    """如果資料庫不存在就創建資料庫"""
    if not os.path.isfile(db):
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            cursor.execute(
                """
                        CREATE TABLE IF NOT EXISTS customer (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        sex TEXT NOT NULL,
                        birth TEXT NOT NULL,
                        address TEXT NOT NULL)"""
            )

            cursor.execute(
                """
                        CREATE TABLE IF NOT EXISTS product (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        price TEXT NOT NULL)"""
            )

            cursor.execute(
                """
                        CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        cid INTEGER NOT NULL,
                        pid INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        price INTEGER NOT NULL,
                        FOREIGN KEY (cid) REFERENCES customer(id),
                        FOREIGN KEY (pid) REFERENCES product(id))"""
            )

            cursor.execute(
                """
                        CREATE TABLE IF NOT EXISTS orders_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        cid INTEGER NOT NULL,
                        pid INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        price INTEGER NOT NULL,
                        FOREIGN KEY (cid) REFERENCES customer(id),
                        FOREIGN KEY (pid) REFERENCES product(id))"""
            )

            cursor.execute(
                """
                        CREATE TABLE IF NOT EXISTS administrator (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        pwd TEXT NOT NULL
                )
            """
            )

            cursor.execute(
                """
                           INSERT INTO product(description, price) VALUES
                           ("PH", "7000"),
                           ("TDS+NTU", "8000"),
                           ("PH+TDS", "8500"),
                           ("PH+TDS+NTU", "10000")
                           """
            )
            cursor.execute(
                """INSERT INTO administrator (username, pwd) VALUES
                           (?, ?)""",
                ("3B017120", "3B017120"),
            )

            conn.commit()

            return conn
        except Exception as e:
            print("資料庫建立失敗")
            print(f"錯誤訊息：{e}")


def get_table(table_name: str) -> list:
    """從選中的TABLE取出所有資料"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f"Select * from {table_name}")
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def get_customer(cid) -> list:
    """透過cid抓取消費者"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("Select * from customer where id=?", (cid,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def update_customer(id, name, pwd, email, phone, sex, birth, address) -> None:
    """更新customer"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql = "Update customer set name=?, password=?, email=?, phone=?,"
    sql = sql + " sex=?, birth=?, address=? where id = ?"
    values = (name, pwd, email, phone, sex, birth, address, id)
    cursor.execute(sql, values)
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def get_orders(oid) -> list:
    """透過oid抓取訂單"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("Select * from orders where id=?", (oid,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def complete_orders(oid, cid, pid, quantity, price):
    """已完成訂單插入orders_history"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql = "DELETE FROM orders WHERE id = ?"
    values = (oid,)
    cursor.execute(sql, values)
    sql = "Insert into orders_history (cid, pid, quantity, price) values(?,?,?,?)"
    values = (cid, pid, quantity, price)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()


def get_horders(hid) -> list:
    """透過hid抓取歷史訂單"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("Select * from orders_history where id=?", (hid,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def get_product(pid) -> list:
    """用pid抓取商品選項"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("Select * from product where id=?", (pid,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def update_product(id, describe, price) -> None:
    """更新商品選項"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql = "Update product set describe=?, price=? where id = ?"
    values = (describe, price, id)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()


def add_product(describe, price) -> None:
    """增加商品選項"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql = "Select id from product"
    cursor.execute(sql)
    result = cursor.fetchall()
    id = result[len(result) - 1][0] + 1
    sql = "Insert into product (id, description, price) values(?,?,?)"
    values = (id, describe, price)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()


def get_admins(aid) -> list:
    """用aid抓取管理員"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("Select * from administrator where id=?", (aid,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def update_admins(id, username, pwd) -> None:
    """更新管理員"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql = "Select username from administrator"
    cursor.execute(sql)
    result = cursor.fetchall()
    for r in result:
        if username == r[0]:
            return "Has same username"
    sql = "Update administrator set username=?, pwd=? where id = ?"
    values = (username, pwd, id)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return "Update success"


def add_admins(username, pwd) -> str:
    """更新管理員"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql = "Select username from administrator"
    cursor.execute(sql)
    result = cursor.fetchall()
    for r in result:
        if username == r[0]:
            return "Has same username"
    sql = "Insert into administrator (username, pwd) values(?,?)"
    values = (username, pwd)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return "Add success"


create_db()


@app.route("/", methods=["GET", "POST"])
def index():
    """顯示首頁"""
    logged_in = "u" in session
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    data = cursor.fetchall()

    if request.method == "GET":
        return render_template("index.html", logged_in=logged_in, product=data, len=len(data))

    return render_template("index.html", logged_in=logged_in, product=data, len=len(data))


@app.route("/login", methods=["GET", "POST"])
def login():
    """處理登入事項"""
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if not name or not password:
            return render_template("login.html")

        try:
            conn = sqlite3.connect(db)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM customer WHERE name = ? AND
                           password = ?""",
                (name, password),
            )
            user = cursor.fetchone()

            if user:
                session["u"] = user["name"]
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="帳號密碼錯誤")
        except Exception as e:
            with open("error.log", "a") as f:
                f.write(f"Login Error: {e}\n")
            return render_template("error.html")
        finally:
            conn and conn.close()
    return render_template("login.html")


@app.route("/user")
def customer():
    """顯示customer"""
    if "u" not in session:
        return redirect(url_for("login"))

    try:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer WHERE name = ?", (session["u"],))
        user = cursor.fetchone()
        return render_template("customer.html", user=user)
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(str(e))
            return render_template("error.html")
    finally:
        conn and conn.close()


@app.route("/register", methods=["GET", "POST"])
def register():
    """處理登入事項"""
    if request.method == "POST":
        try:
            password = request.form.get("password")
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            sex = request.form.get("sex")
            birth = request.form.get("birth")
            address = request.form.get("address")

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM customer WHERE name=?", (name,))
            repeat = cursor.fetchone()
            if repeat:
                error_message = "帳號名稱重複，請重新輸入"
                return render_template("register.html", error=error_message)

            cursor.execute(
                """
                INSERT INTO customer (password, name, email, phone, sex
                , birth, address) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (password, name, email, phone, sex, birth, address),
            )

            conn.commit()
            conn.close()

            return redirect(url_for("index"))
        except Exception as e:
            with open("error.log", "a") as f:
                f.write(str(e))
            return render_template("error.html")

    return render_template("register.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    """處理修改會員資料"""
    try:
        if "u" not in session:
            return redirect(url_for("login"))

        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if request.method == "POST":
            password = request.form.get("password")
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            sex = request.form.get("sex")
            birth = request.form.get("birth")
            address = request.form.get("address")

            cursor.execute(
                """UPDATE customer SET name = ?, password = ?,
                           email = ?, phone = ?, sex = ?, birth = ?,
                           address = ? WHERE name = ?""",
                (
                    password,
                    name,
                    email,
                    phone,
                    sex,
                    birth,
                    address,
                    session["u"],
                ),
            )
            conn.commit()

            return redirect(url_for("customer"))
        cursor.execute("SELECT * FROM customer WHERE name = ?", (session["u"],))
        user = cursor.fetchone()
        return render_template("edit.html", user=user)
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(str(e))
        return render_template("error.html")


@app.route("/logout")
def logout():
    """處理登出"""
    try:
        session.pop("u", None)
        return redirect(url_for("index"))
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(str(e))
        return render_template("error.html")


@app.route("/buy", methods=["GET", "POST"])
def buy():
    """將從首頁收到的訂單資訊插入order"""
    if request.method == "POST":
        # cid = request.form.get('name')
        cid = session["u"]
        pid = request.form.get("id")
        quantity = request.form.get("quantity")
        price = request.form.get("totalprice")

        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO orders (cid, pid, quantity, price)
                VALUES (?, ?, ?, ?)
            """,
                (cid, pid, quantity, price),
            )

            conn.commit()

        except Exception as e:
            with open("error.log", "a") as f:
                f.write(str(e))
            return render_template("error.html")
        finally:
            if conn:
                conn.close()
        return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/orders")
def orders():
    """顯示order"""
    if "u" not in session:
        return redirect(url_for("login"))

    try:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM orders WHERE cid = ?", (session["u"],))

        orders = cursor.fetchall()

        return render_template("orders.html", orders=orders)

    except Exception as e:
        with open("error.log", "a") as f:
            f.write(str(e))
        return render_template("error.html")
    finally:
        if conn:
            conn.close()


@app.route("/orders_history")
def orders_history():
    """顯示order_history"""
    if "u" not in session:
        return redirect(url_for("login"))

    try:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM orders_history WHERE cid = ?", (session["u"],))

        orders = cursor.fetchall()

        return render_template("orders_history.html", orders=orders)

    except Exception as e:
        with open("error.log", "a") as f:
            f.write(str(e))
        return render_template("error.html")
    finally:
        if conn:
            conn.close()


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """管理員登入"""
    if request.method == "GET":
        return render_template("admin_login.html")
    elif request.method == "POST":
        admin = request.form.get("admin")
        pwd = request.form.get("pwd")
        login_list = get_table("administrator")
        correct_login = False
        for ll in login_list:
            if admin == ll[1] and pwd == ll[2]:
                correct_login = True
                session["admin"] = ll[1]
        if correct_login:
            return redirect(url_for("admin_manage"))
        return render_template("admin_login.html", error="請輸入正確的帳號密碼")


@app.route("/admin/manage")
def admin_manage():
    """管理員主頁"""
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        return render_template("admin_manage.html", name=session["admin"])


@app.route("/admin/customers", methods=["GET", "POST"])
def admin_customer():
    """客戶管理"""
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            customer = get_table("customer")
            return render_template("admin_customer.html", customer=customer, index=len(customer))
        if request.method == "POST":
            cid = request.form.get("cid")
            session["admin_cid"] = cid
            return redirect(url_for("admin_edit_customer"))


@app.route("/admin/edit/customers", methods=["GET", "POST"])
def admin_edit_customer():
    """編輯客戶頁面"""
    cid = session["admin_cid"]
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            customer = get_customer(cid)
            return render_template("admin_edit_customer.html", c=customer)
        if request.method == "POST":
            name = request.form.get("nms")
            pwd = request.form.get("pwds")
            email = request.form.get("emails")
            phone = request.form.get("phones")
            sex = request.form.get("sexs")
            birth = request.form.get("births")
            address = request.form.get("addresss")
            update_customer(
                id=cid,
                name=name,
                pwd=pwd,
                email=email,
                phone=phone,
                sex=sex,
                birth=birth,
                address=address,
            )
            session.pop("admin_cid", None)
            return redirect(url_for("admin_customer"))


@app.route("/admin/orders", methods=["GET", "POST"])
def admin_orders():
    """訂單管理"""
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            orders = get_table("orders")
            orders_index = []
            for i in orders:
                orders_index.append(i[0])
            return render_template(
                "admin_orders.html", orders=orders, index=len(orders), oindex=orders_index
            )
        if request.method == "POST":
            oid = request.form.get("oid")
            session["admin_oid"] = oid
            return redirect(url_for("admin_orders_more"))


@app.route("/admin/orders/more", methods=["GET", "POST"])
def admin_orders_more():
    """訂單詳情"""
    oid = session["admin_oid"]
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            orders = get_orders(oid)
            return render_template("admin_orders_more.html", o=orders)
        if request.method == "POST":
            cid = request.form.get("cid")
            pid = request.form.get("pid")
            quantity = request.form.get("quantity")
            price = request.form.get("price")
            complete_orders(oid=oid, cid=cid, pid=pid, quantity=quantity, price=price)
            session.pop("admin_oid", None)
            return redirect(url_for("admin_orders"))


@app.route("/admin/horders", methods=["GET", "POST"])
def admin_horders():
    """歷史訂單"""
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            horders = get_table("orders_history")
            return render_template("admin_horders.html", horders=horders, index=len(horders))
        if request.method == "POST":
            hid = request.form.get("hid")
            session["admin_hid"] = hid
            return redirect(url_for("admin_horders_more"))


@app.route("/admin/horders/more", methods=["GET", "POST"])
def admin_horders_more():
    """歷史訂單詳情"""
    hid = session["admin_hid"]
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            horders = get_horders(hid)
            return render_template("admin_horders_more.html", h=horders)
        if request.method == "POST":
            session.pop("admin_hid", None)
            return redirect(url_for("admin_horders"))


@app.route("/admin/product", methods=["GET", "POST"])
def admin_product():
    """顯示商品"""
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            product = get_table("product")
            return render_template("admin_product.html", product=product, index=len(product))
        if request.method == "POST":
            pid = request.form.get("pid")
            session["admin_pid"] = pid
            return redirect(url_for("admin_edit_product"))


@app.route("/admin/edit/product", methods=["GET", "POST"])
def admin_edit_product():
    """顯示商品管理"""
    pid = session["admin_pid"]
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            product = get_product(pid)
            return render_template("admin_edit_product.html", p=product)
        if request.method == "POST":
            describe = request.form.get("describe")
            price = request.form.get("price")
            update_product(id=pid, describe=describe, price=price)
            session.pop("admin_pid", None)
            return redirect(url_for("admin_product"))


@app.route("/admin/add/product", methods=["GET", "POST"])
def admin_add_product():
    """管理員增加商品選項頁面"""
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            return render_template("admin_add_product.html")
        if request.method == "POST":
            describe = request.form.get("describe")
            price = request.form.get("price")
            add_product(describe=describe, price=price)
            return redirect(url_for("admin_product"))


@app.route("/admin/admins", methods=["GET", "POST"])
def admin_admins():
    """管理員管理"""
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            admins = get_table("administrator")
            return render_template("admin_admins.html", admins=admins, index=len(admins))
        if request.method == "POST":
            aid = request.form.get("aid")
            session["admin_aid"] = aid
            return redirect(url_for("admin_edit_admins"))


@app.route("/admin/edit/admins", methods=["GET", "POST"])
def admin_edit_admins():
    """管理員編輯管理員"""
    aid = session["admin_aid"]
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            admins = get_admins(aid)
            return render_template("admin_edit_admins.html", a=admins)
        if request.method == "POST":
            user = request.form.get("username")
            pwd = request.form.get("password")
            result = update_admins(id=aid, username=user, pwd=pwd)
            session.pop("admin_aid", None)
            if result == "Update success":
                return redirect(url_for("admin_admins"))
            else:
                return redirect(url_for("admin_admins_same"))


@app.route("/admin/add/admins", methods=["GET", "POST"])
def admin_add_admins():
    """管理員新增管理員"""
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            return render_template("admin_add_admins.html")
        if request.method == "POST":
            user = request.form.get("username")
            pwd = request.form.get("password")
            result = add_admins(username=user, pwd=pwd)
            if result == "Add success":
                return redirect(url_for("admin_admins"))
            else:
                return redirect(url_for("admin_admins_same"))


@app.route("/admin/admins/same")
def admin_admins_same():
    """有相同的管理員名稱"""
    return render_template("admin_admins_same.html")


@app.route("/admin/logout")
def admin_logout():
    """管理員登出"""
    session.pop("admin", None)
    return redirect(url_for("index"))


@app.route("/admin/contact")
def admin_call():
    """聯絡開發人員"""
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    else:
        return render_template("admin_call.html")
