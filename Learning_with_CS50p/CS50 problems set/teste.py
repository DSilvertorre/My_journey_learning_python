import sys
from pyfiglet import Figlet
import pyfiglet

figlet = Figlet()
lista = figlet.getFonts()

write = input("Input: ")

if not sys.argv[1] == "-f" or not sys.argv[1] == "--font":
    sys.exit("Invalid Usage")

if len(sys.argv) <= 1:
    sys.exit("Invalid Usage")

for font in lista:
    if sys.argv[2] in lista:
        pass
    else: sys.exit("Invalid Usage")

f = pyfiglet.figlet_format(write, font=sys.argv[2])
print(f"Output:\n{f}")


