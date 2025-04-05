document.addEventListener("DOMContentLoaded", function () {
    // Progress Steps Functionality
    const setupProgressSteps = () => {
        const steps = document.querySelectorAll(".step");
        
        if (!steps.length) return;

        steps.forEach((step, index) => {
            step.addEventListener("click", () => {
                // Remove active class from all steps
                steps.forEach(s => {
                    s.classList.remove("active");
                    s.setAttribute('aria-current', 'false');
                });
                
                // Add active class to clicked step and all previous steps
                for (let i = 0; i <= index; i++) {
                    steps[i].classList.add("active");
                    steps[i].setAttribute('aria-current', 'true');
                }

                // Dispatch custom event for step change
                const event = new CustomEvent('stepChanged', {
                    detail: { currentStep: index + 1 }
                });
                document.dispatchEvent(event);
            });

            // Keyboard accessibility
            step.addEventListener("keydown", (e) => {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    step.click();
                }
            });
        });

        // Initialize first step as active
        if (steps.length > 0) {
            steps[0].classList.add("active");
            steps[0].setAttribute('aria-current', 'true');
        }
    };

    // Cart Button Functionality
    const setupCartButtons = () => {
        const cartButtons = document.querySelectorAll(".btn-cart");
        
        cartButtons.forEach(button => {
            // Add proper ARIA attributes
            button.setAttribute('aria-label', 'Add to cart');
            
            button.addEventListener("click", (e) => {
                e.preventDefault();
                
                // Get product info from data attributes
                const productId = button.dataset.productId;
                const productName = button.dataset.productName;
                
                // Visual feedback
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-check"></i> Added!';
                button.classList.add('added-to-cart');
                
                // Dispatch custom event
                const event = new CustomEvent('productAdded', {
                    detail: { 
                        productId: productId,
                        productName: productName
                    }
                });
                document.dispatchEvent(event);
                
                // Reset button after animation
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.classList.remove('added-to-cart');
                }, 2000);
                
                // Update cart counter if exists
                const cartCounter = document.querySelector('.cart-counter');
                if (cartCounter) {
                    const currentCount = parseInt(cartCounter.textContent) || 0;
                    cartCounter.textContent = currentCount + 1;
                    cartCounter.classList.add('pulse');
                    
                    setTimeout(() => {
                        cartCounter.classList.remove('pulse');
                    }, 500);
                }
            });
        });
    };

    // Initialize all functionality
    const init = () => {
        setupProgressSteps();
        setupCartButtons();
        
        // Listen for custom events
        document.addEventListener('productAdded', (e) => {
            console.log(`Product added: ${e.detail.productName} (ID: ${e.detail.productId})`);
            // Here you could add AJAX call to your backend
        });
        
        document.addEventListener('stepChanged', (e) => {
            console.log(`Current step: ${e.detail.currentStep}`);
            // You could add logic to show/hide content based on step
        });
    };

    init();
});