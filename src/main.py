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

    python extract_fasta.py -g /ruta/genoma.fna \\
                            -p /ruta/picos.tsv \\
                            -s /ruta/salida_fasta/

Versión: 1.0.0
Autor: Pablo Salazar Méndez
Fecha: 01-05-2025
"""

import genoma as gn # Cargado y lectura de genomas
import picos as pc # Extractor de secuencias
import generador_fasta as gf # Generador de archivos FASTA por cada TF
import parseador as pr # Parseo de los agrumentos en la línea de comandos

def main():

    args = pr.parseo()

    # Flujo principal del código
    genoma = gn.cargar_genoma(args.genoma)
    picos = gn.leer_archivo_picos(args.picos)
    secuencias = pc.extraer_secuencias(picos,genoma)
    gf.fasta_por_tf(secuencias,args.salida)

# Asegura que el ámbito main se ejecute únicamente desde la línea de comandos
if __name__ == '__main__':
    main()