
from pathlib import Path

print("Arquivo atual:")
print(__file__)

print("\nCaminho absoluto:")
print(Path(__file__).resolve())

print("\nPasta pai:")
print(Path(__file__).resolve().parent)

print("\nPais do arquivo:")

for indice, pasta in enumerate(Path(__file__).resolve().parents):
    print(f"parents[{indice}]: {pasta}")

BASE_DIR = Path(__file__).resolve().parents[1]

print("\nBASE_DIR:")
print(BASE_DIR)

print("\nA pasta data existe?")
print((BASE_DIR / "data").exists())

ARQUIVO_CSV = BASE_DIR / "data" / "raw" / "vendas.csv"

print("\nCaminho do CSV:")
print(ARQUIVO_CSV)

print("\nO arquivo CSV existe?")
print(ARQUIVO_CSV.exists())
