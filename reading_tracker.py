import os

PROMPT = "tracker > "
TOKENS = ['q']

if __name__ == "__main__":
    os.system('clear')
    while(1):
        print(PROMPT, end='')
        message = input()
        if message not in TOKENS:
            print("Command not found")
        if message == 'q':
            exit()
    
