$(document).ready(function () {
    // Muestra el elemento de carga
    $('#loader-container').show();

    // Establece un temporizador para ocultar la carga después de 2 segundos (2000 milisegundos)
    setTimeout(function () {
        $('#loader-container').hide();
    }, 500);
});