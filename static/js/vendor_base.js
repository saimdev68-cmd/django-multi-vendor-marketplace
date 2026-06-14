/**
 * Marketly Custom UI Dashboard Module Engine
 */
class VendorNavigationManager {
    constructor() {
        this.wrapper = document.getElementById('dashboard-wrapper');
        this.desktopToggle = document.getElementById('sidebar-toggle');
        this.mobileToggle = document.getElementById('mobile-toggle');
        
        this.init();
    }

    init() {
        // Hydrate layouts state directly out of localStorage strings safely
        const isCollapsed = localStorage.getItem('marketly_sidebar_collapsed') === 'true';
        if (isCollapsed && window.innerWidth > 768) {
            this.wrapper.classList.add('sidebar-collapsed');
        }

        this.bindEvents();
    }

    bindEvents() {
        if (this.desktopToggle) {
            this.desktopToggle.addEventListener('click', () => this.toggleDesktopSidebar());
        }

        if (this.mobileToggle) {
            this.mobileToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleMobileSidebar();
            });
        }

        // Close active mobile drawer viewports clicking outside workspace regions
        document.addEventListener('click', (e) => {
            if (this.wrapper.classList.contains('mobile-sidebar-open')) {
                if (!e.target.closest('.aside-sidebar') && !e.target.closest('#mobile-toggle')) {
                    this.toggleMobileSidebar();
                }
            }
        });
    }

    toggleDesktopSidebar() {
        this.wrapper.classList.toggle('sidebar-collapsed');
        const state = this.wrapper.classList.contains('sidebar-collapsed');
        localStorage.setItem('marketly_sidebar_collapsed', state);
    }

    toggleMobileSidebar() {
        this.wrapper.classList.toggle('mobile-sidebar-open');
    }
}

// Global Clean Lifecycle Hook Initializer Routine
document.addEventListener('DOMContentLoaded', () => {
    window.MarketlyNav = new VendorNavigationManager();
});