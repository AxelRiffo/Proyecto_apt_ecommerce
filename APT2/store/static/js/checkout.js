document.addEventListener('DOMContentLoaded', function () {
    const deliveryOptions = document.querySelectorAll('input[name="delivery_method"]');
    const deliveryDetails = document.getElementById('delivery-details');
    const localPickupDetails = document.getElementById('local-pickup-details');
    const comunaDropdown = document.getElementById('comuna');
  
    deliveryOptions.forEach(option => {
      option.addEventListener('change', function () {
        if (option.value === 'delivery') {
          deliveryDetails.style.display = 'block';
          localPickupDetails.style.display = 'none';
          comunaDropdown.style.display = 'block';
        } else if (option.value === 'local_pickup') {
          deliveryDetails.style.display = 'none';
          localPickupDetails.style.display = 'block';
          comunaDropdown.style.display = 'none';
        }
      });
    });
  });
  
  