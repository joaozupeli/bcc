# Simulado RA1 — Programação Imperativa em C

**Tempo sugerido:** 75 minutos  
**Valor:** 12 pontos  
**Regra:** resolva no papel, sem compilar. Só consulte o gabarito depois.

## 1. Tipos, divisão e formatação

```c
int a = 7, b = 2;
double x = a / b;
double y = (double)a / b;
printf("%.1f %.1f", x, y);
```

A. `3.0 3.0`  
B. `3.5 3.5`  
C. `3.0 3.5`  
D. `3 3.5`

<!-- Resposta: (D) 3 3,5 Pois quando eu faço uma divisão sem transformar um dos divididos em double, essa divisão 
resulta em um numero inteiro, então a primeira divisão se tivesse um double teria dado 3.5 porem como nao teve nada, deu 3 -->


## 2. Expressão lógica

Com `a=4`, `b=7`, `c=7`, qual é o valor?

```c
(a < b && b == c) || a > c
```

A. `0`  
B. `1`  
C. `4`  
D. Erro

Resposta: (B) porque em C expressoes logicas  ao inves de retornar um valor booleano ela retorna 0(false) ou 1(true)
logo a afirmação acima se torna true pois temos uma condição de or entre as 2 expressoes

## 3. `switch` e fall-through

```c
int x = 2;
switch (x) {
    case 1: printf("A");
    case 2: printf("B");
    case 3: printf("C"); break;
    default: printf("D");
}
```

A. `B`  
B. `BC`  
C. `ABC`  
D. `BCD`

## 4. Laço

```c
int s = 0;
for (int i = 1; i <= 5; i++) {
    if (i % 2 == 0) s += i;
    else s -= 1;
}
printf("%d", s);
```

A. `3`  
B. `5`  
C. `6`  
D. `9`

## 5. Ponteiros

```c
int a = 5;
int *p = &a;
*p = *p + 3;
int **q = &p;
**q = **q * 2;
printf("%d", a);
```

A. `5`  
B. `8`  
C. `10`  
D. `16`

## 6. Memória contígua

```c
int i;      // 4 bytes
double d;   // 8 bytes
char c;     // 1 byte
```

O enunciado determina alocação contígua numa pilha que cresce para endereços menores. Se `c` começa em `0x1000`, onde começam `d` e `i`?

A. `d=0x1001`, `i=0x1009`  
B. `d=0x0ff8`, `i=0x0ff4`  
C. `d=0x1008`, `i=0x100c`  
D. Não é possível

## 7. Vetor

```c
int v[] = {8, 3, 9, 2, 7};
int N = sizeof(v) / sizeof(v[0]);
int k = 0;
for (int i = 1; i < N; i++)
    if (v[i] < v[k]) k = i;
printf("%d", k);
```

A. `1`  
B. `2`  
C. `3`  
D. `7`

## 8. Matriz

```c
int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
int s = 0;
for (int i = 0; i < 2; i++) s += m[i][i + 1];
printf("%d", s);
```

A. `5`  
B. `7`  
C. `8`  
D. `9`

## 9. Função e referência

```c
void ajuste(int a, int *b) {
    a += 10;
    *b += a;
}

int main(void) {
    int x = 2, y = 3;
    ajuste(x, &y);
    printf("%d %d", x, y);
}
```

A. `2 5`  
B. `2 15`  
C. `12 15`  
D. `12 3`

## 10. Strings

```c
char s[10] = "casa";
s[2] = '\0';
printf("%zu %zu %s", sizeof(s), strlen(s), s);
```

A. `10 4 casa`  
B. `10 2 ca`  
C. `3 2 ca`  
D. `10 3 cas`

## 11. Busca de substring

```c
char *frase = "programacao imperativa";
char *p = strstr(frase, "grama");
printf("%ld", p - frase);
```

A. `0`  
B. `3`  
C. `6`  
D. `NULL`

## 12. Argumentos

Execução: `./calc soma 8 5`

```c
int main(int argc, char *argv[]) {
    printf("%d %s %s", argc, argv[1], argv[3]);
}
```

A. `3 soma 5`  
B. `4 ./calc 8`  
C. `4 soma 5`  
D. `4 8 5`

---

# Gabarito comentado

1. **C.** A primeira divisão é inteira (`3`); o cast torna a segunda real (`3.5`).
2. **B.** As duas comparações ligadas por `&&` são verdadeiras.
3. **B.** Entra no caso 2 e continua até o `break` do caso 3.
4. **A.** Estados: `-1 → 1 → 0 → 4 → 3`.
5. **D.** `*p` muda `a` para 8; `**q` chega ao mesmo `a` e dobra para 16.
6. **A.** Neste modelo, as anteriores ocupam endereços maiores: 1 byte após `c` começa `d`; 8 bytes depois começa `i`.
7. **C.** `k` guarda o índice do menor valor; `2` está no índice 3.
8. **C.** Soma `m[0][1]=2` e `m[1][2]=6`.
9. **B.** `a` é cópia de `x`; `b` aponta para `y`, que recebe mais 12.
10. **B.** O vetor ocupa 10 bytes, mas a string termina no índice 2.
11. **B.** `grama` começa no índice 3.
12. **C.** O nome do programa também conta; `argc=4`.

## Resultado

- **10–12:** pronto para o formato; revise somente os erros.
- **8–9:** boa base; refaça as categorias erradas.
- **6–7:** revise ponteiros, vetores e strings.
- **0–5:** volte aos blocos 1–5 do roadmap antes de tentar novamente.

