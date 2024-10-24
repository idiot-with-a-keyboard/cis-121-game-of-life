#ello guvnah

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
    def __init__(self,pos:Coordinate,alive:bool) -> None:
        self.pos = pos
        self.alive = alive


class Cache:
    def __init__(self,data:list[list[Cell]]) -> None:
        self.data=data


    def get(self,t:Coordinate) -> Cell:
        x,y=t.x,t.y
        return self.data[y][x]

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

if __name__ == "__main__":
    test = Coordinate(0,2)
    print(test + Coordinate(1,2),"1,4")
    print(test - Coordinate(1,2),"-1,0")
