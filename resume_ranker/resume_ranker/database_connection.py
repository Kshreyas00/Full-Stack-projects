import MySQLdb

# Connect to the MySQL server
db = MySQLdb.connect(host="localhost", user="root", passwd="your_password", db="resume_ranker")

# Create a cursor object using the cursor() method
cursor = db.cursor()

# Execute an SQL query
cursor.execute("SELECT * FROM your_table_name")  # Replace with your actual table name

# Fetch all the rows
rows = cursor.fetchall()

# Loop through the rows and print them
for row in rows:
    print(row)

# Close the database connection
db.close()
