
// Accounts
function show_pass_singup() {
    var password = document.getElementById("id_password");
    var confirm_password = document.getElementById("id_confirm_password");
    if (password.type === "password") {
        password.type = "text";
        confirm_password.type = "text";
    } else {
        password.type = "password";
        confirm_password.type = "password";
    }
}

function show_pass_login() {
    var password = document.getElementById("id_password");
    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}


