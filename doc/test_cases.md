### Casos de Prueba para el Módulo 1: Extractor y Creador de Secuencias FASTA


1.  **Caso: Archivo del genoma no se encuentra.**
    
    -   **Entradas:**

        -   Ruta incorrecta o inexistente para el archivo FASTA del genoma.
        -   Archivo de picos válido.
        -   Directorio de salida.

    -   **Esperado:** `"Error: Genome file not found"`
    
    ```python
    mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/ 
    ```
    ```
    Error: "Ecoli.fna" genome file not found
    ```
2.  **Caso: Archivo de picos vacío.**
    
    -   **Entradas:**

        -   Archivo de picos vacío.
        -   Archivo FASTA del genoma.
        -   Directorio de salida.

    -   **Esperado:** `"Error: the peak file is empty."`

```python
mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/ 
```
  
```
Error: the peak file is empty
```

3.  **Caso: Posiciones `Peak_start` y `Peak_end` fuera del rango del genoma.**
    
    -   **Entradas:**

        -   Archivo de picos con algunas posiciones `Peak_start` y `Peak_end` fuera del tamaño del genoma.
        -   Archivo FASTA del genoma válido.
        -   Directorio de salida.

    -   **Esperado:**

        -   El sistema debe imprimir un mensaje de advertencia: `"Warning: Some peaks are bigger than the genome". Check the log.out file`
        
        -   Generar un archivo de log indicando los picos fuera de rango. El archivo debe contener las líneas del archivo de picos que tienen problemas.

```python
    mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/ 
```

```bash
ls
```

```bash
log.out
fasta_peaks/
```
4. **Caso: ausencia de algún campo en el archivo de entrada, sea `Peak_start` o `Peak_end`.**
	
	- **Entradas:**
	
		- Archivo de picos con los `Peak_start` o `Peak_end` faltantes. 
		- Archivo FASTA del genoma válido.
		- Directorio de salida.

	- **Esperado:**

		- El software ha de imprimir un mensaje, respectivamente, indicando el campo faltante:

```py
mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/		
```
`Error: Peak_start is empty`
`Error: Peak_end is empty`

5. **Caso: Directorio de salida inexistente.**

	 - **Entradas:**
		 
		 - Archivo de picos válido.
		 - Archivo FASTA del genoma válido.
		 - Directorio de salida inexistente.
 
	 - **Esperado:**  `Warning: Output directory does not exist`

```py
mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/
```
```
Warning: Output directory does not exist
```

6. **Caso: Ausencia de algún parámetro en el query.**

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

7. **Caso: Valor de `Peak_end` sea mayor a `Peak_start`.**

	- **Entrada:**
	
		- Archivo de picos con un `Peak_start` menor a `Peak_end`.
		- Archivo FASTA del genoma.
		- Directorio de salida.

	- **Esperado:** `Warning: The peak start or end is not correct`.

```py
mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/
```
```
Warning: The peak start or end is not correct
```
