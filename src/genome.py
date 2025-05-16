"""
Módulo de lectura y procesamiento de archivos genómicos y de picos de unión de factores de transcripción.

Este módulo contiene funciones para:
- Leer un archivo FASTA que contiene un genoma y devolverlo como una única cadena de texto.
- Leer un archivo tabulado de picos de unión (formato .tsv o .txt con campos específicos) y organizar la información
  por factor de transcripción (TF) en un diccionario de coordenadas de picos.

Funciones:
- cargar_genoma(fasta_ruta): Lee un archivo FASTA y devuelve el genoma como cadena.
- leer_archivo_picos(peaks_ruta): Lee un archivo de picos y devuelve un diccionario TF -> [(start, end)].

Uso:
    import genome as gn

    genoma = gn.cargar_genoma('genoma.fna')
    picos = gn.leer_archivo_picos('picos.tsv')

Versión: 1.0.0
Autor: Pablo Salazar Méndez
Fecha: 15-05-2025
"""

import os

def cargar_genoma(fasta_ruta: str) -> str:
    """
    Lee un archivo FASTA y devuelve la secuencia genómica como una única cadena de texto.

    Args:
        fasta_ruta (str): Ruta absoluta del archivo FASTA con el genoma.

    Returns:
        str: Genoma representado como una sola cadena (sin encabezados).

    Raises:
        FileNotFoundError: Si no se encuentra el archivo FASTA en la ruta proporcionada.
        ValueError: Si el archivo no tiene el formato FASTA correcto o está vacío.
        RuntimeError: Si ocurre un error al leer el archivo.
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

def leer_archivo_picos(peaks_ruta: str) -> dict:
    """
    Lee un archivo tabulado con información de picos de unión de TFs y retorna un diccionario con los intervalos.

    El archivo debe tener al menos las columnas:
    - 'TF_name': nombre del factor de transcripción.
    - 'Peak_start': posición inicial del pico.
    - 'Peak_end': posición final del pico.

    Args:
        peaks_ruta (str): Ruta al archivo de picos (formato TSV).

    Returns:
        dict: Diccionario con clave el nombre del TF y valor una lista de tuplas (peak_start, peak_end).

    Raises:
        FileNotFoundError: Si no se encuentra el archivo.
        ValueError: Si falta alguno de los campos obligatorios o si las coordenadas son inválidas.
        RuntimeError: Si ocurre un error al leer el archivo.
    """
    
    # Verificando la presencia del archivo
    if not os.path.isfile(peaks_ruta):
        raise FileNotFoundError(f'Error: no se encontró el archivo {peaks_ruta}')
    
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

            for linea in archivo:
                actual = linea.strip().split('\t')
                peak_start = int(float(actual[ind_ps]))
                peak_end = int(float(actual[ind_pe]))
                
                # Creando e inicializando la llave
                if actual[ind_tf] not in dicc_picos:
                    dicc_picos[actual[ind_tf]] = list()
                
                # Verificando el orden de Peak_start y Peak_end
                if (peak_end - peak_start) < 0:
                    raise ValueError(f'Los campos Peak_end y Peak_start son incorrectos en el TF {actual[ind_tf]}')
                
                dicc_picos[actual[ind_tf]].append((peak_start,peak_end))
            
            return dicc_picos
    except OSError as e:
        raise RuntimeError(f'Error al leer el archivo de picos: {peaks_ruta}') from e