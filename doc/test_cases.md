### Casos de Prueba para el Módulo 1: Extractor y Creador de Secuencias FASTA


1.  **Caso: Archivo del genoma no se encuentra.**
    
    -   **Entradas:**

        -   Ruta incorrecta o inexistente para el archivo FASTA del genoma.
        -   Archivo de picos válido.
        -   Directorio de salida.

    -   **Esperado:** `f"Error: No se encontró el archivo {ruta_archivo}"`
    
    ```python
    main.py -g ruta/Ecoli.fna -p ruta/archivo_picos.tsv -s ruta_salida/
    ```
    ```
    Error: No se encontró el archivo ruta/Ecoli.fna
    ```

2. **Caso: Archivo de picos no se encuentra.**

    - **Entradas:**

        - Archivo FASTA del genoma válido.
        - Ruta al archivo de picos inválida.
        - Directorio de salida.
    
    - **Esperado:** `f"Error: no se encontró el archivo {picos_ruta}"`

    ```python
    main.py -g ruta/Ecoli.fna -p ruta/archivo_picos.tsv -s ruta_salida/
    ```
    ```
    Error: no se encontró el archivo {picos_ruta}
    ```

3.  **Caso: Archivo de picos vacío.**
    
    -   **Entradas:**

        -   Archivo de picos vacío.
        -   Archivo FASTA del genoma.
        -   Directorio de salida.

    -   **Esperado:** `"Error: el archivo {picos_ruta} está vacío"`

    ```python
    main.py -g ruta/Ecoli.fna -p ruta/archivo_picos.tsv -s ruta_salida/
    ```
    
    ```
    Error: el archivo ruta/archivo_picos.tsv está vacío
    ```

4. **Caso: Archivo de picos con formato inválido (no TSV o CSV).**

    - **Entradas:**

        - Archivo del genoma válido.
        - Archivo de picos inválido.
        - Ruta de salida válida.

    - **Esperado:** `"Error: Formato de archivo inválido, se esperaba .tsv o .csv"`

    ```python
    main.py -g ruta/Ecoli.fna -p ruta/archivo_picos.tsv -s ruta_salida/
    ```
    ```
    Error: Formato de archivo inválido, se esperaba .tsv o .csv
    ```

5.  **Caso: El archivo de picos no cuenta con alguno de los campos requeridos (`TF_name`, `Peak_start`, `Peak_end`).**
    
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
6. **Caso: Valor de `Peak_start` sea mayor a `Peak_end`.**

	- **Entrada:**
	
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

7. **Caso: Directorio de salida inexistente.**

	 - **Entradas:**
		 
		 - Archivo de picos válido.
		 - Archivo FASTA del genoma válido.
		 - Directorio de salida inexistente.
 
	 - **Esperado:**  `Error: La carpeta {carp_salida} no existe`

    ```py
    main.py -g ruta/Ecoli.fna -p ruta/archivo_picos.tsv -s ruta_salida/
    ```
    ```
    Error: La carpeta {carp_salida} no existe
    ```

8. **Caso: Ausencia de algún parámetro en el query.**

	- **Entrada:** ausencia de alguno de los parámetros necesarios para la extracción y creación del FASTA.

	- **Esperado:** un mensaje de error que indique el/los parámetros faltantes.

```py
# Falta el archivo de picos
mk_fasta_from_peaks.py -i  -g Ecoli.fna -o fasta_peaks/
# Falta el archivo FASTA
mk_fasta_from_peaks.py -i peak_file.txt -g -o fasta_peaks/
# Falta el directorio de salida
mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o
```
```bash
# Falta del archivo de picos
Error: Peak file missing as a parameter
# Falta el archivo FASTA
Error: FASTA file missing as a parameter
# Falta el directorio de salida
Error: Output directory missing as a parameter
```