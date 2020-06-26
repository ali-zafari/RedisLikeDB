import csv
import hashlib
import pickle
from hashtable import HashTable

class Redis:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.loggedin = False
        self.loggedin_username = None
        self.user_temp_data = None
        try:
            with open('password.txt', 'r') as fread:
                reader = csv.reader(fread, delimiter=':')
                users = dict(reader)
                self.usernames = set(users.keys())
                #print(self.usernames)
        except:
            self.usernames = set()

    def command_prompt(self):
        while True:
            if not self.loggedin:
                command = input("Enter 'LOGIN' or 'SIGNUP':")
                if command not in {'LOGIN', 'SIGNUP'}:
                    print('command is not valid!')
                    continue
                else:
                    self.handle_command(command)
            else:
                command, *args = input(f'{self.loggedin_username}# ').split(' ')
                if command not in {'HELP', 'GET', 'SET', 'REMOVE', 'SAVE', 'EXIT'}:
                    print('command is not valid!')
                    continue
                else:
                    self.handle_command(command, args)

    def handle_command(self, command, args = None):
        if command == 'LOGIN':
            self.login()
        elif command == 'SIGNUP':
            self.signup()
        elif command == 'HELP':
            self._help()
        elif command == 'GET':
            self._get(*args)
        elif command == 'SET':
            self._set(*args)
        elif command == 'REMOVE':
            self._remove(*args)
        elif command == 'SAVE':
            self._save()
        elif command == 'EXIT':
            self._exit()

    def _help(self):
        print('''
        GET:\t GETS ELEMENT BY {KEY}
        SET:\t SETS ELEMENT BY {KEY} AND ITS {VALUE}
        REMOVE:\t REMOVES ELEMNT BY {KEY}
        SAVE:\t SAVES USER'S DATA TO FILE
        EXIT:\t EXITS WITH SAVING
        ''')

    def _get(self, key=None):
        try:
            print(self.user_temp_data[key])
        except:
            print('Key not found!')

    def _set(self, key=None, value=None):
        self.user_temp_data[key] = value

    def _remove(self, key=None):
        try:
            self.user_temp_data.remove(key)
        except:
            print('Key not found!')

    def _save(self):
        with open(f'{self.loggedin_username}', 'wb') as fwb:
            pickle.dump(self.user_temp_data, fwb)

    def _exit(self):
        self._save()
        self.loggedin_username = None
        self.loggedin = False
        self.user_temp_data = None

    def verify_user_pass(self):
        username = input('Enter username: ')
        while username in self.usernames:
            username = input('Username already token.\nEnter another one: ')
        password, password_check = 'p', 'pc'
        password = input('Enter password: ')
        while len(password) < 8:
            password = input('Password Length must be at least 8 characters.\nEnter another one: ')
        password_check = input('Enter password again to verify: ')
        while password != password_check:
            password_check = input('Not equal!\nEnter password again to verify: ')
        return (username, password)
    
    def signup(self):
        username, password = self.verify_user_pass()
        self.usernames.add(username)
        with open('password.txt', 'a', newline='') as fappend:
            writer = csv.writer(fappend, delimiter=':')
            writer.writerow([username, hashlib.sha256(password.encode('utf-8')).hexdigest()])
        with open(username, 'wb') as fwrite:
            pickle.dump(HashTable(), fwrite)
    
    def login(self):
        username = input('Enter username: ')
        password = hashlib.sha256(input('Enter password: ').encode('utf-8')).hexdigest()
        with open('password.txt', 'r') as fread:
            reader = csv.reader(fread, delimiter=':')
            users = dict(reader)
        if username not in users:
            print('User not found!')
            return 
        elif users[username] != password:
            print('Wrong password!')
            return
        print(f'Welcome {username}.')
        self.loggedin = True
        self.loggedin_username = username
        with open(f'{self.loggedin_username}', 'rb') as frb:
            self.user_temp_data = pickle.load(frb)


if __name__ == '__main__':
    redis  = Redis()
    redis.command_prompt()