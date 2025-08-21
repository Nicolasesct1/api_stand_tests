import configuration
import requests
import data

def get_docs():
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)

def get_logs():
    return requests.get(configuration.URL_SERVICE + configuration.LOG_MAIN_PATH, params={"count":20})
    #params es lo mismo que si escribieras manualmente el ?count=20 al final del endpoint.

def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)

def post_new_user(body): #Crear Usuario
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

def post_products_kits(ids): #buscar los kits por sus productos
    return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
                         json=ids,
                         headers=data.headers)

#response = post_products_kits(data.product_ids)
#print(response.status_code)
#print(response.json())