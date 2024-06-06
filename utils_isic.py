import os

def elenca_immagini(directory):
    elenco_immagini = []
    # Controlla tutti i file nella directory
    for filename in os.listdir(directory):
        # Verifica se il file è un'immagine
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".gif"):
            elenco_immagini.append(filename)
    return elenco_immagini

def salva_su_file(nomi_immagini, output_file):
    with open(output_file, "w") as file:
        for nome in nomi_immagini:
            file.write(nome + "\n")

if __name__ == "__main__":
    # Directory delle immagini
    directory_immagini = "data/isic_tiny/images/val2017"

    # Ottieni elenco delle immagini
    nomi_immagini = elenca_immagini(directory_immagini)

    # Nome del file di output
    file_output = "val.txt"

    # Salva l'elenco delle immagini su file
    salva_su_file(nomi_immagini, file_output)
