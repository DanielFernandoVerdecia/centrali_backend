import random

#Recuperar cuenta y verificar cuenta para su activación
def generar_codigo_cuenta():

    codigo = ""

    datos = ['A', 'E', 'I', 'O', 'U', 'X', 'Y', 'Z', 'W' ,
             '1', '2', '3', '4', '5', '6', '7', '8', '9']

    while len(codigo) < 8:

        caracter_nuevo = random.choice(datos)

        if codigo.count(caracter_nuevo) < 2:

            codigo += caracter_nuevo

    return codigo