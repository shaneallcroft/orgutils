import os
import argparse
import discord
from orgUtils import SAPOFTO
from mysql.connector import connect, Error



def connectDb(user, host, pswd):
        connection = connect(user=user,
                             host=host,
                             password=pswd,
                             auth_plugin='mysql_native_password',
                             database='wctcg_bot')
        print(connection)
        return connection

def commitOrg(connection, table, server='wctcg_bot'):
    cursor = connection.cursor(dictionary=True)
    
    if not server == 'wctcg_bot':
        use_query = 'USE server_' + str(args.server)
    else:
        use_query = 'USE ' + str(server)
    cursor.execute(use_query)
    cursor.fetchall()
    if table.endswith('.org'):
        table = table[:-4]
    # drop the table so it can be resourced from the org file
    drop_query = 'DROP TABLE IF EXISTS ' + table
    cursor.execute(drop_query)
    cursor.fetchall()
    print('successfully dropped ' + table)
    desc_dict = {}
    with open('orgTables/' + table + '.org') as f:
        lines = f.readlines()
        
    count = len(lines)
    i = 0
    while not lines[i].startswith('* TABLE DESCRIPTION'):
        # find description
        i += 1
    # create table
    creation_query = 'CREATE TABLE '
    while not lines[i+1].startswith('* '):
        i += 1
        line = lines[i]
        creation_query += line
        line = line.split(' ')
        if line[1].endswith(','):
            desc_dict[line[0]] = line[1][:-1]
        else:
            desc_dict[line[0]] = line[1]
        print(line)
    cursor.execute(creation_query)
    cursor.fetchall()
    print('successfully created ' + table)
    connection.commit()
    while i < count:
        i += 1
        line = lines[i]
        if line.startswith('** '):
            # individual table item
            query_dict = {}
            item_name = line[3:]
            while not (i + 1) >= count and lines[i+1].startswith('*** '):
            # while the next item or end of file hasn't been reached
                i += 1
                line = lines[i]
                if not line.startswith('*** '):
                    print('error, you shouldnt be seeing this, line value:')
                    print(line, '\n')
                
                column_name = line[4:]
                column_value = ''
                if column_name.endswith('\n'):
                    column_name = column_name[:-1]

                if lines[i+1].startswith('** '):
                    print('warning, no value provided for ', column_name, ' in ', item_name)
                    break
                    
                if lines[i+1].startswith('*** '):
                    print('warning, no value provided for ', column_name, ' in ', item_name)
                    continue
                while i < count - 1 and not lines[i+1].startswith('*** ') and not lines[i+1].startswith('** '):
                    i += 1
                    column_value += lines[i].strip() # should contain value now
                                
                if column_value.endswith('\n'):
                    column_value = column_value[:-1]


                # get rid of trailing new lines for column name and value
                query_dict[column_name] = column_value
                

                
        
            # build and execute query based on the dict
            query = 'INSERT INTO ' + table
            column_string = '('
            value_string = '('
            for column_name in query_dict.keys():                
                column_string += column_name + ', '
                if not 'int' in desc_dict[column_name]:
                    value_string += '"' + query_dict[column_name] + '", '
                else:
                    value_string += query_dict[column_name] + ', '
            column_string = column_string[:-2]
            value_string = value_string[:-2]
            column_string += ')'
            value_string += ')'
            query += ' ' + column_string + ' VALUES ' + value_string
            print(query, '\n\n')
            cursor.execute(query)
            cursor.fetchall()
            connection.commit()
            
            if i >= count - 1:
                return




def orgDirectoryToSql(connection, table, directory_path='databaseTableOrgs/', server='wctcg_bot'):
    cursor = connection.cursor(dictionary=True)
    
    if not server == 'wctcg_bot':
        use_query = 'USE server_' + str(args.server)
    else:
        use_query = 'USE ' + str(server)
    cursor.execute(use_query)
    cursor.fetchall()
    if table.endswith('.org'):
        table = table[:-4]
    # drop the table so it can be resourced from the org file
    drop_query = 'DROP TABLE IF EXISTS ' + table
    cursor.execute(drop_query)
    cursor.fetchall()
    print('successfully dropped ' + table)
    
    table_desc_node = SAPOFTO(key=table,filename=(directory_path + table + '/' + table.upper() + '_DEFINITION.org'))
    print('ah1')
    creation_query = 'CREATE TABLE ' + table + ' ('
    specification_string = ''
    for child_node in table_desc_node.getContentOrdered():
        print(child_node.getHeadKey(), child_node.tags)
        if 'primary key' in child_node['TYPE'].tags:
            # PRIMARY KEY SPECIFICATION TO BE ADDED AT THE END
            print('primary key specified')
            specification_string += 'primary key(' + child_node.getHeadKey() + ')'
        creation_query += child_node.getHeadKey().lower() + ' '
        creation_query += child_node['TYPE'].getValue() + ',\n'
    creation_query += specification_string + ')'
    print(creation_query)
    print('ah2')
    cursor.execute(creation_query)
    cursor.fetchall()
    print('successfully created ' + table)
    connection.commit()
    
    for row_file in os.listdir(directory_path + table):
        if not row_file.endswith('.org') or row_file == table.upper() + '_DEFINITION.org':
            continue

        row_node = SAPOFTO(key=row_file,filename=os.path.join(directory_path,table,row_file))
        # build and execute query based on the dict        
        query = 'INSERT INTO ' + table
        column_string = '('
        value_string = '('
        for child_node in table_desc_node.getContentOrdered():
            path_list = child_node['ROW ORG KEY PATH'].getValue().split(',')
            column_value_in_row = None
            i = 0
            found_node = row_node
            print('path_list: ',path_list)
            while i < len(path_list) and path_list[i] in found_node.keys():
                found_node = found_node[path_list[i]]
                i += 1
            if i != len(path_list):
                print('missing ', child_node.getHeadKey())
                print('got up to ',found_node.getHeadKey())
                print('found node keys: ', found_node.keys(), '\n')
                continue
            column_string += child_node.getHeadKey() + ', '
            if 'int' in child_node['TYPE'].getValue():
                value_string += found_node.getValue() + ', '
            else:
                value_string += '"' + found_node.getValue().replace('"', '\\"') + '", '

        column_string = column_string[:-2]
        value_string = value_string[:-2]
        column_string += ')'
        value_string += ')'
        query += ' ' + column_string + ' VALUES ' + value_string
        print(query, '\n\n')
        cursor.execute(query)
        cursor.fetchall()
        connection.commit()
                
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--row_directory', default='databaseTableOrgs/') # row directory option specifies a directory for which all files ending in .org
                                           # is a file containing all the information for a single row
    parser.add_argument('--table')
    parser.add_argument('--server', default='wctcg_bot')
    args = parser.parse_args()
    connection = connectDb(args.user, 'localhost', args.password)
    orgDirectoryToSql(connection, args.table, args.row_directory, args.server)
