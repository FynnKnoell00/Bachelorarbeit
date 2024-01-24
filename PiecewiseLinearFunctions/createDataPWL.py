import random
import math

# Zufällige Erzeugung von Angebot (supply) und Nachfrage (demand)
supply = [random.randint(0, 2000) for _ in range(random.randint(10, 10))]
demand = [random.randint(0, min(2000, sum(supply))) for _ in range(random.randint(10, 10))]

# Berechnung der Gesamtwerte von Angebot und Nachfrage
supplyValue = sum(supply)
demandValue = sum(demand)

# Berechnung der Differenz
diff = supplyValue - demandValue

# Verteilung der Differenz gleichmäßig auf alle Elemente
while diff != 0:
    if diff > 0:
        # Angebot ist größer als Nachfrage
        for i in range(len(supply)):
            if (supply[i] > 0):
                supply[i] = min(2000, supply[i] - 1)
                diff -= 1
                if diff == 0:
                    break
    else:
        # Nachfrage ist größer als Angebot
        for i in range(len(demand)):
            if (demand[i] > 0):
                demand[i] = min(2000, demand[i] - 1)
                diff += 1
                if diff == 0:
                    break

# Überprüfung, dass die Summe von Angebot und Nachfrage gleich ist
assert sum(supply) == sum(demand)


nbSupply = len(supply)
nbDemand = len(demand)

# Generiere 3 zufällige Stützstellen
breakpoints = [(0, 0)]
for _ in range(3):
    ulx = min(2000, breakpoints[-1][0] + 750)
    llx = breakpoints[-1][0] + 1
    x = random.randint(llx, ulx)

    uly = min(1000, breakpoints[-1][1] + 400)
    lly = breakpoints[-1][1] + 1
    y = random.randint(lly , uly)
    breakpoints.append((x, y))

breakpoints.append((2000, 1000))


for i in range(1, len(breakpoints) - 1):
    slope_prev = (breakpoints[i][1] - breakpoints[i-1][1]) / (breakpoints[i][0] - breakpoints[i-1][0])
    slope_next = (breakpoints[i+1][1] - breakpoints[i][1]) / (breakpoints[i+1][0] - breakpoints[i][0])
    
    while slope_prev <= slope_next:
        # Solange die Steigung nicht abnimmt, aktualisiere den aktuellen Punkt
        y_increment = random.uniform(0, min(1000 - breakpoints[i][1], 500))
        y_increment = math.ceil(y_increment)
        breakpoints[i] = (breakpoints[i][0], breakpoints[i][1] + y_increment)
        slope_prev = (breakpoints[i][1] - breakpoints[i-1][1]) / (breakpoints[i][0] - breakpoints[i-1][0])
        slope_next = (breakpoints[i+1][1] - breakpoints[i][1]) / (breakpoints[i+1][0] - breakpoints[i][0])

# Schreiben der Daten in eine Textdatei
with open("testdata.txt", "w") as file:
    file.write("Supply: {}\n".format(supply))
    file.write("nbSupply: {}\n".format(nbSupply))
    file.write("Demand: {}\n".format(demand))
    file.write("nbDemand: {}\n".format(nbDemand))

    file.write("\nGenerated Breakpoints:\n")
    for point in breakpoints:
        file.write("({}, {})\n".format(point[0], point[1]))

    file.write("\nSlopes between Breakpoints:\n")
    for i in range(1, len(breakpoints)):
        slope = (breakpoints[i][1] - breakpoints[i-1][1]) / (breakpoints[i][0] - breakpoints[i-1][0])
        file.write("Between {} and {}: {}\n".format(breakpoints[i-1], breakpoints[i], slope))

