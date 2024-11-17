// static/js/main.js

// Fonction pour afficher les toasts
function showToast(title, message, type) {
    const toastId = `toast${Date.now()}`;
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-delay="5000">
            <div class="toast-header bg-${type} text-white">
                <strong class="mr-auto">${title}</strong>
                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    $('#toastContainer').append(toastHtml);
    $(`#${toastId}`).toast('show');
    // Supprimer le toast après la disparition
    $(`#${toastId}`).on('hidden.bs.toast', function () {
        $(this).remove();
    });
}
