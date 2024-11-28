// Función para ejecutar el código interpretado
function ejecutarCodigo(codigo, readonly_editor) {
    const variables = {};
    const funciones = {};
    let enFuncion = false;
    let funcionActual = null;
    const lineas = codigo.split('\n');

    for (let i = 0; i < lineas.length; i++) {
        const linea = lineas[i].trim();
        if (linea) {
            // Simulación de inserción en editor (ajusta según tu implementación)
            readonly_editor.value += '\n';
        }

        // Procesar la declaración de una variable
        if (linea.startsWith('txt ')) {
            const partes = linea.split('=');
            if (partes.length === 2) {
                const nombreVar = partes[0].split()[1].trim();
                const valor = partes[1].trim().replace(/^"|"$/g, '');
                variables[nombreVar] = valor;
                readonly_editor.value += '\n';
            }
        }

        // Procesar la declaración de una función
        else if (linea.startsWith('Funcion ')) {
            const funcionNombre = linea.split()[1].split('(')[0];
            const param = linea.split('(')[1].split(')')[0];
            funciones[funcionNombre] = { param: param, codigo: [] };
            enFuncion = true;
            funcionActual = funcionNombre;
            readonly_editor.value += '\n';
        }

        // Función Delete
        else if (enFuncion && funcionActual === "Delete") {
            if (linea === "Retornar(palabra)") {
                const palabra = variables[param.trim()] || "";
                const resultadoDelete = palabra.split(/\s+/).join(' ');
                variables[param.trim()] = resultadoDelete;
                readonly_editor.value += resultadoDelete + '\n';
            }
        }

        // Función Split
        else if (enFuncion && funcionActual === "Split") {
            if (linea === "Retornar(palabra)") {
                const palabra = (variables[param.trim()] || "").trim();
                const resultadoSplit = palabra.split(/\s+/);
                variables[param.trim()] = resultadoSplit.join(', ');
                readonly_editor.value += variables[param.trim()] + '\n';
            }
        }

        // Función Especial
        else if (enFuncion && funcionActual === "Especial") {
            if (linea === "Retornar(palabra)") {
                const palabra = (variables[param.trim()] || "").trim();
                const resultadoEspecial = palabra.replace(/[^a-zA-Z0-9]/g, '');
                variables[param.trim()] = resultadoEspecial;
                readonly_editor.value += resultadoEspecial + '\n';
            }
        }

        // Función Number
        else if (enFuncion && funcionActual === "Number") {
            if (linea === "Retornar(palabra)") {
                const palabra = (variables[param.trim()] || "").trim();
                const numeros = palabra.split(/\s+/).filter(num => /^\d+$/.test(num));
                variables[param.trim()] = numeros.join(', ');
                readonly_editor.value += variables[param.trim()] + '\n';
            }
        }

        // Procesar la impresión
        else if (linea.startsWith('Imprimir')) {
            const contenido = linea.match(/\(([^)]+)\)/)[1];
            let resultado = "";

            // Manejar concatenación
            if (contenido.includes('+')) {
                const partesConcatenadas = contenido.split('+');
                const resultadoConcatenado = partesConcatenadas.map(parte => {
                    parte = parte.trim();
                    return variables[parte] || parte.replace(/^"|"$/g, '');
                });
                resultado = resultadoConcatenado.join(' ');
            } else {
                const partes = contenido.split(',').map(p => p.trim());
                let conteo = 0;

                resultado = partes.map(parte => {
                    if (variables[parte]) return variables[parte];
                    if (parte === 'Dividir' && funciones['Dividir']) {
                        const param = funciones['Dividir'].param;
                        if (variables[param]) {
                            const texto = variables[param];
                            conteo = texto.split(/\s+/).length;
                            return conteo.toString();
                        }
                        return "Error: Variable para Dividir no encontrada";
                    }
                    return parte.replace(/^"|"$/g, '');
                }).join(' ');
            }

            readonly_editor.value += resultado.trim() + '\n';
        }

        // Procesar el final de la función
        else if (linea === 'Fin') {
            enFuncion = false;
            funcionActual = null;
            readonly_editor.value += '\n';
        }
    }
}