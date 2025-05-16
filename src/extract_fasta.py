"""
Módulo principal del proyecto Peak Analysis: extract_fasta.py

Este script permite extraer secuencias genómicas correspondientes a los picos de unión
de factores de transcripción (TFs) a partir de un archivo FASTA de genoma y un archivo
TSV con coordenadas de picos. El resultado son archivos FASTA individuales por cada TF.

Requisitos:

- El archivo de genoma debe estar en formato FASTA, con una sola secuencia en una línea.
- El archivo de picos debe estar en formato tabular (.tsv), con las columnas:
  'TF_name', 'Peak_start', 'Peak_end'.
- Se recomienda el uso de rutas absolutas para evitar errores de ubicación.

Módulos requeridos:

- os: Para verificar y construir rutas de archivos en el sistema operativo.
- argparse: Para recibir los argumentos desde la línea de comandos.
- genome: Para cargar y leer el genoma de interés.
- peaks: Para extraer los picos de cada TF.
- io_utils: Genera archivos FASTA por cada TF y sus correspondientes picos.

Modo de uso (desde terminal):

    python extract_fasta.py --genoma /ruta/genoma.fna \\
                            --picos /ruta/picos.tsv \\
                            --salida /ruta/salida_fasta/

Versión: 1.0.0
Autor: Pablo Salazar Méndez
Fecha: 01-05-2025
"""

import os # Para interactuar con el sistema operativo local
import argparse # Para que se ingresen los inputs en una única línea de comandos

import genome as gn # Cargado y lectura de genomas
import peaks as pk # Extractor de secuencias
import io_utils as iu # Generador de archivos FASTA por cada TF

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