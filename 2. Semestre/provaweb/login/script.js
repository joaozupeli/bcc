console.log("Script da tela de login rodando normalmente")
const usuario = document.getElementById("usuario")
const senha = document.getElementById("senha")
const btn = document.getElementById("btnEntrar")

const credenciais = {
  "usuario": "mateusmelhorprofessor",
  "senha": "mateuslindao"
}

btn.onclick = () => login(usuario.value,senha.value)

function login (usuario, senha) {
  if (!usuario || !senha){
    alert("Os campos devem ser preenchidos corretamente")
  }

  if (usuario == credenciais.usuario && senha == credenciais.senha ){
    window.location.href="../listagem/listagem.html"
  }

}