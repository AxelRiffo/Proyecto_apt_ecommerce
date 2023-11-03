document.addEventListener('DOMContentLoaded', function () {
  const deliveryOptions = document.querySelectorAll('input[name="delivery_method"]');
  const paymentOptions = document.querySelectorAll('input[name="payment_method"]');
  const deliveryDetails = document.getElementById('delivery-details');
  const comunaDropdown = document.getElementById('comuna');

  deliveryOptions.forEach(option => {
    option.addEventListener('change', function () {
      // Eliminar la clase 'selected' de todas las etiquetas de entrega
      document.querySelectorAll('.delivery-options label').forEach(label => {
        label.classList.remove('selected');
      });

      if (option.value === 'delivery') {
        deliveryDetails.style.display = 'block';
        comunaDropdown.style.display = 'block';
      } else if (option.value === 'local_pickup') {
        deliveryDetails.style.display = 'none';
        comunaDropdown.style.display = 'none';
      }

      // Agregar la clase 'selected' a la etiqueta seleccionada
      option.parentNode.classList.add('selected');
    });
  });

  paymentOptions.forEach(option => {
    option.addEventListener('change', function () {
      // Eliminar la clase 'selected' de todas las etiquetas de pago
      document.querySelectorAll('.payment-options label').forEach(label => {
        label.classList.remove('selected');
      });

      // Agregar la clase 'selected' a la etiqueta seleccionada
      option.parentNode.classList.add('selected');
    });
  });
});
