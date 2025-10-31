# personagens.py
import random

class Personagem:
    def __init__(self, nome, vida=100, mana=50, variacao_dano=0.5):
        self.nome = nome
        self.vida = vida
        self.mana = mana
        self.variacao_dano = variacao_dano

    def atacar(self, outro):
        """Sobrescrito nas subclasses."""
        pass

    def esta_vivo(self):
        return self.vida > 0

    def dano_randomico(self, base):
        """Dano com variação configurável."""
        fator = random.uniform(1 - self.variacao_dano, 1 + self.variacao_dano)
        return int(round(base * fator))


class MagoFogo(Personagem):
    def atacar(self, outro):
        if self.mana >= 10:
            dano = self.dano_randomico(20)
            outro.vida -= dano
            self.mana -= 10
            print(f"{self.nome} lança BOLA DE FOGO em {outro.nome} (-{dano}).")
        else:
            print(f"{self.nome} sem mana suficiente.")


class MagoGelo(Personagem):
    def atacar(self, outro):
        if self.mana >= 8:
            dano = self.dano_randomico(15)
            outro.vida -= dano
            self.mana -= 8
            print(f"{self.nome} lança RAIO DE GELO em {outro.nome} (-{dano}).")
        else:
            print(f"{self.nome} sem mana suficiente.")
