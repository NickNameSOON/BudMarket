    document.addEventListener('DOMContentLoaded', function () {
        const paymentMethodSelect = document.getElementById('paymentMethod');
        const creditCardInfo = document.getElementById('creditCardInfo');
        const deliveryMethodSelect = document.getElementById('deliveryMethod');
        const deliveryInfo = document.getElementById('deliveryInfo');
        const pickupInfo = document.getElementById('pickupInfo');
        const editButton = document.getElementById('editButton');
        const contactInfo = document.getElementById('contactInfo');

        function togglePaymentFields() {
            creditCardInfo.style.display = paymentMethodSelect.value === 'creditCard' ? 'block' : 'none';
        }

        function toggleDeliveryFields() {
            if (deliveryMethodSelect.value === 'delivery') {
                deliveryInfo.style.display = 'block';
                pickupInfo.style.display = 'none';
            } else if (deliveryMethodSelect.value === 'pickup') {
                deliveryInfo.style.display = 'none';
                pickupInfo.style.display = 'block';
            }
        }

        function enableEditMode() {
            Array.from(contactInfo.children).forEach(p => {
                const span = p.querySelector('span');
                const input = document.createElement('input');
                input.type = 'text';
                input.value = span.textContent;
                input.className = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5';
                p.replaceChild(input, span);
            });
            editButton.textContent = 'Зберегти';
            editButton.onclick = saveChanges;
        }

        function saveChanges() {
            // Logic to save changes or toggle back to non-edit mode
        }

        editButton.addEventListener('click', enableEditMode);
        paymentMethodSelect.addEventListener('change', togglePaymentFields);
        deliveryMethodSelect.addEventListener('change', toggleDeliveryFields);
        togglePaymentFields();
        toggleDeliveryFields();
    });