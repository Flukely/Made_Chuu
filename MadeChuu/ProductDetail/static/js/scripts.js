document.addEventListener('DOMContentLoaded', function() {
    const minusButton = document.getElementById('minus-button');
    const plusButton = document.getElementById('plus-button');
    const quantityInput = document.getElementById('quantity-input');

    minusButton.addEventListener('click', function() {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });

    plusButton.addEventListener('click', function() {
        let currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });
});