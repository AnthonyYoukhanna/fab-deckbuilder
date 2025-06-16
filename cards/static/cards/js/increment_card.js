document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.card-clickable').forEach(el => {
    el.addEventListener('click', function (event) {
      event.preventDefault();
      const uniqueId = this.closest('.card-wrapper').dataset.cardUniqueId;

      fetch(window.INCREMENT_URL, {
        method: 'POST',
        headers: {
          'X-CSRFToken': window.csrfToken,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `unique_id=${uniqueId}`
      })
        .then(response => response.json())
        .then(data => {
          if (data.quantity !== undefined) {
            document.getElementById(`quantity-${uniqueId}`).textContent = data.quantity;
          }
        });
    });
  });
});
