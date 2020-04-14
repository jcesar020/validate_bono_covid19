#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import array
import argparse

# Defininos los parametros por consola para aceptar el nombre del archivo
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Nombre del archivo a procesar")
args = parser.parse_args()


def check(dui):
    # Hace una verificacion en la plataforma si es beneficiado
    url = 'https://covid19-elsalvador.com/index.php'
    field = {'dui': dui}

    response = requests.post(url, data=field)

    soup = BeautifulSoup(response.content, 'html.parser')
    aceptado = soup.find(id='accepted')
    if aceptado:
        return True
    else:
        return False


def run():

    if args.file:
        print("El nombre del archivo a procesar es: ", args.file)

        beneficiarios = []
        # Listado de DUIS a evaluar
        file_origen = args.file

        # Abrimos el archivo para procesar
        f_duis = open(file_origen, 'r')

        with f_duis:
            duis = csv.reader(f_duis)
            aceptados = 0
            rechazados = 0

            # Validamos cada uno de los DUIS
            for row in duis:

                for index, col in enumerate(row):
                    if index > 2 and col != '':
                        if check(col):
                            aceptados = aceptados + 1
                            print("{} Beneficiados: {} {}".format(
                                aceptados, col, row[1]))
                            beneficiarios.append(row)
                        else:
                            rechazados = rechazados + 1
                            print("{} No aplican".format(rechazados))

        # LUEGO GUARDAMOS LA LISTA DE DUIS QUE SE ENCONTRARON RESULTARON BENEFICIADOS
        file_output = "res_" + args.file
        f = open(file_output, 'w')
        with f:
            writer = csv.writer(f)
            for row in beneficiarios:
                writer.writerow(row)
        print("### {} registros procesados ###".format(aceptados + rechazados))
        print("### y se encontraron {} beneficiados con $300".format(aceptados))
    else:
        print("No se especifico archivo para procesar")


if __name__ == '__main__':
    run()
