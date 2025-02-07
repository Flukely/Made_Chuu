document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.star-rating').forEach(function(element) {
        let rating = parseInt(element.getAttribute('data-rating'), 10);
        let stars = '★'.repeat(rating) + '☆'.repeat(5 - rating); // 5 ดาวสูงสุด
        element.textContent = stars;
    });
});