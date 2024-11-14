#ello guvnah

from _typeshed import IdentityFunction


class Coordinate:
    def __init__(self,x:int,y:int) -> None:
        self.x=x
        self.y=y

    def __add__(self,other):
        return Coordinate((self.x + other.x), (self.y + other.y))
    def __sub__(self,other):
        other.x = -other.x
        other.y = -other.y
        return self + other
    def __str__(self):
        return f"({self.x},{self.y})"

class Cell:
    def __str__(self) -> str:
        return str(1 if self.alive else 0)
    def __init__(self,pos:(Coordinate|tuple[int,int]),alive:bool) -> None:
        if type(pos) == Coordinate:
            self.pos = pos
        if type(pos) == tuple[int,int]:
            self.pos = Coordinate(x=pos[0],y=pos[1])
        self.alive = alive
    def kill(self):
        self.alive = False
    def live(self):
        self.alive = True
    def set(self,alive:bool):
        self.alive = alive

""" Ignore
data = list[str]
with open("input.txt", "r") as f:
    data = [line.rstrip() for line in fh.readlines()]
"""

class Grid:
    def __init__(self,data:list[list[Cell]] = []) -> None:
        self.data=data

    def get(self,t:(Coordinate|tuple[int,int])) -> Cell:
        if type(t) == Coordinate:
            x=t.x
            y=t.y
        elif type(t) == tuple[int,int]:
            x=t[0]
            y=t[1]
        else:
            x,y=0,0
        return self.data[y][x]
    def set(self,t:(Coordinate|tuple[int,int]),alive:bool) -> None:
        if type(t) == Coordinate:
            x=t.x
            y=t.y
        elif type(t) == tuple[int,int]:
            x=t[0]
            y=t[1]
        else:
            x,y=0,0
        self.data[y][x].set(alive)


    def get_neighbors(self,c:Cell) -> list[Cell]:
        output:list[Cell] = []
        neighbor_pos:list[Coordinate] = []
        neighbor_offsets:list[tuple[int,int]] = [
            (-1,1),  (0,1),  (1,1),
            (-1,0),          (1,0),
            (-1,-1), (0,-1), (1,-1)  ]
        for i in neighbor_offsets:
            neighbor_pos.append(c.pos + Coordinate(*i))

        for i in neighbor_pos:
            output.append(self.get(i))
        return output

    def to_boolean(self) -> list[list[bool]]:
        output:list[list[bool]] = []
        for row in self.data:
            y:int = self.data.index(row)
            output[y] = [*([False]*len(row))] #produces a list of booleans, doing this without unpacking implicitly coverts it to an integer
            for cell in row:
                x=row.index(cell)
                output[y][x] = cell.alive
        return output

    def tick(self) -> None:
        old_grid = self.get_raw()
    def is_out_of_bounds(self,pos:(tuple[int,int]|Coordinate)) -> bool:
        return False
        #TODO make this do sommething
"""
    def __str__(self) -> str:
        output:str = ""
        data:list[list[bool]] = self.to_boolean()
        for i in data:
            pass"""


def read_input_file(filename:str = "input.txt"):
    input_data:list[str] = []
    with open(filename,"r") as f:
        input_data = [line.rstrip() for line in f.readlines()]
    g:Grid = init_empty_grid(width = len(input_data[0]), height = len(input_data))
    for i in range(len(input_data)):
        for j in range(len(input_data[0])):
            alive = input_data[j][i] == "1"
            g.set((j,i),alive)

def init_empty_grid(width:int,height:int) ->  Grid:
    output:list[list[Cell]] = []
    for i in range(height):
        output.append([])
        for j in range(width):
            output[i].append(Cell((j,i),False))
    return Grid(data=output)

if __name__ == "__main__":
    test = Coordinate(0,2)
    print(test + Coordinate(1,2),"1,4")
    print(test - Coordinate(1,2),"-1,0")
