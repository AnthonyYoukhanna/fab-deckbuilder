document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.remove-btn').forEach(button => {
    button.addEventListener('click', async function () {
      const cardId = this.dataset.cardId;

      const response = await fetch('/cards/remove/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ card_id: cardId }),
      });

      if (response.ok) {
        const quantityElem = this.parentElement.querySelector('.quantity');
        if (quantityElem) {
          const newQty = parseInt(quantityElem.textContent) - 1;
          if (newQty > 0) {
            quantityElem.textContent = newQty;
          } else {
            quantityElem.textContent = '0';
          }
        } else {
          this.closest('div').remove();  // fallback
        }
      } else {
        alert('Failed to remove card');
      }
    });
  });
});



// CSRF helper
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
