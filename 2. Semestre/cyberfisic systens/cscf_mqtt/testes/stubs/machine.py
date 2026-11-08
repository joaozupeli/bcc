# Simulação mínima do módulo "machine" para rodar os main.py no MicroPython do PC.
# Os valores dos "sensores" vêm de arquivos na pasta HW_DIR e os "atuadores" escrevem lá.
import os
HW = os.getenv("HW_DIR", "/tmp/hw")

def _ler(nome, padrao):
    try:
        with open(HW + "/" + nome) as f:
            return f.read().strip()
    except OSError:
        return padrao

def _gravar(nome, valor):
    with open(HW + "/" + nome, "w") as f:
        f.write(str(valor))

class Pin:
    OUT = 1
    IN = 0
    def __init__(self, numero, modo=None):
        self.n = numero
    def value(self, v=None):
        if v is None:
            return int(_ler("out_%d" % self.n, "0"))
        _gravar("out_%d" % self.n, v)

class ADC:
    ATTN_11DB = 3
    def __init__(self, pin):
        self.n = pin.n
    def atten(self, a):
        pass
    def read(self):
        return int(_ler("adc_%d" % self.n, "2048"))

class PWM:
    def __init__(self, pin, freq=50):
        self.n = pin.n
    def duty_u16(self, v):
        _gravar("pwm_%d" % self.n, v)
