import time
import sys
import random
import numpy as np

class Coordinate:
    def __init__(self, col, row, value):
        self.col = col
        self.row = row
        self.value = value


class Sequence:
    def __init__(self, pattern, reward):
        self.pattern = pattern
        self.reward = reward

buffer = []
max_buffer = []
sequences = []
buffer_size = 0
max_reward = 0


def readInputFile(file_path):
    while True:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                buffer_size = int(lines[0])
                matrix_col, matrix_row = map(int, lines[1].split())
                matrix = [line.split() for line in lines[2:2+matrix_row]]

                check1 = True
                check2 = True
                for i in range (len(matrix)) :
                    for j in range(len(matrix[0])) :
                        if (len(matrix[i][j])) != 2 :
                            check1 = False
                        if (not(matrix[i][j].isalnum())) :
                            check2 = False

                if(check1 == False) :
                    print("Silahkan run ulang program kembali karena token tidak terdiri dari 2 karakter")
                    sys.exit()
                if(check2 == False) :
                    print("Silahkan run ulang program kembali karena token tidak terdiri dari alfanumerik")
                    sys.exit()

                num_sequences = int(lines[2 + matrix_row])
                current_line = 3 + matrix_row
                for _ in range(num_sequences):
                    sequence = lines[current_line].split()
                    current_line += 1

                    sequence_reward = int(lines[current_line])
                    current_line += 1

                    sequence_instance = Sequence(sequence, sequence_reward)
                    sequences.append(sequence_instance)

            return buffer_size, matrix, sequences

        except FileNotFoundError:
            file_path = input("File tidak ditemukan. Silahkan input ulang nama file: ")


def readInputTerminal():
    check1 = True
    check2 = True
    check3 = True
    total_token = int(input(""))
    token = input("")
    token_list = token.split()

    if (len(token_list)) != total_token :
        check3 = False
    
    if(check3 == False) :
        print("Silahkan run ulang program kembali karena jumlah token tidak sesuai")
        sys.exit()
        
    for i in range (len(token_list)) :
        if (len(token_list[i])) != 2 :
            check1 = False
        if (not(token_list[i].isalnum())) :
            check2 = False

    if(check1 == False) :
        print("Silahkan run ulang program kembali karena token tidak terdiri dari 2 karakter")
        sys.exit()
    
    if(check2 == False) :
        print("Silahkan run ulang program kembali karena token tidak terdiri dari alfanumerik")
        sys.exit()

    buffer_size = int(input(""))
    matrix_size = input("")
    matrix_col, matrix_row = map(int, matrix_size.split())
    matrix = np.array([[random.choice(token_list) for _ in range(matrix_col)] for _ in range(matrix_row)], dtype=object)

    total_sequence = int(input(""))
    sequence_size = int(input(""))

    for _ in range(total_sequence):
        seq = random.randint(2, sequence_size)
        sequence_token = [random.choice(token_list) for _ in range(seq)]
        reward = random.randint(1, 100)
        sequence_instance = Sequence(sequence_token, reward)
        sequences.append(sequence_instance)

    return buffer_size, matrix, sequences


def outputToFile(file_path, max_reward, max_buffer, start_time, end_time):
    try:
        with open(file_path, 'w') as file:
            if max_reward == 0:
                file.write(str(max_reward) + "\n")
                file.write("No Solution\n")
            else:
                file.write(str(max_reward) + "\n")
                for item in max_buffer:
                    file.write(str(item.value) + " ")
                file.write('\n')
                for item in max_buffer:
                    file.write(f'{item.col}, {item.row}\n')
            execution_time = round((end_time - start_time) * 1000)
            file.write(f'{execution_time} ms\n')

        print("Output telah disimpan ke", file_path)
    except IOError:
        print("Error: Unable to write to file", file_path)


def hasSequence(seq, buff):
    has_sequence = True
    for j in range(len(buff) - len(seq.pattern) + 1):
        has_sequence = True
        for i in range(len(seq.pattern)):
            if seq.pattern[i] != buff[i+j].value:
                has_sequence = False
        if has_sequence:
            return True
    return False


def countReward(buff):
    rewards = 0
    for i in range(len(sequences)):
        if hasSequence(sequences[i], buff):
            rewards += sequences[i].reward
    return rewards

def hasPass(coord, buff):
    for i in range(len(buff)):
        if coord.row == buff[i].row and coord.col == buff[i].col:
            return True
    return False

def findRoute(coord, buff, vertical):
    global max_reward
    global max_buffer
    global buffer_size
    if coord.col == 0 and coord.row == 0:
        for i in range(len(matrix[0])):
            newCoord = Coordinate(i + 1, 1, matrix[0][i])
            if not hasPass(newCoord, buff):
                newBuffer = buff[:]
                newBuffer.append(newCoord)
                reward = countReward(newBuffer)
                if reward > max_reward:
                    max_reward = reward
                    max_buffer = newBuffer
                findRoute(newCoord, newBuffer, True)

    elif len(buff) == buffer_size:
        return
    
    elif vertical:
        for i in range(len(matrix)):
            newCoord = Coordinate(coord.col, i + 1, matrix[i][coord.col - 1])
            if not hasPass(newCoord, buff):
                newBuffer = buff[:]
                newBuffer.append(newCoord)
                reward = countReward(newBuffer)
                if reward > max_reward:
                    max_reward = reward
                    max_buffer = newBuffer
                findRoute(newCoord, newBuffer, False)

    elif not vertical:
        for i in range(len(matrix[0])):
            newCoord = Coordinate(i + 1, coord.row, matrix[coord.row - 1][i])
            if not hasPass(newCoord, buff):
                newBuffer = buff[:]
                newBuffer.append(newCoord)
                reward = countReward(newBuffer)
                if reward > max_reward:
                    max_reward = reward
                    max_buffer = newBuffer
                findRoute(newCoord, newBuffer, True)


##################################################################################################
# MAIN PROGRAM
print("__        _______ _     ____ ___  __  __ _____     _____ ___  ")
print("\ \      / / ____| |   / ___/ _ \|  \/  | ____|   |_   _/ _ \ ")
print(" \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|       | || | | |")
print("  \ V  V / | |___| |__| |__| |_| | |  | | |___      | || |_| |")
print("   \_/\_/  |_____|_____\____\___/|_|  |_|_____|     |_| \___/ ")

print("  ______   ______  _____ ____  ____  _   _ _   _ _  __     ____   ___ _____ _____ ")
print(" / ___\ \ / / __ )| ____|  _ \|  _ \| | | | \ | | |/ /    |___ \ / _ \___  |___  |")
print("| |    \ V /|  _ \|  _| | |_) | |_) | | | |  \| | ' /       __) | | | | / /   / / ")
print("| |___  | | | |_) | |___|  _ <|  __/| |_| | |\  | . \      / __/| |_| |/ /   / /  ")
print(" \____| |_| |____/|_____|_| \_\_|    \___/|_| \_|_|\_\    |_____|\___//_/   /_/   ")

print(" ____  ____  _____    _    ____ _   _      ____  ____   ___ _____ ___   ____ ___  _     ")
print("| __ )|  _ \| ____|  / \  / ___| | | |    |  _ \|  _ \ / _ \_   _/ _ \ / ___/ _ \| |    ")
print("|  _ \| |_) |  _|   / _ \| |   | |_| |    | |_) | |_) | | | || || | | | |  | | | | |    ")
print("| |_) |  _ <| |___ / ___ \ |___|  _  |    |  __/|  _ <| |_| || || |_| | |__| |_| | |___ ")
print("|____/|_| \_\_____/_/   \_\____|_| |_|    |_|   |_| \_\\___/ |_| \___/ \____\___/|_____|")

print ("\n")

print("1. Masukkan melalui file .txt")
print("2. Masukkan melalui CLI")

program = input("Pilih jenis masukkan (1/2): ")

while program != "1" and program != "2":
    program = input("Silakan pilih ulang jenis masukan (1/2): ")

if program == "1":
    file = input("Masukkan nama file: ")
    new_file_path = f'test/{file}'
    buffer_size, matrix, sequences = readInputFile(new_file_path)

elif program == "2":
    buffer_size, matrix, sequences = readInputTerminal()

print(f'Ukuran Buffer: {buffer_size}')
print(f'Ukuran Kolom Matrix: {len(matrix[0])}')
print(f'Ukuran Baris Matrix: {len(matrix)}')
print("Matriks: ")
for row in matrix:
    for element in row:
        print(element, end=" ") 
    print() 

print(f'Jumlah sekuens: {len(sequences)}')
print("Sekuens: ")
for i in range (len(sequences)):
    print(f'sekuen {sequences[i].pattern} memiliki reward {sequences[i].reward}')


for i in range (len(sequences)) :
    if (len(sequences[i].pattern)) < 2 :
        print("Silahkan run ulang program kembali karena sekuens reward kurang dari 2 token")
        sys.exit()


start_time = time.time()
start_coord = Coordinate(0, 0, "")
test = findRoute(start_coord, buffer, False)
end_time = time.time()


if max_reward == 0:
    print(max_reward)
    print("No Solution")
else:
    print(max_reward)
    for i in range(len(max_buffer)):
        print(max_buffer[i].value, end=" ")
    print('')
    for i in range(len(max_buffer)):
        print(f'{max_buffer[i].col}, {max_buffer[i].row}')
print(round((end_time - start_time) * 1000), 'ms')


copy = input("Apakah ingin menyimpan solusi? (y/n) : ")
while copy != "y" and copy != "n":
    copy = input("Silahkan pilih ulang untuk simpan (y/n) : ")

if copy == "y":
    file_name = input("Masukkan nama file untuk menyimpan output: ")
    new_path = f'test/{file_name}'
    outputToFile(new_path, max_reward, max_buffer, start_time, end_time)

elif copy == "n":
    sys.exit()