class TooltipManager {
    private tooltip: HTMLDivElement | null = null;
    private hideTimeout: number | null = null;

    constructor() {
        this.createTooltip();
    }

    private createTooltip(): void {
        this.tooltip = document.createElement('div');
        this.tooltip.style.position = 'fixed';
        this.tooltip.style.backgroundColor = '#555';
        this.tooltip.style.color = '#fff';
        this.tooltip.style.padding = '5px 10px';
        this.tooltip.style.borderRadius = '4px';
        this.tooltip.style.zIndex = '10000';
        this.tooltip.style.fontSize = '14px';
        this.tooltip.style.pointerEvents = 'auto';
        this.tooltip.style.display = 'none';
        this.tooltip.style.transition = 'opacity 0.3s ease-in-out';
        this.tooltip.style.opacity = '0';

        this.tooltip.addEventListener('mouseenter', this.handleTooltipMouseEnter.bind(this));
        this.tooltip.addEventListener('mouseleave', this.handleTooltipMouseLeave.bind(this));
        document.body.appendChild(this.tooltip);
    }

    show(data: { content: string; target: HTMLElement }): void {
        if (this.hideTimeout) {
            clearTimeout(this.hideTimeout);
        }
        
        if (this.tooltip) {
            this.tooltip.textContent = data.content;
            this.positionTooltip(data.target);
            this.tooltip.style.display = 'block';
            setTimeout(() => {
                if (this.tooltip) this.tooltip.style.opacity = '1';
            }, 100);
        }
    }

    hide(): void {
        if (this.tooltip) {
            this.hideTimeout = window.setTimeout(() => {
                if (this.tooltip) this.tooltip.style.opacity = '0';
            }, 1000) as unknown as number;
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
    const keywords = ['privacy', 'terms', 'cookies', 'legal', 'policy'];

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
        content: 'This is a legal document. Click for more info.',
        target: link
    });
}

function handleLinkMouseOut(event: MouseEvent) {
    const link = event.target as HTMLAnchorElement;
    link.style.backgroundColor = 'transparent';
    tooltipManager.hide();
}

// Run the main function when the content script loads
identifyLegalLinks();

// Re-run the function when the page content changes (e.g., for single-page applications)
const observer = new MutationObserver(identifyLegalLinks);
observer.observe(document.body, { childList: true, subtree: true });