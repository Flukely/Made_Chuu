document.addEventListener('DOMContentLoaded', function() {
    const replyForms = document.querySelectorAll('.reply-form');
    const editButtons = document.querySelectorAll('.edit-reply-button');

    replyForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Reply added successfully!');
                    this.style.display = 'none';
                } else {
                    alert('Failed to add reply: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    });
});