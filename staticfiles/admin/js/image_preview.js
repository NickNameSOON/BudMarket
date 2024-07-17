// static/admin/js/image_preview.js
document.addEventListener('DOMContentLoaded', function () {
    const imagePreview = document.querySelector('.admin-image-preview img');
    const urlField = document.querySelector('#id_url');

    if (imagePreview) {
        imagePreview.addEventListener('click', function () {
            if (urlField.value) {
                window.open(urlField.value, '_blank');
            }
        });
    }
});
