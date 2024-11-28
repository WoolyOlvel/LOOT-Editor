// Intérprete de Código Intermedio en JavaScript
class InterpreterIntermedio {
    constructor() {
        this.variables = {};
        this.funciones = {};
    }

    // Función para concatenar variables
    concatenacion(op1, op2, op3) {
        const resultado = `${op1} ${op2} ${op3}`;
        this.variables['t1'] = resultado;
        return resultado;
    }

    // Función Dividir (Conteo de palabras)
    Dividir(texto) {
        const palabras = texto.split(/\s+/);
        return palabras.length;
    }

    // Función Delete (Eliminación de espacios en blanco)
    Delete(palabra) {
        return palabra.replace(/\s+/g, ' ').trim();
    }

    // Función Split (Tokenización de texto)
    Split(texto) {
        return texto.split(/\s+/);
    }

    // Función Especial (Remoción de caracteres especiales)
    Especial(texto) {
        return texto.replace(/[^a-zA-Z0-9\s]/g, '');
    }

    // Función Number (Extracción de números)
    Number(texto) {
        return texto.match(/\d+/g) || [];
    }

    // Método para imprimir resultados
    print(valor) {
        console.log(valor);
        return valor;
    }

    // Método para ejecutar operaciones
    ejecutar(operacion, ...args) {
        switch(operacion) {
            case 'concatenacion':
                return this.concatenacion(...args);
            case 'Dividir':
                return this.Dividir(...args);
            case 'Delete':
                return this.Delete(...args);
            case 'Split':
                return this.Split(...args);
            case 'Especial':
                return this.Especial(...args);
            case 'Number':
                return this.Number(...args);
            case 'print':
                return this.print(...args);
            default:
                throw new Error(`Operación no reconocida: ${operacion}`);
        }
    }
}

// Ejemplo de uso
const interprete = new InterpreterIntermedio();

// Demostración de las funciones
/* function demoFunciones() {
    console.log("Prueba de funciones:");
    
    // Concatenación
    console.log("Concatenación:");
    const resultadoConcatenacion = interprete.ejecutar('concatenacion', '+', 'palabra', 'palabras', 't1');
    interprete.ejecutar('print', resultadoConcatenacion);
    
    // Conteo de palabras
    console.log("\nConteo de Palabras:");
    const textoConteo = "Hola mundo este es un ejemplo de conteo";
    const resultadoDividir = interprete.ejecutar('Dividir', textoConteo);
    interprete.ejecutar('print', resultadoDividir);
    
    // Delete (Eliminación de espacios)
    console.log("\nEliminación de Espacios:");
    const textoConEspacios = "  Hola   mundo   con   muchos   espacios  ";
    const resultadoDelete = interprete.ejecutar('Delete', textoConEspacios);
    interprete.ejecutar('print', resultadoDelete);
    
    // Split (Tokenización)
    console.log("\nTokenización:");
    const textoSplit = "Hola mundo este es un ejemplo";
    const resultadoSplit = interprete.ejecutar('Split', textoSplit);
    interprete.ejecutar('print', resultadoSplit);
    
    // Especial (Remoción de caracteres especiales)
    console.log("\nRemoción de Caracteres Especiales:");
    const textoEspecial = "Hola, mundo! Este es un ejemplo. Con signos de puntuación.";
    const resultadoEspecial = interprete.ejecutar('Especial', textoEspecial);
    interprete.ejecutar('print', resultadoEspecial);
    
    // Number (Extracción de números)
    console.log("\nExtracción de Números:");
    const textoNumeros = "Tengo 123 manzanas y 456 naranjas";
    const resultadoNumeros = interprete.ejecutar('Number', textoNumeros);
    interprete.ejecutar('print', resultadoNumeros);
} */

// Ejecutar la demostración
/* demoFunciones(); */