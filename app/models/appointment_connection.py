from app.models.database_connection import DatabaseConnection
# import psycopg2
#Clase que maneja CRUD de la tabla de Appointments en la base de datos PostgreSQL en ElephantSQL
class AppointmentConnection(DatabaseConnection):
    def __init__(self, db_connection):
        self.conn = db_connection
    # def __init__(self):
    #     try:
    #         self.conn = psycopg2.connect("dbname=fdpkijde user=fdpkijde password=BSaXT5TQ8uOvLYRRTQnCCqrH8c8-bDzQ host=rosie.db.elephantsql.com")
    #     except psycopg2.OperationalError as err:
    #         print(err)
    #         self.conn.close()

    def read_all(self):
        with self.conn.cursor() as cur:
            cur.execute(""" 
                        SELECT * FROM medical_appointment;
                        """)
            data =cur.fetchall()
            return data

    def read_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute(""" 
                            SELECT * FROM medical_appointment WHERE id = %s; 
                            """, (id,))
            data = cur.fetchone()
            return data

    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO "medical_appointment"(id, start_datetime, end_datetime, diagnosis,
                        prescription, id_patient, id_doctor, state)
                        VALUES(uuid_generate_v4(), %(start_datetime)s, %(end_datetime)s, %(diagnosis)s,
                        %(prescription)s, %(id_patient)s, %(id_doctor)s, %(state)s)
                        """,data)
            self.conn.commit()

    def delete_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute("""
                        DELETE FROM "medical_appointment" WHERE id = %s;
                        """, (id,))
            self.conn.commit()
    
    def update_one(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                        UPDATE "medical_appointment" SET start_datetime = %(start_datetime)s, end_datetime = %(end_datetime)s, 
                        diagnosis = %(diagnosis)s, prescription = %(prescription)s, id_patient = %(id_patient)s, 
                        id_doctor = %(id_doctor)s, state = %(state)s
                        WHERE id = %(id)s; 
                        """, data)
            self.conn.commit()

    def read_calendar(self, init:str, end:str, id:str):
        print(id, init, end)
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT ma.id AS appointment_id,
                        ma.start_datetime,
                        ma.end_datetime,
                        ma.state,
                        ma.id_doctor,
                        p.first_name AS patient_first_name,
                        p.last_name AS patient_last_name
                        FROM medical_appointment ma
                        JOIN users p ON ma.id_patient = p.id
                        WHERE ma.start_datetime >= %s
                        AND ma.start_datetime <= %s
                        """, ( init, end,))
            data = cur.fetchall()
            print(data)
            return data
#  ma.id_doctor = %s
                        # AND

    def __def__(self):
        self.conn.close()
        