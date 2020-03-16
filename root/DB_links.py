import mysql.connector
import json

# the database connection portal
db = mysql.connector.connect(host='sql9.freemysqlhosting.net', port=3306, user='sql9328281', passwd='YXTh46Irct',
                             database='sql9328281')


# this fetches the product name
def mysqlConnector(product_name):
    cursor = db.cursor()
    sql = "SELECT status FROM product where subcategory  = %s"
    adr = (product_name,)
    cursor.execute(sql, adr)
    result = cursor.fetchall()
    for x in result:
        for v in x:
            return v


# this fetches all product base on the particular stage of the products which the user requires
def get_product_by_stage(stage):
    cursor = db.cursor()
    sql = "SELECT subcategory FROM product where status  = %s"
    adr = (stage,)
    cursor.execute(sql, adr)
    result = cursor.fetchall()
    c = ""
    for x in result:
        c += x[0] + '\n\n'
    return c


# this fetches the product images from the database
def get_product_by_image(product, status):
    cursor = db.cursor()
    sql = "SELECT images FROM product where subcategory  = %s and status = %s"
    adr = (product, status)
    cursor.execute(sql, adr)
    result = cursor.fetchall()
    ab = []
    for x in result:
        for v in x:
            if v is not None:
                c = json.loads(v)
                ab.append(c[0])
    kk = []
    for x in ab:
        cc = {
            "title": product,
            "image_url": 'https://rucove.com/uploads//' + x,
            "subtitle": get_product_title(product, status)[0],
            "default_action": {
                "type": "web_url",
                "url": f"https://rucove.com/products/{get_product_title(product, status)[1]}",
                "webview_height_ratio": "tall",
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": "https://www.messenger.com/t/clair.blair.376",
                    "title": f"Chat with {get_owner_name(product, status)}"
                }
            ]
        }

        kk.append(cc)
    return kk


# this fetches the product titles from the database
def get_product_title(product, status):
    cursor = db.cursor()
    sql = "SELECT title,title_id FROM product where subcategory  = %s and status = %s"
    adr = (product, status)
    cursor.execute(sql, adr)
    result = cursor.fetchall()
    for x in result:
        return x


def quick_product_stage(product_name):
    cursor = db.cursor()
    sql = "SELECT status FROM product where subcategory  = %s"
    adr = (product_name,)
    cursor.execute(sql, adr)
    result = cursor.fetchall()
    c = []
    for x in result:
        for v in x:
            dd = v.lower()
            kk = {
                "content_type": "text",
                "title": dd,
                "payload": 'product_' + v
            }
            c.append(kk)

    return c


def get_owner_id(product, status):
    cursor = db.cursor()
    sql = "SELECT owner FROM product where subcategory  = %s and status = %s"
    adr = (product, status)
    cursor.execute(sql, adr)
    result = cursor.fetchall()
    for x in result:
        for v in x:
            return v


def get_owner_name(product, status):
    cursor = db.cursor()
    sql = "SELECT fullName FROM users where id = %s"
    adr = (get_owner_id(product, status),)
    cursor.execute(sql, adr)
    result = cursor.fetchall()
    for x in result:
        for v in x:
            return v
