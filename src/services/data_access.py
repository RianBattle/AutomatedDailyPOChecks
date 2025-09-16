import oracledb

def create_oracle_connection():
  try:
    oracledb.init_oracle_client(lib_dir=r"C:\app\client\rbattle\product\12.2.0\client_1")
    conn = oracledb.connect(user="tabula", password="har13y", dsn="PRI")
    return conn
  except oracledb.DatabaseError as e:
    print(f"Database connection error: {e}")
    return None

def get_missing_pos(conn, po_numbers):
  missing_pos = []
  for po_number in po_numbers:
    if not check_oracle_for_po(conn, po_number):
      missing_pos.append(po_number)
  
  return missing_pos

def check_oracle_for_po(conn, po_number):
  fs = open("./queries/check_po_exists.sql", "r")
  sql = fs.read()
  fs.close()

  cursor = conn.cursor()
  cursor.execute(sql, poNumber=po_number)
  
  rows = cursor.fetchall()
  cursor.close()

  return len(rows) > 0
