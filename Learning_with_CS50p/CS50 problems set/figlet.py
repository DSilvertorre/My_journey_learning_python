import sys
from pyfiglet import Figlet, figlet_format

figlet = Figlet()
fontes_disponiveis = figlet.getFonts()

if len(sys.argv) < 3:
    sys.exit(1)

if sys.argv[1] not in ["-f", "--format"]:
    sys.exit(1)

fonte_escolhida = sys.argv[2]

if fonte_escolhida not in fontes_disponiveis:
    sys.exit(1)

write = input("Input: ")

resultado = figlet_format(write, font=fonte_escolhida)
print(f"Output: {resultado})
