bunch_size = 25
N = 75

cel = N // bunch_size
ostatok = N % bunch_size

for bunch_num in range(cel+1):
    cycles = bunch_size if (bunch_num != cel) else ostatok
    mass = []
    for i in range(cycles):
        numb = bunch_size * bunch_num + i
        mass.append(numb)
    print (mass)

date = "2023-03-20"
inf = 1234
dead = 342
healed = 50
ill = 543

item_dict = {
    "date":     {"S" : date },
    "infected": {"N": inf   },
    "dead":     {"N": dead  },
    "healed":   {"N": healed},
    "ill":      {"N": ill   },
}
putts = {"PutRequest" : {"Item" : item_dict}}

print (putts)