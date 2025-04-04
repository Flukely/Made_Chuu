document.addEventListener("DOMContentLoaded", function () {
    // ✅ ดึงค่าสถานะจาก Attribute ของ HTML
    const orderState = document.getElementById("order-status-text").dataset.status;

    // ✅ กำหนด State ของคำสั่งซื้อ
    const orderStatus = {
        "จัดส่งสำเร็จ": {
            text: "✅ คำสั่งซื้อของคุณจัดส่งสำเร็จแล้ว!",
            class: "text-success",
            showTracking: false,
            showReview: true
        },
        "อยู่ระหว่างจัดส่ง": {
            text: "🚚 กำลังจัดส่งสินค้า",
            class: "text-warning",
            showTracking: true,
            showReview: false
        },
        "กำลังรอขนส่งเข้ารับ": {
            text: "📦 รอขนส่งเข้ารับสินค้า",
            class: "text-info",
            showTracking: false,
            showReview: false
        },
        "default": {
            text: "⏳ คำสั่งซื้อกำลังดำเนินการ",
            class: "text-secondary",
            showTracking: false,
            showReview: false
        }
    };

    // ✅ เลือก State ปัจจุบัน
    const currentState = orderStatus[orderState] || orderStatus["default"];

    // ✅ อัปเดต UI ตาม State
    const statusText = document.getElementById("order-status-text");
    statusText.innerText = currentState.text;
    statusText.className = currentState.class;

    // ✅ แสดงหรือซ่อน Tracking Number
    document.getElementById("tracking-info").style.display = currentState.showTracking ? "block" : "none";

    // ✅ แสดงหรือซ่อนปุ่มรีวิว
    document.getElementById("review-btn").style.display = currentState.showReview ? "block" : "none";
});
