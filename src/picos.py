"""
Módulo para extraer secuencias genómicas específicas a partir de coordenadas de picos de unión.

Este módulo contiene funciones para:

- Obtener subsecuencias del genoma a partir de coordenadas.
- Asociar secuencias de picos con sus respectivos factores de transcripción (TFs) a partir de un diccionario de picos.

Funciones:

- slicing_sec(genoma, peak_start, peak_end): Devuelve la subsecuencia del genoma correspondiente a un intervalo.
- extraer_secuencias(peaks_data, genoma): Devuelve un diccionario con las secuencias de picos por TF.

Versión: 1.0.0
Autor: Pablo Salazar Méndez
Fecha: 15-05-2025
"""

def slicing_sec(genoma: str,peak_start: int,peak_end: int) -> str:
    """
    Extrae una subsecuencia del genoma entre dos coordenadas específicas (inclusive).

    Args:
        genoma (str): Genoma completo cargado como una cadena de texto.
        peak_start (int): Posición inicial del pico.
        peak_end (int): Posición final del pico.

    Returns:
        str: Subcadena del genoma correspondiente al intervalo [peak_start, peak_end].

    Raises:
        ValueError: Si el intervalo especificado no corresponde a una secuencia válida dentro del genoma.
    """

    # Extrayendo el pico
    sec = genoma[peak_start:peak_end + 1]

    # Verificación de la secuencia
    if not sec:
        raise ValueError(f'El locus {(peak_start,peak_end)} no está disponible en el genoma.')
    
    return sec

def extraer_secuencias(peaks_data: dict,genoma: str) -> dict:
    """
    Extrae las secuencias correspondientes a los picos de unión para cada TF.

    Args:
        peaks_data (dict): Diccionario con claves de nombre de TF (str) y valores como listas de tuplas (peak_start, peak_end).
        genoma (str): Genoma completo cargado como una cadena de texto.

    Returns:
        dict: Diccionario con claves de nombre de TF (str) y valores como listas de secuencias (str) correspondientes a sus picos.
    """

    # Diccionario TF-secuencias de picos
    dicc_sec = {
        tf_name: [
            slicing_sec(genoma,tupla[0],tupla[1])
            for tupla in lista_tup
        ]
        for tf_name,lista_tup in peaks_data.items()
    }
    
    return dicc_sec