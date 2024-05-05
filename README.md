# Requisitos para la ejecución

## Python 3.11

Este programa fue desarrollado y probado en Python 3.11.9. Aunque puede funcionar en versiones anteriores de Python 3.10, se recomienda ejecutarlo en Python 3.11.1 o versiones posteriores para garantizar la compatibilidad y el correcto funcionamiento.

## Librerías Necesarias

Para mostrar los resultados de la ejecución del analizador sintáctico, se utilizaron las librerías **tabulate** y **anytree**.

Además, dado que la lectura de la matriz de transiciones se realiza a través de un archivo .xlsx, se utilizó la librería **pandas** para esto.

Por lo tanto, será necesario (en caso de no tenerlas en el sistema) instalar estas librerías. Puedes hacerlo ejecutando los siguientes comandos en la consola del sistema:

```sh
pip install pandas
pip install tabulate
pip install anytree
```

# Requisitos para un funcionamiento deseado

El programa **solo acepta** lectura de *archivos de texto*, es decir, con extensión **.txt**.

Además, es necesario que los *archivos de texto* a analizar  se encuentren en el mismo directorio que los archivos **main.py**, **functions.py** y **Transitions.xlsx**.


# Forma de ejecutar el programa

Ya teniendo en un mismo directorio los archivos:
- **main.py**
- **functions.py**
- **Transitions.xlsx**
- **falak.txt** (ejemplo de archivo a analizar)

Para ejecutar el programa se deben seguir los siguientes pasos:
1. Abrir la consola/terminal del ordenador.
2. Ejecutar el archivo **main.py** en la terminal de la siguiente forma:
    ```sh
    $ python .\main.py
    ```
3. Se solicitará el nombre del archivo a analizar, este deberá de ser escrito sin la extensión .txt, es decir, solo el nombre del archivo:
    ```sh
     $ python .\main.py
     Nombre del programa: falak
    ```
4. Si el programa contenido en el archivo de texto no presenta errores, se mostrará en la terminal el árbol sintáctico de este. Véase un ejemplo a continuación:
    1. Archivo Falak:
    ```txt
    <# a
    #>

    # CEM

    var A;
    ```
    2. Arból sintáctico:
    ```sh
    PROGRAM
    └── DEF_LIST
        ├── DEF_LIST
        └── DEF
            └── VAR_DEF
                ├── var_kwd
                ├── VAR_LIST
                │   └── ID_LIST
                │       ├── ID
                │       └── ID_LIST_CONT
                └── limit_op
    ```
    En caso de presentar errores, se mostrará lo siguiente:
    ```sh
    Error en la línea 6 con un caracter inesperado.
    Se terminó el código de manera inesperada
    Posibles caracteres: ['limit_op', 'coma_op', 'bracket2_op']
    Revisar la documentación para más información sobre el error. 
    Los posibles caracteres no indican el error específico.
    ```