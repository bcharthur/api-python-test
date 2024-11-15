document.getElementById('deleteBtn').addEventListener('click', function(e) {
    e.preventDefault();

    const id = document.getElementById('editItemId').value; // ID de l'item à supprimer

    fetch(`/api/item/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.status === 'success') location.reload();
    })
    .catch(error => console.error('Erreur lors de la suppression de l’item:', error));
});
