
# Proyecto de Automatización para la Identificación de Sitios de Unión de Factores de Transcripción en E. coli en experimentos de ChIP-Seq

## Resumen

Este proyecto tiene como objetivo automatizar el proceso de identificación del sitio exacto de unión de los reguladores transcripcionales para 144 factores de transcripción (TFs) en el genoma completo de *Escherichia coli*. Las regiones de unión de estos TFs se han determinado mediante la técnica ChIP-seq.

## Datos Disponibles

### Archivo de Picos
Contiene información sobre las regiones de unión de los 144 factores de transcripción. Se organiza en las siguientes columnas:

- **Dataset_Ids**: Identificadores de los datasets. Cada identificador representa un experimento o condición específica bajo la cual se identificaron los sitios de unión para el TF correspondiente.
- **TF_name**: Nombre del factor de transcripción que se une a la secuencia de ADN especificada.
- **Peak_start**: Posición inicial del pico de unión en el genoma.
- **Peak_end**: Posición final del pico de unión en el genoma.
- **Peak_center**: Posición central del pico de unión en el genoma.
- **Peak_number**: Número secuencial del pico, útil para referencias internas dentro del mismo conjunto de datos.
- **Max_Fold_Enrichment**: Enriquecimiento máximo observado en el pico.
- **Max_Norm_Fold_Enrichment**: Enriquecimiento máximo normalizado.
- **Proximal_genes**: Genes próximos al sitio de unión.
- **Center_position_type**: Tipo de posición central del pico (por ejemplo, intergénica, intrónica, etc.).

### Genoma Completo de E. coli
Disponible en formato FASTA.

## Objetivos del Proyecto

### Generación de Archivos FASTA
Desarrollar un programa que extraiga y compile las secuencias de picos para cada TF en archivos individuales en formato FASTA. Cada archivo representará un regulador específico.

```python
python3 main.py -g ruta_genoma/Ecoli.txt -p ruta_picos/picos.tsv -s resultados/
```

## Colaboración y Recursos

El proyecto pretende facilitar la materia prima para una futura adición del software `meme`:
- Secuencias en formato FASTA de todos los TFs.
- Archivo `U00096.3.fna`.
- URL del repositorio de GitHub donde se aloja el proyecto y el código, facilitando el feedback y las contribuciones de todos los colaboradores.

## Buenas Prácticas de Desarrollo

Para asegurar la calidad y mantenibilidad del software, el proyecto seguirá estas buenas prácticas:

- **Control de Versiones**: Uso de Git para el control de versiones, asegurando una gestión eficaz de los cambios y la colaboración.
- **Revisión de Código**: Implementación de revisiones de código periódicas para mejorar la calidad del software y compartir conocimientos entre el equipo.
- **Documentación Exhaustiva**: Mantener una documentación completa tanto del código como de los procesos operativos, asegurando que cualquier nuevo colaborador pueda integrarse fácilmente.
- **Pruebas Automatizadas**: Desarrollo de pruebas automatizadas para validar la funcionalidad y robustez del software.

## Plan de Implementación

1. **Desarrollo del Extractor de Secuencias**: Programación de la tarea que consiste en genera los archivos FASTA a partir del archivo de picos. Como es un proceso automatizado, todos la información requerida para ejecutar los programas debe ser por línea de comandos.
2. **Integración y Pruebas**: Combinación de los módulos desarrollados y realización de pruebas integrales para asegurar la funcionalidad.
3. **Despliegue y Capacitación**: Implementación del sistema en el servidor del colaborador y capacitación de usuarios sobre su uso.