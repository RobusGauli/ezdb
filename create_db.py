import psycopg2


def table_commands():
    '''This function creates tables in the database'''

    role_table = '''
                CREATE TABLE roles (
                    id SERIAL PRIMARY KEY,
                    role_type VARCHAR(255) NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT Now(),
                    updated_at TIMESTAMPTZ DEFAULT Now()
                );
                '''
    
    
    
    branch_table = '''
                    CREATE TABLE branches (
                        id SERIAL PRIMARY KEY, 
                        name VARCHAR(255) NOT NULL UNIQUE,
                        branch_code VARCHAR(255) NOT NULL UNIQUE,
                        created_at TIMESTAMPTZ DEFAULT Now(),
                        updated_at TIMESTAMPTZ DEFAULT Now(),
                        verified BOOL DEFAULT 'f',
                        address VARCHAR(255),
                        remarks TEXT
                    );
                    '''
    teller_table = '''
                    CREATE TABLE tellers (
                        id SERIAL PRIMARY KEY,
                        teller_id VARCHAR(255) NOT NULL UNIQUE,
                        password VARCHAR(1000) NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT Now(),
                        updated_at TIMESTAMPTZ DEFAULT Now(),
                        access_token VARCHAR(1000) UNIQUE,
                        expiry_date TIMESTAMPTZ DEFAULT Now() + INTERVAL '30 days',
                        verified BOOL DEFAULT 'f',
                        activate BOOL DEFAULT 'f',
                        teller_cash_account VARCHAR(400) NOT NULL,
                        branch_id integer NOT NULL,
                        FOREIGN KEY (branch_id) REFERENCES branches (id) ON UPDATE CASCADE ON DELETE RESTRICT
                    );
                    '''
    teller_role_table = '''
                        CREATE TABLE teller_role (
                            teller_id integer NOT NULL,
                            role_id integer NOT NULL, 
                            created_at TIMESTAMPTZ DEFAULT Now(),
                            updated_at TIMESTAMPTZ DEFAULT Now(),
                            PRIMARY KEY (teller_id, role_id),
                            CONSTRAINT teller_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES roles(id) ON UPDATE CASCADE ON DELETE RESTRICT,
                            CONSTRAINT teller_role_teller_id_fkey FOREIGN KEY (teller_id) REFERENCES tellers (id) ON UPDATE CASCADE ON DELETE RESTRICT
                        );
                        '''
    deposit_table = '''
                        CREATE TABLE deposits (
                            id SERIAL PRIMARY KEY,
                            cvs_tranid VARCHAR (500),
                            transaction_approved BOOL DEFAULT 'f',
                            teller_cash_account VARCHAR (500) NOT NULL, 
                            created_at TIMESTAMPTZ DEFAULT Now(),
                            updated_at TIMESTAMPTZ DEFAULT Now(),
                            transcation_timestamp TIMESTAMPTZ,
                            deposit_amount VARCHAR (50),
                            customer_name VARCHAR (100),
                            deposit_account_num VARCHAR (300) NOT NULL,
                            branch_id integer NOT NULL,
                            teller_id integer NOT NULL,
                            FOREIGN KEY (branch_id) REFERENCES branches (id) ON UPDATE CASCADE ON DELETE RESTRICT,
                            FOREIGN KEY (teller_id) REFERENCES tellers (id) ON UPDATE CASCADE ON DELETE RESTRICT
                        );
                        '''
    denomination_table = '''
                            CREATE TABLE denominations (
                                id SERIAL PRIMARY KEY, 
                                denomination_unit VARCHAR (50) NOT NULL UNIQUE,
                                remarks VARCHAR 
                            );
                            '''
    return (role_table,  branch_table, teller_table, teller_role_table, deposit_table, denomination_table)

def createdb(host, port, user, password, database):
    conn = None
    try:
        conn = psycopg2.connect(database=database,
                                 user=user, 
                                 password=password, 
                                 host=host, 
                                 port=port)
        cur = conn.cursor()
        for command in table_commands():
            cur.execute(command)
        #close the cursoe
        cur.close()
        #commit the changes
        conn.commit()
        #close the connection
        conn.close()
        print('Tables successfully created')
    except (Exception, psycopg2.DatabaseError) as e:

        print(e)
    finally:
        if conn is not None:
            conn.close()
    

    
   

if __name__ == '__main__':
    host = 'localhost'
    port = '5432'
    user = 'user'
    password = 'postgres'
    database = 'testdb2'
    create_db(host, port, user, password, database)
