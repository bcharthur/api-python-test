// static/js/get-info.js
document.addEventListener('DOMContentLoaded', function() {
    const getTitleForm = document.getElementById('getTitleForm');
    const resultTitleDiv = document.getElementById('resultTitle');

    getTitleForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Empêche le rechargement de la page
        const url = document.getElementById('title_url').value.trim();
        if (!url) {
            alert('Veuillez entrer une URL YouTube valide.');
            return;
        }

        const encodedURL = encodeURIComponent(url);
        console.log(`Encoded URL for get-title: ${encodedURL}`);

        fetch(`/api/get-title?ytb_url=${encodedURL}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    resultTitleDiv.innerHTML = `<div class="alert alert-success" role="alert"><strong>Titre:</strong> ${data.title}</div>`;
                } else {
                    resultTitleDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${data.message}</div>`;
                }
            })
            .catch(err => {
                resultTitleDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${err}</div>`;
            });
    });
});
