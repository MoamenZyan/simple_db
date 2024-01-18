#!/usr/bin/python3
import sqlite3

# Making db file and connect to it
def db_connect(file_name):
    with open(file_name, "a") as file:
        pass
    db = sqlite3.connect(file_name)
    return db

# Making db tables
def mk_table(db):
    cursor = db.cursor()
    cursor.execute("CREATE TABLE if not exists team(t_name TEXT PRIMARY KEY, coach TEXT, city TEXT, captain TEXT, FOREIGN KEY (captain) REFERENCES player(p_name))")
    cursor.execute("CREATE TABLE if not exists player(p_name TEXT PRIMARY KEY, position TEXT, skill_level TEXT, t_name TEXT, FOREIGN KEY (t_name) REFERENCES team(t_name))")
    cursor.execute("CREATE TABLE if not exists game(host_team TEXT, guest_team TEXT, date TEXT, score TEXT, PRIMARY KEY(host_team, guest_team), FOREIGN KEY (host_team) REFERENCES team(t_name), FOREIGN KEY (guest_team) REFERENCES team(t_name))")
    cursor.execute("CREATE TABLE if not exists injury_record(p_name TEXT PRIMARY KEY, description TEXT, FOREIGN KEY (p_name) REFERENCES player(p_name))")

# Saving and closing db
def commit_disconnect(db):
    db.commit()
    db.close()


# Adding records / tubles to db tables
def db_add():
    # connecting to db
    db = db_connect("efl.db")

    # making cursor
    cursor = db.cursor()

    # invoking mk_table method
    mk_table(db)

    # asking user for table to add record to
    x = input("team, player, game, injury_record, exit: ").lower()
    if x == "team":
        while True:
            y = input("- name, coach, city, captain: ").lower().split(" ")

            if y[0] == "exit":
                break
            elif len(y) != 4:
                print("*" * 40)
                print("-- please enter the info in one line seperating by spaces.")
                print("-- Example: AHLY Koller Cairo Shenawy")
                print("-- If you want to exit type: exit")
                print("*" * 40)

            else:
                # Handling error
                try:
                    cursor.execute(f"INSERT INTO {x} (t_name, coach, city, captain) VALUES (?, ?, ?, ?)", (str(y[0]), str(y[1]), str(y[2]), str(y[3])))
                    print(f"-- {x.capitalize()} added successfully")
                except sqlite3.DatabaseError as err:
                    print(f"-- Error when adding {x} !!")
                    print(err)
        # Saving the changes to db
        commit_disconnect(db)

    elif x == "player":
        while True:
            y = input("- name, position, skill_level, t_name: ").lower().split(" ")
            if y[0] == "exit":
                break
            elif len(y) != 4:
                print("*" * 40)
                print("-- please enter the info in one line seperating by spaces.")
                print("-- Example: shenawy goalkeeper high AHLY")
                print("-- If you want to exit type: exit")
                print("*" * 40)
            else:
                # Handling error
                try:
                    cursor.execute(f"INSERT INTO {x} (p_name, position, skill_level, t_name) VALUES (?, ?, ?, ?)", (str(y[0]), str(y[1]), str(y[2]), str(y[3])))
                    print(f"-- {x.capitalize()} added successffully")
                except sqlite3.DatabaseError as err:
                    print(f"-- Error when adding {x} !!")
                    print(err)
        # Saving the changes to db
        commit_disconnect(db)

    elif x == "game":
        while True:
            y = input("- host_team, guest_team, date, score: ").lower().split(" ")
            if y[0] == "exit":
                break
            # Checking info length
            elif len(y) != 4:
                print("*" * 40)
                print("-- please enter the info in one line seperating by spaces.")
                print("-- Example: ahly zamalek 1/7 6-1")
                print("-- If you want to exit type: exit")
                print("*" * 40)
            else:
                # Handling error
                try:
                    cursor.execute(f"INSERT INTO {x} (host_team, guest_team, date, score) VALUES (?, ?, ?, ?)", (str(y[0]), str(y[1]), str(y[2]), str(y[3])))
                    print(f"-- {x.capitalize()} added successffully")
                except sqlite3.DatabaseError as err:
                    print(f"-- Error when adding {x} !!")
                    print(err)
        # Saving the changes to db
        commit_disconnect(db)

    elif x == "injury_record":
        y = input("- player name: ")
        z = input("- description: ")
        # Handling error
        try:
            cursor.execute(f"INSERT INTO {x} (p_name, description) VALUES (?, ?)", (str(y), str(z)))
            print(f"-- {x} added successffully")
        except sqlite3.DatabaseError as err:
            print("*" * 40)
            print(f"-- Error when adding {x} !!")
            print(err)
            print("*" * 40)
        finally:
            # Saving the changes to db
            commit_disconnect(db)
    elif x == "exit":
        # Exiting DB
        print("Exiting DB")
        exit(0)


def db_del():
    # connecting to db
    db = db_connect("efl.db")

    # making cursor
    cursor = db.cursor()

    # asking user for table to delete a record
    x = input("team, player, game, injury, exit: ").lower()
    while True:
        if x == "exit":
            break

        y = input("- key, value: ").lower().split(" ")
        if len(y) != 2:
            print("*" * 40)
            print("-- please enter the info in one line seperating by spaces.")
            print(f"-- Example: delete from {x} where [KEY] = [VALUE]")
            print("-- Type exit to exit.")
            print("*" * 40)
        else:
            # Handling error
            try:
                cursor.execute(f"DELETE FROM {x} WHERE {str(y[0])} = ?", (str(y[1]),))
                print(f"-- {x.capitalize()} deleted successfully")
            except sqlite3.DatabaseError as err:
                print(f"-- Error when deleting {x} !!")
                print(err)
    # Saving the changes to db
    commit_disconnect(db)

def db_list():
    # connecting to db
    db = db_connect("efl.db")

    # making cursor
    cursor = db.cursor()

    # asking user for table to list it's content
    while True:
        tables = ["team", "player", "game", "injury_record"]

        x = input("- team, player, game, injury_record: ").lower()
        if x == "exit":
            break
        elif x not in tables:
            print("*" * 40)
            print("-- Table not found !!")
            print("-- Type exit to exit.")
            print("*" * 40)
        else:
            try:
                cursor.execute(f"SELECT * FROM {x}")
                data = cursor.fetchall()
            except sqlite3.DatabaseError as err:
                print(f"-- Error when listing {x} !!")
                print(err)

        if len(data) == 0:
            print("Table is empty !!")
        else:
            print("*" * 40)
            for i in data:
                print()
                print(' | '.join(i))
            print()
            print("*" * 40)
    # Saving the changes to db
    commit_disconnect(db)