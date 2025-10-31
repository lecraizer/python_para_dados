import json
from personagens import MagoFogo, MagoGelo
from batalha import Batalha

CLASSES = {"MagoFogo": MagoFogo, "MagoGelo": MagoGelo}

if __name__ == "__main__":
    with open("config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    mago1 = CLASSES[cfg["mago1"]](cfg["nome1"])
    mago2 = CLASSES[cfg["mago2"]](cfg["nome2"])

    batalha = Batalha(
        mago1, mago2,
        delay=cfg["delay"],
        iniciativa_aleatoria=cfg.get("iniciativa_aleatoria", False),
        verbose=cfg.get("verbose", True),
        status_period=cfg.get("status_period", 5),
        save_output=cfg.get("save_output", False)
    )
    vencedor = batalha.run()
    batalha.to_dataframe()
