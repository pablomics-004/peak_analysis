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

def fasta_por_tf(dic_tf,carp_salida):
    """
    Args:
        dic_tf: diccionario TF-secuencias con picos de unión.
        carp_salida: directorio de salida de los archivos FASTA.
    Return:
        Archivos FASTA por cada TF dentro del directorio proporcionado.
    Raises:
        NotADirectoryError: en caso de que la carpeta de salida no exista.
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