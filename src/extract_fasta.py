"""
Este programa comprende el primer módulo del proyecto Peak analysis, bajo el nombre extract_fasta.py. Permite
extraer los picos de unión de TFs a genomas en formato FASTA, devuelve un archivo FASTA por cada TF proporcionado
en el archivo de picos.

Autor: Pablo Salazar Méndez
Fecha: 01-05-2025
"""

import os

def cargar_genoma(fasta_ruta):
    """
    Args:
        fasta_ruta: recibe la ruta absoluta del archivo FASTA con el genoma.
    Return:
        Genoma en una única cadena de texto.
    Raises:
        FileNotFoundError: no se encontró el archivo en fasta_ruta.
        ValueError: el archivo FASTA está vacío o no tiene el formato esperado.
        RunTimeError: error al leer archivo FASTA proporcionado en fasta_ruta.
    """

    # Verificando la ruta
    if not os.path.isfile(fasta_ruta):
        raise FileNotFoundError(f'Error: No se encontró el archivo: {fasta_ruta}')

    try:

        with open(fasta_ruta) as archivo:
            
            # Verificando la primer línea
            if not archivo.readline().startswith('>'):
                raise ValueError(f'El archivo no tiene el formato FASTA esperado.')

            # Lista temporal para las secuencias
            secuencias = [
                linea.strip()
                for linea in archivo
                if not linea.startswith('>')
            ]
    
        genoma = ''.join(secuencias)

        if not genoma:
            raise ValueError(f'El archivo FASTA está vacío.')

        return genoma
    
    except OSError as e:
        raise RuntimeError(f'Error al leer el archivo FASTA: {fasta_ruta}') from e

def leer_archivo_picos(peaks_ruta):
    """
    """
    ...