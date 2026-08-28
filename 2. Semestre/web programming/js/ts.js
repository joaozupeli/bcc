console.log("Pagina carregada com sucesso")

const dado = [
    {
        nome: "WhatsApp",
        descricao: "WhatsApp é um aplicativo de mensagens instantâneas que permite enviar e receber mensagens de texto, imagens, vídeos e arquivos.",
        versao: "1.0.0",
        data_publicacao: "2026-01-01",
        imagem: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUZRR41jUmacEK0f2jajsAemwyelOyZ-8dAZEI8tNIrQ&s=10",
    },
    {
        nome: "Facebook",
        descricao: "Facebook é uma rede social que permite aos usuários criar perfis, adicionar amigos, compartilhar fotos e vídeos, e interagir com outros usuários.",
        versao: "1.0.0",
        data_publicacao: "2026-01-01",
        imagem: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzAuR8OqhfT7L1FBw7WAmtOSB_OzEsuARF-hPe8hr2Zg&s=10",
    },
    {
        nome: "Instagram",
        descricao: "Instagram é uma rede social que permite aos usuários compartilhar fotos e vídeos.",
        versao: "1.0.0",
        data_publicacao: "2026-01-01",
        imagem: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Instagram.svg/250px-Instagram.svg.png?utm_source=pt.wikipedia.org&utm_campaign=index&utm_content=thumbnail",
    },
    {
        nome: "Telegram",
        descricao: "Telegram é um aplicativo de mensagens instantâneas que permite enviar e receber mensagens de texto, imagens, vídeos e arquivos.",
        versao: "1.0.0",
        data_publicacao: "2026-01-01",
        imagem: "https://static.vecteezy.com/system/resources/thumbnails/009/428/317/small/3d-social-media-icons-telegram-free-png.png",
    },

]

const respostaMap = dado.map(item => `
    <tr>
        <td>${item.nome}</td>
        <td>${item.descricao}</td>
        <td>${item.versao}</td>
        <td>${item.data_publicacao}</td>
    </tr>
`).join("");

const cardMap = dado.map(item => 
    `
    <div class="card generic">
                 <div card-img>
                    <img class="img generic" src="${item.imagem}">
                    <div class="card-content generic" style="flex-direction: column;"">
                        <h3>-${item.nome}</h3>
                        <h3>-${item.descricao}</h3>                        
                        <h3>-${item.versao}</h3>                        
                        <h3>-${item.data_publicacao}</h3>                        
                    </div>
                </div>
            </div>
    `

).join("");


const tabela_Corpo = document.getElementById("tabelaCorpo")
const cardCorpo = document.getElementById("card-corpo")

cardCorpo.innerHTML = cardMap;
tabela_Corpo.innerHTML = respostaMap;

