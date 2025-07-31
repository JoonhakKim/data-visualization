import sqlite3


a = "example.db"  # your database file

with sqlite3.connect(a) as conn:
    curr = conn.cursor()
    
    b = input("Enter the name of the table: ").strip()
    # You must use string formatting to insert table names
    curr.execute(f"CREATE TABLE IF NOT EXISTS {b} (ticker TEXT)")
    print("Enter tickers one at a time. Type 'done' when finished.")
    while True:
        c = input("Ticker: ").strip()
        if c.lower() == 'done':
            break
        curr.execute(f"INSERT INTO {b} (ticker) VALUES (?)", (c,))
    conn.commit()
    curr.execute(f"SELECT * from {b}")
    f= curr.fetchall()
    print(f)