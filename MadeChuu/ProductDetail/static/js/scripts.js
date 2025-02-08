document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".star-rating").forEach(function (element) {
        let rating = parseInt(element.getAttribute("data-rating"), 10);
        if (!isNaN(rating)) {
            let stars = "★".repeat(rating) + "☆".repeat(5 - rating); // สูงสุด 5 ดาว
            element.textContent = stars;
        }
    });

    // New code to calculate and display average rating
    let ratings = document.querySelectorAll(".star-rating");
    let totalRating = 0;
    let countRatings = 0;
    
    ratings.forEach(function (element) {
        let rating = parseInt(element.getAttribute("data-rating"), 10);
        if (!isNaN(rating)) {
            totalRating += rating;
            countRatings++;
        }
    });

    if (countRatings > 0) {
        let averageRating = totalRating / countRatings;
        let averageStars = "★".repeat(Math.round(averageRating)) + "☆".repeat(5 - Math.round(averageRating));

        let averageRatingElement = document.getElementById("average-rating");
        if (averageRatingElement) {
            averageRatingElement.textContent = averageStars + " (" + averageRating.toFixed(1) + " / 5)";
        }
    }

    // Filter reviews by rating
    document.querySelectorAll('.filter-button').forEach(function(button) {
        button.addEventListener('click', function() {
            let filterRating = parseInt(this.getAttribute('data-rating'), 10);
            document.querySelectorAll('.review').forEach(function(review) {
                let reviewRating = parseInt(review.querySelector('.star-rating').getAttribute('data-rating'), 10);
                if (reviewRating === filterRating) {
                    review.style.display = 'block';
                } else {
                    review.style.display = 'none';
                }
            });
        });
    });

    // Show all reviews
    document.querySelector('.show-all-button').addEventListener('click', function() {
        document.querySelectorAll('.review').forEach(function(review) {
            review.style.display = 'block';
        });
    });

    countElement.addEventListener("input", function () {
        let value = parseInt(countElement.value);
        if (isNaN(value) || value < 0) {
            countElement.value = 0;
        } else if (value > maxLimit) {
            countElement.value = maxLimit;
        }
        count = parseInt(countElement.value);
    });
});