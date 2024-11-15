document.getElementById('editForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const id = document.getElementById('editItemId').value; // Correspond à l'ID de l'item
    const nom = document.getElementById('editItemName').value; // Correspond au nom modifié

    fetch(`/api/item/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nom: nom })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.status === 'success') location.reload();
    })
    .catch(error => console.error('Erreur lors de la modification de l’item:', error));
});
