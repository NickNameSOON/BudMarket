document.getElementById('paymentMethod').addEventListener('change', function() {
    var paymentMethod = this.value;
    document.getElementById('creditCardInfo').style.display = 'none';
    document.getElementById('deliveryInfo').style.display = 'none';
    document.getElementById('pickupInfo').style.display = 'none';

    if (paymentMethod === 'creditCard') {
        document.getElementById('creditCardInfo').style.display = 'block';
    } else if (paymentMethod === 'delivery') {
        document.getElementById('deliveryInfo').style.display = 'block';
    } else if (paymentMethod === 'pickup') {
        document.getElementById('pickupInfo').style.display = 'block';
    }
});

// Ініціалізуйте форму з даними замовлення за допомогою JavaScript або від сервера
