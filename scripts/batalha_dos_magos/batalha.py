import time
import random
import pandas as pd
from pathlib import Path

class Batalha:
    def __init__(self, p1, p2, delay=0.4, iniciativa_aleatoria=False, status_period=5, verbose=True, save_output=True):
        self.p1 = p1
        self.p2 = p2
        self.delay = delay
        self.iniciativa_aleatoria = iniciativa_aleatoria
        self.status_period = status_period
        self.verbose = verbose
        self.logs = []
        self.save_output = save_output
        self.vencedor = None

    def status_turno(self, turno):
        '''
        Aplica efeitos de aumento de mana e perda de vida periodicamente.
        '''
        if self.status_period and turno % self.status_period == 0:
            # valores fixos (simples): +2 mana / -2 vida
            self.p1.mana += 2; 
            self.p2.mana += 2
            self.p1.vida -= 2; 
            self.p2.vida -= 2
            if self.verbose:
                print(f"\nTurno {turno}: +2 mana / -2 vida para ambos.")
        if self.verbose:
            print(f"\n--- Turno {turno} ---")

    def ordem_atacantes(self):
        jogadores = random.sample([self.p1, self.p2], k=2)
        return ((jogadores[0], jogadores[1]), (jogadores[1], jogadores[0]))
    
    def aplicar_ataques(self, turno):
        for atacante, alvo in self.ordem_atacantes():
            vida_antes = alvo.vida
            atacante.atacar(alvo)
            dano = max(0, vida_antes - alvo.vida)
            self.logs.append({
                "turno": turno,
                "atacante": atacante.nome,
                "alvo": alvo.nome,
                "dano": dano,
                "vida_alvo_pos": alvo.vida,
                "mana_atacante_pos": atacante.mana
            })
            if not alvo.esta_vivo():
                return True
        return False

    def imprimir_status(self):
        if self.verbose:
            print(f"{self.p1.nome} -> Vida: {self.p1.vida} | Mana: {self.p1.mana}")
            print(f"{self.p2.nome} -> Vida: {self.p2.vida} | Mana: {self.p2.mana}")

    def decidir_vencedor(self):
        if self.p1.esta_vivo() and not self.p2.esta_vivo():
            return self.p1.nome
        if self.p2.esta_vivo() and not self.p1.esta_vivo():
            return self.p2.nome
        return "Empate"

    def run(self):
        turno = 1
        while self.p1.esta_vivo() and self.p2.esta_vivo():
            self.status_turno(turno)
            alguem_morreu = self.aplicar_ataques(turno)
            self.imprimir_status()
            if alguem_morreu or not self.p1.esta_vivo() or not self.p2.esta_vivo():
                break
            turno += 1
            time.sleep(self.delay)

        self.vencedor = self.decidir_vencedor()
        if self.verbose:
            print("\n--- FIM DE JOGO ---")
            print("Vencedor:", self.vencedor)
        return self.vencedor

    def to_dataframe(self):
        df_logs = pd.DataFrame(self.logs)
        Path("output").mkdir(parents=True, exist_ok=True) # cria pasta se nao existir
        if self.save_output:
            df_logs.to_csv("output/logs_batalha.csv", index=False) # salva logs detalhados
            if not df_logs.empty:
                summary = df_logs.pivot_table(index="atacante", values="dano", aggfunc=["count", "sum"])
                summary.columns = ["ataques", "dano_total"]
                summary = summary.reset_index()
                filename = "output/resumo_batalha.csv"
                summary.to_csv(filename, index=False) # salva resumo da batalha
                if self.verbose:
                    print("Arquivos salvos em", filename)
            return df_logs
