// static/js/download.js

document.addEventListener('DOMContentLoaded', function() {
    const downloadForm = document.getElementById('downloadForm');
    const downloadBtn = document.getElementById('downloadBtn');
    const resultDownloadDiv = document.getElementById('resultDownload');

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
                return response.blob().then(blob => ({ blob, filename }));
            })
            .then(({ blob, filename }) => {
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
            })
            .catch(err => {
                resultDownloadDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${err.message}</div>`;
            })
            .finally(() => {
                // Rétablir le contenu original du bouton et réactiver le bouton
                downloadBtn.disabled = false;
                downloadBtn.innerHTML = originalBtnContent;
            });
    });
});
