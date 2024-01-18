#!/usr/bin/python3

import database, subprocess

subprocess.call("clear", shell=True)
print("Welcome to our database app !!\n")

while True:
    x = input("-> add, delete, list, exit: ").lower()
    if x == "add":
        database.db_add()
    elif x == "delete":
        database.db_del()
    elif x == "list":
        database.db_list()
    elif x == "exit":
        print("Exiting...")
        exit(0)