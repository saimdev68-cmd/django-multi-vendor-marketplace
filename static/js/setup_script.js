document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Multi-step Multi-View Feature Logic ---
    const step1 = document.getElementById('step-1');
    const step2 = document.getElementById('step-2');
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    const indicator1 = document.getElementById('step-indicator-1');
    const indicator2 = document.getElementById('step-indicator-2');

    if (nextBtn && prevBtn) {
        nextBtn.addEventListener('click', () => {
            step1.classList.remove('active');
            step2.classList.add('active');
            indicator1.classList.remove('active');
            indicator2.classList.add('active');
        });

        prevBtn.addEventListener('click', () => {
            step2.classList.remove('active');
            step1.classList.add('active');
            indicator2.classList.remove('active');
            indicator1.classList.add('active');
        });
    }

    // --- 2. Advanced Dynamic Toast Manager ---
    window.showToast = function(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        // Structure content inside the notification block
        toast.innerHTML = `
            <span class="toast-message">${message}</span>
            <button class="toast-close" type="button">&times;</button>
        `;

        // Interaction setup for click-to-dismiss behavior
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => dismissToast(toast));

        container.appendChild(toast);

        // Auto collapse element after standard 4.5 second delay
        setTimeout(() => {
            if (toast.parentElement) dismissToast(toast);
        }, 4500);
    };

    function dismissToast(toast) {
        toast.style.animation = 'fadeOutUp 0.3s ease forwards';
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }

    // Capture standard system messages loaded by Django context view
    const djangoMessages = document.querySelectorAll('.hidden-django-message');
    djangoMessages.forEach(msg => {
        const text = msg.textContent.trim();
        let tag = msg.getAttribute('data-tags') || 'info';
        
        // Mapping fallback names variations
        if (tag.includes('success')) tag = 'success';
        else if (tag.includes('error') || tag.includes('danger')) tag = 'error';
        else if (tag.includes('warning')) tag = 'warning';
        else tag = 'info';

        window.showToast(text, tag);
        msg.remove(); // Keep layout crisp and clean
    });

    // --- 3. Custom Form Errors Pre-processor ---
    // Finds incoming validation problems flagged by server and injects style frames
    const structuralParagraphs = document.querySelectorAll('.django-form-fields p');
    structuralParagraphs.forEach(p => {
        const validationErrorList = p.querySelector('.errorlist');
        if (validationErrorList) {
            const entryField = p.querySelector('input, select, textarea');
            if (entryField) {
                entryField.classList.add('input-has-error');
            }
        }
    });
});