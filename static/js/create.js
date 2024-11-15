document.getElementById('createForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Corriger l'ID de l'input
    const nom = document.getElementById('itemName').value;

    fetch('/api/item', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nom: nom })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Affiche un message d'alerte avec le retour de l'API
            if (data.status === 'success') {
                document.getElementById('itemName').value = ''; // Réinitialiser le champ
                location.reload(); // Recharger la page pour actualiser la liste
            }
        })
        .catch(error => {
            console.error('Erreur lors de la création de l\'item :', error);
        });
});
