# Aplicación de Gestión de Encuestas

Este proyecto es una aplicación de escritorio para la gestión de encuestas utilizando Python y Tkinter para la interfaz gráfica, y MySQL para la base de datos.

## Características

- **Agregar Encuestas**: Permite agregar nuevas encuestas a la base de datos.
- **Actualizar Encuestas**: Permite editar encuestas existentes.
- **Eliminar Encuestas**: Permite eliminar encuestas de la base de datos.
- **Filtrar Encuestas**: Permite filtrar encuestas basadas en diferentes criterios.
- **Exportar a Excel**: Permite exportar los datos de las encuestas a un archivo Excel.
- **Mostrar Gráficos**: Permite visualizar gráficos de barras y de pastel basados en los datos de las encuestas.

## Requisitos

- Python 3.13
- MySQL
- Librerías de Python:
  - `tkinter`
  - `pandas`
  - `matplotlib`
  - `pymysql`

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
    ```

2. Instala las dependencias:
    ```sh
    pip install pandas matplotlib pymysql
    ```

3. Configura la base de datos MySQL:
    - Crea una base de datos llamada `encuestas`.
    - Importa el esquema de la base de datos desde el archivo `schema.sql`.

4. Configura la conexión a la base de datos en el archivo `src/main/java/com/empresa/conexionBD.py`:
    ```python
    self.connection = pymysql.connect(host='localhost', user='root', password='curso', db='encuestas')
    ```

## Uso

1. Ejecuta la aplicación:
    ```sh
    python src/main/java/com/empresa/InterfazGUI.py
    ```

2. Utiliza la interfaz gráfica para gestionar las encuestas.

## Estructura del Proyecto

- `src/main/java/com/empresa/InterfazGUI.py`: Interfaz gráfica de la aplicación.
- `src/main/java/com/empresa/conexionBD.py`: Módulo para la conexión a la base de datos.
- `src/main/java/com/empresa/Encuesta.py`: Módulo para la gestión de encuestas.
- `pom.xml`: Archivo de configuración de Maven.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
