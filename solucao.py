fileName = 'corrida.log'

def mergeSort(arr): 
    if len(arr) >1: 
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:] 
        mergeSort(L) 
        mergeSort(R)
  
        i = j = k = 0
          
        while i < len(L) and j < len(R): 
            if type(R[j]) == str:
                print(R)
            if L[i]['hour'] < R[j]['hour']: 
                arr[k] = L[i]
                i+=1
            else: 
                arr[k] = R[j]
                j+=1
            k+=1
          
        while i < len(L): 
            arr[k] = L[i]
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j]
            j+=1
            k+=1


def readFile(fileName):
    with open(fileName) as f:
        text = f.readlines()
        racing = []
        pilots = set()
        bestTurn = {
            'turnTime':'59:59.999'
        }
        for line in text:
            line = line.split()
            turn = {
                'hour': line[0],
                'code': line[1],
                'pilot': line[3],
                'turnNumber': int(line[4]),
                'turnTime': line[5],
                'turnSpeed': line[6]
            }
            if turn['turnTime'] < bestTurn['turnTime']:
                bestTurn = turn

            pilots.add(turn['code'])
            racing.append(turn)
    mergeSort(racing)
    return racing, pilots, bestTurn   # Creates a dictionary with data about every turn, a set with pilots names and the best turn

racing, pilots, bestTurn = readFile(fileName)


def getRacingTime(racing, turn):
    import datetime

    racingStart = datetime.datetime.strptime(racing[0]['hour'], '%H:%M:%S.%f') - datetime.datetime.strptime(racing[0]['turnTime'], '%M:%S.%f')
    racingEnd = datetime.datetime.strptime(turn['hour'], '%H:%M:%S.%f')
    return (racingEnd - racingStart).strftime('%M:%S.%f')


def getBestTurn(racing, pilot):
    best = {
        'turnTime': '59:59.999'
    }
    for turn in racing:
        if turn['code'] == pilot and turn['turnTime'] < best['turnTime']:
            best['turnTime'] = turn['turnTime']
            best['turnNumber'] = turn['turnNumber']
            best['turnSpeed'] = turn['turnSpeed']
    return best


def getSpeed(racing, pilot):
    i = 0
    speed = 0
    for turn in racing:
        if turn['code'] == pilot:
            i += 1
            turnSpeed = '.'.join(turn['turnSpeed'].split(','))
            speed += float(turnSpeed)
    return speed / i


arrivalOrder = []
for turn in racing:
    if turn['turnNumber'] == 4:     # Read the positions of the pilots that completed 4 turns
        arrival = {
            'position': len(arrivalOrder) + 1,
            'code': turn['code'],
            'pilot': turn['pilot'],
            'numberOfTurns': turn['turnNumber'],
            'racingTime': getRacingTime(racing, turn),
            'bestTurn': getBestTurn(racing, turn['code'])
        }
        pilots.remove(turn['code'])
        arrivalOrder.append(arrival)

auxPilots = pilots.copy()
lastArrival = []
if auxPilots:       # Read the positions of the pilots that didn't completed 4 turns
    for pilot in auxPilots:
        for turn in racing[::-1]:
            if pilot == turn['code']:
                pilots.remove(pilot)
                arrival = {
                    'position': len(arrivalOrder) + 1,
                    'code': turn['code'],
                    'pilot': turn['pilot'],
                    'numberOfTurns': turn['turnNumber'],
                    'racingTime': getRacingTime(racing, turn),
                    'bestTurn': getBestTurn(racing, turn['code'])
                }
                lastArrival.append(arrival)
                break

del auxPilots
arrivalOrder.extend(lastArrival)
del lastArrival

mainOutput = """
Position\t\tPilot's Code\t\tPilot's Name\t\tCompleted Turns\t\tAverage Speed\t\tBest Turn Speed\t\tBest Turn Time\t\tBest Turn Number\t\tTotal Time
"""

for arrival in arrivalOrder:
    text = '\n{:^8}\t\t{:^12}\t\t{:^12}\t\t{:^15}\t\t{:^13.5}\t\t{:^15}\t\t{:^14}\t\t{:^15}\t\t{:^10.7}'.format(
        arrival['position'],
        arrival['code'],
        arrival['pilot'],
        arrival['numberOfTurns'],
        getSpeed(racing, arrival['code']),
        arrival['bestTurn']['turnSpeed'],
        arrival['bestTurn']['turnTime'],
        arrival['bestTurn']['turnNumber'],
        arrival['racingTime'])
    mainOutput += text
print(mainOutput)
print("""\n\nRace's best turn:

Pilot's Code: {},
Pilot's Name: {},
Turn Number: {},
Turn Time: {},
Turn Speed: {}""".format(bestTurn['code'], bestTurn['pilot'], bestTurn['turnNumber'], bestTurn['turnTime'], bestTurn['turnSpeed']))
