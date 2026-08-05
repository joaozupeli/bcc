# =============================================================================
# SIMULADO P2 — LÓGICA DE PROGRAMAÇÃO
# Vetores · Funções · Recursividade
# Resolva cada questão antes de rodar. Na prova é na folha, sem computador.
# =============================================================================


# =============================================================================
# BLOCO 1 — TESTE DE MESA
# Leia o código, calcule o resultado mentalmente e anote antes de rodar.
# =============================================================================

print("=" * 50)
print("BLOCO 1 — TESTE DE MESA")
print("=" * 50)


print("\n--- Q1 ---")
vet = [4, 6, 4, 1, 2, 9, 13]
tam = len(vet)
a = 0

for i in range(tam):
    if vet[i] % 2 == 0:
        a += vet[i]
print(a)


print("\n--- Q2 ---")
vet = [0, 1]
for i in range(2, 8):
    vet.append(vet[i-1] + vet[i-2])
print(vet)


print("\n--- Q3 ---")
vet = [4, 6, 4, 1, 2, 9, 13]
tam = len(vet)
b = 0

for i in range(tam):
    if (vet[i] + vet[tam-1-i]) % 2 == 0:
        b += vet[i]
print(b)


print("\n--- Q4 ---")
vet = [66, 111, 109, 32, 100, 105, 97]

for i in range(len(vet)):
    print(chr(vet[i]), end='')
print()


print("\n--- Q5 ---")
def altera(a, b):
    temp = a
    a = b
    b = temp
    return a, b

vet = [4, 6, 4, 1, 2, 9, 13]
tam = len(vet)
for i in range(tam):
    m = i
    for j in range(i, tam):
        if vet[j] > vet[m]:
            m = j
    vet[i], vet[m] = altera(vet[i], vet[m])
print(vet)


print("\n--- Q6 ---")
def func(n, vet):
    ret = False
    for i in range(len(vet)):
        if n == vet[i]:
            ret = True
    return ret

vet = [1, 2, 3, 1, 3, 5, 8, 9, 10, 5]
r = func(3, vet)
print(r)


print("\n--- Q7 ---")
def avalia(string):
    count = 0
    for char in string:
        ascii_value = ord(char)
        if 65 <= ascii_value <= 90 or 97 <= ascii_value <= 122:
            count += 1
    return count

texto = "aB@c@dabra1234"
resultado = avalia(texto)
print(resultado)


print("\n--- Q8 ---")
def modifica(string):
    new_str = ''
    for char in string:
        ascii_value = ord(char)
        if 65 <= ascii_value <= 90:
            new_str += chr(ascii_value + 32)
        elif 97 <= ascii_value <= 122:
            new_str += chr(ascii_value - 32)
        else:
            new_str += char
    return new_str

texto = "Em 24/06/2023 fez UM belo DIA de Sol"
resultado = modifica(texto)
print(resultado)


# =============================================================================
# BLOCO 2 — IMPLEMENTAÇÃO
# Escreva cada função do zero. Sem usar max, min, sort, etc.
# =============================================================================

print("\n" + "=" * 50)
print("BLOCO 2 — IMPLEMENTAÇÃO")
print("=" * 50)


# Q9 — Maior elemento de um vetor sem usar max()
print("\n--- Q9: Maior elemento ---")

def maior_elemento(vet):
    pass  # escreva aqui

print(maior_elemento([3, 7, 2, 9, 1, 5]))
print(maior_elemento([10, 44, 3, 22, 8]))


# Q10 — Dois maiores elementos de um vetor
print("\n--- Q10: Dois maiores elementos ---")

def dois_maiores(vet):
    pass  # escreva aqui

print(dois_maiores([3, 7, 2, 9, 1, 5]))


# Q11 — Ordenação crescente sem sort()
print("\n--- Q11: Ordenação crescente ---")

def sort_(vet):
    pass  # escreva aqui

print(sort_([5, 2, 1, 3, 4]))
print(sort_([9, 3, 7, 1, 6, 2]))


# Q12 — Frequência dos elementos (retorna matriz)
# Ex: [1,2,1,3,3,4] → [[1,2],[2,1],[3,2],[4,1]]
print("\n--- Q12: Frequência dos elementos ---")

def frequencia(vet):
    pass  # escreva aqui

print(frequencia([1, 2, 1, 3, 3, 4, 3, 1, 2, 1, 1]))


# Q13 — Índices dos elementos pares
# Ex: [10, 11, 12, 13, 14] → [0, 2, 4]
print("\n--- Q13: Índices dos pares ---")

def indices_pares(vet):
    pass  # escreva aqui

print(indices_pares([10, 11, 12, 13, 14]))
print(indices_pares([3, 8, 5, 2, 7, 4]))


# Q14 — Validador de senha (usando ord(), sem isupper/isdigit)
# Regras: 8+ caracteres, 3+ maiúsculas, 3+ números
print("\n--- Q14: Validador de senha ---")

def valida_senha(senha):
    pass  # escreva aqui

print(valida_senha("ABC123def"))
print(valida_senha("abc123"))
print(valida_senha("AAAA1111bb"))


# Q15 — Inverter um vetor sem usar reverse()
print("\n--- Q15: Inverter vetor ---")

def invert_(vet):
    pass  # escreva aqui

print(invert_([1, 2, 3, 4, 5]))
print(invert_([9, 3, 7]))


# Q16 — Verificar se um vetor está ordenado (return True ou False)
print("\n--- Q16: Vetor está ordenado? ---")

def ordenado(vet):
    pass  # escreva aqui

print(ordenado([1, 2, 3, 4, 5]))
print(ordenado([1, 3, 2, 4, 5]))


# =============================================================================
# BLOCO 3 — RECURSIVIDADE
# Implemente cada função usando recursão — sem usar loops.
# =============================================================================

print("\n" + "=" * 50)
print("BLOCO 3 — RECURSIVIDADE")
print("=" * 50)


# Q17 — Fibonacci recursivo
# fibo(0)=0, fibo(1)=1, fibo(n)=fibo(n-1)+fibo(n-2)
print("\n--- Q17: Fibonacci recursivo ---")

def fibo(n):
    pass  # escreva aqui

for i in range(8):
    print(f"fibo({i}) =", fibo(i))


# Q18 — Fatorial recursivo
print("\n--- Q18: Fatorial recursivo ---")

def fatorial(n):
    pass  # escreva aqui

print(fatorial(5))
print(fatorial(0))
print(fatorial(7))


# Q19 — Soma dos dígitos recursiva
# Ex: soma_digitos(4871) = 4+8+7+1 = 20
print("\n--- Q19: Soma dos dígitos recursiva ---")

def soma_digitos(n):
    pass  # escreva aqui

print(soma_digitos(4871))
print(soma_digitos(123))
print(soma_digitos(9))


# Q20 — Soma dos elementos de um vetor (recursiva, sem loop)
print("\n--- Q20: Soma do vetor recursiva ---")

def soma_vetor(vet, i=0):
    pass  # escreva aqui

print(soma_vetor([1, 2, 3, 4, 5]))
print(soma_vetor([10, 20, 30]))


# Q21 — Imprimir de N até 0 recursivamente
print("\n--- Q21: Contagem regressiva recursiva ---")

def regressiva(n):
    pass  # escreva aqui

regressiva(5)


# Q22 — Contar dígitos de um número recursivamente
# Ex: conta_digitos(4871) = 4
print("\n--- Q22: Contar dígitos recursivo ---")

def conta_digitos(n):
    pass  # escreva aqui

print(conta_digitos(4871))
print(conta_digitos(99))
print(conta_digitos(7))