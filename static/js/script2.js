document.addEventListener("DOMContentLoaded", function() {
    const orders = [
        {
            shop: "KONVY_Official Shop",
            product: "Black Magic Plus GSH CE-II [20 Capsules]",
            price: 319,
            discountPrice: 261,
            image: "product1.jpg"
        },
        {
            shop: "LALIVING",
            product: "ชั้นวางจอคอม ชั้นวางโน้ตบุ๊ค ขาตั้งจอคอม ที่วาง...",
            price: 136,
            discountPrice: 57,
            image: "product2.jpg"
        },
        {
            shop: "Tsunami_Distributor",
            product: "คีย์บอร์ดเกมมิ่ง Ajazz K870T Rainbow",
            price: 1900,
            discountPrice: 899,
            image: "product3.jpg"
        }
    ];

    const orderList = document.getElementById("orderList");

    orders.forEach(order => {
        const orderCard = document.createElement("div");
        orderCard.classList.add("order-card");

        orderCard.innerHTML = `
            <div class="order-info">
                <img src="${order.image}" alt="${order.product}">
                <div class="order-details">
                    <h3>${order.shop}</h3>
                    <p>${order.product}</p>
                    <p><s>฿${order.price}</s> <strong>฿${order.discountPrice}</strong></p>
                </div>
            </div>
            <div class="order-actions">
                <button class="btn-detail">ดูรายละเอียด</button>
                <button class="btn-buy">ซื้ออีกครั้ง</button>
            </div>
        `;

        orderList.appendChild(orderCard);
    });
});

function showTab(tabName) {
    console.log("แสดงแท็บ:", tabName);
}
