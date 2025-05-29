"""
Módulo de análisis de argumentos para línea de comandos.

Este módulo define y gestiona los argumentos que el usuario debe proporcionar
al ejecutar el script principal del proyecto *Peak Analysis* desde la terminal.

Se utiliza para capturar:
- La ruta del archivo FASTA con el genoma.
- La ruta del archivo TSV con los picos de unión.
- El directorio de salida donde se almacenarán los archivos FASTA generados.

Módulos requeridos:

- argparse: Permite definir y procesar los argumentos ingresados por el usuario.

Uso desde otro módulo:

    import parseador as pr

    args = pr.parseo()

Autor: Pablo Salazar Méndez
Versión: 1.0.3
Fecha: 16-05-2025
"""

import argparse as ap # Argumentos desde línea de comandos

def parseo() -> ap.Namespace:
    """
    Procesa y devuelve los argumentos ingresados por el usuario en la línea de comandos.

    Returns:
        argparse.Namespace: Objeto con los argumentos:
            - genoma (str): Ruta al archivo FASTA del genoma.
            - picos (str): Ruta al archivo TSV que contiene los picos de unión.
            - salida (str): Directorio donde se generarán los archivos FASTA por TF.

    Raises:
        SystemExit: Si falta alguno de los argumentos obligatorios o son inválidos,
                    argparse imprimirá un mensaje de error y finalizará el script.
    """
    parser = ap.ArgumentParser(
        prog='Módulo 1',
        description='Extrae secuencias FASTA por TF a partir de picos y un genoma en formato FASTA.'
    )
    
    # Definiendo argumentos de la línea de comandos
    parser.add_argument(
        '-g','--genoma',
        type=str,
        required=True,
        help='Ruta al archivo FASTA del genoma'
    )
    parser.add_argument(
        '-p','--picos', 
        type=str, 
        required=True, 
        help='Ruta al archivo TSV de picos'
    )
    parser.add_argument(
        '-s','--salida', 
        type=str, 
        help='Ruta de salida de los archivos FASTA por TF'
    )

    return parser.parse_args()