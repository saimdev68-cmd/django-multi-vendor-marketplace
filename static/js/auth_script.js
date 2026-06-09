document.addEventListener("DOMContentLoaded", function () {
    // -------------------------------------------------------------
    // 1. Toast Notification Handler
    // -------------------------------------------------------------
    const toasts = document.querySelectorAll('.toast-card');
    toasts.forEach((toast, index) => {
        // Trigger presentation entry transition smoothly
        setTimeout(() => {
            toast.classList.add('show');
        }, index * 120);

        // Auto-dismiss execution lifecycle (5 seconds)
        setTimeout(() => {
            removeToastElement(toast);
        }, 5000);
    });

    // -------------------------------------------------------------
    // 2. Dynamic Password Visibility Toggle
    // -------------------------------------------------------------
    const toggleButtons = document.querySelectorAll('.password-toggle-btn');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault(); // Prevents optional form triggers
            
            // Look for the input element strictly inside its own container scope
            const passwordInput = this.closest('.password-wrapper').querySelector('input');
            const viewIcon = this.querySelector('.view-icon');
            const hideIcon = this.querySelector('.hide-icon');

            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                viewIcon.style.display = 'none';
                hideIcon.style.display = 'block';
            } else {
                passwordInput.type = 'password';
                viewIcon.style.display = 'block';
                hideIcon.style.display = 'none';
            }
        });
    });
});

// Manual Close Trigger Event Function
function dismissToast(button) {
    const toast = button.closest('.toast-card');
    removeToastElement(toast);
}

function removeToastElement(toast) {
    if (toast) {
        toast.classList.remove('show');
        // Let CSS transitions finalize before destroying element node from DOM
        setTimeout(() => {
            toast.remove();
        }, 400);
    }
}