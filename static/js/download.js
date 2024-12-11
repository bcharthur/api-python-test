// static/js/download.js

document.addEventListener('DOMContentLoaded', function() {
    const downloadForm = document.getElementById('downloadForm');
    const downloadBtn = document.getElementById('downloadBtn');
    const resultDownloadDiv = document.getElementById('resultDownload');

    if (!downloadForm || !downloadBtn || !resultDownloadDiv) {
        console.error("Les éléments du formulaire de téléchargement ne sont pas trouvés.");
        return;
    }

    downloadForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Empêche le rechargement de la page

        const ytbUrl = document.getElementById('download_url').value.trim();

        if (!ytbUrl) {
            resultDownloadDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> Veuillez entrer une URL YouTube valide.</div>`;
            return;
        }

        // Afficher le message de téléchargement en cours
        resultDownloadDiv.innerHTML = `<div class="alert alert-info" role="alert">Téléchargement en cours...</div>`;

        // Désactiver le bouton et ajouter le spinner
        downloadBtn.disabled = true;
        const originalBtnContent = downloadBtn.innerHTML; // Sauvegarder le contenu original
        downloadBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Téléchargement...
        `;

        // Envoyer la requête avec fetch
        fetch(`/api/download?ytb_url=${encodeURIComponent(ytbUrl)}`)
            .then(response => {
                console.log('Réponse reçue:', response);
                if (!response.ok) {
                    return response.json().then(errData => { throw new Error(errData.message || 'Erreur lors du téléchargement.'); });
                }
                const disposition = response.headers.get('Content-Disposition');
                let filename = 'video.mp4'; // Nom par défaut
                if (disposition && disposition.includes('attachment')) {
                    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    const matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) {
                        filename = matches[1].replace(/['"]/g, '');
                    }
                }
                console.log('Nom de fichier déterminé:', filename);
                return response.blob().then(blob => {
                    console.log('Blob reçu:', blob);
                    return { blob, filename };
                });
            })
            .then(({ blob, filename }) => {
                // Vérifiez que le blob a une taille non nulle
                if (blob.size === 0) {
                    throw new Error('Le fichier téléchargé est vide.');
                }

                // Créer un lien temporaire pour télécharger le fichier
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);

                // Afficher le message de succès
                resultDownloadDiv.innerHTML = `<div class="alert alert-success" role="alert">Téléchargement terminé. Le fichier a été enregistré.</div>`;
                console.log('Téléchargement réussi.');
            })
            .catch(err => {
                console.error('Erreur lors du téléchargement:', err);
                resultDownloadDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${err.message}</div>`;
            })
            .finally(() => {
                // Rétablir le contenu original du bouton et réactiver le bouton
                downloadBtn.disabled = false;
                downloadBtn.innerHTML = originalBtnContent;
            });
    });
});
