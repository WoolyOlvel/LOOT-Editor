import tkinter as tk
import customtkinter as ctk
from customtkinter import CTk
from PIL import Image, ImageTk  # Necesario para cargar y manejar imágenes
import re
import ply.lex as lex
import ply.yacc as yacc
from tabulate import tabulate
# Definir tokens válidos y sus expresiones regulares
tokens_validos = {
    'IDENTIFICADOR': r'^txt',
    'ESPACIO': r'^ +',
    'IGUALDAD': r'^=',
    'VARIABLE': r'[a-z]{1,10}',
    'COMILLA': r'^"',
    'CADENA': r'^[a-zA-Z][a-zA-Z0-9\s\.,;:!?"\']*?(?=")',
    'PARENTESIS_DE_ABERTURA': r'\(',
    'PARENTESIS_DE_CERRADURA': r'\)',
    'TIPO_DE_FUNCION': r'Dividir|Delete|Split|Especial|Number',
    'PALABRA_RESERVADA': r'Retornar',
    'IMPRIMIR': r'Imprimir',
    'FIN_DE_LA_FUNCION': r'Fin',
    'FUNCION': r'Funcion',
    'COMENTARIO': r'^#.*?(?=\s|$)',
    'CONCATENACION': r'\+',
    'DOS_PUNTOS': r'\:',
    'SALTOS': r'\n',
    'TABULACION': r'\t',
    'COMA': r'^,',
    'NUMERO': r'\d+(\.\d+)?'
}
def scanner(sentencia):
    tokens = []
    pos = 0
    if sentencia == '':
        return [('ERROR', 'Espacio vacío', 'Error: La sentencia está vacía')]
    
    lines = sentencia.split('\n')
    for line_num, line in enumerate(lines, 1):
        pos = 0
        while pos < len(line):
            token_encontrado = False
            for nombre, patron in tokens_validos.items():
                match = re.match(patron, line[pos:])
                if match:
                    token_valor = match.group(0)
                    if nombre == 'CADENA':
                        # Asegurarse de que las cadenas estén entre comillas
                        if token_valor.startswith('"') and token_valor.endswith('"'):
                            tokens.append((nombre, token_valor, line_num))
                        else:
                            # Si no está entre comillas, lo tratamos como un token diferente
                            tokens.append(('TEXTO_SIN_COMILLAS', token_valor, line_num))
                    elif nombre not in ['ESPACIO', 'SALTOS', 'TABULACION']:
                        tokens.append((nombre, token_valor, line_num))
                    pos += len(token_valor)
                    token_encontrado = True
                    break
            
            if not token_encontrado:
                tokens.append(('ERROR', line[pos], f'Error: Carácter "{line[pos]}" no válido en la línea {line_num}, posición {pos}'))
                pos += 1
    
    return tokens
# Definición de la gramática y el análisis sintáctico
tokens = (
    'IDENTIFICADOR',
    'ESPACIO',
    'IGUALDAD',
    'VARIABLE',
    'COMILLA',
    'CADENA',
    'PARENTESIS_DE_ABERTURA',
    'PARENTESIS_DE_CERRADURA',
    'TIPO_DE_FUNCION',
    'PALABRA_RESERVADA',
    'FIN_DE_LA_FUNCION',
    'FUNCION',
    'COMENTARIO',
    'CONCATENACION',
    'DOS_PUNTOS',
    'SALTOS',
    'TABULACION',
    'COMA',
    'NUMERO',
)
# Expresiones regulares para los tokens
t_IDENTIFICADOR = r'^txt'
t_ESPACIO = r'\s+'
t_IGUALDAD = r'^='
t_VARIABLE = r'[a-z]{1,10}'
t_COMILLA = r'^"'
t_CADENA = r'^[ -~ñ]*?(?=")'
t_PARENTESIS_DE_ABERTURA = r'\('
t_PARENTESIS_DE_CERRADURA = r'\)'
t_TIPO_DE_FUNCION = r'Dividir|Delete|Split|Especial|Number'
t_PALABRA_RESERVADA = r'Imprimir|Retornar'
t_FIN_DE_LA_FUNCION = r'Fin'
t_FUNCION = r'Funcion'
t_COMENTARIO = r'^\#.*?(?=\s|$)'
t_CONCATENACION = r'\+'
t_DOS_PUNTOS = r'\:'
t_SALTOS = r'\n'
t_TABULACION = r'\t'
t_COMA = r'^,'
t_NUMERO = r'\d+(\.\d+)?'
# Ignorar espacios en blanco y tabulaciones
t_ignore = ''
# Manejo de errores de tokens no válidos
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)
# Construcción del analizador léxico
lexer = lex.lex()
# Reglas de precedencia
precedence = (
    ('left', 'CONCATENACION'),
)
# Definición de la gramática
def p_start(p):
    '''
    start : statement
    '''
    pass  # Implementar lógica adicional aquí si es necesario
def p_statement(p):
    '''
    statement : IDENTIFICADOR IGUALDAD expression
              | FUNCION expression
              | PALABRA_RESERVADA expression
              | COMENTARIO
    '''
   
    if len(p) == 4:  # Para asignación de variable
        identificador = p[1]  # Esto debe ser 'txt'
        variable = p[2]       # La variable proporcionada por el usuario
        valor = p[3]          # El valor que se asigna
        # Verificar si el identificador es 'txt'
        if identificador != 'txt':
            print(f"Error: El identificador '{identificador}' debe ser 'txt'.")
            return
        # Verificar si la variable ya está en la tabla de símbolos
        if variable in tabla_simbolos:
            print(f"Error: La variable '{variable}' ya ha sido declarada.")
        else:
            # Asegurarse de que el valor asignado es una cadena (CADENA)
            if isinstance(valor, str):  # Comprobación del tipo
                tabla_simbolos[variable] = valor.strip('"')  # Asignar el tipo correcto a la variable
                print(f"Variable '{variable}' asignada con valor: '{tabla_simbolos[variable]}'")
            else:
                print(f"Error: Asignación de tipo incompatible a la variable '{variable}'.")
    elif len(p) == 2:  # Para comentarios
        print("Comentario:", p[1])
def p_expression(p):
    '''
    expression : VARIABLE
               | CADENA
               | NUMERO
               | expression CONCATENACION expression
    '''
    if len(p) == 2:
        p[0] = p[1]  # Asigna el valor directamente si es VARIABLE o CADENA
    elif len(p) == 4:
        p[0] = p[1] + p[3]  # Manejo de concatenación
# Manejo de errores de sintaxis
def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)
# Construcción del analizador sintáctico
parser = yacc.yacc()
# Función para realizar la derivación
def parse_input(input_str):
    return parser.parse(input_str)
# Tabla de símbolos global
tabla_simbolos = {}


def verificar_semantica(tokens):
    errores_semanticos = []
    variables_definidas = {}
    funciones_definidas = {}
    esperando_fin = False
    dentro_funcion = False
    
    palabras_reservadas = ['Funcion', 'Fin', 'txt', 'Imprimir', 'Dividir', 'Split', 'Number']
    

    i = 0
    while i < len(tokens):
        token = tokens[i]
        var_name = None
    
    # Actualizar el número de línea
        if token[0] == 'SALTOS':
            linea_actual += 1
            i += 1
            continue
        
        # Verificar declaración de variables
        if token[0] == 'IDENTIFICADOR' and token[1] == 'txt':
            if i + 2 < len(tokens) and tokens[i + 1][0] == 'VARIABLE' and tokens[i + 2][0] == 'IGUALDAD':
                var_name = tokens[i + 1][1]
                if var_name in palabras_reservadas:
                    errores_semanticos.append((tokens[i+1][2], f"Se está utilizando la palabra reservada '{var_name}' como nombre de variable, lo cual es un error semántico."))
                else:
                    valor_tokens = []
                    j = i + 3 

                    while j < len(tokens) and tokens[j][0] not in ['SALTOS', 'COMENTARIO']:
                        valor_tokens.append(tokens[j])
                        j += 1
                    
                    if valor_tokens:
                        valor = ' '.join(token[1] for token in valor_tokens)
                        
                    # Verificar si el valor es un número
                    if valor_tokens[0][0] == 'NUMERO':
                        errores_semanticos.append((tokens[i][2], f"Se está asignando un número en lugar de una cadena de texto a '{var_name}'."))

                    # Verificar si el valor es una cadena válida (entre comillas dobles)
                    elif (valor_tokens[0][0] == 'CADENA' or 
                          (valor.startswith('"') or valor.endswith('"')) and
                          'VARIABLE'):
                        variables_definidas[var_name] = ''
                    else:
                        errores_semanticos.append((tokens[i][2], f"El valor asignado a '{var_name}' no es una cadena de texto válida."))

            else:
                errores_semanticos.append((tokens[i][2], f"Falta el valor para la variable o has puesto una palabra reservada.")) 
                i += 1  # Incrementar aquí para evitar bucles infinitos
            


        elif token[0] == 'CONCATENACION':
          if i- 1 >= 0 and i + 1 < len(tokens):
            # Obtener los valores de var1 y var2
            var1 = tokens[i-1][1] if i-1 >= 0 else None
            var2 = tokens[i+1][1] if i+1 < len(tokens) else None
        
        # Verificar si var1 es una cadena literal o una variable definida
            es_literal_var1 = var1.startswith('"') and var1.endswith('"')
            es_literal_var2 = var2.startswith('"') and var2.endswith('"')

          if not es_literal_var1 and (var1 not in variables_definidas or variables_definidas[var1] != 'txt'):
            errores_semanticos.append((token[2], f"Error: {var1} debe ser una variable de tipo txt o una cadena literal para concatenar."))

        # Verificar si var2 es una cadena literal o una variable definida
          if not es_literal_var2 and (var2 not in variables_definidas or variables_definidas[var2] != 'txt'):
            errores_semanticos.append((token[2], f"Error: {var2} debe ser una variable de tipo txt o una cadena literal para concatenar."))


       

                 
                 
        elif token[0] == 'FUNCION':
          dentro_funcion = True
          esperando_fin = True
          if i + 1 < len(tokens) and tokens[i + 1][0] == 'VARIABLE':
           nombre_funcion = tokens[i + 1][1]
        
        # Verifica si el nombre de la función es Dividir
           if nombre_funcion == 'Dividir':
            if i + 2 < len(tokens) and tokens[i + 2][0] == 'PARENTESIS_DE_ABERTURA':
                if i + 3 < len(tokens) and tokens[i + 3][0] == 'VARIABLE' and tokens[i + 3][1] == 'txt':
                    funciones_definidas[nombre_funcion] = {'params': ['txt']}
                else:
                      errores_semanticos.append((token[2], f"Falta el parámetro txt en la declaración de la función '{nombre_funcion}'."))    
            else:
                errores_semanticos.append((token[2], "Falta el nombre de la función después de 'Funcion'."))
         

        # Verificar fin de función
        elif token[0] == 'FIN_DE_LA_FUNCION':
            if esperando_fin:
                dentro_funcion = False
                esperando_fin = False
    

        # Verificar uso de operaciones y variables no definidas
        elif token[0] in ['TIPO_DE_FUNCION', 'PALABRA_RESERVADA']:
            if token[1] == 'Imprimir':
                if i + 2 < len(tokens) and tokens[i + 1][0] == 'PARENTESIS_DE_ABERTURA' and tokens[i + 2][0] == 'VARIABLE':
                    var_name = tokens[i + 2][1]
                    if var_name not in variables_definidas:
                        errores_semanticos.append((tokens[i][2], f"Se está intentando imprimir la variable '{var_name}' que no ha sido definida previamente."))
            else:
                if i + 1 < len(tokens) and tokens[i + 1][0] == 'VARIABLE':
                    var_name = tokens[i + 1][1]
                    if var_name not in variables_definidas:
                        errores_semanticos.append((token[2], f"Se está utilizando la variable '{var_name}' en una operación, pero no ha sido definida previamente."))
                    elif variables_definidas[var_name] != 'txt':
                        errores_semanticos.append((token[2], f"Las operaciones requieren variables de tipo txt. La variable '{var_name}' no es de tipo txt."))

        # Verificar asignación de funciones que retornan listas a variables txt
        elif token[0] == 'FUNCION':
            if i - 1 >= 0 and i + 1 < len(tokens):
                var_asignada = tokens[i-1][1]
                funcion_llamada = tokens[i+1][1]
                if var_asignada in variables_definidas and variables_definidas[var_asignada] == 'txt':
                    if funcion_llamada in ['Dividir', 'Split', 'Number']:
                        errores_semanticos.append((token[2], f"Las funciones que retornan listas no pueden ser asignadas directamente a variables de tipo txt: '{funcion_llamada}'."))

        # Añadir variables a variables_definidas cuando se declaran
        if token[0] == 'VARIABLE' and i > 0 and tokens[i-1][1] == 'txt':
            variables_definidas[token[1]] = 'txt'

        i += 1  # Incrementar siempre al final del bucle
    
    if esperando_fin:
        errores_semanticos.append((tokens[-1][2], "Falta 'Fin' al final de la función."))
    
    return errores_semanticos



# Clase para manejar la generación de código intermedio
class GeneradorCodigoIntermedio:
    def __init__(self):
        self.codigo_intermedio = []
        self.temp_counter = 1
        self.variables = {}
        self.tripleta_counter = 1
        self.en_funcion = False
        self.nombre_funcion = None
        self.funciones = {}

    def nuevo_temporal(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def nueva_tripleta(self):
        num = self.tripleta_counter
        self.tripleta_counter += 1
        return f"#{num}"

    def generar_codigo(self, tokens):
        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Manejo de asignación con 'txt'
            if token[0] == 'IDENTIFICADOR' and token[1] == 'txt':
                if i + 2 < len(tokens) and tokens[i + 1][0] == 'VARIABLE' and tokens[i + 2][0] == 'IGUALDAD':
                    var_name = tokens[i + 1][1]
                    
                    # Manejar asignación de cadena
                    if i + 3 < len(tokens) and tokens[i + 3][0] == 'CADENA':
                        literal = tokens[i + 3][1]
                        temp = self.nuevo_temporal()
                        
                        tripleta1 = self.nueva_tripleta()
                        self.codigo_intermedio.append(f"{tripleta1}: (=, \"{literal}\", {temp})")
                        
                        tripleta2 = self.nueva_tripleta()
                        self.codigo_intermedio.append(f"{tripleta2}: (=, {tripleta1}, {var_name})")
                        
                        self.variables[var_name] = temp
                        i += 4
                        continue

            # Manejo de concatenación
            elif token[0] == 'CONCATENACION' and token[1] == '+':
                # Manejar concatenación de cadenas literales
                if (i - 1 >= 0 and tokens[i - 1][0] == 'CADENA' and 
                    i + 1 < len(tokens) and tokens[i + 1][0] == 'CADENA'):
                    var1 = tokens[i - 1][1]  # Primer cadena literal
                    var2 = tokens[i + 1][1]  # Segunda cadena literal
                    temp = self.nuevo_temporal()
                    
                    tripleta_concat = self.nueva_tripleta()
                    self.codigo_intermedio.append(f"{tripleta_concat}: (+, \"{var1}\", \"{var2}\", {temp})")
                    
                    tripleta_print = self.nueva_tripleta()
                    self.codigo_intermedio.append(f"{tripleta_print}: (print, {temp}, _)")

                    i += 2
                    continue
                
                # Manejar concatenación de variables
                elif (i - 1 >= 0 and tokens[i - 1][0] == 'VARIABLE' and 
                      i + 1 < len(tokens) and tokens[i + 1][0] == 'VARIABLE'):
                    var1 = tokens[i - 1][1]  # Primer operando
                    var2 = tokens[i + 1][1]  # Segundo operando
                    temp = self.nuevo_temporal()  # Temporal para el resultado de la concatenación
                    
                    tripleta_concat = self.nueva_tripleta()
                    self.codigo_intermedio.append(f"{tripleta_concat}: (+, {var1}, {var2}, {temp})")
                    
                    tripleta_print = self.nueva_tripleta()
                    self.codigo_intermedio.append(f"{tripleta_print}: (print, {temp}, _)")

                    i += 2  # Avanzamos al siguiente token después de la concatenación
                    continue

            # Manejo de funciones
            if token[0] == 'FUNCION':
                self.en_funcion = True
                # Obtener nombre de la función
                nombre_funcion = tokens[i + 1][1]
                self.nombre_funcion = nombre_funcion
                tripleta_func = self.nueva_tripleta()
                self.codigo_intermedio.append(f"{tripleta_func}: (Funcion, {nombre_funcion}, _)")
                
                # Procesar parámetros de la función si los hay
                if i + 2 < len(tokens) and tokens[i + 2][0] == 'VARIABLE':
                    parametro = tokens[i + 2][1]
                    self.funciones[nombre_funcion] = parametro

            # Retorno dentro de la función
            if token[0] == 'PALABRA_RESERVADA' and token[1] == 'Retornar':
                if i + 1 < len(tokens):
                    # Obtener la variable a retornar
                    var_retornada = tokens[i + 1][1]
                    
                    # Si es una cadena literal
                    if tokens[i + 1][0] == 'CADENA':
                        var_retornada = f"\"{var_retornada}\""
                    
                    tripleta_retornar = self.nueva_tripleta()
                    self.codigo_intermedio.append(f"{tripleta_retornar}: (return, {var_retornada}, _)")
                    
                    # Imprimir el valor retornado
                    tripleta_imprimir = self.nueva_tripleta()
                    self.codigo_intermedio.append(f"{tripleta_imprimir}: (print, {var_retornada}, _)")
                
                i += 2
                continue

            # Manejo de Imprimir
            if token[0] == 'FUNCION' and token[1] == 'Imprimir':
                # Manejar diferentes tipos de impresión
                if i + 1 < len(tokens):
                    # Imprimir cadena literal
                    if tokens[i + 1][0] == 'CADENA':
                        valor = tokens[i + 1][1]
                        tripleta_imprimir = self.nueva_tripleta()
                        self.codigo_intermedio.append(f"{tripleta_imprimir}: (print, \"{valor}\", _)")
                    
                    # Imprimir variable
                    elif tokens[i + 1][0] == 'VARIABLE':
                        valor = tokens[i + 1][1]
                        tripleta_imprimir = self.nueva_tripleta()
                        self.codigo_intermedio.append(f"{tripleta_imprimir}: (print, {valor}, _)")
                    
                    i += 2
                    continue

            # Cierre de la función
            if token[0] == 'FIN_DE_LA_FUNCION':
                tripleta_fin = self.nueva_tripleta()
                if self.nombre_funcion:
                    self.codigo_intermedio.append(f"{tripleta_fin}: (Fin, {self.nombre_funcion}, _)")
                self.en_funcion = False
                self.nombre_funcion = None
                i += 1
                continue

            i += 1

    def optimizar_codigo(self):
        """
        Método de optimización mejorado que aplica múltiples técnicas de optimización
        """
        # Aplicar optimizaciones en secuencia
        self.eliminacion_codigo_muerto()  # Eliminar código muerto primero
        self.reducir_temporales()  # Reducir temporales
        self.reordenamiento_codigo()  # Reordenar código
        
        # Optimización base original
        codigo_optimizado = []
        skip_next = False
        
        for i in range(len(self.codigo_intermedio)):
            if skip_next:
                skip_next = False
                continue
                
            actual = self.codigo_intermedio[i]
            
            # Si hay siguiente instrucción
            if i + 1 < len(self.codigo_intermedio):
                siguiente = self.codigo_intermedio[i + 1]
                
                # Eliminar asignaciones redundantes
                if ":" in actual and ":" in siguiente:
                    actual_parts = actual.split(': ')[1].strip('()')
                    siguiente_parts = siguiente.split(': ')[1].strip('()')
                    
                    if actual_parts.startswith('=') and siguiente_parts.startswith('='):
                        temp_actual = actual_parts.split(',')[2].strip()
                        temp_siguiente = siguiente_parts.split(',')[1].strip()
                        
                        if temp_actual == temp_siguiente:
                            valor_original = actual_parts.split(',')[1].strip()
                            var_destino = siguiente_parts.split(',')[2].strip()
                            tripleta = actual.split(':')[0]
                            codigo_optimizado.append(f"{tripleta}: (=, {valor_original}, {var_destino})")
                            skip_next = True
                            continue
            
            codigo_optimizado.append(actual)
            
        self.codigo_intermedio = codigo_optimizado

    def reducir_temporales(self):
        """
        Optimización de reducción de temporales
        """
        ultima_referencia = {}
        referencias_reemplazadas = {}

        # Primera pasada: encontrar la última referencia de cada temporal
        for i, linea in enumerate(self.codigo_intermedio):
            if ':' in linea:
                partes = linea.split(': ')[1].strip('()')
                partes = [p.strip() for p in partes.split(',')]
                
                # Buscar temporales en la línea
                for j, parte in enumerate(partes):
                    if parte.startswith('t'):
                        ultima_referencia[parte] = i

        # Segunda pasada: optimizar y reemplazar temporales
        codigo_optimizado = []
        for i, linea in enumerate(self.codigo_intermedio):
            if ':' in linea:
                tripleta, codigo = linea.split(': ')
                codigo = codigo.strip('()')
                partes = [p.strip() for p in codigo.split(',')]
                
                # Reemplazar temporales si es posible
                for j, parte in enumerate(partes):
                    if parte.startswith('t'):
                        # Si este temporal ya no es la última referencia, intentar reemplazarlo
                        if ultima_referencia.get(parte, -1) != i:
                            # Buscar un reemplazo más reciente o definitivo
                            for temp, ultima_ref in ultima_referencia.items():
                                if temp != parte and ultima_ref > ultima_referencia.get(parte, -1):
                                    partes[j] = temp
                                    referencias_reemplazadas[parte] = temp
                                    break
                
                # Reconstruir la línea
                nuevo_codigo = f"({', '.join(partes)})"
                codigo_optimizado.append(f"{tripleta}: {nuevo_codigo}")
            else:
                codigo_optimizado.append(linea)
        
        self.codigo_intermedio = codigo_optimizado
        return referencias_reemplazadas

    def reordenamiento_codigo(self):
        """
        Optimización por Reordenamiento
        """
        definiciones = {}
        usos = {}
        codigo_reordenado = []
        instrucciones_procesadas = set()

        # Primera pasada: identificar definiciones y usos
        for i, linea in enumerate(self.codigo_intermedio):
            if ':' in linea:
                tripleta, codigo = linea.split(': ')
                codigo = codigo.strip('()')
                partes = [p.strip() for p in codigo.split(',')]
                
                # Identificar operaciones de asignación
                if codigo.startswith('='):
                    variable = partes[-1]
                    definiciones[variable] = (i, linea)
                
                # Identificar usos de variables
                for parte in partes:
                    if parte.startswith('t') or (parte not in ['_', 'print', 'return', 'Funcion', 'Fin']):
                        if parte not in usos:
                            usos[parte] = []
                        usos[parte].append(i)

        # Estrategia de reordenamiento
        for i, linea in enumerate(self.codigo_intermedio):
            if i in instrucciones_procesadas:
                continue
            
            if ':' in linea:
                tripleta, codigo = linea.split(': ')
                codigo = codigo.strip('()')
                partes = [p.strip() for p in codigo.split(',')]
                
                # Priorizar instrucciones de función y retorno
                if codigo.startswith(('Funcion', 'Fin', 'return')):
                    codigo_reordenado.append(linea)
                    instrucciones_procesadas.add(i)
                
                # Reordenar asignaciones cerca de su primer uso
                elif codigo.startswith('='):
                    variable = partes[-1]
                    primer_uso = min(usos.get(variable, [float('inf')]))
                    
                    if primer_uso != float('inf'):
                        # Insertar cerca del primer uso
                        insert_index = min(len(codigo_reordenado), primer_uso)
                        codigo_reordenado.insert(insert_index, linea)
                    else:
                        codigo_reordenado.append(linea)
                    
                    instrucciones_procesadas.add(i)
                
                # Otras instrucciones
                else:
                    codigo_reordenado.append(linea)
                    instrucciones_procesadas.add(i)

        # Agregar cualquier instrucción no procesada
        for i, linea in enumerate(self.codigo_intermedio):
            if i not in instrucciones_procesadas:
                codigo_reordenado.append(linea)

        self.codigo_intermedio = codigo_reordenado

    def eliminacion_codigo_muerto(self):
        """
        Eliminación de Código Muerto
        """
        variables_utilizadas = set()
        codigo_sin_muerto = []

        # Identificar variables utilizadas
        for linea in self.codigo_intermedio:
            if ':' in linea:
                codigo = linea.split(': ')[1].strip('()')
                partes = [p.strip() for p in codigo.split(',')]
                
                # Considerar variables en operaciones
                for parte in partes[1:]:  # Ignorar el operador
                    if parte not in ['_', 'print', 'return', 'Funcion', 'Fin']:
                        variables_utilizadas.add(parte)

        # Filtrar código
        for linea in self.codigo_intermedio:
            if ':' in linea:
                tripleta, codigo = linea.split(': ')
                codigo = codigo.strip('()')
                partes = [p.strip() for p in codigo.split(',')]
                
                # Mantener instrucciones críticas
                if (codigo.startswith(('Funcion', 'Fin', 'return', 'print')) or 
                    # Mantener asignaciones a variables utilizadas
                    (codigo.startswith('=') and partes[-1] in variables_utilizadas) or
                    # Mantener operaciones con variables utilizadas
                    any(parte in variables_utilizadas for parte in partes[1:])):
                    codigo_sin_muerto.append(linea)

        self.codigo_intermedio = codigo_sin_muerto

    def guardar_codigo(self, archivo_salida):
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write("Código Intermedio (Código Optimizado):\n\n")
            for linea in self.codigo_intermedio:
                f.write(linea + '\n')





# Ejemplo de uso
def ejecutar_codigo():
    codigo = editor.get("1.0", tk.END)
    tokens = scanner(codigo)

    # Verificación semántica
    errores_semanticos = verificar_semantica(tokens)

    # Limpiar el editor de solo lectura
    readonly_editor.configure(state="normal")
    readonly_editor.delete("1.0", tk.END)

    if errores_semanticos:
        for linea, error in errores_semanticos:
            readonly_editor.insert(tk.END, f"Error Línea {linea}: {error}\n")
    else:
        readonly_editor.insert(tk.END, "No se encontraron errores semánticos.\n\n")


         # Generar código intermedio
        generador = GeneradorCodigoIntermedio()
        generador.generar_codigo(tokens)
        
        # Optimizar el código
        #generador.optimizar_codigo()
        
        # Guardar el código intermedio en un archivo
        generador.guardar_codigo("codigo_optimizado.cio")
        
        readonly_editor.insert(tk.END, "Código intermedio generado y optimizado correctamente.\n")
        readonly_editor.insert(tk.END, "Se ha guardado en 'codigo_optimizado.cio'\n\n")
        
        # Mostrar el código intermedio en el editor
        readonly_editor.insert(tk.END, "Código Intermedio:\n")
        for linea in generador.codigo_intermedio:
            
            readonly_editor.insert(tk.END, f"{linea}\n")

        # Ejecutar el código
        variables = {}
        funciones = {}
        en_funcion = False
        funcion_actual = None
        lineas = codigo.split('\n')
        i = 0

        while i < len(lineas):
            linea = lineas[i].strip()
            if linea:
                readonly_editor.insert(tk.END, f"")

            # Procesar la declaración de una variable
            if linea.startswith('txt '):
                partes = linea.split('=')
                if len(partes) == 2:
                    nombre_var = partes[0].split()[1].strip()
                    valor = partes[1].strip().strip('"')
                    variables[nombre_var] = valor
                    readonly_editor.insert(tk.END, f"")

            # Procesar la declaración de una función
            elif linea.startswith('Funcion '):
                funcion_nombre = linea.split()[1].split('(')[0]
                param = linea.split('(')[1].split(')')[0]
                funciones[funcion_nombre] = {'param': param, 'codigo': []}
                en_funcion = True
                funcion_actual = funcion_nombre
                readonly_editor.insert(tk.END, f"")

            # Agregar el código de la función Delete
            elif en_funcion and funcion_actual == "Delete":
                if linea == "Retornar(palabra)":
                    palabra = variables.get(param.strip(), "").strip()
                    resultado_delete = ' '.join(palabra.split())  # Eliminar espacios en blanco
                    variables[param.strip()] = resultado_delete  # Actualizar la variable con el resultado
                    readonly_editor.insert(tk.END, f"{resultado_delete}")

            # Agregar el código de la función Split
            elif en_funcion and funcion_actual == "Split":
                if linea == "Retornar(palabra)":
                    palabra = variables.get(param.strip(), "").strip()
                    # Tokenizar el texto
                    resultado_split = palabra.split()  # Separar por espacios
                    # Actualizar la variable con la lista de tokens (como cadena)
                    variables[param.strip()] = ', '.join(resultado_split)  # Guardar como cadena separada por comas
                    readonly_editor.insert(tk.END, f"{variables[param.strip()]}")

            # Agregar el código de la función Especial
            elif en_funcion and funcion_actual == "Especial":
                if linea == "Retornar(palabra)":
                    palabra = variables.get(param.strip(), "").strip()
                    # Remoción de caracteres especiales
                    resultado_especial = ''.join(char for char in palabra if char.isalnum())  # Mantiene solo caracteres alfanuméricos
                    variables[param.strip()] = resultado_especial  # Actualizar la variable con el resultado
                    readonly_editor.insert(tk.END, f"{resultado_especial}")

            # Agregar el código de la función Number
            elif en_funcion and funcion_actual == "Number":
                if linea == "Retornar(palabra)":
                    palabra = variables.get(param.strip(), "").strip()
                    # Extraer los números
                    numeros = [num for num in palabra.split() if num.isdigit()]  # Filtrar solo los números
                    variables[param.strip()] = ', '.join(numeros)  # Guardar como cadena separada por comas
                    readonly_editor.insert(tk.END, f"{variables[param.strip()]}")

            # Procesar la impresión (antes de 'Fin')
            elif linea.startswith('Imprimir'):
                contenido = linea[linea.index('(')+1:linea.rindex(')')]
                # Manejar la concatenación (uso del símbolo '+')
                if '+' in contenido:
                    partes_concatenadas = contenido.split('+')
                    resultado_concatenado = []
                    for parte in partes_concatenadas:
                        parte = parte.strip()
                        if parte in variables:
                            resultado_concatenado.append(str(variables[parte]).strip())
                        else:
                            resultado_concatenado.append(parte.strip('"'))
                    resultado = ' '.join(resultado_concatenado).strip()
                else:
                    partes = [p.strip() for p in contenido.split(',')]
                    resultado = " "

                    conteo = 0  # Inicializar conteo

                    for parte in partes:
                        parte = parte.strip()
                        if parte in variables:
                            resultado += str(variables[parte]).strip() + ' '  # Agregar el valor de la variable al resultado
                        elif parte == 'Dividir':
                            if 'Dividir' in funciones:
                                param = funciones['Dividir']['param']
                                if param in variables:
                                    texto = variables[param]
                                    palabras = texto.split()
                                    conteo = len(palabras)  # Calcular el conteo aquí
                                    resultado += f" {conteo} "  # Agregar conteo
                                else:
                                    resultado += "Error: Variable para Dividir no encontrada "
                            else:
                                resultado += "Error: Función Dividir no definida "
                        else:
                            resultado += parte.strip('"') + ' '  # Agregar cadena entre comillas

                # Aquí se imprime el resultado completo
                readonly_editor.insert(tk.END, f"{resultado.strip()}")  # Quitar espacios adicionales

            # Procesar el final de la función
            elif linea == 'Fin':
                en_funcion = False
                funcion_actual = None
                readonly_editor.insert(tk.END, "")

            i += 1

    # Guardar en archivo (mantener esta parte si es necesaria)
    ruta_archivo = r"C:\\Users\\puc-a\\Downloads\\EDITOR-LOOT_ACTUALIZADO\\EDITOR-LOOT_ACTUALIZADO\\tabla_simbolos.txt"
    with open(ruta_archivo, 'w') as f:
        f.write(tabulate(tokens, headers=['Token', 'Valor', 'Línea'], tablefmt='plain'))



# Crear la GUI
# Función para actualizar los números de línea
def update_line_numbers(event=None):
    # Obtener el índice de la última línea visible
    last_visible_line_index = editor.index("@0,%d" % editor.winfo_height())
    last_visible_line = int(last_visible_line_index.split('.')[0])
    
    line_numbers_text = ""
    for i in range(1, last_visible_line + 1):
        line_numbers_text += f"{i}\n"
    
    # Actualizar el texto en la caja de números de línea
    line_numbers.configure(state="normal")
    line_numbers.delete("1.0", "end")
    line_numbers.insert("1.0", line_numbers_text)
    line_numbers.configure(state="disabled")
 
# Configuración de la ventana principal
root = CTk()
root.title("LOOT")
root.geometry("800x600")
root.attributes('-transparentcolor', 'grey')

# Crear un marco superior para simular un "nav"
top_frame = ctk.CTkFrame(root, height=50, width=800, fg_color="gray20")
top_frame.pack(side="top", fill="x")

# Crear el texto en la parte superior izquierda
label_texto = ctk.CTkLabel(top_frame, text="Editor De Texto De LOOT", font=("Arial", 16), text_color="white")
label_texto.place(x=10, y=10)

# Cargar un ícono para el botón "Ejecutar"
icon_image = Image.open("EDITOR-LOOT_ACTUALIZADO\play.png")
icon_image = icon_image.resize((40, 40))
icon_tk = ImageTk.PhotoImage(icon_image)

# Crear el botón de ejecutar con un ícono a la izquierda
boton_ejecutar = ctk.CTkButton(top_frame, text=" Ejecutar", image=icon_tk, compound="left", command=lambda: ejecutar_codigo(), corner_radius=10, fg_color="gray20", hover_color="gray30")
boton_ejecutar.pack(side="right", padx=10, pady=10)

# Crear el editor de texto principal con bordes iluminados
editor_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=10)
editor_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 20))

# Crear un Canvas para los números de línea
line_numbers = ctk.CTkTextbox(editor_frame, width=30, fg_color="gray20", text_color="white", state="disabled", border_color="gray50", border_width=2)
line_numbers.pack(side="left", fill="y", padx=(5, 0), pady=10)

# Crear el editor de texto sin scrollbar
editor = ctk.CTkTextbox(editor_frame, height=30, width=80, fg_color="gray20", text_color="white", border_color="gray50", border_width=2, wrap="none")
editor.pack(side="right", fill="both", expand=True, padx=5, pady=10)

# Vincular eventos de actualización de números de línea al editor
editor.bind("<KeyRelease>", update_line_numbers)
editor.bind("<MouseWheel>", update_line_numbers)
editor.bind("<Return>", update_line_numbers)
editor.bind("<BackSpace>", update_line_numbers)
editor.bind("<Control-v>", update_line_numbers)
editor.bind("<Control-z>", update_line_numbers)

# Crear un nuevo frame en la parte inferior para el editor de solo lectura
readonly_frame = ctk.CTkFrame(root, fg_color="LightGray", corner_radius=10)
readonly_frame.pack(side="bottom", fill="x", padx=45, pady=(0, 20))

# Crear una caja de texto de solo lectura dentro del nuevo frame
readonly_editor = ctk.CTkTextbox(readonly_frame, height=100, width=800, fg_color="gray20", text_color="white", border_color="gray50", border_width=2)
readonly_editor.pack(fill="both", expand=True, padx=10, pady=10)

# Hacer que la caja de texto sea de solo lectura
readonly_editor.configure(state="disabled")

# Inicializar los números de línea
update_line_numbers()


# Ejecutar la ventana principal
root.mainloop()