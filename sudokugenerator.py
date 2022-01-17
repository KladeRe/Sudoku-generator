import random
import math
import copy


class sudoku():

    def __init__(self): 
        self.size = 9
        self.empty_slots = 40
        self.root = int(math.sqrt(self.size))
        self.all_choices = list(range(1, self.size + 1))
        self.grid = [[0]*self.size for _ in range(self.size)]
        self.slots = sorted(list(range(self.size**2)), key=lambda k: random.random())
        self.solvedgrid = []
        

    
    def find0(self): # Löytää paikan jossa on nolla
        for row in self.grid:
            for col in row:
                if col == 0:
                    return (self.grid.index(row), row.index(col))

        return False

   
    def getchoices(self, y, x): # Antaa kaikki mahdolliset numerot koordinaateille

        x_value = x
        y_value = y
        # Katsoo läpi kaikki numerot samalla rivillä
        choices_row = [x for x in self.grid[y_value] if x > 0]

        # Katsoo läpi kaikki numerot jotka ovat samassa sarakkeessa
        choices_column = []
        for row in self.grid:
            if row[x_value] > 0:
                choices_column.append(row[x_value])

        # Katsoo läpi kaikki numerot jotka ovat samassa 3x3 laatikossa
        in_box = []
        box_x = x_value // self.root
        box_y = y_value // self.root

        for i in range(box_y*self.root, box_y*self.root + self.root):
            for j in range(box_x*self.root, box_x*self.root + self.root):
                if self.grid[i][j] > 0:
                    in_box.append(self.grid[i][j])

        # Yhdistää kaikki mahdolliset numerot rivin, sarakkeen sekä laatikon mukaan
        common_members = [x for x in self.all_choices if x not in choices_column and x not in choices_row and x not in in_box]
        random.shuffle(common_members)
        return common_members


    
    def generate(self): # Tekee ratkaistun sudokun rekursion avulla
        zeros = self.find0()

        if not zeros:
            return True
        else:
            row, col = zeros
            common_members = self.getchoices(int(row), int(col))

        for n in common_members:
            self.grid[row][col] = n
                
            if self.generate():
                return self.grid

            self.grid[row][col] = 0
        return False



    def solveForDelete(self, row, col): # Ratkaisee sudokun valitusta paikasta

        common_members = self.getchoices(row, col)

        for member in common_members:
            self.grid[row][col] = member

            if self.generate():
                return self.grid

            self.grid[row][col] = 0

        return False



    def find0ForSolve(self): # Antaa kaikki koordinaatit joissa numero on 0
        coordinates = []
        for row in self.grid:
            indexcol = -1
            for col in row:
                indexcol += 1
                if col == 0:
                    coordinates.append((self.grid.index(row), indexcol))
                    
        return coordinates




    def findNumberOfSolutions(self): #Funktio joka hälyttää jos on monta eri ratkaisua
        coordinates = self.find0ForSolve()
        for coordinate in coordinates:
            sudokucopy = copy.deepcopy(self)
            if sudokucopy.solveForDelete(coordinate[0], coordinate[1]) != self.solvedgrid:
                return False
        return True



    def generatePuzzle(self): # Ottaa pois numeroita kunnes on saavuttanut tavoitteensa tai on epäonnistunut tarpeeksi monta kertaa
        counter = 0
        tries = 0
        while counter < self.empty_slots:
            tries += 1
            if tries > 100:
                break
            row = random.randint(0,8)
            col = random.randint(0,8)

            if self.grid[row][col] > 0:
                deletednumber = self.grid[row][col]
                self.grid[row][col] = 0

                if not self.findNumberOfSolutions():
                    self.grid[row][col] = deletednumber
                    continue

                counter += 1


    def print_grid(self): #Näyttää sudokutehtävän hienossa muodossa
        for i in range(len(self.grid)):
            if i % self.root == 0 and i != 0:
                print("_ " * (self.size + ((self.root-1)*2)) + "\n")
            for j in range(self.size):
                if j % self.root == 0 and j != 0:
                    print(" | ", end = " ")

                if j == self.size -1:
                    print(self.grid[i][j])
                else:
                    print(str(self.grid[i][j]) + " ", end = "") 
        print("")





def main(): #Main-funktio joka kontrolloi kaikkia funktioita sekä luokkia
    print("")
    a = sudoku()
    a.generate()
    a.print_grid()
    print(" ")
    a.solvedgrid = copy.deepcopy(a.grid)
    a.generatePuzzle()
    a.print_grid()



if __name__ == "__main__":
    main()
