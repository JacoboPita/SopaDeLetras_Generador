import os
import random
import re
import string
from reportlab.pdfgen import canvas


def generar_sopa(palabras, x, y):
    sopa = [['' for _ in range(x)] for _ in range(y)]
    palabras_posiciones = []

    def colocar_palabra(palabra):
        longitud = len(palabra)
        colocado = False
        while not colocado:
            orientacion = random.choice(['H', 'V', 'D', 'H2', 'V2', 'D2'])
            if orientacion in ['H2', 'V2', 'D2']:
                palabra = ''.join(reversed(palabra))

            if orientacion == 'H' or orientacion == 'H2':
                fila = random.randint(0, y - 1)
                columna = random.randint(0, x - longitud)
                if all(sopa[fila][columna + i] in ('', letra) for i, letra in enumerate(palabra)):
                    for i, letra in enumerate(palabra):
                        sopa[fila][columna + i] = letra
                    colocado = True
                    palabras_posiciones.append((palabra, (fila, columna), 'H'))
            elif orientacion == 'V' or orientacion == 'V2':
                fila = random.randint(0, y - longitud)
                columna = random.randint(0, x - 1)
                if all(sopa[fila + i][columna] in ('', letra) for i, letra in enumerate(palabra)):
                    for i, letra in enumerate(palabra):
                        sopa[fila + i][columna] = letra
                    colocado = True
                    palabras_posiciones.append((palabra, (fila, columna), 'V'))
            elif orientacion == 'D' or orientacion == 'D2':
                orientacion = random.choice(['Arriba', 'Abajo'])
                if orientacion == 'Arriba':
                    fila = random.randint(0, y - longitud)
                    columna = random.randint(longitud, x - 1)
                    if all(sopa[fila + i][columna - i] in ('', letra) for i, letra in enumerate(palabra)):
                        for i, letra in enumerate(palabra):
                            sopa[fila + i][columna - i] = letra
                        colocado = True
                        palabras_posiciones.append((palabra, (fila, columna), 'Darriba'))
                if orientacion == 'Abajo':
                    fila = random.randint(0, y - longitud)
                    columna = random.randint(0, x - longitud)
                    if all(sopa[fila + i][columna + i] in ('', letra) for i, letra in enumerate(palabra)):
                        for i, letra in enumerate(palabra):
                            sopa[fila + i][columna + i] = letra
                        colocado = True
                        palabras_posiciones.append((palabra, (fila, columna), 'Dabajo'))

    for palabra in palabras:
        colocar_palabra(palabra)

    for i in range(y):
        for j in range(x):
            if sopa[i][j] == '':
                sopa[i][j] = random.choice(string.ascii_uppercase)

    return sopa, palabras_posiciones


def encontrar_siguiente(base_name, extension):
    base_path = os.getcwd()

    num_anterior = -1
    pattern = re.compile(rf'^{re.escape(base_name)}_(\d+){re.escape(extension)}$')

    for filename in os.listdir(base_path):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num == (num_anterior + 1):
                num_anterior = num

    siguiente = (num_anterior + 1)

    return siguiente


def sopa_a_pdf(sopa, base_name, palabras_posiciones):
    extension = ".pdf"
    siguiente = encontrar_siguiente(base_name, extension)
    filename = base_name + '_' + str(siguiente) + extension
    c = canvas.Canvas(filename)

    count = 1
    text = c.beginText(300 - 12 * len(sopa[0]), (780 - (count * 20)))
    text.setFont("Courier", 20)
    for fila in sopa:
        text.textLine(' '.join(fila))

    c.drawText(text)

    if palabras_posiciones:
        for palabra, (fila, columna), orientacion in palabras_posiciones:
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(2)
            if orientacion == 'H':
                x_start = 300 - 12 * len(sopa[0]) + columna * 24
                y_start = 780 - (count * 20) - (fila * 24) + 6
                x_end = x_start + len(palabra) * 22.5
                y_end = y_start
            elif orientacion == 'V':
                x_start = 300 - 12 * len(sopa[0]) + columna * 24 + 6
                y_start = 780 - (count * 20) - (fila * 24) + 12
                x_end = x_start
                y_end = y_start - len(palabra) * 22.5
            elif orientacion == 'Darriba':
                x_start = 300 - 12 * len(sopa[0]) + columna * 24 + 12
                y_start = 780 - (count * 20) - fila * 24 + 12
                x_end = x_start - len(palabra) * 22.5
                y_end = y_start - len(palabra) * 22.5
            elif orientacion == 'Dabajo':
                x_start = 300 - 12 * len(sopa[0]) + columna * 24
                y_start = 780 - (count * 20) - fila * 24 + 12
                x_end = x_start + len(palabra) * 22.5
                y_end = y_start - len(palabra) * 22.5
            c.line(x_start, y_start, x_end, y_end)

    c.showPage()
    c.save()


carpeta = "SOPAS DE LETRAS"
os.makedirs(carpeta, 0o777, True)
os.chdir(carpeta)
titulo = input("¿Cómo quieres llamar a esta sopa? ")
cantidad: int = int(input("¿Cuántas palabras deseas poner? "))
palabras = ['' for i in range(cantidad)]
print("Lista de palabras a encontrar: ")
for i in range(cantidad):
    palabras[i] = input()
palabras.sort()

base_name = "palabras"
extension = ".txt"
siguiente = encontrar_siguiente(base_name, extension)
filename = base_name + '_' + str(siguiente) + extension

with open(filename, "w") as file:
    file.write(titulo + "\n\n")
    for palabra in palabras:
        file.write(palabra + "\n")
x: int = int(input("¿Cuántas filas quieres? "))
y: int = int(input("¿Cuántas columnas quieres? "))
sopa, palabras_posiciones = generar_sopa(palabras, x, y)
sopa_a_pdf(sopa, "sopa", False)
sopa_a_pdf(sopa, "solucionario", palabras_posiciones)
