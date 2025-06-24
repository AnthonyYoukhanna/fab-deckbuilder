document.addEventListener('DOMContentLoaded', function () {
    const bulkButtons = document.querySelectorAll('.bulk-add-btn');

    bulkButtons.forEach(button => {
        button.addEventListener('click', function () {
            const setId = this.dataset.setId;
            const setName = this.dataset.setName
            fetch(`/cards/bulk-add/?set_id=${setId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    alert(`Added bulk cards from ${setName}`);
                }
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
