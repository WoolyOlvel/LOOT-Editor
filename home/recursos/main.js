class MainJsGenerator {
    constructor(interpreter, printToTerminal) {
        this.interpreter = interpreter;
        this.printToTerminal = printToTerminal;
    }

    generarYEjecutarCodigo(codigo) {
        const terminalContent = document.getElementById('terminal-content');
        terminalContent.innerHTML = ''; // Limpiar terminal

        const lineas = codigo.split('\n');
        let funcionActual = null;
        let operacion = null;
        let textoActual = null;

        const imprimirEnAmbos = (mensaje, escodigo = false) => {
            // Imprimir en terminal de interfaz
            const outputElement = document.createElement('div');
            outputElement.textContent = mensaje;
            if (escodigo) {
                outputElement.style.color = 'blue';
            }
            terminalContent.appendChild(outputElement);

            // Imprimir en consola del navegador
            console.log(mensaje);
        };

        // Nueva función para dividir en sílabas
        const dividirSilabas = (texto) => {
            // Implementación simple de división de sílabas
            const vocales = 'aeiouáéíóú';
            const silabas = [];
            let silabaActual = '';

            for (let i = 0; i < texto.length; i++) {
                silabaActual += texto[i];

                // Condiciones para cortar sílaba
                if (i + 1 < texto.length && 
                    vocales.includes(texto[i]) && 
                    !vocales.includes(texto[i+1])) {
                    silabas.push(silabaActual);
                    silabaActual = '';
                }
            }

            // Agregar la última sílaba si quedó algo
            if (silabaActual.length > 0) {
                silabas.push(silabaActual);
            }

            return silabas;
        };

        for (let linea of lineas) {
            linea = linea.trim();
            
            const matchTexto = linea.match(/txt\s*=\s*"([^"]*)"/);
            const matchOperacion = linea.match(/\(([^,]+),\s*([^,]+),\s*([^,)]+)\)/);
            
            if (matchTexto) {
                textoActual = matchTexto[1];
            }

            if (matchOperacion) {
                const [, comando, param1, param2] = matchOperacion;

                switch (comando) {
                    case '+':
                        // Concatenación
                        const concatenado = `${param1} ${param2}`;
                        imprimirEnAmbos(`Código: Concatenación(${param1}, ${param2})`, true);
                        imprimirEnAmbos(`Resultado: ${concatenado}`);
                        break;
                    case 'Funcion':
                        if (param1 === 'Silvi') {
                            funcionActual = 'Silvi';
                            operacion = 'Silvi';
                        } else {
                            funcionActual = param1;
                            operacion = param1;
                        }
                        break;
                    case 'print':
                        if (funcionActual) {
                            if (param1 === 't1') {
                                // Imprimir variable t1
                                imprimirEnAmbos(`Código: print(t1)`, true);
                                imprimirEnAmbos(`Resultado: ${concatenado}`);
                            } else {
                                const codigoEjemplo = `${operacion}("${textoActual}")`;
                                imprimirEnAmbos(`Código: ${codigoEjemplo}`, true);
                                
                                try {
                                    let resultado;
                                    if (operacion === 'Silvi') {
                                        // Implementación específica para Silvi
                                        resultado = dividirSilabas(textoActual);
                                        imprimirEnAmbos(`Resultado de Silvi: ${JSON.stringify(resultado)}`);
                                    } else {
                                        resultado = this.interpreter.ejecutar(operacion, textoActual);
                                        imprimirEnAmbos(`Resultado: ${JSON.stringify(resultado)}`);
                                    }
                                } catch (error) {
                                    imprimirEnAmbos(`Error: ${error.message}`);
                                }
                            }
                        }
                        break;
                    case 'Fin':
                        funcionActual = null;
                        operacion = null;
                        break;
                }
            }
        }
    }
}

// El resto del código permanece igual
function executeCode() {
    const interpreter = new InterpreterIntermedio();
    const mainJsGenerator = new MainJsGenerator(interpreter, (message, isCode) => {
        const terminalContent = document.getElementById('terminal-content');
        const outputElement = document.createElement('div');
        outputElement.textContent = message;
        if (isCode) {
            outputElement.style.color = 'blue';
        }
        terminalContent.appendChild(outputElement);
    });

    const editor = document.getElementById('code-editor');
    const code = Array.from(editor.children)
        .map(line => line.textContent.trim())
        .filter(line => line.length > 0)
        .join('\n');

    try {
        mainJsGenerator.generarYEjecutarCodigo(code);
    } catch (error) {
        const terminalContent = document.getElementById('terminal-content');
        const errorElement = document.createElement('div');
        errorElement.textContent = `Error: ${error.message}`;
        errorElement.style.color = 'red';
        terminalContent.appendChild(errorElement);
        console.error(error);
    }
}

// Asegurar que el evento de ejecución esté vinculado
document.addEventListener('DOMContentLoaded', () => {
    const executeButton = document.querySelector('a.btn-soft-dark:nth-child(2)');
    if (executeButton) {
        executeButton.addEventListener('click', executeCode);
    }
});