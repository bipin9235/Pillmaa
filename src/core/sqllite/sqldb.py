import sqlite3
import pandas as pd

# df = pd.read_csv("default_config_data/pharmaceutical_database.csv")

# Connect to SQLite database (creates pharma.db if not exists)
conn = sqlite3.connect("pharma.db")

# Save DataFrame to SQLite
# df.to_sql("drugs", conn, if_exists="replace", index=False)

# Example query
cursor = conn.cursor()
cursor.execute("SELECT * FROM drugs limit 5")
#cursor.execute("SELECT name, manufacturer FROM drugs WHERE price < 50")
for row in cursor.fetchall():
    print(row)


conn.close()

