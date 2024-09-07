class TooltipManager {
    private tooltip: HTMLDivElement | null = null;
    private hideTimeout: number | null = null;

    constructor() {
        this.createTooltip();
    }

    private createTooltip(): void {
        this.tooltip = document.createElement('div');
        this.tooltip.id = 'legal-tooltip';
        this.tooltip.style.position = 'fixed';
        this.tooltip.style.backgroundColor = '#555';
        this.tooltip.style.color = '#fff';
        this.tooltip.style.padding = '10px';
        this.tooltip.style.borderRadius = '4px';
        this.tooltip.style.zIndex = '10000';
        this.tooltip.style.fontSize = '14px';
        this.tooltip.style.pointerEvents = 'auto';
        this.tooltip.style.display = 'none';
        this.tooltip.style.transition = 'opacity 0.3s ease-in-out';
        this.tooltip.style.opacity = '0';
        this.tooltip.style.width = '250px';
        this.tooltip.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';

        this.tooltip.innerHTML = `
            <div id="tooltip-content" style="margin-bottom: 10px;">Placeholder Content</div>
            <div style="display: flex; justify-content: space-between;">
                <button id="tooltip-dismiss" style="background: none; border: none; color: #fff; cursor: pointer;">Dismiss</button>
                <button id="tooltip-see-more" style="background: none; border: none; color: #fff; cursor: pointer;">See more</button>
            </div>
        `;

        const dismissButton = this.tooltip.querySelector('#tooltip-dismiss');
        const seeMoreButton = this.tooltip.querySelector('#tooltip-see-more');

        if (dismissButton) {
            dismissButton.addEventListener('click', () => this.hideImmediately());
        }

        if (seeMoreButton) {
            seeMoreButton.addEventListener('click', () => {
                console.log('See more clicked');
            });
        }

        this.tooltip.addEventListener('mouseenter', this.handleTooltipMouseEnter.bind(this));
        this.tooltip.addEventListener('mouseleave', this.handleTooltipMouseLeave.bind(this));
        document.body.appendChild(this.tooltip);
    }

    async show(data: { target: HTMLElement; url: string }): Promise<void> {
        if (this.hideTimeout) {
            clearTimeout(this.hideTimeout);
        }
        
        if (this.tooltip) {
            const contentDiv = document.getElementById('tooltip-content');
            if (contentDiv) {
                contentDiv.textContent = 'Loading summary...';
            }
            this.positionTooltip(data.target);
            this.tooltip.style.display = 'block';
            setTimeout(() => {
                if (this.tooltip) this.tooltip.style.opacity = '1';
            }, 100);

            try {
                const summary = await this.fetchSummary(data.url);
                if (contentDiv) {
                    contentDiv.textContent = summary.user_friendly_summary;
                }
            } catch (error) {
                console.error('Failed to fetch summary:', error);
                if (contentDiv) {
                    contentDiv.textContent = 'Failed to load summary.';
                }
            }
        }
    }

    private async fetchSummary(url: string): Promise<any> {
        console.log('Fetching summary for', url);
        const response = await fetch('http://127.0.0.1:8000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    }

    hide(): void {
        this.hideTimeout = window.setTimeout(() => {
            this.hideImmediately();
        }, 1000);
    }

    private hideImmediately(): void {
        if (this.tooltip) {
            this.tooltip.style.opacity = '0';
            setTimeout(() => {
                if (this.tooltip) this.tooltip.style.display = 'none';
            }, 300);
        }
        if (this.hideTimeout) {
            clearTimeout(this.hideTimeout);
            this.hideTimeout = null;
        }
    }

    private handleTooltipMouseEnter(): void {
        if (this.hideTimeout) {
            clearTimeout(this.hideTimeout);
            this.hideTimeout = null;
        }
    }

    private handleTooltipMouseLeave(): void {
        this.hide();
    }

    private positionTooltip(target: HTMLElement): void {
        if (!this.tooltip) return;

        const targetRect = target.getBoundingClientRect();
        const tooltipRect = this.tooltip.getBoundingClientRect();

        let top = targetRect.top - tooltipRect.height - 10;
        let left = targetRect.left + (targetRect.width / 2) - (tooltipRect.width / 2);

        // Adjust if tooltip would go off the top of the screen
        if (top < 0) {
            top = targetRect.bottom + 10;
        }

        // Adjust if tooltip would go off the left or right of the screen
        if (left < 10) left = 10;
        if (left + tooltipRect.width > window.innerWidth - 10) {
            left = window.innerWidth - tooltipRect.width - 10;
        }

        this.tooltip.style.top = `${top}px`;
        this.tooltip.style.left = `${left}px`;
    }
}

const tooltipManager = new TooltipManager();

function identifyLegalLinks() {
    const highlightedHrefs:Set<string> = new Set();
    const links = document.querySelectorAll('a');
    const keywords = ['privacy', 'terms', 'cookie', 'legal', 'policy'];

    for (let i = 0; i < links.length; i++) {
        const link = links[i];
        const href = link.href;
        const linkText = link.textContent?.toLowerCase() || '';

        if (keywords.some(word => linkText.includes(word) && href && !highlightedHrefs.has(href))) {
            highlightLinks(link);
            highlightedHrefs.add(link.href);
        }
    }
}

function highlightLinks(link: HTMLAnchorElement) {    
    link.style.background = 'linear-gradient(to right, #8e2de2, #4a00e0)';
    link.style.backgroundSize = '100% 3px';
    link.style.backgroundRepeat = 'no-repeat';
    link.style.backgroundPosition = '0 100%';
    link.style.paddingBottom = '2px';
    link.style.transition = 'background-size 0.2s ease-in-out';

    link.addEventListener('mouseover', handleLinkMouseOver);
    link.addEventListener('mouseout', handleLinkMouseOut);
}

function handleLinkMouseOver(event: MouseEvent) {
    const link = event.target as HTMLAnchorElement;
    link.style.backgroundColor = 'rgba(142, 45, 226, 0.1)';
    tooltipManager.show({
        target: link,
        url: link.href
    });
}

function handleLinkMouseOut(event: MouseEvent) {
    const link = event.target as HTMLAnchorElement;
    link.style.backgroundColor = 'transparent';
    tooltipManager.hide();
}

identifyLegalLinks();

// Re-run the function when the page content changes (e.g., for single-page applications)
const observer = new MutationObserver(identifyLegalLinks);
observer.observe(document.body, { childList: true, subtree: true });