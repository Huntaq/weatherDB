import os
import sqlite3
import pandas as pd

def create_table_from_csv(cursor, table_name, csv_file):
    df = pd.read_csv(csv_file)
    columns = df.columns.tolist()
    
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    create_table_query += ", ".join([f"{col.replace(' ', '_').replace('(', '').replace(')', '').replace('%', 'Pct').replace('/', '_per_')} TEXT" for col in columns])
    create_table_query += ");"
    
    cursor.execute(create_table_query)
    
    for _, row in df.iterrows():
        insert_query = f"INSERT INTO {table_name} VALUES ("
        insert_query += ", ".join(["?" for _ in columns])
        insert_query += ");"
        cursor.execute(insert_query, tuple(row))

def main():
    data_folder = 'data'
    db_file = 'weather_data.db'
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    for file_name in os.listdir(data_folder):
        if file_name.endswith('.csv'):
            if file_name == 'cords.csv':
                table_name = 'coordinates'
            else:
                date_str = file_name.split('_')[-1].split('.')[0].replace('-', '_')
                table_name = f"weather_data_{date_str}"
                
            csv_file = os.path.join(data_folder, file_name)
            create_table_from_csv(cursor, table_name, csv_file)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
