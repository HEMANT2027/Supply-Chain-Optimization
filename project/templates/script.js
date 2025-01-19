// Function to check if an element is in the viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return rect.top <= window.innerHeight && rect.bottom >= 0;
}

// Add animation class when element comes into view
function handleScroll() {
    const elements = document.querySelectorAll('.animate');
    elements.forEach(element => {
        if (isInViewport(element)) {
            if (element.classList.contains('fade-in')) {
                element.classList.add('fade-in');
            } else if (element.classList.contains('slide-up')) {
                element.classList.add('slide-up');
            }
        }
    });
}

// Listen for scroll events
window.addEventListener('scroll', handleScroll);

// Run on initial load in case elements are already in view
handleScroll();

// Scroll to top button functionality
const scrollToTopBtn = document.createElement('button');
scrollToTopBtn.innerHTML = '↑';
scrollToTopBtn.style.position = 'fixed';
scrollToTopBtn.style.bottom = '30px';
scrollToTopBtn.style.right = '30px';
scrollToTopBtn.style.padding = '10px 20px';
scrollToTopBtn.style.backgroundColor = '#f1c40f';
scrollToTopBtn.style.border = 'none';
scrollToTopBtn.style.borderRadius = '5px';
scrollToTopBtn.style.fontSize
