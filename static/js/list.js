document.addEventListener('DOMContentLoaded', function () {
    const itemList = document.getElementById('itemList');
    const toastContainer = document.getElementById('toastContainer');

    // Fonction pour afficher un toast Bootstrap avec FontAwesome
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type} border-0`;
        toast.role = 'alert';
        toast.ariaLive = 'assertive';
        toast.ariaAtomic = 'true';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close me-2 m-auto text-white" data-bs-dismiss="toast" aria-label="Close">
                    <i class="fa-solid fa-times"></i>
                </button>
            </div>
        `;
        toastContainer.appendChild(toast);

        // Initialiser le toast avec Bootstrap
        const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
        bsToast.show();

        // Supprimer le toast une fois masqué
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    // Charger les items
    function loadItems() {
        fetch('/api/items')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success' && data.items.status === 'success') {
                    const items = data.items.data;
                    itemList.innerHTML = ''; // Nettoyer la liste

                    items.forEach(item => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item d-flex justify-content-between align-items-center';
                        li.innerHTML = `
                            <span>${item.nom} (ID: ${item.id})</span>
                            <div>
                                <button class="btn btn-info btn-sm edit-btn" data-id="${item.id}" data-nom="${item.nom}">Modifier</button>
                                <button class="btn btn-danger btn-sm delete-btn" data-id="${item.id}">Supprimer</button>
                            </div>
                        `;
                        itemList.appendChild(li);
                    });

                    attachEventHandlers();
                }
            })
            .catch(error => {
                console.error('Erreur lors du chargement des items :', error);
                showToast('Erreur lors du chargement des items', 'danger');
            });
    }

    // Charger les items au démarrage
    loadItems();

    // Attacher des événements pour Modifier et Supprimer
    function attachEventHandlers() {
        document.querySelectorAll('.edit-btn').forEach(button => {
            button.addEventListener('click', function () {
                const id = this.dataset.id;
                const nom = this.dataset.nom;

                document.getElementById('editItemName').value = nom;

                const editForm = document.getElementById('editItemForm');
                editForm.onsubmit = function (e) {
                    e.preventDefault();
                    const newName = document.getElementById('editItemName').value;

                    // Ajouter un spinner
                    const spinner = document.createElement('span');
                    spinner.className = 'spinner-border spinner-border-sm ms-2';
                    spinner.role = 'status';
                    spinner.ariaHidden = 'true';
                    e.submitter.appendChild(spinner);

                    fetch(`/api/item/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nom: newName })
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                showToast('Item modifié avec succès');
                                loadItems(); // Rafraîchir la liste
                                const editModal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
                                editModal.hide(); // Cacher la modale
                            } else {
                                showToast('Erreur lors de la modification', 'danger');
                            }
                        })
                        .catch(error => {
                            console.error('Erreur lors de la modification :', error);
                            showToast('Erreur lors de la modification', 'danger');
                        })
                        .finally(() => spinner.remove());
                };

                // Afficher la modale d'édition
                const editModal = new bootstrap.Modal(document.getElementById('editModal'));
                editModal.show();
            });
        });

        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', function () {
                const id = this.dataset.id;

                const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
                confirmDeleteBtn.onclick = function () {
                    confirmDeleteBtn.disabled = true;

                    // Ajouter un spinner
                    const spinner = document.createElement('span');
                    spinner.className = 'spinner-border spinner-border-sm ms-2';
                    spinner.role = 'status';
                    spinner.ariaHidden = 'true';
                    confirmDeleteBtn.appendChild(spinner);

                    fetch(`/api/item/${id}`, { method: 'DELETE' })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                showToast('Item supprimé avec succès', 'danger');
                                loadItems(); // Rafraîchir la liste
                                const deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
                                deleteModal.hide(); // Cacher la modale
                            } else {
                                showToast('Erreur lors de la suppression', 'danger');
                            }
                        })
                        .catch(error => {
                            console.error('Erreur lors de la suppression :', error);
                            showToast('Erreur lors de la suppression', 'danger');
                        })
                        .finally(() => {
                            spinner.remove();
                            confirmDeleteBtn.disabled = false;
                        });
                };

                // Afficher la modale de suppression
                const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
                deleteModal.show();
            });
        });
    }
});
