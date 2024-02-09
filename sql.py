import psycopg2

def create_db():
    conn = psycopg2.connect(database="clients_db", user="postgres", password="postgres")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            email VARCHAR(255),
            phones TEXT
        );
    """)
    conn.commit()
    conn.close()

def add_client(conn, first_name, last_name, email, phones=None):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (first_name, last_name, email, phones)
        VALUES (%s, %s, %s, %s);
    """, (first_name, last_name, email, phones))
    conn.commit()
    conn.close()

def add_phone(conn, client_id, phone):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clients
        SET phones = phones || ARRAY[%s]
        WHERE id = %s;
    """, (phone, client_id))
    conn.commit()
    conn.close()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    query = "UPDATE clients SET "
    params = []
    if first_name:
        query += "first_name = %s, "
        params.append(first_name)
    if last_name:
        query += "last_name = %s, "
        params.append(last_name)
    if email:
        query += "email = %s, "
        params.append(email)
    if phones:
        query += "phones = %s, "
        params.append(phones)
    query = query.rstrip(', ')
    query += " WHERE id = %s;"
    params.append(client_id)
    cursor = conn.cursor()
    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()

def delete_phone(conn, client_id, phone):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clients
        SET phones = phones - ARRAY[%s]
        WHERE id = %s;
    """, (phone, client_id))
    conn.commit()
    conn.close()

def delete_client(conn, client_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = %s;", (client_id,))
    conn.commit()
    conn.close()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    query = "SELECT * FROM clients WHERE "
    params = []
    if first_name:
        query += "first_name = %s AND "
        params.append(first_name)
    if last_name:
        query += "last_name = %s AND "
        params.append(last_name)
    if email:
        query += "email = %s AND "
        params.append(email)
    if phone:
        query += "phones && ARRAY[%s] "
        params.append(phone)
    query = query.rstrip(' AND ')
    cursor = conn.cursor()
    cursor.execute(query, tuple(params))
    result = cursor.fetchall()
    conn.close()
    return result

create_db()

with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    add_client(conn, "John", "Doe", "john.doe@example.com", ["+1112345678", "+1987654321"])
    add_phone(conn, 1, "+1112345678")
    change_client(conn,1, first_name="Jane", email="jane.doe@example.com")
    delete_phone(conn, 1, "+1112345678")
    delete_client(conn, 1)
    result = find_client(conn, email="jane.doe@example.com")
    print(result)