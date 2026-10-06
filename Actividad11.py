

#Actividad 11. Analizador de complejidad (y Analizador de Autómatas)
#Estudiante: Rogelio Sotomayor Carrasco
#No. de cuenta: 195721
#Programa: Ingeniería en Sistemas Computacionales
#Universidad: IBERO Puebla


import re
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import PlainTextResponse, JSONResponse

app = FastAPI(title="Backend: Analizador de Autómatas y Complejidad")

#analizador de atomatas

#definicion de tokens simulando las transiciones de un Autómata Finito
TOKEN_REGEX = [
    ('RESERVADA', r'\b(if|else|while|for|return|def|int|float|class|print|in|range)\b'),
    ('NUMERO', r'\b\d+(\.\d+)?\b'),
    ('IDENTIFICADOR', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('OPERADOR', r'[\+\-\*/=<>!]+'),
    ('SIMBOLO', r'[():;{},\[\]]'),
    ('ESPACIO', r'\s+'),
    ('DESCONOCIDO', r'.')
]

@app.post("/api/automata/analizar")
async def analizar_automata(file: UploadFile = File(...)):
    contenido = (await file.read()).decode("utf-8")
    tokens_encontrados = []
    
    # Ensamblar la expresión regular global
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_REGEX)
    
    for mo in re.finditer(tok_regex, contenido):
        tipo = mo.lastgroup
        valor = mo.group()
        
        if tipo == 'ESPACIO':
            continue
        elif tipo == 'DESCONOCIDO':
            tokens_encontrados.append({"tipo": "ERROR_LEXICO", "valor": valor})
        else:
            tokens_encontrados.append({"tipo": tipo, "valor": valor})
            
    return JSONResponse(content={"tokens": tokens_encontrados})

#analizador de complejidad

def calcular_complejidad(codigo: str, notacion: str) -> str:
    lineas = codigo.split("\n")
    lineas_procesadas = []
    complejidades_encontradas = set()
    grado_maximo = 0
    
    #pila para controlar el anidamiento
    pila_ciclos = []

    for linea in lineas:
        texto_limpio = linea.strip()
        
        if not texto_limpio or texto_limpio.startswith("#"):
            lineas_procesadas.append(linea)
            continue
            
        indentacion = len(linea) - len(linea.lstrip(' '))
        
        #sacar ciclos cerrados de la pila
        while pila_ciclos and pila_ciclos[-1][0] >= indentacion:
            pila_ciclos.pop()

        #deteccion heurística de operaciones iterativas
        if texto_limpio.startswith("for ") or texto_limpio.startswith("while "):
            pila_ciclos.append([indentacion, 1.0])
            
        #deteccion de operaciones logarítmicas
        if "// 2" in texto_limpio or "/ 2" in texto_limpio:
            if pila_ciclos:
                pila_ciclos[-1][1] = 0.5 # Reclasifica a O(log n)

    
        suma_actual = sum(c[1] for c in pila_ciclos)
        grado_maximo = max(grado_maximo, suma_actual)

        #formateo asint0tico
        if suma_actual == 0:
            comp_str = f"{notacion}(1)"
        elif suma_actual == 0.5:
            comp_str = f"{notacion}(log n)"
        elif suma_actual == 1.0:
            comp_str = f"{notacion}(n)"
        elif suma_actual == 1.5:
            comp_str = f"{notacion}(n log n)"
        else:
            comp_str = f"{notacion}(n^{int(suma_actual)})"

        complejidades_encontradas.add(comp_str)
        linea_sin_salto = linea.replace('\n', '').replace('\r', '')
        lineas_procesadas.append(f"{linea_sin_salto:<50} # {comp_str}")

    #determinar complejidad dominante
    if grado_maximo == 0:
        mayor = f"{notacion}(1)"
    elif grado_maximo == 0.5:
        mayor = f"{notacion}(log n)"
    elif grado_maximo == 1.0:
        mayor = f"{notacion}(n)"
    elif grado_maximo == 1.5:
        mayor = f"{notacion}(n log n)"
    else:
        mayor = f"{notacion}(n^{int(grado_maximo)})"

    resumen = "\n\n" + "="*65 + "\n"
    resumen += "RESUMEN DE COMPLEJIDAD IDENTIFICADA\n"
    resumen += "="*65 + "\n"
    resumen += f"Suma de complejidades individuales: {' + '.join(sorted(complejidades_encontradas))}\n"
    resumen += f"Complejidad de mayor grado: {mayor}\n"
    resumen += "="*65 + "\n"

    return "\n".join(lineas_procesadas) + resumen

@app.post("/api/complejidad/big-o", response_class=PlainTextResponse)
async def endpoint_big_o(file: UploadFile = File(...)):
    contenido = (await file.read()).decode("utf-8")
    return calcular_complejidad(contenido, "O")

@app.post("/api/complejidad/big-omega", response_class=PlainTextResponse)
async def endpoint_big_omega(file: UploadFile = File(...)):
    contenido = (await file.read()).decode("utf-8")
    return calcular_complejidad(contenido, "Ω")
