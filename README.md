

# Actividad 11: Backend Integrado - Analizador de Autómatas y Complejidad
**Estudiante:** Rogelio Sotomayor Carrasco
**No. de cuenta:** 195721
**Programa:** Ingeniería en Sistemas Computacionales
**Universidad:** IBERO Puebla

Este repositorio contiene el código fuente de un backend desarrollado con FastAPI que integra dos módulos de análisis de código fuente: un analizador léxico (basado en la teoría de autómatas) y un analizador heurístico de complejidad asintótica temporal.

## Módulo 1: Analizador de Autómatas
Este módulo simula un Autómata Finito Determinista (AFD) mediante expresiones regulares para clasificar los componentes léxicos de un código fuente.

### Endpoint: Analizador Léxico
- **Método y Ruta:** `POST /api/automata/analizar`
- **Descripción:** Recibe un archivo de código fuente y extrae los tokens clasificándolos en categorías como palabras reservadas, identificadores, números, operadores y símbolos.
- **Input:** Archivo en formato `multipart/form-data` (clave: `file`).
- **Output:** Objeto `JSON` que contiene un arreglo de diccionarios, donde cada elemento detalla el `tipo` de token detectado y su `valor` textual original. Registra caracteres no reconocidos bajo la etiqueta `ERROR_LEXICO`.

## Módulo 2: Analizador de Complejidad (Actividad 11)
Este módulo evalúa la estructura de un código fuente para determinar su tasa de crecimiento asintótico mediante heurísticas de indentación y detección de operaciones matemáticas clave.

### Endpoint: Analizador del Peor Caso (Big-O)
- **Método y Ruta:** `POST /api/complejidad/big-o`
- **Descripción:** Analiza el código línea por línea y devuelve el mismo código comentado con la complejidad superior $O(g(n))$ de cada instrucción, finalizando con un bloque de resumen.
- **Input:** Archivo en formato `multipart/form-data` (clave: `file`).
- **Output:** Texto plano (`PlainTextResponse`) formateado con los resultados del análisis.

### Endpoint: Analizador del Mejor Caso (Big-Omega)
- **Método y Ruta:** `POST /api/complejidad/big-omega`
- **Descripción:** Aplica la misma heurística de rastreo de ciclos y saltos, pero formatea la salida utilizando la notación de cota inferior $\Omega(g(n))$.
- **Input:** Archivo en formato `multipart/form-data` (clave: `file`).
- **Output:** Texto plano con la salida expresada en notación Omega.

## Lógica Heurística del Analizador de Complejidad
El algoritmo rastrea el flujo de ejecución mediante una **Pila de Indentación** que evalúa el nivel de anidamiento de cada línea:
1. **Detección Lineal $O(n)$:** Identifica estructuras de control iterativas (`for`, `while`). Por defecto, la apertura de un ciclo añade un grado lineal a la suma temporal.
2. **Detección Polinomial $O(n^k)$:** Si un ciclo se anida dentro de otro (detectado por un incremento en los espacios de indentación respecto al ciclo padre), los grados se suman para reflejar complejidades cuadráticas o superiores.
3. **Detección Logarítmica $O(\log n)$:** El motor busca patrones de partición del espacio de búsqueda (ej. división entera `// 2`). Si esta instrucción ocurre dentro del ámbito de un ciclo, el analizador actualiza el valor de ese ciclo en la pila para representarlo como logarítmico, identificando exitosamente algoritmos como la Búsqueda Binaria.
4. **Resumen de Grado Máximo:** Al terminar la lectura del archivo, el sistema evalúa todas las cotas registradas y extrae el término dominante para dictaminar la complejidad general del programa.

