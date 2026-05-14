/**
 * termynal.js
 * A lightweight and modern terminal window, with no dependencies.
 * 
 * @author Ines Montani <ines@ines.io>
 * @version 0.0.1
 * @license MIT
 */

class Termynal {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        this.pfx = `data-${options.prefix || 'ty'}`;
        this.startDelay = options.startDelay
            || parseFloat(this.container.getAttribute(`${this.pfx}-startDelay`)) || 600;
        this.typeDelay = options.typeDelay
            || parseFloat(this.container.getAttribute(`${this.pfx}-typeDelay`)) || 90;
        this.lineDelay = options.lineDelay
            || parseFloat(this.container.getAttribute(`${this.pfx}-lineDelay`)) || 1500;
        this.progressLength = options.progressLength
            || parseFloat(this.container.getAttribute(`${this.pfx}-progressLength`)) || 40;
        this.progressChar = options.progressChar
            || this.container.getAttribute(`${this.pfx}-progressChar`) || '█';
        this.progressPercent = options.progressPercent
            || parseFloat(this.container.getAttribute(`${this.pfx}-progressPercent`)) || 100;
        this.cursor = options.cursor
            || this.container.getAttribute(`${this.pfx}-cursor`) || '▋';
        this.showInitialContent = options.showInitialContent !== false;
        this.init();
    }

    init() {
        this.lines = [...this.container.querySelectorAll(`[${this.pfx}]`)].filter(line => 
            line.hasAttribute(this.pfx)
        );
        this.container.style.display = 'block';
        this.container.setAttribute('data-termynal', '');
        
        // Mostrar contenido inicial inmediatamente
        if (this.showInitialContent) {
            this.showInitialLines();
        } else {
            this.container.innerHTML = '';
        }
        
        this.start();
    }

    showInitialLines() {
        // Mostrar las primeras líneas sin animación
        const initialLines = this.lines.slice(0, 3); // Mostrar las primeras 3 líneas
        this.container.innerHTML = '';
        
        initialLines.forEach(line => {
            const clonedLine = line.cloneNode(true);
            clonedLine.removeAttribute(`${this.pfx}-cursor`);
            this.container.appendChild(clonedLine);
        });
    }

    async start() {
        await this._wait(this.startDelay);

        // Si ya mostramos contenido inicial, empezar desde la línea 4
        const startIndex = this.showInitialContent ? 3 : 0;
        
        for (let i = startIndex; i < this.lines.length; i++) {
            const line = this.lines[i];
            const type = line.getAttribute(this.pfx);
            const delay = line.getAttribute(`${this.pfx}-delay`) || this.lineDelay;

            if (type == 'input') {
                line.setAttribute(`${this.pfx}-cursor`, this.cursor);
                await this.type(line);
                await this._wait(delay);
            }

            else if (type == 'progress') {
                await this.progress(line);
                await this._wait(delay);
            }

            else {
                this.container.appendChild(line);
                await this._wait(delay);
            }

            line.removeAttribute(`${this.pfx}-cursor`);
        }
    }

    async type(line) {
        const chars = [...line.textContent];
        const delay = line.getAttribute(`${this.pfx}-typeDelay`) || this.typeDelay;
        line.textContent = '';
        this.container.appendChild(line);

        for (let char of chars) {
            await this._wait(delay);
            line.textContent += char;
        }
    }

    async progress(line) {
        const progressLength = line.getAttribute(`${this.pfx}-progressLength`) || this.progressLength;
        const progressChar = line.getAttribute(`${this.pfx}-progressChar`) || this.progressChar;
        const chars = progressChar.repeat(progressLength);
        const progressPercent = line.getAttribute(`${this.pfx}-progressPercent`) || this.progressPercent;
        line.textContent = '';
        this.container.appendChild(line);

        for (let i = 1; i < chars.length + 1; i++) {
            await this._wait(this.typeDelay);
            const percent = Math.round(i / chars.length * 100);
            line.textContent = `${chars.slice(0, i)} ${percent}%`;
            if (percent > progressPercent) {
                break;
            }
        }
    }

    _wait(time) {
        return new Promise(resolve => setTimeout(resolve, time));
    }
}

/**
 * Auto-initialize Termynal if data-termynal is present
 */
document.addEventListener('DOMContentLoaded', () => {
    const containers = document.querySelectorAll('[data-termynal]');
    containers.forEach(container => new Termynal(container, { showInitialContent: true }));
});