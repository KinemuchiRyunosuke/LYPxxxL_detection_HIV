import mysql.connector as mydb

cnx = mydb.connect(
        host = 'localhost',
        user='root',
        password='***',
        database='SLiM_detection'
)

cur = cnx.cursor()

# csvファイル取り込み
cur.execute("CREATE TABLE IF NOT EXIST seq_data"\
            "    (seq str, label int, virus varchar(4), protein varchar(5)")
cur.execute("LOAD DATA LOCAL INFILE dataset.csv INTO seq_data"\
            "    FIELDS TERMINATED BY ','")

# ランダムに番号を振って，新しいtableを作成
cur.execute("CREATE TABLE datasets AS"\
            "SELECT seq,"\
            "       label"\
            "       ROW_NUMBER() OVER(ORDER BY RAND()) id"\
            "FROM seq_data")
