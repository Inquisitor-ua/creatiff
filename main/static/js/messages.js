document.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('.toast-notification');
    
    toasts.forEach((toast) => {
        setTimeout(() => {
            removeToast(toast);
        }, 5000);

        const closeButton = toast.querySelector('.toast-close-btn');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                console.log('close');
                removeToast(toast);
            });
        }
    });
});

function removeToast(toast) {
    if (toast.classList.contains('fade-out')) return;

    toast.classList.add('fade-out');
    
    toast.addEventListener('transitionend', () => {
        toast.remove();
    }, { once: true });
}