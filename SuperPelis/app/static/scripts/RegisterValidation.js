function validateFields() {
    let password = document.getElementsByName("password")[0];
    let passwordCheck = document.getElementsByName("passwordCheck")[0];

    if (password.value !== passwordCheck.value) {
        passwordCheck.setCustomValidity("Las contraseñas no coinciden.");
    } else {
        passwordCheck.setCustomValidity("");
    }
}