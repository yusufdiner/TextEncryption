import sys
try:
    assert sys.argv[1] == 'enc' or sys.argv[1] == 'dec'
except AssertionError:
    print("Undefined parameter error")
    exit()
try:
    assert (sys.argv[3])[-4:] == '.txt'
except AssertionError:
    print("The input file could not be read error")
    exit()

try:
    assert (sys.argv[2])[-4:] == '.txt'
except AssertionError:
    print("Key file could not be read error")
    exit()
try:
    assert len(sys.argv) == 5
except AssertionError:
    print("Parameter number error")
    exit()
try:
    key = open(sys.argv[2],"r")
except FileNotFoundError:
    print("Key file not found error")
    exit()
try:
    input_file = open(sys.argv[3])
except FileNotFoundError:
    print("Input file not found error")
    exit()
operation_type = sys.argv[1]
key = open(sys.argv[2],"r")
key_list = []
for i in key.readlines():
    i = i.strip("\n").split(",")
    key_list.append(i)
key.close()
try:
    assert len(key_list) != 0
except:
    print("Key file is empty error")
    exit()
dict_alphabet ={1:["A","a"],2:["B","b"],3:["C","c"],4:["D","d"],5:["E","e"],6:["F","f"],\
               7:["G","g"],8:["H","h"],9:["I","i"],10:["J","j"],11:["K","k"],12:["L","l"],\
               13:["M","m"],14:["N","n"],15:["O","o"],16:["P","p"],17:["Q","q"],18:["R","r"],\
               19:["S","s"],20:["T","t"],21:["U","u"],22:["V","v"],23:["W","w"],24:["X","x"],\
               25:["Y","y"],26:["Z","z"],27:[" ","\t"]}
def lettertonumber(x):
    for a in dict_alphabet.keys():
        for j in [0,1]:
            if dict_alphabet[a][j] == x:
                return a
def numbertoletter(x):
    return dict_alphabet[x][0]
try:
    code3 = []
    for i in input_file.readlines():
        j = i.strip("\n")
        while len(j) % len(key_list) != 0:
            j += "\t"
        for k in range(int(len(j)/len(key_list))):
            code3.append(j[k*len(key_list):(k+1)*len(key_list)])
    assert len(code3) != 0
except:
    print("Input file is empty error")
    exit()
try:
    for t in range(len(key_list)):
        for y in range(len(key_list[t])):
            key_list[t][y] = int(key_list[t][y])
except ValueError:
    print("Invalid character in key file error")
    exit()
def matrixinverse(a):
    def determinantfunc(a):
        if len(a) == 2:#2x2 deternminant
            return int(a[0][0])*int(a[1][1])-int(a[0][1])*int(a[1][0])
        determinant = 0
        for c in range(len(a)):#nxn deternminant
            minor = []
            for line in a[1:]:
                minor.append(line[:c]+line[c+1:])
            determinant += ((-1)**c)*a[0][c]*determinantfunc(minor)
        return determinant
    determinant = determinantfunc(a)
    if len(a) == 2:#2x2 matrix
        return [[a[1][1]/determinant,a[0][1]/determinant * (-1) , a[1][0]/determinant * (-1), a[0][0]/determinant]]
    cofactor2 = []
    #nxn matrix
    for b in range(len(a)):# b are the rows of the matrix
        cofactor1 = []
        for c in range(len(a)):# c are the columns of the matrix
            minor = []
            for line in a[:b]+a[b+1:]:
                minor.append(line[:c]+line[c+1:]) #2x2 piece of matrix
            cofactor1.append(determinantfunc(minor)*((-1)**(b+c)))
        cofactor2.append(cofactor1)
    cofactors = []
    for j in zip(*cofactor2):# relocate matrix cofactor
        cofactors.append(list(j))
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors
if operation_type == 'enc':
    code = []
    code1 = []
    input_file = open(sys.argv[3],"r")
    for i in input_file.readlines():
        j = i.strip("\n")
        while len(j) % len(key_list) != 0:
            j += "\t"
        for k in range(int(len(j)/len(key_list))):
            code.append(j[k*len(key_list):(k+1)*len(key_list)]) #split the code by key length
        for a in code:
            List = []
            for j in range(len(a)):
                List.append(lettertonumber(a[j]))
            code1.append(List)
    input_file.close()
    result1 = []
    for a in range(len(code1)):#matrix multiplication code
        result = []
        z = 0
        while z < len(key_list):
            result.append([0])
            z += 1
        result1.extend(result)
        for i in range(len(key_list)):
            for k in range(len(code1[a])):
                try:
                    result[i][0] += int(key_list[i][k]) * int(code1[a][k])
                except TypeError:
                    print("Invalid character in input file")
                    exit()
    numbers = ""
    for x in range(len(result1)):
        numbers += str(result1[x][0]) + ","
    output = open(sys.argv[4],"w")
    output.write(str(numbers)[:-1])
    output.close()
elif operation_type == 'dec':
    code = []
    input_file = open(sys.argv[3],"r")
    for i in input_file.readlines():
        j = i.strip("\n").split(",")
        for k in range(int(len(j)/len(key_list))):
            code.append(j[k*len(key_list):(k+1)*len(key_list)])
    input_file.close()
    inverse_key = matrixinverse(key_list)
    result1 = []
    for a in range(len(code)):
        result = []
        z = 0
        while z < len(inverse_key):
            result.append([0])
            z += 1
        for i in range(len(inverse_key)):
            for k in range(len(code[a])):
                result[i][0] += int(inverse_key[i][k]) * int(code[a][k])
        result1.extend(result)
    messageCode = []
    for x in range(len(result1)):
        messageCode.append(result1[x][0])
    message = []
    for a in messageCode:
        message.append(numbertoletter(a))
    message = "".join(message)
    output = open(sys.argv[4],"w")
    output.write(message)
    output.close()
