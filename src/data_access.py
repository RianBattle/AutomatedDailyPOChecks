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
  sql = check_oracle_for_po_sql

  cursor = conn.cursor()
  cursor.execute(sql, poNumber=po_number)

  rows = cursor.fetchall()
  cursor.close()

  return len(rows) > 0

check_oracle_for_po_sql = """
  SELECT sklc_actualpo
  FROM skl$orders
  WHERE sklc_actualpo = :poNumber
  UNION
  SELECT sklc_reference
  FROM skl$deal
  WHERE sklc_reference = :poNumber
    or sklc_reference = :poNumber || 'BK'
  UNION
  SELECT sklc_actualpo
  FROM skl$skl_ediload
  WHERE sklc_actualpo = :poNumber
  UNION
  SELECT sklc_actualpo
  FROM skl$skl_ediload2
  WHERE sklc_actualpo = :poNumber
  UNION
  SELECT sklc_actualpo
  FROM skl$skl_ediload3
  WHERE sklc_actualpo = :poNumber
  UNION
  SELECT orderid
  FROM skl$sklc_amazonload
  WHERE orderid = :poNumber
  UNION
  SELECT po_no
  FROM ediadmin.edi850q
  WHERE po_no = :poNumber
  UNION
  SELECT po_no
  FROM ediadmin.edi850q
  WHERE po_no in(
      SELECT po_no
      FROM ediadmin.edi850hbeg
      WHERE actualpo = :poNumber
    )
"""