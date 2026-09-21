console.log("JS RODANDO")
const email = document.getElementById("login")
const senha = document.getElementById("pass")
const btn = document.getElementById("btnEntrar")

const cred = {
    "email": "zupelidev@gmail.com",
    "senha": "0306"
}

btn.onclick = validate(email.value,senha.value)

function validate(email,senha) {
    if (!email || !senha){
        alert("Os campos deverão ser preenchidos corretamente")
    }

    if (email == cred.email && senha == cred.senha){
        console.log("Entrou")
    }
}
