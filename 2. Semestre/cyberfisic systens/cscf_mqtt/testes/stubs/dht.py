import os
HW = os.getenv("HW_DIR", "/tmp/hw")
class DHT22:
    def __init__(self, pin):
        self.n = pin.n
    def _ler(self, nome, padrao):
        try:
            with open(HW + "/" + nome) as f:
                return float(f.read().strip())
        except OSError:
            return padrao
    def measure(self):
        pass
    def temperature(self):
        return self._ler("dht_temp", 24.0)
    def humidity(self):
        return self._ler("dht_umid", 60.0)
