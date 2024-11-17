// static/js/get-musique.js

$(document).ready(function() {
    // Gestionnaire pour "Télécharger la musique"
    $('#downloadMusiqueBtn').on('click', function() {
        const url = $('#musique_url').val();

        if (!url) {
            showToast('Erreur', 'Veuillez fournir une URL de vidéo.', 'danger');
            return;
        }

        $('#downloadMusiqueBtn').prop('disabled', true).text('Téléchargement...');

        // Fonction pour déclencher le téléchargement
        const downloadMusique = function(audioUrl) {
            // Créer un lien temporaire
            const link = document.createElement('a');
            link.href = audioUrl;
            link.download = ''; // Laisser le navigateur décider du nom du fichier
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            $('#downloadMusiqueBtn').prop('disabled', false).text('Télécharger la musique');
            showToast('Succès', 'Musique téléchargée avec succès!', 'success');
        };

        // Effectuer la requête pour obtenir l'URL de l'audio
        $.ajax({
            url: '/api/get_audio',
            method: 'GET',
            data: { url: url },
            success: function(response) {
                if (response.audio_url) {
                    downloadMusique(response.audio_url);
                } else if (response.error) {
                    showToast('Erreur', response.error, 'danger');
                    $('#downloadMusiqueBtn').prop('disabled', false).text('Télécharger la musique');
                }
            },
            error: function(xhr) {
                const error = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'Erreur inconnue';
                showToast('Erreur', error, 'danger');
                $('#downloadMusiqueBtn').prop('disabled', false).text('Télécharger la musique');
            }
        });
    });
});
