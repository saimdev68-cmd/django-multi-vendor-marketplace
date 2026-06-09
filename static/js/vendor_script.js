const desktopCollapseBtn = document.getElementById('desktopCollapseBtn');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const sidebarPanel = document.getElementById('sidebarPanel');
const navItems = document.querySelectorAll('.nav-item');

// Handle desktop minimization transformations action toggle events
desktopCollapseBtn.addEventListener('click', () => {
    sidebarPanel.classList.toggle('minimized');
});

// Handle mobile sliding view actions overlay toggles
mobileMenuToggle.addEventListener('click', (e) => {
    sidebarPanel.classList.toggle('open');
    e.stopPropagation();
});

// Safe closure overlay checks if user taps outward from modal elements
document.addEventListener('click', (e) => {
    if (sidebarPanel.classList.contains('open') && !sidebarPanel.contains(e.target)) {
        sidebarPanel.classList.remove('open');
    }
});

// High-performance slider line synchronization feedback loops 
navItems.forEach(item => {
    item.addEventListener('click', function() {
        if (this.querySelector('.nav-link')) {
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        }
    });
});