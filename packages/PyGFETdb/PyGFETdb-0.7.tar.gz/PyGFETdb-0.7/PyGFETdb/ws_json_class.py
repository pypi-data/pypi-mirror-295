#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
#
import json
import traceback
import sys
import requests
import base64



class ws_json:
    '''
        Paràmetres: 
            query: Les dades en json que enviarem al servei web
        Retorn: Array amb el resultat:
            'error' => [true|false]
            'errorCode' => Codi de l'error (0) si no hi ha error
            'message' => En cas d'error, el missatge d'error.
                    Si no hi ha error, aquest camp no existeix
            'result' => Resultat de la crida
    '''
    @staticmethod
    def send(WS_ENTRY, query):
        data_string = json.dumps(query)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(WS_ENTRY,
                                 headers=headers,
                                 data=data_string)

        try:
            result = json.loads(response.text)
        except:
            result = {'error': 1,
                      'errorCode': 1,
                      'message': 'Cannot exec json request'}
            return(result)

        try:
            error = result['error']
        except:
            result = {'error': 1,
                      'errorCode': 2,
                      'message': 'malformed answer ...'}

        try:
            result['result'] = ws_json.ws_unpack(result['result'])
        except:
            result['result'] = ''
            try:
                message = result['message']
            except:
                result['message'] = 'unknown error'

        return result

    '''
        Aquesta funció composa l'array amb els paràmetres que enviarem al servei web
        Paràmetres:
            module: El mòdul al que fem referència. Pot set pyfet o pyegnite
            data: La crida sql que volem executar (query)
                            array amb els camps a inserir/actualitzar
            oper: Operacio a realizar
                query -> query arbitrària (select, delete, show tables, ...)
                insert -> INSERT
                update -> UPDATE
        Retorn: El resultat de la crida al servei web
            Array amb el resultat:
            'error' => [true|false]
            'errorCode' => Codi de l'error (0) si no hi ha error
            'message' => En cas d'error, el missatge d'error.
                    Si no hi ha error, aquest camp no existeix
            'result' => Resultat de la crida
    '''
    @staticmethod
    def call(connection, data, oper='query'):
        module = connection['module']
        username = connection['username']
        password = connection['password']
        WS_ENTRY = connection['WS_ENTRY']
        if oper == 'insert':
            for i in data['fields']:
                if (data['fields'][i]['type'] == "bin"):
                    if (type(data['fields'][i]['value']) == str):
                        data['fields'][i]['value'] = base64.b64encode(data['fields'][i]['value'].encode('ascii')).decode()
                    else:
                        data['fields'][i]['value'] = base64.b64encode(data['fields'][i]['value']).decode()
            query = {'username': username,
                     'password': password,
                     'module': module,
                     'oper': 'insert',
                     'table': data['table'],
                     'fields' : data['fields']}
            return ws_json.send(WS_ENTRY, query)

        elif oper == 'update':
            if (type(data['where']) == str):
                data['where'] = base64.b64encode(data['where'].encode('ascii')).decode()
            else:
                data['where'] = base64.b64encode(data['where']).decode()
            for i in data['fields']:
                if (data['fields'][i]['type'] == "bin"):
                    if (type(data['fields'][i]['value']) == str):
                        data['fields'][i]['value'] = base64.b64encode(data['fields'][i]['value'].encode('ascii')).decode()
                    else:
                        data['fields'][i]['value'] = base64.b64encode(data['fields'][i]['value']).decode()
            query = {'username': username,
                     'password': password,
                     'module': module,
                     'oper': 'update',
                     'table': data['table'],
                     'fields': data['fields'],
                     'where': data['where']}
            return ws_json.send(WS_ENTRY, query)

        else:
            if (type(data) == str):
                encoded_data = base64.b64encode(data.encode('ascii')).decode()
            else:
                encoded_data = base64.b64encode(data).decode()
            query = {'username': username,
                     'password': password,
                     'module': module,
                     'oper': 'query',
                     'sql' : encoded_data}            
            return ws_json.send(WS_ENTRY, query)

    '''
        Aquesta funció retorna una llista on cada element es un array (dictionary)
        Si un valor en concret el volem en binary, podem fer bytesarray(valor)
        Si un valor en concret el volem en string, podem fer valor.decode()
        (valor és cada un dels elements de row[j]) ...
        Paràmetres:
            data => llista d'entrada on cada element és un array associatiu amb el valor en b64
        Retorn: La llista amb els valors decodificats. Cada element de l'array que forma cada element de la llista
            es retorna en 'bytes'
    '''
    @staticmethod 
    def ws_unpack(data):
        retVal = list()
        k = 0
        for i in data:
            row = {} 
            keys = i.keys()
            for j in keys:
                row[j] = base64.b64decode(i[j])
            retVal.append(row)
        return(retVal)


if __name__ == "__main__":
    connection = {'WS_ENTRY': 'http://opter6.cnm.es/ws/pyfet/pyfet.php',
                  'module': 'pyfet',
                  'password': '6345HGdfkfmjk',
                  'username': 'py-imb-dbtools'}

    # Insert to Users table works
    # q = {'fields': {0: {'name': 'Name',
    #                     'type': 'str',
    #                     'value': 'TestUser1'}},
    #      'table': 'Users'}
    # oper = 'insert'
    # res = ws_json.call(connection=connection,
    #                    data=q,
    #                    oper=oper)
    # if res['error']:
    #     # print(q)
    #     print('Error in call ', res['errorCode'])
    # else:
    #     print('Good', res)

    # q = {'fields': {0: {'name': 'Data',
    #                     'type': 'bin',
    #                     'value': b'\x80\x04\x95q\x02\x00\x00\x00\x00\x00\x00}\x94(\x8c\x02Ig\x94\x8c\x16numpy._core.multiarray\x94\x8c\x0c_reconstruct\x94\x93\...%\x8c\x08DateTime\x94\x8c\x08datetime\x94\x8c\x08datetime\x94\x93\x94C\n\x07\xe8\x08\x1c\n\x03+\x00\xdf\xc3\x94\x85\x94R\x94u.'},
    #                 1: {'name': 'User_id',
    #                     'type': 'int',
    #                     'value': 58},
    #                 2: {'name': 'MeasDate',
    #                     'type': 'str',
    #                     'value': '2024-08-28 10:03:43.057283'},
    #                 3: {'name': 'UpdateDate',
    #                     'type': 'str',
    #                     'value': '2024-09-10 19:20:12.266279'},
    #                 4: {'name': 'Name',
    #                     'type': 'str',
    #                     'value': 'WF16815-01-Gate'},
    #                 5: {'name': 'FileName',
    #                     'type': 'str',
    #                     'value': 'WF16815--01--DEV1--FS_BareEtOH3min--SO_PBS--PH_7p21--DC--AC--Bode--Cy01'}},
    #     'table': 'Gcharacts'}


    q = {'fields': {
                    0: {'name': 'Name',
                        'type': 'str',
                        'value': 'TestData1'},
                    1: {'name': 'Data',
                        'type': 'bin',
                        'value': b'gghh'},

                    # 1: {'name': 'FileName',
                    #     'type': 'str',
                    #     'value': 'WF16815--01--DEV1--FS_BareEtOH3min--SO_PBS--PH_7p21--DC--AC--Bode--Cy01'}

        # 0: {'name': 'Data',
                    #     'type': 'bin',
                    #     'value': b'gghh'},
                    # 1: {'name': 'User_id',
                    #     'type': 'int',
                    #     'value': 58},
                    2: {'name': 'MeasDate',
                        'type': 'str',
                        'value': '2024-08-28 10:03:43.057283'},
                    3: {'name': 'UpdateDate',
                        'type': 'str',
                        'value': '2024-09-10 19:20:12.266279'},
                    },
        'table': 'Gcharacts'}
    oper = 'insert'
    res = ws_json.call(connection=connection,
                       data=q,
                       oper=oper)
    if res['error']:
        # print(q)
        print('Error in call ', res['errorCode'], res['message'])
    else:
        print('Good', res)