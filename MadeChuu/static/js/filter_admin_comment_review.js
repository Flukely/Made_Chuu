document.addEventListener('DOMContentLoaded', function() {
    const filterCommentsElement = document.getElementById('filter-comments');
    const filterProductsElement = document.getElementById('filter-products');

    if (filterCommentsElement && filterProductsElement) {
        filterCommentsElement.addEventListener('change', filterComments);
        filterProductsElement.addEventListener('change', filterComments);

        function filterComments() {
            const commentType = filterCommentsElement.value;
            const productName = filterProductsElement.value;
            const comments = document.getElementsByClassName('comment-card');

            console.log('Filtering comments with type:', commentType, 'and product:', productName);

            for (let i = 0; i < comments.length; i++) {
                const comment = comments[i];
                const commentTypeMatch = (commentType === 'all' || comment.getAttribute('data-comment-type') === commentType);
                const productNameMatch = (productName === 'all' || comment.getAttribute('data-product-name') === productName);

                console.log('Comment:', comment, 'Type Match:', commentTypeMatch, 'Product Match:', productNameMatch);

                if (commentTypeMatch && productNameMatch) {
                    comment.style.display = 'block';
                } else {
                    comment.style.display = 'none';
                }
            }
        }

        // Initial filter on page load
        filterComments();
    }
});