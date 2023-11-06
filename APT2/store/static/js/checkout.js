document.addEventListener('DOMContentLoaded', function () {
  const deliveryOptions = document.querySelectorAll('input[name="delivery_method"]');
  const paymentOptions = document.querySelectorAll('input[name="payment_method"]');
  const deliveryDetails = document.getElementById('delivery-details');
  const comunaDropdown = document.getElementById('comuna');

  deliveryOptions.forEach(option => {
    option.addEventListener('change', function () {
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
      option.parentNode.classList.add('selected');
      updateDeliveryCost();
    });
  });
  paymentOptions.forEach(option => {
    option.addEventListener('change', function () {
      document.querySelectorAll('.payment-options label').forEach(label => {
        label.classList.remove('selected');
      });
      option.parentNode.classList.add('selected');
    });
  });
  comunaDropdown.addEventListener('change', updateDeliveryCost);
  function updateDeliveryCost() {
    const selectedDeliveryMethod = document.querySelector('input[name="delivery_method"]:checked');
    const selectedComuna = comunaDropdown.value;
    const deliveryCosts = {
      comuna1: 2000,
      comuna2: 3000,
    };

    if (selectedDeliveryMethod && selectedComuna) {
      const deliveryPrice = deliveryCosts[selectedComuna];
      const resumenTable = document.querySelector('#resumen');
      const existingDeliveryRow = document.querySelector('.delivery-row');
      if (selectedDeliveryMethod.value === 'delivery') {
        if (existingDeliveryRow) {
          updateDeliveryRow(existingDeliveryRow, `Delivery`, deliveryPrice);
        } else {
          addDeliveryRow(`Delivery`, deliveryPrice);
        }
      } else {
        if (existingDeliveryRow) {
          resumenTable.deleteRow(existingDeliveryRow.rowIndex);
        }
      }
      const total = calculateTotal(resumenTable, deliveryPrice);
      updateTotal(total);
    }
  }
  function calculateTotal(table) {
    let total = 0;
    const rows = table.rows;
    for (let i = 0; i < rows.length; i++) {
      const cells = rows[i].cells;
      if (cells.length === 2) {
        total += parseFloat(cells[1].textContent.replace('$', ''));
      }
    }

    return total;
  }
  function updateTotal(total) {
    const totalElement = document.querySelector('.total');
    totalElement.textContent = `Total compra: $${total.toFixed(0)}`;
  }
  function addDeliveryRow(deliveryName, deliveryPrice) {
    const resumenTable = document.querySelector('#resumen');
    const newRow = resumenTable.insertRow(-1);
    newRow.classList.add('delivery-row');
    const cell1 = newRow.insertCell(0);
    const cell2 = newRow.insertCell(1);
    cell1.textContent = deliveryName;
    cell2.textContent = `$${deliveryPrice}`;
  }
  function updateDeliveryRow(existingRow, deliveryName, deliveryPrice) {
    const cells = existingRow.cells;
    cells[0].textContent = deliveryName;
    cells[1].textContent = `$${deliveryPrice}`;
  }
  updateDeliveryCost();
});
