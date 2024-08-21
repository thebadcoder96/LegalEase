// Function to identify and color ToS/PP links
function identifyLegalLinks() {
    const links = document.querySelectorAll('a');
    const keywords = ['privacy', 'terms', 'cookies', 'legal', 'policy'];

    for (let i = 0; i < links.length; i++) {
        const link = links[i];
        const linkText = link.textContent?.toLowerCase() || '';

        if (keywords.some(word => linkText.includes(word))) {
            highlightLinks(link);
        }
    }
}

function highlightLinks(link: HTMLAnchorElement) {
    link.style.border = '2px solid #4CAF50';
    link.style.padding = '2px 5px';
    link.style.borderRadius = '3px';
    link.style.textDecoration = 'none';
    link.style.color = '#4CAF50';
    
    // Add event listener for hover effect
    // link.addEventListener('mouseover', showTooltip);
    // link.addEventListener('mouseout', hideTooltip);
}


// Function to show tooltip
// function showTooltip(event: MouseEvent) {
//     const link = event.target as HTMLAnchorElement;
//     const tooltip = document.createElement('div');
//     tooltip.textContent = 'This is a legal document. Click for more info.';
//     tooltip.style.position = 'absolute';
//     tooltip.style.backgroundColor = '#555';
//     tooltip.style.color = '#fff';
//     tooltip.style.padding = '5px';
//     tooltip.style.borderRadius = '6px';
//     tooltip.style.zIndex = '1000';
//     tooltip.style.fontSize = '14px';

//     document.body.appendChild(tooltip);

//     const linkRect = link.getBoundingClientRect();
//     tooltip.style.left = `${linkRect.left}px`;
//     tooltip.style.top = `${linkRect.bottom + 5}px`;

//     link.dataset.tooltip = 'active';
// }

// // Function to hide tooltip
// function hideTooltip(event: MouseEvent) {
//     const link = event.target as HTMLAnchorElement;
//     const tooltip = document.querySelector('div[style*="position: absolute"]');
//     if (tooltip) {
//         document.body.removeChild(tooltip);
//     }
//     delete link.dataset.tooltip;
// }

// Run the main function when the content script loads
identifyLegalLinks();

// Re-run the function when the page content changes (e.g., for single-page applications)
const observer = new MutationObserver(identifyLegalLinks);
observer.observe(document.body, { childList: true, subtree: true });