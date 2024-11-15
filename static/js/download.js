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

        resultDownloadDiv.innerHTML = `<div class="alert alert-info" role="alert">Téléchargement en cours...</div>`;

        // Envoyer la requête GET pour télécharger la vidéo
        fetch(`/api/download?ytb_url=${encodeURIComponent(ytbUrl)}`)
            .then(response => {
                const contentType = response.headers.get('Content-Type');
                if (!response.ok) {
                    return response.json().then(errData => { throw new Error(errData.message || 'Erreur lors du téléchargement.'); });
                }
                if (contentType && contentType.includes('application/json')) {
                    return response.json().then(errData => { throw new Error(errData.message || 'Erreur lors du téléchargement.'); });
                }
                return response.blob().then(blob => ({ blob, headers: response.headers }));
            })
            .then(({ blob, headers }) => {
                // Extraire le nom de fichier depuis le header 'Content-Disposition'
                const disposition = headers.get('Content-Disposition');
                let filename = 'video.mp4'; // Nom par défaut
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    const matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) {
                        filename = matches[1].replace(/['"]/g, '');
                    }
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
                resultDownloadDiv.innerHTML = `<div class="alert alert-success" role="alert">Téléchargement terminé. Le fichier a été enregistré.</div>`;
            })
            .catch(err => {
                resultDownloadDiv.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Erreur:</strong> ${err.message}</div>`;
            });
    });
});
