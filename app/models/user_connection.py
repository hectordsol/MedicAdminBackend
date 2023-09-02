import psycopg2
#Clase que maneja CRUD de la tabla de usuarios en la base de datos PostgreSQL en ElephantSQL
class UserConnection():
    conn = None

    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname=fdpkijde user=fdpkijde password=BSaXT5TQ8uOvLYRRTQnCCqrH8c8-bDzQ host=rosie.db.elephantsql.com")
        except psycopg2.OperationalError as err:
            print(err)
            self.conn.close()

    def read_all(self,type):
        with self.conn.cursor() as cur:
            cur.execute(""" 
                        SELECT * FROM users WHERE user_type = %s; 
                        """,(type,))
            data =cur.fetchall()
            return data

    def read_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute(""" 
                            SELECT * FROM users WHERE id = %s; 
                            """, (id,))
            data = cur.fetchone()
            return data

    def read_by_email(self, mail):
        with self.conn.cursor() as cur:
            cur.execute(""" 
                            SELECT * FROM users WHERE email = %s LIMIT 1; 
                            """, (mail,))
            data = cur.fetchone()
            return data

    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO "users"(id, first_name, last_name, email, address, city, country, 
                        phone, date_of_birth, gender, password, specialty, health_insurance, user_type) 
                        VALUES(uuid_generate_v4(), %(first_name)s, %(last_name)s, %(email)s, %(address)s,
                        %(city)s, %(country)s, %(phone)s, %(date_of_birth)s, %(gender)s, %(password)s,
                        %(specialty)s, %(health_insurance)s, %(user_type)s)
                        """,data)
            self.conn.commit()

    def delete_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute(""" 
                            DELETE FROM "users" WHERE id = %s; 
                            """, (id,))
            self.conn.commit()
    
    def update_one(self, data):
        with self.conn.cursor() as cur:
            cur.execute(""" 
                        UPDATE "users" SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s,
                        address = %(address)s, city = %(city)s, country = %(country)s, phone = %(phone)s, date_of_birth = %(date_of_birth)s, 
                        gender = %(gender)s, password = %(password)s, specialty = %(specialty)s, health_insurance = %(health_insurance)s,
                        user_type = %(user_type)s,
                        WHERE id = %(id)s; 
                        """, data)
            self.conn.commit()

    def __def__(self):
        self.conn.close()