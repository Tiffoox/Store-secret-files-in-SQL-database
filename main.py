import sqlite3
import cv2
import base64
import re
class SecretFileProgram():
    def __init__(self):
        self.not_the_end = True
        self.on_start()

    def on_start(self):
        secret_password = '123456'
        user_password = input("Enter your database password")
        while secret_password != user_password:
            print("Invalid password")
            user_password = input("Enter your database password")

        self.conn = sqlite3.connect('my_secret_database.db')
        self.c = self.conn.cursor()

        try:
            # Create table if it doesn't exist
            self.c.execute('''
            CREATE TABLE my_secret_database
            (FullName TEXT primary key,
             FileName TEXT,
             FileType TEXT, 
             FileString TEXT)
                         ''')

            print("Table created")
        except Exception as e:
            print("Table already exists")

        self.user_program()
    def user_program(self):
        stars = "*" * 50
        while self.not_the_end:
            choice = input(f"""
{stars}
Write quit if you want to quit the program
{stars}
Write open if you want to open an existing image
{stars}
Write store if you want to store a new image
{stars}
                    """)
            if choice == 'quit':
                self.quit_the_program()
            elif choice == 'open':
                self.open_new_file()
            elif choice == 'store':
                self.store_new_file()
            else:
                print(f"{choice} is not a good command, Try again :")
        self.save_and_close_the_database()

    def open_new_file(self):
        user_file_format = input("What is the type of the file \n")
        user_file_name = input("What is the name of the file ?\n")
        full_name = user_file_name + '.' + user_file_format
        try:
            self.c.execute(f"""
            SELECT * FROM my_secret_database 
            WHERE (FullName = {'"' + full_name + '"'})
            """)
            file_from_database = self.c.fetchone()

            try:
                with open(f"{file_from_database[0]}", "wb") as f:
                    f.write(base64.b64decode(file_from_database[3]))
                print("File successfully created in the directory")
            except Exception as e:
                print("An error has occured")
        except Exception as e:
            print("This file is not in the database. ")


    def quit_the_program(self):
        print("Program closed")
        self.not_the_end = False
    def store_new_file(self):
        path = input(r"""What is the name of your file ? 
Specify the path of the file. 
Ex: C:\Users\Quentin Dijkstra\Documents\Python Projects\Store-secret-files-in-SQL-database\485311.png
                """)
        try:
            user_file = re.split(r'[\\]', path)[-1]
            user_file_name = user_file.split(".")[0]
            user_file_type = user_file.split(".")[1]

            try:
                if user_file_type == 'png' or user_file_type == 'jpg' or user_file_type == 'jpeg':
                    IMAGE = cv2.imread(path)
                    file_string = base64.b64encode(cv2.imencode(f'.{user_file_type}', IMAGE)[1]).decode()

                elif user_file_type == 'txt' or user_file_type == 'py':
                    with open(path, "r") as f:
                        file_string = f.read()
                        file_string = base64.b64encode(bytes(file_string, encoding="ascii"))
                        file_string = file_string.decode("utf-8")

                else:
                    print("Incorrect type")

                try:
                    # Insert a row of data

                    self.c.execute(f"""
                    INSERT INTO my_secret_database VALUES ('{user_file}','{user_file_name}','{user_file_type}', '{file_string}')
                    """)
                    self.conn.commit()
                    # # Save (commit) the changes
                    print("File successfully added to the database")
                except Exception as e:
                    print("Image with the same name already exists in the database")

            except Exception as e:
                print("File not found, Try again: ")
        except Exception as e:
            print("Invalid Format")

    def save_and_close_the_database(self):
        self.conn.commit()
        # # Save (commit) the changes

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.conn.close()


if __name__ == '__main__':
    SecretFileProgram()
