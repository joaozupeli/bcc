# Guia de sobrevivência para a RA1 — Programação Imperativa em C

Este guia foi montado a partir dos módulos, do cronograma, do aviso e da prova anterior disponíveis no AVA da disciplina **Programação Imperativa — Turma 2º B — Ciência da Computação (manhã), 2026/2**.

## O que foi confirmado no AVA

- Prova: **quarta-feira, 16/09/2026, das 9h às 11h**.
- Valor: **10 pontos**; formato **somente teórico**, sem consulta.
- O professor informou que haverá **mais questões e maior complexidade** que no modelo de 2026/1, pois naquela edição também havia prova prática.
- Antes da prova haverá espaço para dúvidas, das **7h50 às 8h40**.
- Conteúdo anterior à RA1: fundamentos de C, controle de fluxo, funções, ponteiros, vetores, matrizes, tipos compostos, strings e argumentos de programa.

> O cronograma e os nomes dos PDFs trocam a numeração intermediária de alguns tópicos. O conjunto de assuntos, porém, é inequívoco. Este guia usa a ordem de dependência conceitual.

## Plano intensivo para hoje — 6 horas

| Bloco | Tempo | Objetivo | Teste de domínio |
|---|---:|---|---|
| Sintaxe, tipos e I/O | 50 min | Ler programas pequenos | Acertar `printf`, `scanf` e conversões |
| Decisões e repetição | 55 min | Rastrear `if`, `switch` e laços | Preencher uma tabela de execução |
| Memória e ponteiros | 70 min | Separar valor, endereço e desreferência | Explicar `x`, `&x`, `p`, `&p`, `*p` |
| Vetores, matrizes e `struct` | 65 min | Rastrear índices e alterações | Resolver mínimo, inversão e matriz |
| Funções | 45 min | Entender parâmetros e retorno | Dizer quando o original é alterado |
| Strings e argumentos | 50 min | Entender `\0`, limites e biblioteca | Prever `strlen`, `strcmp`, `argc/argv` |
| Prova anterior + simulado | 65 min | Treinar no formato real | Resolver sem executar o código |

Faça ciclos de 25 minutos de foco e 5 de pausa. Em cada bloco: conceito, rastreamento no papel e explicação em voz alta.

### Amanhã

1. 7h50–8h10: tire dúvidas sobre endereços, `sizeof`, `switch` e strings.
2. 8h10–8h30: refaça as quatro questões resolvidas da prova anterior.
3. 8h30–8h40: revise a folha mental no fim deste guia.
4. Depois, pare de estudar e entre na prova descansado.

## 1. O modelo mental de C

Em Python/TypeScript você pensa principalmente no valor. Em C pense em **tipo, valor e endereço**.

```c
int x = 82;
int *p = &x;
printf("%d", x);          // 82
printf("%p", (void *)&x); // endereço de x
printf("%p", (void *)p);  // o mesmo endereço
printf("%d", *p);         // 82
```

- `x` é uma casa e 82 é o morador.
- `&x` é o endereço da casa.
- `p` é um papel que guarda esse endereço.
- `*p` é “vá ao endereço do papel e veja o morador”.

Python e TypeScript escondem a maior parte dessa mecânica; C permite manipulá-la diretamente.

## 2. Estrutura mínima, tipos e I/O

```c
#include <stdio.h>

int main(void) {
    int idade = 20;
    double altura = 1.75;
    char inicial = 'A';
    printf("%d %.2f %c\n", idade, altura, inicial);
    return 0;
}
```

- `#include` é processado antes da compilação; `main` é o ponto de entrada.
- Blocos usam `{}`; indentação não tem semântica; comandos terminam em `;`.
- Tipos principais: `char`, `int`, `float`, `double` e `bool` (`stdbool.h`).

### Formatos essenciais

| Tipo | `printf` | `scanf` |
|---|---|---|
| `int` | `%d` | `%d` |
| `unsigned int` | `%u` | `%u` |
| `char` | `%c` | `%c` |
| `float` | `%f` | `%f` |
| `double` | `%f` | `%lf` |
| string | `%s` | `%s` |
| endereço | `%p` | — |
| `size_t`/`sizeof` | `%zu` | — |

```c
int idade;
double altura;
scanf("%d %lf", &idade, &altura);
```

`scanf` precisa alterar as variáveis e recebe seus endereços. Para vetor/string, o nome já se comporta como endereço do primeiro elemento:

```c
char nome[20];
scanf("%19s", nome); // sem &
```

### Armadilhas

```c
double a = 1 / 2;   // 0.0: divisão inteira primeiro
double b = 1.0 / 2; // 0.5
```

- `'A'` é `char`; `"A"` é uma string com `'A'` e `'\0'`.
- Caracteres participam de contas: `'D' - 'A' == 3`.
- Zero é falso; qualquer valor diferente de zero é verdadeiro.
- `=` atribui; `==` compara.

### Constantes, `enum` e `typedef`

```c
const double PI = 3.14159;
#define MAX 50
typedef enum { VERMELHO, VERDE, AMARELO } Cor;
Cor semaforo = VERDE; // normalmente 1
```

`const` cria dado somente leitura com tipo; `#define` faz substituição textual; `enum` cria constantes inteiras nomeadas; `typedef` cria sinônimo de tipo.

## 3. Controle de fluxo

- Relacionais: `>`, `<`, `>=`, `<=`, `==`, `!=`.
- Lógicos: `&&`, `||`, `!`.
- Aritméticos: `+`, `-`, `*`, `/`, `%`.

Sem chaves, um `else` pertence ao `if` anterior que ainda não tem `else`:

```c
if (a < b)
    if (b < c) x = 0;
    else x = 1; // pertence a if (b < c)
```

No `switch`, a expressão resulta em inteiro ou `char`. Sem `break`, a execução continua nos próximos casos (*fall-through*).

```c
switch (op) {
    case '+': resultado = a + b; break;
    case '-': resultado = a - b; break;
    default:  resultado = 0;
}
```

Laços:

```c
for (int i = 0; i < N; i++) { /* N vezes */ }
while (condicao) { /* talvez zero vezes */ }
do { /* pelo menos uma vez */ } while (condicao);
```

`for (int i=0; i<N; i++)` é a versão explícita de `for i in range(N)` do Python. Para rastrear, faça uma linha por iteração com `i`, condição, alterações e saída.

## 4. Ponteiros e memória

```c
int x = 10;
int *p = &x;
*p = 20; // altera x
```

| Expressão | Significado | Tipo |
|---|---|---|
| `x` | valor | `int` |
| `&x` | endereço de x | `int *` |
| `p` | endereço guardado | `int *` |
| `&p` | endereço do ponteiro | `int **` |
| `*p` | valor apontado | `int` |

```c
int **q = &p;
printf("%d", **q); // 20
```

Se o enunciado disser “alocação contígua, sem espaços”, some/subtraia os tamanhos. Na prova anterior, dado `c` em `0x...4f`, com as declarações `int k`, `float f`, `double d`, `char c`, os inícios esperados no modelo usado eram `d = 0x...50`, `f = 0x...58` e `k = 0x...5c`.

Se `p` é `int *`, `p + 1` avança `sizeof(int)` bytes, não um byte.

## 5. Vetores, matrizes e `struct`

```c
int v[5] = {4, 8, 5, 7, 9};
int N = sizeof(v) / sizeof(v[0]);
for (int i = 0; i < N; i++) printf("%d\n", v[i]);
```

- Índices válidos: `0` a `N-1`.
- C não verifica limites: `v[N]` é comportamento indefinido.
- `v[i]` equivale a `*(v + i)`.
- O nome do vetor geralmente converte-se em ponteiro para o primeiro elemento.

Padrão para localizar o menor:

```c
int menor = v[0], indice = 0;
for (int i = 1; i < N; i++) {
    if (v[i] < menor) {
        menor = v[i];
        indice = i;
    }
}
```

Matriz é parecida com lista de listas, mas possui dimensões fixas:

```c
int m[3][4];
for (int i = 0; i < 3; i++)
    for (int j = 0; j < 4; j++)
        printf("%d ", m[i][j]);
```

Estruturas agrupam campos:

```c
typedef struct {
    int matricula;
    float nota;
} Estudante;

Estudante e = {123, 8.5f};
Estudante *p = &e;
printf("%.1f", e.nota);
printf("%.1f", p->nota); // igual a (*p).nota
```

`struct` lembra uma `interface` TypeScript, mas também define um formato concreto em memória.

## 6. Funções

```c
int diferenca(int a, int b) {
    int d = a - b;
    return d < 0 ? -d : d;
}
```

C passa argumentos por valor:

```c
void tentar_mudar(int x) { x = 99; }
int a = 10;
tentar_mudar(a); // a continua 10
```

Para alterar a variável original, passe seu endereço:

```c
void mudar(int *x) { *x = 99; }
int a = 10;
mudar(&a); // a agora é 99
```

Vetores como parâmetros decaem para ponteiro e podem ter os elementos alterados. Passe o tamanho separadamente; dentro da função, `sizeof(v)` mede o ponteiro, não o vetor inteiro.

Em múltiplos arquivos, `.h` guarda contratos/protótipos e `.c` guarda implementações. Proteções como `#ifndef`, `#define`, `#endif` evitam inclusão dupla.

## 7. Strings

C não tem tipo nativo `string`: string é vetor de `char` terminado por `\0`.

```c
char nome[] = "Ana"; // 'A','n','a','\0'
```

- `sizeof(nome) == 4`; `strlen(nome) == 3`.
- `%s` imprime até `\0`.
- `scanf("%s", ...)` para no primeiro espaço.
- `gets` é insegura e não deve ser usada.
- `fgets(v, MAX, stdin)` lê no máximo `MAX-1` caracteres e pode guardar o Enter.

Remoção do Enter:

```c
fgets(texto, MAX, stdin);
texto[strcspn(texto, "\r\n")] = '\0';
```

| Função (`string.h`) | Resultado |
|---|---|
| `strlen(s)` | comprimento antes de `\0` |
| `strcpy(d, o)` | copia; destino precisa ter espaço |
| `strcat(d, o)` | concatena; destino precisa ter espaço |
| `strcmp(a, b)` | negativo, zero ou positivo |
| `strstr(frase, chave)` | ponteiro para ocorrência ou `NULL` |
| `strcspn(a, b)` | índice do primeiro caractere de `a` presente em `b` |

Não compare strings com `==`: isso compara endereços. Use `strcmp(a, b) == 0`.

`char mutavel[] = "abc"` pode ser alterado; um ponteiro para literal deve ser tratado como somente leitura: `const char *texto = "abc"`.

## 8. Argumentos do programa

```c
int main(int argc, char *argv[]) {
    for (int i = 0; i < argc; i++) printf("%s\n", argv[i]);
}
```

Em `./programa um dois`, `argc == 3`, `argv[0]` é o programa, `argv[1]` é `um` e `argv[2]` é `dois`. Tudo chega como string. Valide `argc` antes de acessar posições e converta com `sscanf`, `strtol`, `atoi` etc.

## A prova anterior resolvida

O modelo tinha 4 questões em 60 minutos. A prova atual terá 120 minutos, mais questões e maior complexidade.

### 1. Matemática e formatação

Para `x = 16`, `5*sqrt(x) + 3*x + 2.05 = 70.05`; `log2(x) + pow(x,2) = 260.00`. O formato `%.2f` preserva duas casas.

### 2. Endereços e tamanhos

Com `char=1`, `int/float=4`, `double=8` e alocação contígua, reconstrua os endereços somando tamanhos, sem inventar alinhamento.

### 3. Rastreamento de vetor

O candidato em `v[0]` mudava quando aparecia letra menor: `y → r → p → h → f`. Saída: **f**.

### 4. Ponteiro, ASCII e `switch`

`'D' - 'A' == 3`; entra em `case 3`; `'F' < 'A'` é falso; saída: **6**.

## Método para qualquer questão

1. Circule todo `printf`/`putchar`.
2. Liste tipos e valores iniciais.
3. Para ponteiros, desenhe setas.
4. Para laços/vetores, faça uma linha por iteração.
5. Em `switch`, calcule a expressão, marque o `case` e procure `break`.
6. Em strings, desenhe o `\0`.
7. Só depois aplique a formatação de saída.
8. Revise divisão inteira, limites, `= / ==`, `& / *` e `break`.

## Folha mental de 2 minutos

```text
scanf altera variável → geralmente precisa de &
vetor/string já vira endereço → scanf("%s", nome), sem &
&x = endereço | p = endereço guardado | *p = valor apontado
v[i] == *(v + i); índices válidos: 0..N-1
sizeof(v)/sizeof(v[0]) funciona onde v ainda é o vetor
char usa ' '; string usa " " e termina em \0
strlen não conta \0; sizeof(char[]) conta
strcmp(a,b)==0 significa strings iguais
switch sem break continua no próximo case
0 é falso; qualquer outro valor é verdadeiro
1/2 é 0; 1.0/2 é 0.5
argc conta argv[0], o nome do programa
```

Você está pronto se consegue prever saídas, rastrear decisões/laços, explicar ponteiros, achar mínimo em vetor, separar `sizeof` de `strlen`, explicar passagem por valor/referência e interpretar `argc/argv`. Meta: **9 de 12** no simulado.

