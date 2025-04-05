document.addEventListener("DOMContentLoaded", function () {
    // 1. Get order status from HTML data attribute
    const orderStateElement = document.getElementById("order-status-text");
    if (!orderStateElement) return;
    
    const orderState = orderStateElement.dataset.status;
    const trackingNumber = orderStateElement.dataset.tracking;

    // 2. Order status configuration with Made Chuu styling
    const orderStatus = {
        "จัดส่งสำเร็จ": {
            text: "🎀 คำสั่งซื้อของคุณจัดส่งสำเร็จแล้ว!",
            class: "status-delivered",
            icon: "fa-check-circle",
            showTracking: false,
            showReview: true,
            progress: 100
        },
        "อยู่ระหว่างจัดส่ง": {
            text: "🚚 กำลังจัดส่งสินค้า",
            class: "status-shipping",
            icon: "fa-truck",
            showTracking: true,
            showReview: false,
            progress: 75
        },
        "กำลังรอขนส่งเข้ารับ": {
            text: "📦 รอขนส่งเข้ารับสินค้า",
            class: "status-processing",
            icon: "fa-box-open",
            showTracking: false,
            showReview: false,
            progress: 50
        },
        "กำลังเตรียมสินค้า": {
            text: "✂️ กำลังเตรียมสินค้า",
            class: "status-preparing",
            icon: "fa-scissors",
            showTracking: false,
            showReview: false,
            progress: 25
        },
        "default": {
            text: "⏳ รอการยืนยันคำสั่งซื้อ",
            class: "status-pending",
            icon: "fa-clock",
            showTracking: false,
            showReview: false,
            progress: 10
        }
    };

    // 3. Get current status configuration
    const currentState = orderStatus[orderState] || orderStatus["default"];

    // 4. Update status display
    orderStateElement.innerHTML = `
        <i class="fas ${currentState.icon}"></i> ${currentState.text}
    `;
    orderStateElement.className = `order-status ${currentState.class}`;

    // 5. Update tracking information if available
    const trackingInfo = document.getElementById("tracking-info");
    if (trackingInfo) {
        trackingInfo.style.display = currentState.showTracking ? "block" : "none";
        if (trackingNumber && currentState.showTracking) {
            document.getElementById("tracking-number").textContent = trackingNumber;
        }
    }

    // 6. Show/hide review button
    const reviewBtn = document.getElementById("review-btn");
    if (reviewBtn) {
        reviewBtn.style.display = currentState.showReview ? "block" : "none";
        if (currentState.showReview) {
            reviewBtn.innerHTML = `
                <i class="fas fa-star"></i> เขียนรีวิวสินค้า
            `;
        }
    }

    // 7. Update progress bar if exists
    const progressBar = document.getElementById("order-progress-bar");
    if (progressBar) {
        progressBar.style.width = `${currentState.progress}%`;
        progressBar.setAttribute('aria-valuenow', currentState.progress);
        progressBar.classList.add(currentState.class);
    }

    // 8. Add click event for tracking copy button
    const copyTrackingBtn = document.getElementById("copy-tracking-btn");
    if (copyTrackingBtn && trackingNumber) {
        copyTrackingBtn.addEventListener("click", function() {
            navigator.clipboard.writeText(trackingNumber).then(() => {
                const tooltip = new bootstrap.Tooltip(copyTrackingBtn, {
                    title: "คัดลอกแล้ว!",
                    trigger: "manual"
                });
                tooltip.show();
                setTimeout(() => tooltip.hide(), 1000);
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // ฟังก์ชันแสดงสินค้าคล้ายคลึงกัน
    const showSimilarProducts = () => {
        const currentProductCategory = "{{ product.category }}"; // รับประเภทสินค้าปัจจุบันจาก backend
        const similarProducts = document.querySelectorAll('.similar-products .product-card');
        
        similarProducts.forEach(product => {
            const productCategory = product.dataset.category;
            // ซ่อนสินค้าที่ไม่ตรงประเภท
            if(productCategory !== currentProductCategory) {
                product.style.display = 'none';
            }
        });
    }

    // เรียกใช้ฟังก์ชันเมื่อโหลดหน้า
    showSimilarProducts();

    // ปรับการแสดงผลบนมือถือ
    const adjustForMobile = () => {
        const productList = document.querySelector('.similar-products');
        if(window.innerWidth < 768) {
            productList.style.gridTemplateColumns = 'repeat(auto-fit, 150px)';
            productList.style.overflowX = 'auto';
            productList.style.scrollSnapType = 'x mandatory';
        }
    }

    window.addEventListener('resize', adjustForMobile);
    adjustForMobile(); // เรียกครั้งแรกเมื่อโหลดหน้า
});