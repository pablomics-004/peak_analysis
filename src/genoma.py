"""
Módulo de lectura y procesamiento de archivos genómicos y de picos de unión de factores de transcripción.

Este módulo contiene funciones para:

- Leer un archivo FASTA que contiene un genoma y devolverlo como una única cadena de texto.
- Leer un archivo tabulado de picos de unión (formato .tsv o .txt con campos específicos) y organizar la información
  por factor de transcripción (TF) en un diccionario de coordenadas de picos.

Módulos requeridos:

- pandas: Para leer el archivo tsv con los picos.
- os: Para verificar rutas de archivos y carpetas en el sistema operativo.
  
Funciones:

- cargar_genoma(fasta_ruta): Lee un archivo FASTA y devuelve el genoma como cadena.
- leer_archivo_picos(picos_ruta): Lee un archivo de picos y devuelve un diccionario TF -> [(start, end)].

Uso:
    import genome as gn

    genoma = gn.cargar_genoma('genoma.fna')
    picos = gn.leer_archivo_picos('picos.tsv')

Versión: 2.0.7
Autor: Pablo Salazar Méndez
Fecha: 29-05-2025
"""
import pandas as pd # Lectura de tsv
import os # Interactuar con el sistema operativo

def cargar_genoma(fasta_ruta: str) -> str:
    """
    Lee un archivo FASTA y devuelve la secuencia genómica como una única cadena de texto.

    PARÁMETROS:
        fasta_ruta (str): Ruta absoluta del archivo FASTA con el genoma.

    RETURNS:
        str: Genoma representado como una sola cadena (sin encabezados).

    RAISES:
        FileNotFoundError: Si no se encuentra el archivo FASTA en la ruta proporcionada.
        ValueError: Si el archivo no tiene el formato FASTA correcto o está vacío.
        RuntimeError: Si ocurre un error al leer el archivo.
    """

    # Verificando la ruta
    if not os.path.isfile(fasta_ruta):
        raise FileNotFoundError(f'No se encontró el archivo: {fasta_ruta}')

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

def detectar_sep(picos_ruta: str) -> str | None:
    """
    Dado un archivo, lee las primeras cinco líneas para dectar el tipo de separador que tiene.

    PARÁMETROS:
        picos_ruta (str): Ruta del archivo de picos.

    RETURN:
        str: Indica el separador que tiene el archivo.
        None en caso de que no haya '\t' o ',' como separadores.
    """

    # Primeras cinco líneas
    with open(picos_ruta) as pr:
        lineas = [pr.readline() for _ in range(5)]
    
    tab = sum(l.count('\t') for l in lineas)
    coma = sum(l.count(',') for l in lineas)

    if tab > coma:
        return '\t'
    elif coma > tab:
        return ','
    else:
        return None # Error en la función leer_archivo_picos()

def leer_archivo_picos(picos_ruta: str) -> dict[str, list[tuple[int, int]]]:
    """
    Lee un archivo tabulado o con comas con información de picos de unión de TFs y retorna un diccionario con los 
    intervalos.

    El archivo debe tener al menos las columnas:
    - 'TF_name': nombre del factor de transcripción.
    - 'Peak_start': posición inicial del pico.
    - 'Peak_end': posición final del pico.

    PARÁMETROS:
        picos_ruta (str): Ruta al archivo de picos (formato TSV, TXT tabulado o CSV).

    RETURNS:
        dict: Diccionario con clave el nombre del TF y valor una lista de tuplas (peak_start, peak_end).

    RAISES:
        FileNotFoundError: Si no se encuentra el archivo.
        ValueError: Si el archivo está vacío, no es TSV o CSV, si falta alguno de los campos obligatorios o si las 
        coordenadas son inválidas.
        RuntimeError: Si ocurre un error al leer el archivo.
    """

    if not os.path.isfile(picos_ruta):
        raise FileNotFoundError(f'No se encontró el archivo {picos_ruta}')
    
    # Verificar que el archivo no esté vacío
    if not os.path.getsize(picos_ruta):
        raise ValueError(f'El archivo {picos_ruta} está vacío')

    # Verificar que el archivo sea tsv o cvs
    sep = detectar_sep(picos_ruta)
    if not sep:
        raise ValueError('Formato de archivo inválido, se esperaba .tsv o .csv')
    
    campos = ['TF_name', 'Peak_start', 'Peak_end']

    try:
        # Leer archivo con pandas
        df = pd.read_csv(picos_ruta, sep=sep)

        # Verificar que el archivo tenga más que solo el encabezado
        if df.empty():
            raise ValueError(f'El archivo de {picos_ruta} tiene encabezado pero ningún dato')

        # Verificar columnas requeridas
        if not all(col in df.columns for col in campos):
            raise ValueError(f'El archivo no cuenta con alguno de los campos requeridos: {campos}')

        # Convertir a enteros y verificar coordenadas
        df['Peak_start'] = df['Peak_start'].astype(int)
        df['Peak_end'] = df['Peak_end'].astype(int)

        if (df['Peak_end'] < df['Peak_start']).any():
            raise ValueError('Existen filas con Peak_end menor que Peak_start.')

        # Agrupar por TF y convertir a diccionario de listas de tuplas
        dicc_picos = (
            df.groupby('TF_name')
            .apply(lambda x: list(zip(x['Peak_start'], x['Peak_end'])))
            .to_dict()
        )

        return dicc_picos

    except Exception as e:
        raise RuntimeError(f'Error al procesar el archivo de picos: {e}') from e