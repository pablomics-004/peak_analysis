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
- leer_archivo_picos(peaks_ruta): Lee un archivo de picos y devuelve un diccionario TF -> [(start, end)].

Uso:
    import genome as gn

    genoma = gn.cargar_genoma('genoma.fna')
    picos = gn.leer_archivo_picos('picos.tsv')

Versión: 2.0.3
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

def leer_archivo_picos(peaks_ruta: str) -> dict[str, list[tuple[int, int]]]:
    """
    Lee un archivo tabulado con información de picos de unión de TFs y retorna un diccionario con los intervalos.

    El archivo debe tener al menos las columnas:
    - 'TF_name': nombre del factor de transcripción.
    - 'Peak_start': posición inicial del pico.
    - 'Peak_end': posición final del pico.

    PARÁMETROS:
        peaks_ruta (str): Ruta al archivo de picos (formato TSV o TXT tabulado).

    RETURNS:
        dict: Diccionario con clave el nombre del TF y valor una lista de tuplas (peak_start, peak_end).

    RAISES:
        FileNotFoundError: Si no se encuentra el archivo.
        ValueError: Si falta alguno de los campos obligatorios o si las coordenadas son inválidas.
        RuntimeError: Si ocurre un error al leer el archivo.
    """

    if not os.path.isfile(peaks_ruta):
        raise FileNotFoundError(f'Error: no se encontró el archivo {peaks_ruta}')
    
    campos = ['TF_name', 'Peak_start', 'Peak_end']

    try:
        # Leer archivo con pandas
        df = pd.read_csv(peaks_ruta, sep='\t')

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