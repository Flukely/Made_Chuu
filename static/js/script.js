document.addEventListener("DOMContentLoaded", function () {
    const steps = document.querySelectorAll(".step");
    
    steps.forEach((step, index) => {
        step.addEventListener("click", () => {
            steps.forEach(s => s.classList.remove("active"));
            for (let i = 0; i <= index; i++) {
                steps[i].classList.add("active");
            }
        });
    });

    const cartButtons = document.querySelectorAll(".btn-cart");
    cartButtons.forEach(button => {
        button.addEventListener("click", () => {
            alert("เพิ่มสินค้าในตะกร้าแล้ว!");
        });
    });
});