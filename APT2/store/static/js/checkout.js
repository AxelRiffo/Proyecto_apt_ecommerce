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

document.addEventListener('DOMContentLoaded', function () {
  const checkoutButton = document.getElementById('checkout-button');
  checkoutButton.addEventListener('click', function () {
    const paymentMethodEfectivo = document.getElementById('payment-method-efectivo');
    if (paymentMethodEfectivo.checked) {
      fetch('ruta/a/checkout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),  // Asegúrate de tener la función getCookie
        },
        body: JSON.stringify({
          delivery_method: getSelectedDeliveryMethod(),
          comuna: getSelectedComuna(),
          // ... (otros campos del formulario)
        }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alertify.alert('Proceso completado', 'Pedido realizado con éxito.', function () {
            window.location.href = '{% url "Store" %}';
          });
        } else {
          alert('Error al procesar el pedido.');  // Manejar errores si es necesario
        }
      })
      .catch(error => {
        console.error('Error en la solicitud:', error);
      });
    }
  });
});

function getSelectedDeliveryMethod() {
  // Implementa la lógica para obtener el método de entrega seleccionado
}

function getSelectedComuna() {
  // Implementa la lógica para obtener la comuna seleccionada
}

document.getElementById('checkout-button').addEventListener('click', function (event) {
  event.preventDefault();
  var paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
  if (paymentMethod === 'mercadopago') {
    window.location.href = this.getAttribute('data-url');
  } else if (paymentMethod === 'efectivo') {
    alertify.alert('Proceso completado', 'Pedido realizado con éxito.', function () {
      window.location.href = cuentaUrl;
    });
  }
});


//PAL MERCADO PAGO
document.getElementById('checkout-button').addEventListener('click', function (event) {
  event.preventDefault();
  var paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
  if (paymentMethod === 'mercadopago') {
    fetch('/procesar_pago/', {  // Asegúrate de que esta es la ruta correcta a tu vista `procesar_pago`
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),  // Asegúrate de tener la función getCookie
      },
      body: JSON.stringify({
        delivery_method: getSelectedDeliveryMethod(),
        comuna: getSelectedComuna(),
        direccion: getDireccion(),
        telefono: getTelefono(),
        payment_method: getPaymentMethod(),
        total: getTotal(),
        status: getStatus(),
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data && data.success) {
          window.location.href = data.payment_url;
        } else {
          console.error('Error al procesar el pedido:', data && data.error);
          alert('Error al procesar el pedido.');
        }
      })
      .catch(error => {
        console.error('Error en la solicitud:', error);
      });
  } else if (paymentMethod === 'efectivo') {
    alertify.alert('Proceso completado', 'Pedido realizado con éxito.', function () {
      window.location.href = cuentaUrl;
    });
  }
});

function getSelectedDeliveryMethod() {
  const selectedDeliveryMethod = document.querySelector('input[name="delivery_method"]:checked');
  return selectedDeliveryMethod ? selectedDeliveryMethod.value : null;
}

function getSelectedComuna() {
  const selectedComuna = document.getElementById('comuna');
  return selectedComuna ? selectedComuna.value : null;
}


function getDireccion() {
  return document.getElementById('address').value;
}

function getTelefono() {
  return document.getElementById('phone').value;
}

function getPaymentMethod() {
  return document.querySelector('input[name="payment_method"]:checked').value;
}

function getTotal() {
  // Aquí necesitas implementar la lógica para calcular el total del pedido
  // Esto dependerá de cómo estés manejando los precios y las cantidades en tu carrito de compras
}

function getStatus() {
  return 'preparacion';
}


function getTotal() {
  // Obtiene los items del carrito
  var items = getCarritoItems();

  // Calcula el total sumando el precio de cada item multiplicado por su cantidad
  var total = items.reduce(function (sum, item) {
    return sum + item.producto.precio * item.cantidad;
  }, 0);

  return total;
}

function getCarritoItems() {
  // Obtiene los items del carrito del almacenamiento local
  var carrito = JSON.parse(localStorage.getItem('carrito')) || {};

  // Convierte los items del carrito en un array de objetos
  var items = Object.keys(carrito).map(function (key) {
    return {
      producto: carrito[key]['producto'],
      cantidad: carrito[key]['cantidad']
    };
  });

  return items;
}

