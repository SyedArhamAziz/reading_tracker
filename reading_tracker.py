import os
import re
import sqlite3
import readline

CONN = sqlite3.connect("books.db")
CUR = CONN.cursor()
CUR.execute(
'''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT
    )
'''
)

PROMPT = "tracker > "
BUILTINS = ['q', 'help', 'add-book', 'clear', 'list-books']

def quit():
    CONN.close()
    exit()

def help():
    print(
'''
add-book: add a book
clear: clear the terminal
help: prints out list of commands
list-books: lists out the added books and their authors
q: quit
''')

def add_book():
    title = input('title: ')
    author = input('author: ')

    CUR.execute(
    '''
    INSERT INTO books VALUES
        (NULL, ?, ?)
    ''', (title, author)
    )
    CONN.commit()

def list_books():
    res = CUR.execute("SELECT title, author FROM books") 
    num = 0
    book = res.fetchone()
    while book is not None:
        print(f'{num}: {book[0]} by {book[1]}')
        book = res.fetchone()

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
            case 'list-books':
                list_books()

