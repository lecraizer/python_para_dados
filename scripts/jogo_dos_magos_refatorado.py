'''
# Exercício: Batalha de Magos (Herança e Polimorfismo)

## Objetivo
Simular uma batalha entre dois magos usando classes, herança e polimorfismo, registrando logs e gerando um resumo com pandas.

## Instruções

1) Crie a classe base `Personagem` com:
   - Atributos: `nome` (string), `vida` (padrão: 100) e `mana` (padrão: 50).
   - Método `atacar(outro)`: definido na base, mas **sobrescrito** nas subclasses.
   - Método `esta_vivo()`: retorna `True` se `vida > 0`.

2) Crie as subclasses:
   - `MagoFogo`: ataque custa **10 de mana** e causa **20 de dano**.
   - `MagoGelo`: ataque custa **8 de mana** e causa **15 de dano**.

3) Regras do ataque:
   - Reduz a **vida** do oponente e a **mana** do atacante.
   - Imprime a ação e o dano causado.
   - Se faltar mana, imprimir mensagem e **não** causar dano.

4) Simulação:
   - Instancie um `MagoFogo` e um `MagoGelo`.
   - Em turnos alternados, cada um tenta atacar enquanto **ambos** estiverem vivos.
   - **Efeito periódico:** a cada **5 turnos**, ambos **recuperam +2 de mana** e **perdem -2 de vida**.
   - Após cada turno, mostre vida e mana de ambos.
   - A batalha termina quando algum personagem não estiver mais vivo (`vida <= 0`).

5) Final:
   - Imprima o vencedor.
   - Se os dois chegarem a `vida <= 0` no mesmo turno, imprima **"Empate"**.

6) Logs da batalha:
   - Após **cada ataque tentado**, adicione um registro (dicionário) em uma lista `logs` com:
     `{"turno": ..., "atacante": ..., "alvo": ..., "dano": ...}`
   - O **dano efetivo** é a diferença entre a vida do alvo **antes** e **depois** do ataque, com mínimo **0**.

7) Resumo com pandas:
   - Converta `logs` em um `DataFrame`.
   - Use `pivot_table` para gerar, por **atacante**, a **contagem de ataques** e a **soma do dano**.
   - Renomeie as colunas para `ataques` e `dano_total` e exiba o resumo.

   
Novas funcionalidades (desafios extras):

8) Adicione variação randômica ao dano: 
    - Entre −20% e +20% do valor base do dano.
    - Utilize o método `dano_randomico` nas subclasses.

9) Iniciativa aleatória:
    - Em cada turno, sorteie aleatoriamente a ordem dos atacantes.
    - Utilize o método `ordem_atacantes` na classe `Batalha`.

10) Encapsule a lógica da luta em uma classe `Batalha` com `run()`.

11) Logs e Resumo:
    - Centralize o registro de eventos na `Batalha` (lista `logs`).
    - Faça a `Batalha` gerar e salvar o resumo com pandas em CSV.
    - Mova parâmetros da simulação (nomes, classes, delay, etc.) para `config.json`.
'''

import time
import pandas as pd
import random

class Personagem:
    def __init__(self, nome, vida=100, mana=50, variacao=0.2):
        self.nome = nome
        self.vida = vida
        self.mana = mana
        self.variacao = variacao

    def atacar(self, outro):  # para sobrescrever nas subclasses
        pass

    def esta_vivo(self):
        return self.vida > 0


class MagoFogo(Personagem):
    def atacar(self, outro):
        if self.mana >= 10:
            fator = random.uniform(1-self.variacao, 1+self.variacao)
            dano_total = round(20 * fator, 2)
            outro.vida -= dano_total
            self.mana -= 10
            print(f"{self.nome} lança BOLA DE FOGO em {outro.nome} (-20).")
        else:
            print(f"{self.nome} sem mana suficiente.")


class MagoGelo(Personagem):
    def atacar(self, outro):
        if self.mana >= 8:
            fator = random.uniform(1-self.variacao, 1+self.variacao)
            dano_total = round(15 * fator, 2)
            outro.vida -= dano_total
            self.mana -= 8
            print(f"{self.nome} lança RAIO DE GELO em {outro.nome} (-15).")
        else:
            print(f"{self.nome} sem mana suficiente.")


class Batalha:
    def __init__(self, p1, p2, delay=0.8):
        self.p1 = p1
        self.p2 = p2
        self.delay = delay
        self.vencedor = None

    def ordem_jogadores(self):
        ordem = random.sample([self.p1, self.p2], k=2)
        return ordem

    def turno_especial(self, turno):
        '''
        A cada n rodadas, os jogadores perder vida e recebem mana
        '''
        if turno % 5 == 0:
            self.p1.mana += 2
            self.p2.mana += 2
            self.p1.vida -= 2
            self.p2.vida -= 2
            print(f"\nRecuperação de mana e perda de vida no turno {turno}!")

    def aplicar_ataque(self):
        jogadores = self.ordem_jogadores()
        for atacante, alvo in ((jogadores[0], jogadores[1]), (jogadores[1], jogadores[0])):
            # Ataque p1
            # vida_alvo_antes = alvo.vida
            atacante.atacar(alvo)
            # dano = max(0, vida_alvo_antes - alvo.vida)

            if not alvo.esta_vivo():
                return True # se alguém morre, encerra o turno
        return False

    def imprimir_status(self):
        print(f"{self.p1.nome} -> Vida: {self.p1.vida:.2f} | Mana: {self.p1.mana}")
        print(f"{self.p2.nome} -> Vida: {self.p2.vida:.2f} | Mana: {self.p2.mana}")

    def get_vencedor(self):
        if self.p1.esta_vivo() and not self.p2.esta_vivo():
            return self.p1.nome
        elif self.p2.esta_vivo() and not self.p1.esta_vivo():
            return self.p2.nome
        else:
            return "Empate"

    def run(self):
        turno = 1
        while self.p1.esta_vivo() and self.p2.esta_vivo():
            # A cada 5 rodadas, jogadores recuperam 2 de mana e perdem 2 de vida
            self.turno_especial(turno)

            print(f"\n--- Turno {turno} ---")

            # Ordena aleatoriamente uma lista de jogadores
            alguem_morreu = self.aplicar_ataque()
            if alguem_morreu:
                break
            
            turno += 1
            time.sleep(self.delay)

        self.vencedor = self.get_vencedor()
        print('\nO Vencedor do jogo é: ', self.vencedor)
        return self.vencedor


# --- Instâncias ---
p1 = MagoFogo("Arkon", vida=120, mana=40)
p2 = MagoGelo("Frost", vida=120,  mana=60)

batalha = Batalha(p1, p2)
batalha.run()



'''
# --- Pandas: log e resumo (meio termo com pivot_table) ---
df = pd.DataFrame(logs)
print("\nLOG:")
print(df)

summary = df.pivot_table(index="atacante", values="dano", aggfunc=["count", "sum"])
summary.columns = ["ataques", "dano_total"]
summary = summary.reset_index()

# summary.to_csv('sumario_do_jogo.csv', index=False)

print("\nRESUMO:")
print(summary)
'''