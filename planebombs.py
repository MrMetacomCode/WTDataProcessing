import csv
import os
import sqlite3

conn = sqlite3.connect('PlaneOrdnances.db')
c = conn.cursor()


def create_table_if_not_exist(table):
    # One-time script for creating the table.
    with conn:
        try:
            c.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name={table} ''')
        except sqlite3.OperationalError:
            c.execute(f"""CREATE TABLE {table} (
                        PlaneName text,
                        Ordnance text
                        )""")


def insert_ordnance(country, plane_name, ordnance):
    with conn:
        c.execute(f"INSERT INTO {country} VALUES (?, ?)", (plane_name, ordnance))


directory = 'Plane Ordnances by Country CSV Files'
for filename in os.listdir(directory):
    country = filename.split(".")[0]
    create_table_if_not_exist(country)
    file = os.path.join(directory, filename)
    with open(file, 'r') as csv_file:
        country_planes = csv.reader(csv_file)

        for line in country_planes:
            if line[0] != "":
                plane_name = line[0]
                plane_ordnances = line[1:]
                if "None" in plane_ordnances:
                    insert_ordnance(country, plane_name, "None")
                else:
                    for ordnance in plane_ordnances:
                        if ordnance != "":
                            insert_ordnance(country, plane_name, ordnance)

conn.commit()
conn.close()
