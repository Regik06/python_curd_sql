import psycopg2
from pprint import pprint


def create_db(cur):
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
    print(f'Done! Table created')


def add_client(cur, name, last_name, email, phones=None):
    cur.execute('''
        INSERT INTO clients(name, last_name, email) VALUES(%s, %s, %s)
        RETURNING id, name;
    ''', (name, last_name, email))
    cur.execute("""
    SELECT * FROM clients;
    """)
    print(f'INSERT CLIENT INFO {cur.fetchall()}')


def exist_clients(cur, client_id):
    cur.execute('''
    SELECT EXISTS(SELECT id FROM clients WHERE id = %s)
    ''', (client_id,))
    return cur.fetchone()


def add_phone(cur, client_id, number):
    if True in exist_clients(cur, client_id):
        cur.execute('''
        INSERT INTO phone(client_id, number) VALUES(%s, %s)
        RETURNING id, number;
        ''', (client_id, number))
        cur.execute("""
        SELECT * FROM phone;
        """)
        print(f' INSERT PHONE {cur.fetchall()}')
    else:
        print(f'INSERT PHONE: Клиента с идентификатором {client_id} нет в базе!')


def change_client(cur, client_id, name=None, last_name=None, email=None, phones=None):
    if True in exist_clients(cur, client_id):
        cur.execute('''
        UPDATE clients SET name = %s WHERE id = %s;
        ''', (name, client_id,))
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

        pprint(f' UPDATE DATA {cur.fetchall()}')
    else:
        print(f'UPDATE DATA: Клиента с идентификатором {client_id} нет в базе!')


def delete_phone(cur, client_id):
    if True in exist_clients(cur, client_id):
        cur.execute('''
        DELETE FROM phone WHERE id = %s;
        ''', (client_id,))
        cur.execute("""
        SELECT * FROM phone;
        """)
        print(f'DELETE PHONE {cur.fetchall()}')
    else:
        print(f'DELETE PHONE: Клиента с идентификатором {client_id} нет в базе!')


def delete_client(cur, client_id):
    if True in exist_clients(cur, client_id):
        cur.execute('''
                DELETE FROM clients WHERE id = %s;
                ''', (client_id,))
        cur.execute("""
                SELECT * FROM clients;
                """)
        print(f'DELETE CLIENTS {cur.fetchall()}')
    else:
        print(f'DELETE CLIENTS: Клиента с идентификатором {client_id} нет в базе!')


def find_client(cur, phone=None, email=None, name=None, lastname=None):
    if phone is not None:
        cur.execute('''
            SELECT name, last_name, p.number FROM clients as c
            LEFT JOIN phone as p on p.client_id=c.id
            WHERE p.number=%s;
            ''', (phone,))
        print(f'SELECT PHONE {cur.fetchall()}')
    elif email is not None:
        cur.execute('''
           SELECT name, email, p.number FROM clients as c
           LEFT JOIN phone as p on p.client_id=c.id
           WHERE c.email=%s;
           ''', (email,))
        print(f'SELECT EMAIL {cur.fetchall()}')
    elif name is not None:
        cur.execute("""
                SELECT name, last_name, p.number FROM clients as c
                LEFT JOIN phone as p on p.client_id=c.id
                WHERE c.name=%s;
                   """, (name,))
        print(f'SELECT NAME {cur.fetchall()}')
    elif lastname is not None:
        cur.execute("""
        SELECT name, last_name, p.number FROM clients as c
        LEFT JOIN phone as p on p.client_id=c.id
        WHERE c.last_name=%s;
        """, (lastname,))
        print(f'SELECT LASTNAME {cur.fetchall()}')


if __name__ == '__main__':
    with psycopg2.connect(database="clients", user="postgres") as conn:
        with conn.cursor() as cur:
            print('------------------------')
            create_db(cur)
            print('------------------------')
            add_client(cur, 'Mayk', 'Vazovski', 'korporation@monstr.com')
            add_client(cur, 'Morty', 'Smith', 'child@scientist.world')
            add_client(cur, 'Mill', 'Pops', 'lyalyalya@juju.ju')
            print('------------------------')
            add_phone(cur, 1, 791078)
            add_phone(cur, 2, 349739)
            add_phone(cur, 3, 99028)
            print('------------------------')
            change_client(cur, 1, 'Rick', 'Sunchez', 'interplanetary@scientist.world', 66690)
            print('------------------------')
            delete_phone(cur, 1)
            delete_client(cur, 5)
            print('------------------------')
            find_client(cur, name='Morty')
            find_client(cur, lastname='Pops')
            find_client(cur, email='child@scientist.world')
            find_client(cur, phone=99028)
            print('------------------------')

    conn.close()
