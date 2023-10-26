$(document).ready(function () {
    // Muestra el elemento de carga
    $('#loader-container').show();

    // Establece un temporizador para aplicar un fade out al elemento de carga después de 2 segundos (2000 milisegundos)
    setTimeout(function () {
        $('#loader-container').fadeOut(500); // 500 milisegundos para la animación de fade out
    }, 100); // 2000 milisegundos para mostrar el elemento de carga
});
