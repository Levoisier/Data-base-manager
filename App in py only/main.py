import sys
import os
import csv

CLIENT_TABLE = '.clients.csv'
CLIENT_SCHEMA = ['name', 'company', 'email', 'position']
clients = []


def _initialize_clients_from_storage():
    with open (CLIENT_TABLE, mode='r') as f:
        reader = csv.DictReader(f, fieldnames=CLIENT_SCHEMA)
        
        for row in reader:
            clients.append(row)


def _save_clients_to_storage():
    tmp_table_name = '{}.tmp'.format(CLIENT_TABLE)
    with open(tmp_table_name, mode = 'w') as f:
        writer = csv.DictWriter(f, fieldnames=CLIENT_SCHEMA)
        writer.writerows(clients)

    os.remove(CLIENT_TABLE)
    os.rename(tmp_table_name, CLIENT_TABLE)


def create_client(client):
    global clients

    if client not in clients:
        clients.append(client)
    else:
        print('>>> Client is already listed <<<')

def list_clients():
    print('')    
    print('List of clients: ')
    print('-' * 80)
    print('ID | Name | Company | Email | Position ')
    
    for index, client in enumerate(clients):
        print('{id} | {name} | {company} | {email} | {position}'.format(
            id=index,
            name=client['name'],
            company=client['company'],
            email=client['email'],
            position=client['position']))


def update_client(client_id, updated_client):
    global clients
    
    clients[client_id] = updated_client
    print('>>> Client updated succesfully <<<')    


def delete_client(client_id):
    
    global clients

    for index, client in enumerate(clients):
        if index == client_id:
            print('>>> Client found... <<<')
            confirmation()
            del clients[index]
            print('>>> Client deleted succesfully <<<')
            break
        

def search_client(client_name):
    for client in clients:
        if client['name'] != client_name:
            continue
        else: 
            return True


def confirmation():
    while True:
        response = input("Do you want to continue? (yes/no) ")
        if response.lower() == "yes":
            break
        elif response.lower() == "no":
            print("Reestarting program...")
            sys.exit(0)
        else:
            print("Invalid response. Please type 'yes' or 'no'.")


def _print_welcome():
    print('-'*33)
    print('>>> Welcome to Sellish Sales <<<')
    print('-' * 33)
    print('')
    print('[C]reate client')
    print('[L]ist of clients')
    print('[U]pdate client')
    print('[D]elete client')
    print('[S]earch client')
    print('[E]xit')
    print('')

def _get_client_field(field_name):
        field = None

        while not field:
            field = input(f'What\'s the client {field_name}? ')
            
        return field


def _get_client_from_user():
    print('>>> Please fill down below the client information <<<')
    client = {
        'name': _get_client_field('name').title().replace(' ',''),
        'company': _get_client_field('company').title().replace(' ',''),
        'email': _get_client_field('email'),
        'position': _get_client_field('position').title().replace(' ',''),
    }

    return client


if __name__=='__main__':
    _initialize_clients_from_storage()
    _print_welcome()
    
    command = None

    while command != 'C' or command != 'L' or command != 'D' or command != 'U' or command != 'S':

        command = input('What\'d you like to do?: ')
        command = command.upper()

        if command == 'C':
            client = _get_client_from_user()

            create_client(client)
        elif command == 'L':
            list_clients()
        elif command == 'D':
            client_id = int(_get_client_field('id'))
            delete_client(client_id)
        elif command == 'U':
            client_id = int(_get_client_field('id'))  
            if len(clients) - 1 >= client_id:
                print('>>> Client found... <<<')
                confirmation()
                updated_client = _get_client_from_user()
                update_client(client_id, updated_client)
            else:
                print('>>> Client is not in clients list <<<')
        elif command == 'S':
            client_name = _get_client_field('name')
            client_name = client_name.title().replace(' ','')
            print(client_name)
            found = search_client(client_name)

            if found:
                print(f'>>> {client_name} is in the client\'s list. <<<')
            else:
                print(f'>>> {client_name} NOT in our client\'s list. <<<')
        elif command == 'E':
            sys.exit()
        else:
            print('Invalid command')
        

        _save_clients_to_storage()

