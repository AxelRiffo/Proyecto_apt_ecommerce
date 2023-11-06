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
      updateDeliveryCost();
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

  comunaDropdown.addEventListener('change', updateDeliveryCost);

  function updateDeliveryCost() {
    const selectedDeliveryMethod = document.querySelector('input[name="delivery_method"]:checked');
    const selectedComuna = comunaDropdown.value;

    // Define los precios según la comuna
    const deliveryCosts = {
      comuna1: 2000,
      comuna2: 3000,
    };

    if (selectedDeliveryMethod && selectedComuna) {
      const deliveryPrice = deliveryCosts[selectedComuna];
      const resumenTable = document.querySelector('#resumen');

      // Verificar si ya existe una fila de "Delivery" en la tabla
      const existingDeliveryRow = document.querySelector('.delivery-row');
    
      if (selectedDeliveryMethod.value === 'delivery') {
        if (existingDeliveryRow) {
          // Si ya existe una fila de "Delivery", actualiza su contenido
          updateDeliveryRow(existingDeliveryRow, `Delivery`, deliveryPrice);
        } else {
          // Si no existe una fila de "Delivery", agrégala
          addDeliveryRow(`Delivery`, deliveryPrice);
        }
      } else {
        // Si se selecciona "Retiro en local" y existe una fila de "Delivery", elimínala
        if (existingDeliveryRow) {
          resumenTable.deleteRow(existingDeliveryRow.rowIndex);
        }
      }
    
      // Calcular el total de la compra incluyendo el costo de entrega si es necesario
      const total = calculateTotal(resumenTable, deliveryPrice);
      updateTotal(total);
    }
  }

  function calculateTotal(table) {
    let total = 0;
    
    // Recorrer todas las filas de la tabla para sumar los precios de los productos
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
    totalElement.textContent = `Total compra: $${total.toFixed(2)}`;
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

  // Ejecuta la función para inicializar el valor
  updateDeliveryCost();
});
