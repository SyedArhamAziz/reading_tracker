import os
import re
import sqlite3
import readline
import signal
import subprocess

def exit_signals(signum, sigframe):
    print("\n\nexiting...")
    quit()

signal.signal(signal.SIGINT, exit_signals)
signal.signal(signal.SIGTERM, exit_signals)

PROMPT = "tracker > "
BUILTINS = ['quit', 'help', 'add-book', 'clear', 'list-books', 'remove-books']
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
'''add-book: add a book
clear: clear the terminal
edit-books: edit books
help: prints out list of commands
list-books: lists out the added books and their authors
remove-books: removes book(s)
quit: exit the program''')

def add_book(*args):
    title = ''
    author = ''
    if len(args) == 0:
        title = input('title: ')
        author = input('author: ')

    else: 
        i = 0
        while i < len(args):
            if args[i][0] != '-' or args[i][1:] not in BOOK_PROPS:
                print(f'error: \'{args[i]}\' is not an argument for \'add-book\'')
                return
            if i >= len(args) - 1:
                print(f'error: no argument given for {args[i][1:]}')
                return
            match args[i][1:]:
                case 'title':
                    title = args[i+1]
                case 'author':
                    author = args[i+1]
            i += 2
    if title == '':
        print('error: no title given')
        return

    confirmation = input(f'\nis this information correct? \ntitle: {title}\nauthor: {author}\n(y/N): ')
    if confirmation.strip().lower() != 'y':
        print('book not added')
        return

    CUR.execute(
    '''
    INSERT INTO books VALUES
        (NULL, ?, ?)
    ''', (title, author)
    )
    CONN.commit()
    print('book added successfully')
    return
        
def edit_books(*args):
    ids = []
    if len(args) == 0:
        response = input("no book IDs given, would you like to view a list? (Y/n) ")
        if response.lower() == 'n':
            return
        list_books()
        response = input("enter ID(s) of the book(s) you wish to edit: ")
        if response == '':
            print("error: no ID(s) given")
            return
        ids = response.split(' ')
    else:
        ids = list(args)
    try:
        ids = [int(x) for x in ids]
    except:
        print("error: invalid ID(s) given, make ensure the values are numerical and space-separated")
        return
    for i in ids:
        res = CUR.execute("SELECT title, author FROM books WHERE id=?", (i,))
        book = res.fetchone()
        if book is None:
            print(f"{i} is not a valid id, skipping...")
            continue
        new_title = book[0]
        new_author = book[1]
        response = input(f'edit {book[0]} by {book[1]}? (Y/n): ')
        if response.lower() == 'n':
            continue
        response = input(f'would you like to change the title: {book[0]}? (y/N): ')
        if response.lower() == 'y':
            new_title = input("enter a new title: ")
        response = input(f'would you like to change the author: {book[0]}? (y/N): ')
        if response.lower() == 'y':
            new_author = input("enter a new author: ")
        response = input(f"is the following information correct? (y/N):\ntitle: {new_title}\nauthor: {new_author}\n")
        if response.lower() == 'n':
            print('cancelling...')
            continue
        CUR.execute("UPDATE books SET author = ?, title = ? WHERE id = ?", (new_author, new_title, i))
        CONN.commit()

def list_books():
    res = CUR.execute("SELECT id, title, author FROM books") 
    books = res.fetchall()
    s = ''
    for book in books:
        s += f'{book[0]}, {book[1]}, {book[2]}\n'
        book = res.fetchone()
    result = subprocess.run(
            ["column", '-t', '-N', 'ID, Title, Author', '-s,'],
            input = s,
            text = True,
            capture_output = True
            )
    print(result.stdout)

def remove_books(*args):
    ids = []
    if len(args) == 0:
        response = input("no book IDs given, would you like to view a list? (Y/n) ")
        if response.lower() == 'n':
            return
        list_books()
        response = input("enter ID(s) of the book(s) you wish to remove: ")
        if response == '':
            print("error: no ID(s) given")
            return
        ids = response.split(' ')
    else:
        ids = list(args)
    try:
        ids = [int(x) for x in ids]
    except:
        print("error: invalid ID(s) given, make ensure the values are numerical and space-separated")
    books = []
    for i in ids:
        res = CUR.execute("SELECT title, author FROM books WHERE id=?", (i,))
        book = res.fetchone()
        books.append((book[0], book[1]))
    
    print("Remove the following book(s)?")
    for book in books: print(f"\"{book[0]}\" by {book[1]}")
    confirmation = input('y/N: ')
    if confirmation == 'y':
        for i in ids:
            res = CUR.execute("DELETE FROM books WHERE id=?", (i,))
            res.fetchone()
        CONN.commit()
        print('book(s) removed successfully')
        return
    print('book(s) not removed')

if __name__ == "__main__":
    while(1):
        message = input(PROMPT)
        
        message = message.strip()
        tokens = re.split(r'[ \n\r\t]+', message)

        match tokens[0]:
            case '':
                continue
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
            case 'remove-books':
                remove_books(*tokens[1:])
            case 'edit-books':
                edit_books(*tokens[1:])
            case _:
                print(f"{tokens[0]}: command not found")
                print("enter 'help' to view commands")

