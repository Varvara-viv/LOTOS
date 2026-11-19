// Плавное появление элементов при прокрутке

const elements = document.querySelectorAll('.hero-content, .hero-bottom');

elements.forEach(function(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = '1s';
});

window.addEventListener('load', function() {
    elements.forEach(function(element, index) {
        setTimeout(function() {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 300);
    });
});
