# Nama  : Ahmad Hasan Albana
# NIM   : 13522041

def splitList(string): # mengubah string menjadi list biner
    panjang = len(string)
    if (panjang == 1):
        return [string]
    else:
        return [splitList(string[:panjang//2]), splitList(string[panjang//2:])]
    
def listToString(list): # mengubah list biner menjadi string
    panjang = len(list)
    if (panjang == 1):
        return str(list[0])
    else:
        return str(listToString(list[0]) + listToString(list[1]))
    
def paddingBin(biner, pad): # membuat string biner dengan panjang pad
    strings = bin(biner)[2:]
    totalpad = pad - len(strings)
    strings = totalpad*'0' + strings

    return strings

def deleteByStrIdx(strIdx):
    global nonUsedBtrail
    print('\n----- Menambahkan', strIdx, 'ke Hasil Utama! -----\n')
    listHasil.append(strIdx)
    strIdxList = convertXtoValidStr([strIdx])

    for i in strIdxList:
        idx = int(i, 2)
        nonUsedBtrail[idx] = '0'

def geserString(intString, strIdx):
    i = nVar

    for j in strIdx:
        i -= 1
        if (j == '0'):
            intString <<= 2**i

    return intString

def convertXtoValidStr(strIdxList):
    panjang = len(strIdxList)
    ketemuX = False

    for _ in range(panjang):
        a = strIdxList.pop(0)
        idx = a.find('X')
        if (idx != -1):
            ketemuX = True
            strIdxList.append(a[:idx] + '0' + a[idx+1:])
            strIdxList.append(a[:idx] + '1' + a[idx+1:])
        else:
            strIdxList.append(a)

    if (ketemuX):
        strIdxList = convertXtoValidStr(strIdxList)

    return strIdxList
    
def parsingHasil():
    global listHasil
    for urutan in range(len(listHasil)):
        hasil = listHasil[urutan]
        for i in range(len(hasil)):
            if (hasil[i] == '1'):
                print(chr(65+i), end='')
            elif (hasil[i] == '0'):
                print(chr(65+i)+ '\'', end='')
        if (urutan != len(listHasil)-1):
            print(' + ', end='')

def searchPattern(list, prevIdxStr, isDoneComparing):
    global nonUsedBtrail
    global listHasil

    string0 = listToString(list[0])
    string1 = listToString(list[1])

    print('\nHASIL NOW: '+prevIdxStr)
    print('STRING0: '+string0)
    print('STRING1: '+string1+'\n')

    stop = False # bernilai True saat telah mencapai kondisi basis

    if (len(prevIdxStr) == nVar-1): # mengecek apakah sudah mencapai kondisi basis
        stop = True

    andOp = int(string0, 2) & int(string1, 2) # persamaan pola antara kedua child

    if (andOp != 0): # Kondisi: kedua child tidak memiliki pola
        # Kondisi: pola kedua child memuat bit '1' yang belum digunakan
        if (isDoneComparing or ((geserString(andOp, prevIdxStr+'1') & int("".join(nonUsedBtrail), 2)) != 0)
         or ((geserString(andOp, prevIdxStr+'0') & int("".join(nonUsedBtrail), 2)) != 0)):
            isDoneComparing = True # bernilai True saat tidak perlu dicek apakah bit '1' yang ada telah digunakan
            panjang = len(string0)

            print('Menambahkan X!')
            if (not stop): # Kondisi Basis
                listBaru = splitList(paddingBin(andOp, panjang))
                searchPattern(listBaru, prevIdxStr+'X', isDoneComparing) # menyederhanakan B-Trail pola yang didapat
            else: # Kondisi Rekurens
                deleteByStrIdx(prevIdxStr+'X') # menandai bit '1' sebagai 'telah digunakan'
                print('LIST NONUSED: ', end='')
                print("".join(nonUsedBtrail))

            isDoneComparing = False

    if (int("".join(nonUsedBtrail),2) != 0): # Kondisi: masih terdapat bit '1' yang belum digunakan
        cmp0 = int(string0, 2) != 0 
        cmp1 = int(string1, 2) != 0
        if (cmp0 and cmp1): # Kondisi: child kiri & kanan tidak bernilai nol dan tidak memiliki pola
            isCompare2 = False # bernilai True saat tidak perlu dicek apakah bit '1' yang ada telah digunakan
        else:
            isCompare2 = isDoneComparing
        if (cmp0): # Kondisi: child kiri tidak bernilai nol
            if (isCompare2 or ((geserString(int(string0, 2), prevIdxStr+'0') & int("".join(nonUsedBtrail), 2)) != 0)):
                print('Menambahkan 0!')
                if (not stop): # Kondisi Rekurens
                    searchPattern(list[0], prevIdxStr+"0", isDoneComparing) # menulusuri child kiri
                else: # Kondisi Basis
                    deleteByStrIdx(prevIdxStr+'0') # menandai bit '1' sebagai 'telah digunakan'
                    print('LIST NONUSED: ', end='')
                    print("".join(nonUsedBtrail))

        if (cmp1): # Kondisi: child kanan tidak bernilai nol         
            if (isCompare2 or ((geserString(int(string1, 2), prevIdxStr+'1') & int("".join(nonUsedBtrail), 2)) != 0)):
                print('Menambahkan 1!')
                if (not stop): # Kondisi Rkurens
                    searchPattern(list[1], prevIdxStr+'1', isDoneComparing) # menulusuri child kanan
                else: # Kondisi Basis
                    deleteByStrIdx(prevIdxStr+'1') # menandai bit '1' sebagai 'telah digunakan'
                    print('LIST NONUSED: ', end='')
                    print("".join(nonUsedBtrail))



''' MAIN PROGRAM '''
nVar = int(input("Masukkan banyak variabel: "))
input = input("Masukkan bentuk SOP: ")

# inisiasi B-trail
Btrail = ['0' for _ in range(2**nVar)]
nonUsedBtrail = ['0' for _ in range(2**nVar)] 
listHasil = []

# membuat B-trail berdasarkan input
input = input.split(" ")
for i in input:
    Btrail[int(i)] = '1'
    nonUsedBtrail[int(i)] = '1'

Btrail = "".join(Btrail)
print('B-TRAIL: ' + Btrail)
print(int(Btrail, 2))
Btrail = splitList(Btrail) # convert B-Trail menjadi Pohon Biner dalam bentuk array

# Kasus Semesta atau Null
if (int(listToString(Btrail)) == 0): # Kondisi: seluruh bit bernilai 0
    print('Null')
elif (int(listToString(Btrail), 2) == (2**(2**nVar)-1)): # Kondisi: seluruh bit bernilai 1
    print('All True')
else:
    listHasil = []
    searchPattern(Btrail, "", False)
    print(f'LIST_HASIL: ', end='')
    print(listHasil)
    parsingHasil()