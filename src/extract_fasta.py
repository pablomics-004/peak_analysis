"""
Este programa comprende el primer módulo del proyecto Peak analysis, bajo el nombre extract_fasta.py. Permite
extraer los picos de unión de TFs a genomas en formato FASTA, devuelve un archivo FASTA por cada TF proporcionado
en el archivo de picos; se recomienda el uso de rutas absolutas para los archivos.

Modo de uso:

python extract_fasta.py --genoma ruta_genoma/ --picos ruta_picos/ --salida ruta_salida_fasta/

Autor: Pablo Salazar Méndez
Fecha: 01-05-2025
"""

import os # Para interactuar con el sistema operativo local
import argparse # Para que se ingresen los inputs en una única línea de comandos

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
        Diccionario TF-lista de (peak_start,peak_end).
    Raises:
        FileNotFoundError: si el archivo no es encontrado.
        ValueError: si falta alguno de los campos o están incorrectos.
        RunTimeError: de no ser posible la lectura del archivo.
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

            next(archivo)
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

def slicing_sec(genoma,peak_start,peak_end):
    """
    Args:
        genoma: genoma cargado en un único str.
        peak_start: coordenada de inicio del pico.
        peak_end: coordenada de fin del pico.
    Return:
        Secuencia correspondiente del genoma.
    Raise:
        ValueError: en caso de que no haya habido dicha secuencia en el genoma.
    """

    # Extrayendo el pico
    sec = genoma[peak_start:peak_end + 1]

    # Verificación de la secuencia
    if not sec:
        raise ValueError(f'El locus {(peak_start,peak_end)} no está disponible en el genoma.')
    
    return sec

def extraer_secuencias(peaks_data,genoma):
    """
    Args:
        peaks_data: diccionario TF-lista con las coordenadas de picos.
        genoma: genoma cargado en un único string.
    Return:
        Diccionario TF-secuencias de picos.
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

def main():
    parser = argparse.ArgumentParser(
        prog='Módulo 1',
        description='Extrae secuencias FASTA por TF a partir de picos y un genoma en formato FASTA.'
    )
    
    # Definiendo argumentos de la línea de comandos
    parser.add_argument('--genoma', required=True, help='Ruta al archivo FASTA del genoma')
    parser.add_argument('--picos', required=True, help='Ruta al archivo TSV de picos')
    parser.add_argument('--salida', required=True, help='Ruta de salida de los archivos FASTA por TF')

    # Analiza los argumentos en la línea de comandos
    args = parser.parse_args()

    # Flujo principal del código
    genoma = cargar_genoma(args.genoma)
    picos = leer_archivo_picos(args.picos)
    secuencias = extraer_secuencias(picos,genoma)
    fasta_por_tf(secuencias,args.salida)

# Asegura que el ámbito main se ejecute únicamente desde la línea de comandos
if __name__ == '__main__':
    main()