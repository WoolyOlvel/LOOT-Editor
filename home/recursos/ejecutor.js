const interpreter = new InterpreterIntermedio();

// Function to execute code from the editor
function executeCode() {
    // Clear previous terminal output
    const terminalContent = document.getElementById('terminal-content');
    terminalContent.innerHTML = '';

    // Capture the code from the editor
    const editor = document.getElementById('code-editor');
    const code = Array.from(editor.children)
        .map(line => line.textContent.trim())
        .filter(line => line.length > 0)
        .join('\n');

    // Redirect console.log to terminal output
    const originalConsoleLog = console.log;
    console.log = function(...args) {
        const output = args.map(arg => 
            typeof arg === 'object' ? JSON.stringify(arg) : arg
        ).join(' ');
        
        const outputElement = document.createElement('div');
        outputElement.textContent = output;
        terminalContent.appendChild(outputElement);
        
        originalConsoleLog.apply(console, args);
    };

    try {
        // Execute the code in a try-catch block
        const lines = code.split('\n');
        lines.forEach(line => {
            // Basic parsing of function calls
            const functionMatch = line.match(/^(\w+)\((.*)\)$/);
            if (functionMatch) {
                const funcName = functionMatch[1];
                const args = functionMatch[2].split(',').map(arg => {
                    // Remove quotes and trim
                    arg = arg.replace(/^['"]|['"]$/g, '').trim();
                    return arg;
                });

                // Execute the function using the interpreter
                try {
                    const result = interpreter.ejecutar(funcName, ...args);
                } catch (err) {
                    console.log(`Error executing ${funcName}: ${err.message}`);
                }
            }
        });
    } catch (error) {
        // Display any execution errors
        const errorElement = document.createElement('div');
        errorElement.textContent = `Error: ${error.message}`;
        errorElement.style.color = 'red';
        terminalContent.appendChild(errorElement);
    } finally {
        // Restore original console.log
        console.log = originalConsoleLog;
    }
}

// Add event listener to the "Ejecutar" button
document.addEventListener('DOMContentLoaded', () => {
    const executeButton = document.querySelector('a.btn-soft-dark:nth-child(2)');
    if (executeButton) {
        executeButton.addEventListener('click', executeCode);
    }
});