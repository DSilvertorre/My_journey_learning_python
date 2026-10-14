lista_de_nomes = []
def main():
	name = input("Name: ")
	while name.isalpha:
		name = input("Nome: ")
		lista_de_nomes.append(name)
		if name == "":
			print("Adieu, adieu to", *lista_de_nomes)
		if name == "Fim":
			break	
main()
