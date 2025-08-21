import sender_stand_request
import data

def get_user_body(first_name): #edita el first_name en una copia
    current_body = data.user_body.copy() # Crea una copia del diccionario
    current_body["firstName"] = first_name # Cambia el valor del campo "firstName"
    return current_body # Devuelve el nuevo diccionario con el nombre actualizado

def positive_assert(first_name): # “Caso de prueba de crear un usuario”.
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body) #Se hace el Post para crear usuario con la data nueva

    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"] #",,," Ese trozo representa columnas vacías en la tabla de usuarios una "," por cada columna

    # Comprueba si el usuario o usuaria existe y es único/a. text (busca todos los textos iguales y los cuenta)
    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_body["firstName"] == first_name # (opcional) Comprueba que recibe una versión actualizada del cuerpo de solicitud de creación
    assert user_response.status_code == 400 # Comprueba si la respuesta contiene el código 400.
    assert user_response.json()["code"] == 400 # Comprueba si el atributo "code" en el cuerpo de respuesta es 400. Es solo la respuesta
    assert user_response.json()["message"] == "Has introducido un nombre de usuario no válido. El nombre solo puede contener letras del alfabeto latino, la longitud debe ser de 2 a 15 caracteres."

def negative_assert_no_firstname(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

# Prueba 1. Creación de un nuevo usuario o usuaria con 2 letras. El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa") #Le asignamos "Aa" de firstName en la funcion positive_assert

# Prueba 2. Creacion postiva usuario con 15 letras
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("ABCDEFGHIJKLMNO")

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("ABCDEFGHIJKLMNOP")

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("a Aaa")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"A%@\",") #para probar caracteres especiales poner "\"%$#$\","

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol(123)

def test_create_user_no_first_name_get_error_response(): #la solicitud no contiene el parametro firstname
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    # De lo contrario, se podrían perder los datos del diccionario de origen
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)

def test_create_user_empty_first_name_get_error_response(): #es por si hay un string vacio
    # El cuerpo de la solicitud se guarda en la variable user_body
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12) #en este caso first_name recbiria un int en vez de un string ya que la funcion get_user_body tiene como parametro el first_name
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400