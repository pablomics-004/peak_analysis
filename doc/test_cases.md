### Casos de Prueba para el Módulo 1: Extractor y Creador de Secuencias FASTA


1.  **Caso: Archivo del genoma no se encuentra.**
    
    -   **Entradas:**

        -   Ruta incorrecta o inexistente para el archivo FASTA del genoma.
        -   Archivo de picos válido.
        -   Directorio de salida.

    -   **Esperado:** `f"FileNotFoundError: No se encontró el archivo: ruta_genoma/genoma.fa"`
    
    ```python
    python3 src/main.py -g doc/E_coli_K12_MG1655_U00096.3.txt -p data/union_peaks_file.tsv -s results/
    ```
    ```
    FileNotFoundError: No se encontró el archivo: doc/E_coli_K12_MG1655_U00096.3.txt
    ```

2. **Caso: Archivo de picos no se encuentra.**

    - **Entradas:**

        - Archivo FASTA del genoma válido.
        - Ruta al archivo de picos inválida.
        - Directorio de salida.
    
    - **Esperado:** `f"FileNotFoundError: no se encontró el archivo {picos_ruta}"`

    ```python
    python3 src/main.py -g data/E_coli_K12_MG1655_U00096.3.txt -p doc/union_peaks_file.tsv -s results/
    ```
    ```
    FileNotFoundError: No se encontró el archivo doc/union_peaks_file.tsv
    ```

3.  **Caso: Archivo de picos vacío.**
    
    -   **Entradas:**

        -   Archivo de picos vacío.
        -   Archivo FASTA del genoma.
        -   Directorio de salida.

    -   **Esperado:** `"ValueError: el archivo {picos_ruta} está vacío"`

    ```python
    python3 src/main.py -g data/E_coli_K12_MG1655_U00096.3.txt -p data/picos_vacios.tsv -s results/
    ```
    
    ```
    ValueError: El archivo data/picos_vacios.tsv está vacío
    ```

4. **Caso: Archivo de picos con formato inválido (no TSV o CSV).**

    - **Entradas:**

        - Archivo del genoma válido.
        - Archivo de picos inválido.
        - Ruta de salida válida.

    - **Esperado:** `"ValueError: Extensión inválida: se esperaba .tsv, .csv o .txt → data/picos.xlsx"`

    ```python
    python3 src/main.py -g data/E_coli_K12_MG1655_U00096.3.txt -p data/picos.xlsx -s results/
    ```
    ```
    ValueError: Extensión inválida: se esperaba .tsv, .csv o .txt → data/picos.xlsx
    ```

5. **Caso: El archivo de picos tiene encabezado pero ningún dato.**

    - **Entradas:**

        -   Archivo de picos con encabezado únicamente.
        -   Archivo FASTA del genoma válido.
        -   Directorio de salida.

    - **Esperado:** `f'El archivo de {picos_ruta} tiene encabezado pero ningún dato'`

    ```python
    python3 src/main.py -g data/E_coli_K12_MG1655_U00096.3.txt -p data/picos_vacios.tsv -s results/
    ```
    ```
    RuntimeError: Error al procesar el archivo de picos: El archivo de data/picos_vacios.tsv tiene encabezado pero ningún dato
    ```

6.  **Caso: El archivo de picos no cuenta con alguno de los campos requeridos (`TF_name`, `Peak_start`, `Peak_end`).**
    
    -   **Entradas:**

        -   Archivo de picos con ausencia de alguno de los campos `TF_name`, `Peak_start`, `Peak_end`.
        -   Archivo FASTA del genoma válido.
        -   Directorio de salida.

    -   **Esperado:** `Error: El archivo no cuenta con alguno de los campos requeridos: {campos}`

    ```python
    main.py -g ruta/Ecoli.fna -p ruta/archivo_picos.tsv -s ruta_salida/
    ```

    ```python
    Error: El archivo no cuenta con alguno de los campos requeridos: TF_name
    ```
7. **Caso: Valor de `Peak_start` sea mayor a `Peak_end`.**

	- **Entradas:**
	
		- Archivo de picos con un `Peak_end` menor a `Peak_start_`.
		- Archivo FASTA del genoma.
		- Directorio de salida.

	- **Esperado:** `"Existen filas con Peak_end menor que Peak_start."`.

    ```py
    main.py -g ruta/Ecoli.fna -p ruta/archivo_picos.tsv -s ruta_salida/
    ```
    ```
    Existen filas con Peak_end menor que Peak_start.
    ```

8. **Caso: Directorio de salida inexistente.**

	 - **Entradas:**
		 
		 - Archivo de picos válido.
		 - Archivo FASTA del genoma válido.
		 - Directorio de salida inexistente.
 
	 - **Esperado:**  `Error: La carpeta {carp_salida} no existe`

    ```py
    main.py -g ruta/Ecoli.fna -p ruta/archivo_picos.tsv -s ruta_salida/
    ```
    ```
    Error: La carpeta ruta_salida/ no existe
    ```

9. **Caso: Ausencia de algún parámetro en el query.**

	- **Entradas:** ausencia de alguno de los parámetros necesarios para la extracción y creación del FASTA.

	- **Esperado:** un mensaje de error que indique el/los parámetros faltantes.

    ```python
    # Falta el archivo de picos
    main.py -g ruta/Ecoli.fna -s ruta_salida/
    # Falta el archivo FASTA
    main.py -p ruta/archivo_picos.tsv -s ruta_salida/
    ```
    ```bash
    # Falta del archivo de picos
    usage: Módulo 1 [-h] -g GENOMA -p PICOS [-s SALIDA]
    Módulo 1: error: the following arguments are required: -p/--picos

    # Falta el archivo FASTA
    usage: Módulo 1 [-h] -g GENOMA -p PICOS [-s SALIDA]
    Módulo 1: error: the following arguments are required: -g/--genoma
    ```