import os
import json
import pika
import pandas as pd

from config.db import SessionLocal
from models import Patient, Hospital


# ==========================
# RABBITMQ CONNECTION
# ==========================

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost"
    )
)

channel = connection.channel()

channel.queue_declare(
    queue="csv_queue",
    durable=True
)


# ==========================
# CALLBACK FUNCTION
# ==========================

def callback(ch, method, properties, body):

    data = json.loads(body)

    file_path = data["file_path"]
    entity = data["entity"].lower()

    print("\n==========================")
    print(f"Received {entity} job")
    print(f"File: {file_path}")
    print("==========================")

    db = SessionLocal()

    try:

        if not os.path.exists(file_path):
            print(f"ERROR: File not found: {file_path}")
            return

        df = pd.read_csv(file_path)

        inserted_count = 0

        # =================================
        # PATIENT CSV
        # =================================

        if entity == "patient":

            required_columns = [
                "name",
                "age",
                "contact_no",
                "height",
                "weight",
                "blood_group"
            ]

            for col in required_columns:
                if col not in df.columns:
                    raise Exception(
                        f"Missing column: {col}"
                    )

            for _, row in df.iterrows():

                existing_patient = db.query(
                    Patient
                ).filter(
                    Patient.name == row["name"],
                    Patient.age == int(row["age"]),
                    Patient.contact_no == str(
                        row["contact_no"]
                    )
                ).first()

                if existing_patient:
                    continue

                patient = Patient(
                    name=row["name"],
                    age=int(row["age"]),
                    contact_no=str(
                        row["contact_no"]
                    ),
                    height=float(
                        row["height"]
                    ),
                    weight=float(
                        row["weight"]
                    ),
                    blood_group=row[
                        "blood_group"
                    ]
                )

                db.add(patient)

                inserted_count += 1

        # =================================
        # HOSPITAL CSV
        # =================================

        elif entity == "hospital":

            required_columns = [
                "name",
                "city"
            ]

            for col in required_columns:
                if col not in df.columns:
                    raise Exception(
                        f"Missing column: {col}"
                    )

            for _, row in df.iterrows():

                hospital_name = str(
                    row["name"]
                ).strip()

                hospital_city = str(
                    row["city"]
                ).strip()

                existing_hospital = db.query(
                    Hospital
                ).filter(
                    Hospital.name.ilike(
                        hospital_name
                    ),
                    Hospital.city.ilike(
                        hospital_city
                    )
                ).first()

                if existing_hospital:
                    continue

                hospital = Hospital(
                    name=hospital_name,
                    city=hospital_city
                )

                db.add(hospital)

                inserted_count += 1

        else:
            raise Exception(
                "Invalid entity type"
            )

        db.commit()

        print(
            f"SUCCESS: {inserted_count} "
            f"{entity} records inserted."
        )

        # Delete file after processing

        if os.path.exists(file_path):
            os.remove(file_path)
            print(
                f"Deleted file: {file_path}"
            )

    except Exception as e:

        db.rollback()

        print("ERROR:", str(e))

    finally:

        db.close()

        # Tell RabbitMQ job completed
        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )


# ==========================
# START CONSUMER
# ==========================

channel.basic_consume(
    queue="csv_queue",
    on_message_callback=callback,
    auto_ack=False
)

print("Waiting for CSV jobs...")

channel.start_consuming()