import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
            DROP TABLE phone;
            DROP TABLE clients;
            ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        name VARCHAR(30) NOT NULL,
        last_name VARCHAR(30) NOT NULL,
        email VARCHAR(30) NOT NULL,
        phones INTEGER );
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS phone (
        id SERIAL PRIMARY KEY,
        number INTEGER ,
        client_id INTEGER REFERENCES clients(id)
        );
        ''')
        conn.commit()
        print(f'Done! Table created')


def add_client(conn, name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO clients(name, last_name, email) VALUES(%s, %s, %s)
        RETURNING id, name;
        ''', (name, last_name, email))
        cur.execute("""
        SELECT * FROM clients;
        """)
        print(f'INSERT CLIENT INFO {cur.fetchall()}')


def add_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO phone(client_id, number) VALUES(%s, %s)
        RETURNING id, number;
        ''', (client_id, number))
        cur.execute("""
        SELECT * FROM phone;
        """)
        print(f' INSERT PHONE {cur.fetchall()}')



def change_client(conn, client_id, name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE clients SET name = %s WHERE id = %s;
        ''', (name, client_id, ))
        cur.execute('''
        UPDATE clients SET last_name = %s WHERE id = %s;
        ''', (last_name, client_id))
        cur.execute('''
                UPDATE clients SET email = %s WHERE id = %s;
                ''', (email, client_id))
        cur.execute('''
                        UPDATE clients SET phones = %s WHERE id = %s;
                        ''', (phones, client_id))
        cur.execute("""
                SELECT * FROM clients;
                """)

        print(f' UPDATE DATA {cur.fetchall()}')


def exist_clients(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT EXISTS(SELECT id FROM clients WHERE id = %s)
        ''',(client_id,))
        return cur.fetchone()


def delete_phone(conn, client_id):
    if True in exist_clients(conn, client_id):
        with conn.cursor() as cur:
            cur.execute('''
            DELETE FROM phone WHERE id = %s;
            ''', (client_id,))
            cur.execute("""
            SELECT * FROM phone;
            """)
            print(f'DELETE PHONE {cur.fetchall()}')
    else:
        print('DELETE PHONE: !!Такого клиента нет в базе!!')

def delete_client(conn, client_id):
    if True in exist_clients(conn, client_id):
        with conn.cursor() as cur:
            cur.execute('''
                    DELETE FROM clients WHERE id = %s;
                    ''', (client_id,))
            cur.execute("""
                    SELECT * FROM clients;
                    """)
            print(f'DELETE CLIENTS {cur.fetchall()}')
    else:
        print('DELETE CLIENTS: !!Такого клиента нет в базе!!')

def find_client(conn, name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                SELECT name, last_name, p.number FROM clients as c 
                LEFT JOIN phone as p on p.client_id=c.id
                WHERE c.name=%s;
                """, (name,))
        print(f'SELECT NAME {cur.fetchall()}')
        cur.execute("""
        SELECT name, last_name, p.number FROM clients as c 
        LEFT JOIN phone as p on p.client_id=c.id
        WHERE c.last_name=%s;
        """, (last_name,))
        print(f'SELECT LASTNAME {cur.fetchall()}')
        cur.execute('''
        SELECT name, email, p.number FROM clients as c
        LEFT JOIN phone as p on p.client_id=c.id
        WHERE c.email=%s;
        ''', (email,))
        print(f'SELECT EMAIL {cur.fetchall()}')
        cur.execute('''
        SELECT name, last_name, p.number FROM clients as c
        LEFT JOIN phone as p on p.client_id=c.id
        WHERE p.number=%s;
        ''', (phone,))
        print(f'SELECT PHONE {cur.fetchall()}')




with psycopg2.connect(database="clients", user="postgres") as conn:
    print('------------------------')
    create_db(conn)
    print('------------------------')
    # name = input('Введите имя клиента: ')
    # last_name = input('Введите фамилию клиента: ')
    # email = input('Введите email клиента: ')
    add_client(conn, 'Mayk', 'Vazovski', 'korporation@monstr.com')
    add_client(conn, 'Morty', 'Smith', 'child@scientist.world')
    add_client(conn, 'Mill', 'Pops', 'lyalyalya@juju.ju')
    print('------------------------')
    # number = input('Введите номер телефона, если он существует: ')
    add_phone(conn, 1, 791078)
    add_phone(conn, 2, 349739)
    add_phone(conn, 3, 99028)
    print('------------------------')
    change_client(conn, 1, 'Rick', 'Sunchez', 'interplanetary@scientist.world', 66690)
    print('------------------------')
    delete_phone(conn, 1)
    delete_client(conn, 5)
    print('------------------------')
    find_client(conn, 'Morty', 'Pops', 'korporation@monstr.com', 99028)
    print('------------------------')

conn.close()