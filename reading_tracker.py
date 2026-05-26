import os
import re
import sqlite3

CONN = sqlite3.connect("books.db")
CURSOR = CONN.cursor()
CURSOR.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    status TEXT
                                )
               '''
)


PROMPT = "tracker > "
BUILTINS = ['q', 'help', 'add-book', 'clear']

def quit():
    exit()

def help():
    print(
'''clear: clear the terminal
help: prints out list of commands
q: quit''')

def add_book():
    name = input('name: ')
    author = input('author: ')
    publish_date = input('publish_date: ')
    page_number = input('number of pages: ')

if __name__ == "__main__":
    while(1):
        print(PROMPT, end='')
        message = input()
        
        #tokenize input
        message = message.strip()
        tokens = re.split(' \n\r\t', message)
        if tokens[0] == '':
            continue
        if message not in BUILTINS:
            print(f"{tokens[0]}: Command not found")
    
        match tokens[0]:
            case 'q':
                quit()
            case 'help':
                help()
            case 'add-book':
                add_book()
            case 'clear':
                os.system('clear')

