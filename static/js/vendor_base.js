document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Unified Sidebar Responsive Control Engine ---
    const wrapper = document.getElementById('dashboard-wrapper');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    
    // Pull desktop memory footprint state from browser cache
    const isCollapsed = localStorage.getItem('sidebar-state') === 'collapsed';
    
    // Initialize desktop layout state immediately on page load
    if (isCollapsed && wrapper && window.innerWidth > 768) {
        wrapper.classList.add('sidebar-collapsed');
    }

    if (sidebarToggle && wrapper) {
        sidebarToggle.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                // MOBILE MODE: Toggle responsive sliding drawer drawer
                wrapper.classList.toggle('mobile-sidebar-open');
                wrapper.classList.remove('sidebar-collapsed'); // Ensure desktop state doesn't clash
            } else {
                // DESKTOP MODE: Toggle mini layout grid column widths
                wrapper.classList.toggle('sidebar-collapsed');
                wrapper.classList.remove('mobile-sidebar-open'); // Clean up mobile state trace
                
                // Save layout preference to memory cache
                if (wrapper.classList.contains('sidebar-collapsed')) {
                    localStorage.setItem('sidebar-state', 'collapsed');
                } else {
                    localStorage.setItem('sidebar-state', 'expanded');
                }
            }
        });
    }

    // --- 2. Live Global Micro Toast Message Broadcaster ---
    window.showToast = function(message, type = 'info') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        toast.innerHTML = `
            <span class="toast-message">${message}</span>
            <button class="toast-close" type="button" aria-label="Close message">&times;</button>
        `;

        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => dismissToast(toast));
        }

        container.appendChild(toast);

        setTimeout(() => {
            if (toast.parentElement) dismissToast(toast);
        }, 4000);
    };

    function dismissToast(toast) {
        toast.style.animation = 'fadeOutUp 0.25s ease forwards';
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }

    // Capture background Django middleware notifications lists
    const djangoMessages = document.querySelectorAll('.hidden-django-message');
    djangoMessages.forEach(msg => {
        const text = msg.textContent.trim();
        let tag = msg.getAttribute('data-tags') || 'info';
        
        if (tag.includes('success')) tag = 'success';
        else if (tag.includes('error') || tag.includes('danger')) tag = 'error';
        else if (tag.includes('warning')) tag = 'warning';
        else tag = 'info';

        window.showToast(text, tag);
        msg.remove();
    });
});