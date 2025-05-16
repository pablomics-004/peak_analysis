"""
Módulo para la exportación de secuencias en formato FASTA por cada factor de transcripción (TF).

Este módulo permite tomar un diccionario con listas de secuencias por TF y generar un archivo `.fna` 
(indistintamente compatible con el formato FASTA) para cada TF en el directorio de salida especificado.

Cada archivo contendrá múltiples entradas FASTA, una por cada secuencia asociada a ese TF.

Módulos requeridos:

- os: Para verificar y construir rutas de archivos en el sistema operativo.

Funciones:

- fasta_por_tf(dic_tf, carp_salida): Exporta archivos FASTA por TF en el directorio indicado.

Uso:

    fasta_por_tf(diccionario_tf_secuencias, "./output")

Versión: 1.0.0  
Autor: Pablo Salazar Méndez 
Fecha: 15-05-2025
"""

import os
ruta_actual = os.getcwd()

def fasta_por_tf(dic_tf: dict,carp_salida: str = ruta_actual):
    """
    Genera archivos FASTA (.fna) por cada TF usando las secuencias proporcionadas.

    Args:
        dic_tf (dict): Diccionario con claves como nombres de TFs (str) y valores como listas de secuencias (str).
        carp_salida (str): Ruta del directorio donde se guardarán los archivos FASTA (por defecto es la actual).

    Returns:
        None. Se generan archivos en disco con extensión .fna, uno por TF.

    Raises:
        NotADirectoryError: Si el directorio especificado no existe.

    Formato de salida:
        Cada archivo tendrá líneas con encabezados tipo:
            >TF_nombre_peak=1_len=200
        Seguido por la secuencia correspondiente en la línea siguiente.
    """

    # Verificando la validez del directorio
    if not os.path.isdir(carp_salida):
        raise NotADirectoryError(f'La carpeta {carp_salida} no existe.')
    
    for tf,secuencias in dic_tf.items():

        ruta_comp = os.path.join(carp_salida,tf + '.fna')
        pico = 0

        with open(ruta_comp, 'w') as fasta:

            # Imprimiendo las secuencias
            for secuencia in secuencias:
                pico += 1
                print(f'>{tf}_peak={pico}_len={len(secuencia)}', file=fasta)
                print(secuencia, file=fasta)
    
    print(f'\nArchivos FASTA disponibles en {carp_salida}.\n')