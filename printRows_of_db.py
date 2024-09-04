import sqlite3
import sys

#Usage: 0 is the column number.
# python3 printRows_of_db.py project_repo_mapping.db 0

def print_column_values(db_file, column_number):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Query to select all columns from the project_repo table
        c.execute('SELECT * FROM project_repo')
        
        # Fetch all rows
        rows = c.fetchall()

        # Print the values of the specified column
        for row in rows:
            if len(row) > column_number:
                print(row[column_number])
            else:
                print(f"Row does not have column {column_number}")
        
        # Close the database connection
        conn.close()

    except sqlite3.Error as e:
        print(f"Error while connecting to database: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <db_file> <column_number>")
        sys.exit(1)

    db_file = sys.argv[1]
    try:
        column_number = int(sys.argv[2])
    except ValueError:
        print("Column number must be an integer.")
        sys.exit(1)

    print_column_values(db_file, column_number)

if __name__ == '__main__':
    main()
