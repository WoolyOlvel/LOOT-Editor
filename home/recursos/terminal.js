const editor = document.getElementById('code-editor');
        const terminalContent = document.getElementById('terminal-content');
        let maxLine = 0;

        function syncScroll() {
            document.getElementById("line-numbers").scrollTop = editor.scrollTop;
        }

        function updateLineNumbers() {
            const lineCount = editor.children.length;
            document.getElementById("line-numbers").innerHTML = Array.from(
                {length: lineCount}, 
                (_, i) => i + 1
            ).join('<br>');
        }

        function getCurrentLineElement() {
            const selection = window.getSelection();
            if (!selection.rangeCount) return null;
            
            let node = selection.getRangeAt(0).startContainer;
            while (node && !node.classList?.contains('code-line')) {
                node = node.parentNode;
            }
            return node;
        }

        function getLineNumber(element) {
            return Array.from(editor.children).indexOf(element);
        }

        function updateEditableLines() {
            maxLine = Math.max(maxLine, editor.children.length - 1);
            Array.from(editor.children).forEach((line, index) => {
                if (index <= maxLine) {
                    line.classList.remove('inactive-line');
                } else {
                    line.classList.add('inactive-line');
                }
            });
        }

        function insertTab(element) {
            const selection = window.getSelection();
            const range = selection.getRangeAt(0);
            const tabNode = document.createTextNode('    ');
            range.insertNode(tabNode);
            range.setStartAfter(tabNode);
            range.setEndAfter(tabNode);
            selection.removeAllRanges();
            selection.addRange(range);
        }

        function handleKeyDown(event) {
            const currentLine = getCurrentLineElement();
            if (!currentLine) return;

            const currentLineNumber = getLineNumber(currentLine);

            if (event.key === 'Tab') {
                event.preventDefault();
                if (currentLineNumber <= maxLine) {
                    insertTab(currentLine);
                }
                return;
            }

            if (currentLine.classList.contains('inactive-line')) {
                event.preventDefault();
                return;
            }

            if (event.key === 'Enter') {
                event.preventDefault();
                if (currentLineNumber === 0 && editor.children.length > 1) {
                    // Si estamos en la línea 1 y ya existe una línea 2
                    const newLine = document.createElement('div');
                    newLine.className = 'code-line';
                    editor.insertBefore(newLine, editor.children[1]);
                } else if (currentLineNumber === editor.children.length - 1) {
                    const newLine = document.createElement('div');
                    newLine.className = 'code-line';
                    editor.appendChild(newLine);
                }
                
                const range = document.createRange();
                range.setStart(editor.children[currentLineNumber + 1], 0);
                range.collapse(true);
                const selection = window.getSelection();
                selection.removeAllRanges();
                selection.addRange(range);
                
                maxLine = Math.max(maxLine, editor.children.length - 1);
                updateLineNumbers();
                updateEditableLines();
            } else if (event.key === 'Backspace') {
                const selection = window.getSelection();
                const range = selection.getRangeAt(0);
                
                if (currentLine.textContent === '' && editor.children.length > 1) {
                    event.preventDefault();
                    const prevLine = currentLine.previousElementSibling;
                    currentLine.remove();
                    
                    if (prevLine) {
                        const range = document.createRange();
                        range.selectNodeContents(prevLine);
                        range.collapse(false);
                        const selection = window.getSelection();
                        selection.removeAllRanges();
                        selection.addRange(range);
                    }
                    
                    maxLine = editor.children.length - 1;
                    updateLineNumbers();
                    updateEditableLines();
                } else if (range.startOffset === 4 && /^\s{4}/.test(currentLine.textContent)) {
                    // Si hay 4 espacios al inicio y el cursor está justo después de ellos
                    event.preventDefault();
                    currentLine.textContent = currentLine.textContent.substring(4);
                    range.setStart(currentLine, 0);
                    range.collapse(true);
                    selection.removeAllRanges();
                    selection.addRange(range);
                }
            }
        }

        function handleInput() {
            if (editor.children.length === 0) {
                const newLine = document.createElement('div');
                newLine.className = 'code-line';
                editor.appendChild(newLine);
            }
            updateLineNumbers();
            updateEditableLines();
        }

        function handlePaste(event) {
            event.preventDefault();
            
            const currentLine = getCurrentLineElement();
            if (!currentLine || currentLine.classList.contains('inactive-line')) return;
            
            const text = event.clipboardData.getData('text/plain');
            const lines = text.split('\n');
            
            if (lines.length === 1) {
                document.execCommand('insertText', false, text);
            } else if (getLineNumber(currentLine) === editor.children.length - 1) {
                lines.forEach((line, index) => {
                    if (index === 0) {
                        document.execCommand('insertText', false, line);
                    } else {
                        const newLine = document.createElement('div');
                        newLine.className = 'code-line';
                        newLine.textContent = line;
                        editor.appendChild(newLine);
                    }
                });
            }
            
            updateLineNumbers();
            updateEditableLines();
        }

        function handleClick(event) {
            const clickedLine = getCurrentLineElement();
            if (clickedLine) {
                const lineNumber = getLineNumber(clickedLine);
                if (lineNumber > maxLine) {
                    event.preventDefault();
                    return false;
                }
            }
        }

        function clearTerminal() {
            terminalContent.textContent = '';
        }

        // Inicialización
        window.addEventListener('load', () => {
            const firstLine = document.createElement('div');
            firstLine.className = 'code-line';
            editor.innerHTML = '';
            editor.appendChild(firstLine);
            maxLine = 0;
            updateLineNumbers();
            updateEditableLines();
            editor.focus();

            const range = document.createRange();
            range.setStart(firstLine, 0);
            range.collapse(true);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
        });