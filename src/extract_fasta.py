"""
Este programa comprende el primer módulo del proyecto Peak analysis, bajo el nombre extract_fasta.py. Permite
extraer los picos de unión de TFs a genomas en formato FASTA, devuelve un archivo FASTA por cada TF proporcionado
en el archivo de picos; se recomienda el uso de rutas absolutas para los archivos.

Modo de uso:

    python extract_fasta.py --genoma ruta_genoma/ --picos ruta_picos/ --salida ruta_salida_fasta/

Autor: Pablo Salazar Méndez
Fecha: 01-05-2025
"""

import os # Para interactuar con el sistema operativo local
import argparse # Para que se ingresen los inputs en una única línea de comandos

import genome as gn # Cargado y lectura de genomas
import peaks as pk # Extractor de secuencias
import io_utils as iu

def main():
    parser = argparse.ArgumentParser(
        prog='Módulo 1',
        description='Extrae secuencias FASTA por TF a partir de picos y un genoma en formato FASTA.'
    )
    
    # Definiendo argumentos de la línea de comandos
    parser.add_argument('--genoma', required=True, help='Ruta al archivo FASTA del genoma')
    parser.add_argument('--picos', required=True, help='Ruta al archivo TSV de picos')
    parser.add_argument('--salida', required=True, help='Ruta de salida de los archivos FASTA por TF')

    # Analiza los argumentos en la línea de comandos
    args = parser.parse_args()

    # Flujo principal del código
    genoma = gn.cargar_genoma(args.genoma)
    picos = gn.leer_archivo_picos(args.picos)
    secuencias = pk.extraer_secuencias(picos,genoma)
    iu.fasta_por_tf(secuencias,args.salida)

# Asegura que el ámbito main se ejecute únicamente desde la línea de comandos
if __name__ == '__main__':
    main()