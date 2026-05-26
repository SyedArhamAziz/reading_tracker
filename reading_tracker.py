import os
import re
import sqlite3
import readline
import signal

def exit_signals(signum, sigframe):
    print("\n\nexiting...")
    quit()

signal.signal(signal.SIGINT, exit_signals)
signal.signal(signal.SIGTERM, exit_signals)

PROMPT = "tracker > "
BUILTINS = ['quit', 'help', 'add-book', 'clear', 'list-books']
BOOK_PROPS = ['title', 'author']

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

def quit(*args):
    if len(args) != 0:
        print('error: \'quit\' does not take any arguments')
        return
    CONN.close()
    exit()

def clear(*args):
    if len(args) != 0:
        print('error: \'clear\' does not take any arguments')
        return
    os.system('clear')

def help(*args):
    if len(args) != 0:
        print('error: \'help\' does not take any arguments')
        return
    print(
'''
add-book: add a book
clear: clear the terminal
help: prints out list of commands
list-books: lists out the added books and their authors
q: quit
''')

def add_book(*args):
    if len(args) == 0:
        title = input('title: ')
        author = input('author: ')

        confirmation = input(f'is this information correct? (y/N)\ntitle: {title}\nauthor: {author}\n')
        if confirmation.lower != 'y':
            print('book not added')
            return

        CUR.execute(
        '''
        INSERT INTO books VALUES
            (NULL, ?, ?)
        ''', (title, author)
        )
        CONN.commit()

    for arg in args:
        print(arg)

def list_books():
    res = CUR.execute("SELECT title, author FROM books") 
    num = 0
    books = res.fetchall()
    for book in books:
        print(f'{num}: "{book[0]}" by {book[1]}')
        book = res.fetchone()
        num += 1

if __name__ == "__main__":
    while(1):
        message = input(PROMPT)
        
        #tokenize input
        message = message.strip()
        tokens = re.split(r'[ \n\r\t]+', message)
        if tokens[0] == '':
            continue
        if tokens[0] not in BUILTINS:
            print(f"{tokens[0]}: command not found")
    
        match tokens[0]:
            case 'quit':
                quit(*tokens[1:])
            case 'help':
                help(*tokens[1:])
            case 'add-book':
                add_book(*tokens[1:])
            case 'clear':
                clear(*tokens[1:])
            case 'list-books':
                list_books()

