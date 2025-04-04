with open("datos.txt") as archivo:
    for line in archivo:
        print(line.strip()) # Quita los espacios vacíos (\s,\n,\t)