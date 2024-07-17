document.addEventListener('DOMContentLoaded', function() {
    const categoryField = document.getElementById('id_category');
    const attributeRows = document.querySelectorAll('.dynamic-productattributevalue_set');

    function updateAttributeFields() {
        const categoryId = categoryField.value;
        attributeRows.forEach(row => {
            const attributeField = row.querySelector('select[id$="-attribute"]');
            if (attributeField) {
                const url = `/admin/market/productattribute/?category__id=${categoryId}&_popup=1`;
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        attributeField.innerHTML = '';
                        data.results.forEach(optionData => {
                            const option = document.createElement('option');
                            option.value = optionData.id;
                            option.textContent = optionData.text;
                            attributeField.appendChild(option);
                        });
                    });
            }
        });
    }

    categoryField.addEventListener('change', updateAttributeFields);
    updateAttributeFields();
});
