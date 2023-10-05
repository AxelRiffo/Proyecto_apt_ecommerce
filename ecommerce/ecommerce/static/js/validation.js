const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm_password');
const passwordRequirements = document.getElementById('password-requirements');
const confirmMessage = document.getElementById('confirm-password-message');

function checkPasswordRequirements() {
    const password = passwordInput.value;
    let message = '';

    if (password.length < 6) {
        message += 'La contraseña debe tener al menos 6 caracteres.<br>';
    }
    if (!/[A-Z]/.test(password)) {
        message += 'La contraseña debe contener al menos una mayúscula.<br>';
    }
    if (!/\d/.test(password)) {
        message += 'La contraseña debe contener al menos un número.<br>';
    }

    passwordRequirements.innerHTML = message;
}

function checkPasswordMatch() {
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    let message = '';

    if (password === '' || confirmPassword === '') {
        confirmMessage.innerHTML = '';  // Limpiar mensaje si uno o ambos campos están vacíos
    } else if (password !== confirmPassword) {
        message = 'Las contraseñas no coinciden.<br>';
    }

    confirmMessage.innerHTML = message;
}

passwordInput.addEventListener('input', function () {
    checkPasswordRequirements();
    checkPasswordMatch();
});

confirmPasswordInput.addEventListener('input', function () {
    checkPasswordMatch();
});
