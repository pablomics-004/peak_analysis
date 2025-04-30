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
    Args:
        peaks_ruta: ruta al archivo de picos.
    Return:
        Diccionario TF-lista de (peak_start,peak_end)
    """
    
    # Verificando la presencia del archivo
    if not os.path.isfile(peaks_ruta):
        raise FileNotFoundError(f'Error: no se encontró el archivo: {peaks_ruta}')
    
    # Campos que debe tener
    campos = ['TF_name','Peak_start','Peak_end']
    
    try:
        
        with open(peaks_ruta) as archivo:

            # Verificando que no falte alguno de los parámetros
            encabezado = archivo.readline().strip('\n').split('\t')
            if not all(campo in encabezado for campo in campos):
                raise ValueError(f'El archivo no cuenta con alguno de los campos TF_name, Peak_start o Peak_end.')

            # Diccionario e índices
            dicc_picos = {}
            ind_tf = encabezado.index(campos[0])
            ind_ps = encabezado.index(campos[1])
            ind_pe = encabezado.index(campos[2])

            next(archivo)
            for linea in archivo:
                actual = linea.strip().split('\t')
                
                # Creando e inicializando la llave
                if actual[ind_tf] not in dicc_picos:
                    dicc_picos[actual[ind_tf]] = list()
                
                # Verificando el orden de Peak_start y Peak_end
                if (int(actual[ind_pe]) - int(actual[ind_ps])) < 0:
                    raise ValueError(f'Los campos Peak_end y Peak_start son incorrectos en el TF {actual[ind_tf]}')
                
                dicc_picos[actual[ind_tf]].append((actual[ind_ps],actual[ind_pe]))
            
            return dicc_picos

    except OSError as e:
        raise RuntimeError(f'Error al leer el archivo de picos: {peaks_ruta}') from e