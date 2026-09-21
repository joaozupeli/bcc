console.log("Pagina carregada com sucesso")

const dado = [
    {
        nome: "Airbnb",
        descricao: "Airbnb é uma plataforma online de hospedagem que conecta anfitriões e viajantes ao redor do mundo.",
        ranking: 1,
        valor_mercado: "US$ 100 bilhões"
    },
    {
        nome: "Uber",
        descricao: "Uber é um aplicativo de transporte privado que conecta motoristas parceiros a passageiros.",
        ranking: 2,
        valor_mercado: "US$ 90 bilhões"
    },
    {
        nome: "Stripe",
        descricao: "Stripe é uma fintech de pagamentos online que oferece infraestrutura para pagamentos digitais.",
        ranking: 3,
        valor_mercado: "US$ 50 bilhões"
    },
    {
        nome: "Nubank",
        descricao: "Nubank é uma fintech brasileira líder em serviços financeiros digitais com atuação internacional.",
        ranking: 4,
        valor_mercado: "US$ 37 bilhões"
    },
    {
        nome: "SpaceX",
        descricao: "SpaceX é uma empresa aeroespacial com foco em tecnologia de foguetes e exploração espacial.",
        ranking: 5,
        valor_mercado: "US$ 140 bilhões"
    },
    {
        nome: "ByteDance",
        descricao: "ByteDance é uma gigante chinesa de tecnologia conhecida pelo aplicativo TikTok.",
        ranking: 6,
        valor_mercado: "US$ 225 bilhões"
    },
    {
        nome: "Canva",
        descricao: "Canva é uma plataforma de design gráfico online que permite a criação de designs de forma simples.",
        ranking: 7,
        valor_mercado: "US$ 26 bilhões"
    },
    {
        nome: "Revolut",
        descricao: "Revolut é uma empresa de tecnologia financeira que oferece serviços bancários digitais inovadores.",
        ranking: 8,
        valor_mercado: "US$ 33 bilhões"
    },
    {
        nome: "Didi Chuxing",
        descricao: "Didi Chuxing é uma empresa chinesa líder em serviços de transporte por aplicativo.",
        ranking: 9,
        valor_mercado: "US$ 38 bilhões"
    },
    {
        nome: "Epic Games",
        descricao: "Epic Games é uma desenvolvedora de jogos conhecida por títulos como Fortnite e pelo motor Unreal Engine.",
        ranking: 10,
        valor_mercado: "US$ 31 bilhões"
    }
]

const respostaMap = dado.map(item => `
    <tr>
        <td>${item.nome}</td>
        <td>${item.descricao}</td>
        <td>${item.ranking}</td>
        <td>${item.valor_mercado}</td>
    </tr>
`).join("");

const tabela_Corpo = document.getElementById("tabelaCorpo")

tabela_Corpo.innerHTML = respostaMap;