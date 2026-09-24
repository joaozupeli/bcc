console.log("JS RODANDO")
const usuario = document.getElementById("usuario")
const senha = document.getElementById("senha")
const btn = document.getElementById("btnEntrar")

const cred = {
    "usuario": "zupeli",
    "senha": "0209"
}

btn.onclick = () => validate(usuario.value,senha.value)

function validate(usuario,senha) {
    if (!usuario || !senha){
        alert("Os campos deverão ser preenchidos corretamente")
    }

    if (usuario == cred.usuario && senha == cred.senha){
        console.log("Entrou")
        window.location.href="../listagem/listagem.html"
    }else{
        alert("Usuário ou senha inválidos")
    }
}


