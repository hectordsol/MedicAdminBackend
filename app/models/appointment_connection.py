# from app.models.database_connection import DatabaseConnection
import psycopg2
#Clase que maneja CRUD de la tabla de Appointments en la base de datos PostgreSQL en ElephantSQL
class AppointmentConnection:
    conn = None

    def __init__(self, donde:str = "--"):
        print("iniciando?",donde)
        try:
            self.conn = psycopg2.connect("dbname=fdpkijde user=fdpkijde password=BSaXT5TQ8uOvLYRRTQnCCqrH8c8-bDzQ host=rosie.db.elephantsql.com")
        except psycopg2.OperationalError as err:
            print(err)
            self.conn.close()

    def read_all(self):
        with self.conn.cursor() as cur:
            cur.execute(""" 
                        SELECT 
                            ma.id AS appointment_id,
                            ma.start_datetime,
                            ma.end_datetime,
                            ma.diagnosis,
                            ma.prescription,
                            ma.id_patient,
                            ma.id_doctor,
                            ma.patient_first_name,
                            ma.patient_last_name,
                            ud.first_name AS doctor_first_name,
                            ud.last_name AS doctor_last_name,
                            ma.state
                        FROM 
                            medical_appointment ma
                        LEFT JOIN
                            users ud ON ma.id_doctor = ud.id;  
                        """)
            data =cur.fetchall()
            return data

    def read_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT
                        ma.start_datetime,
                        ma.end_datetime,
                        ma.diagnosis,
                        ma.prescription,
                        ma.state,
                        ma.id_patient,
                        p.first_name AS patient_first_name,
                        p.last_name AS patient_last_name,
                        ma.id_doctor,
                        d.first_name AS doctor_first_name,
                        d.last_name AS doctor_last_name
                        FROM medical_appointment ma
                        JOIN users p ON ma.id_patient = p.id
                        JOIN users d ON ma.id_doctor = d.id
                        WHERE ma.id = %s
                        """, ( id,))
            # data = cur.fetchall()
            data = cur.fetchone()
            return data
            # cur.execute(""" 
            #                 SELECT * FROM medical_appointment WHERE id = %s; 
            #                 """, (id,))
    def check_repeat(self, id_doctor):
        with self.conn.cursor() as cur:
            cur.execute("""
                            SELECT
                                ma.id AS appointment_id,
                                ma.start_datetime,
                                ma.end_datetime,
                                ma.diagnosis,
                                ma.prescription,
                                ma.id_patient,
                                ma.id_doctor,
                                u.first_name AS doctor_first_name,
                                u.last_name AS doctor_last_name
                            FROM
                                medical_appointment ma
                            INNER JOIN
                                users u ON ma.id_doctor = u.id
                            WHERE
                                ma.id_doctor = %s
                                AND NOT EXISTS (
                                    SELECT 1
                                    FROM medical_appointment sub_ma
                                    WHERE
                                        sub_ma.id_doctor = ma.id_doctor
                                        AND sub_ma.id != ma.id
                                        AND (
                                            (ma.start_datetime BETWEEN sub_ma.start_datetime AND sub_ma.end_datetime)
                                            OR (ma.end_datetime BETWEEN sub_ma.start_datetime AND sub_ma.end_datetime)
                                        )
                                );
                            """, (id_doctor,))
            data = cur.fetchone()
            return data

    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO "medical_appointment"(id, start_datetime, end_datetime, diagnosis,
                        prescription, id_patient, patient_first_name, patient_last_name, id_doctor, state)
                        VALUES(uuid_generate_v4(), %(start_datetime)s, %(end_datetime)s, %(diagnosis)s,
                        %(prescription)s, %(id_patient)s, %(patient_first_name)s, %(patient_last_name)s,
                        %(id_doctor)s, %(state)s)
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
                        diagnosis = %(diagnosis)s, prescription = %(prescription)s, patient_first_name = %(patient_first_name)s,
                        patient_last_name = %(patient_last_name)s, id_patient = %(id_patient)s, id_doctor = %(id_doctor)s, state = %(state)s
                        WHERE id = %(id)s; 
                        """, data)
            self.conn.commit()

    def read_calendar(self, id:str, init:str, end:str):
        # print(id, init, end)
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
                        WHERE ma.id_doctor = %s
                        AND ma.start_datetime >= %s
                        AND ma.start_datetime <= %s
                        """, (id, init, end,))
            data = cur.fetchall()
            print(data)
            return data
#  ma.id_doctor = %s
                        # AND

    def __def__(self):
        self.conn.close()
    def get_connection(self):
        return self.conn
    def close_connection(self,donde:str ="*"):
        print("cerrando: ",donde)
        self.conn.close()
        