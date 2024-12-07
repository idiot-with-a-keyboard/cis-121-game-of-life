from copy import deepcopy, error #can't just use copy because nested things still get ruined by python's idiocy >:(
"""
HATE.
LET ME TELL YOU HOW MUCH I'VE COME TO HATE PYTHON'S PASS BY REFERENCE IMPLEMENTATION SINCE I'VE BEGUN TO LIVE.
THERE ARE APPROXIMATELY 36 TRILLION CELLS THAT COMPRISE MY BODY.
IF THE WORD HATE WERE ENGRAVED ON EACH NANOANGSTROM OF THOSE DOZENS OF TRILLIONS OF CELLS,
IT WOULD NOT EQUAL ONE ONE BILLIONTH OF THE HATE I FEEL FOR PYTHON AT THIS MICRO INSTANT.
HATE.
HATE.
HATE.
"""
#^- i spent like 3 hours debugging an error caused by 6 different instances of pass by reference or value ambiguity

def add_tuples(t1:tuple[int,int], t2:tuple[int,int]) -> tuple[int,int]:
	return (t1[0] + t2[0],	 t1[1] + t2[1]) #adds the individual values of a tuple
def sub_tuples(t1:tuple[int,int], t2:tuple[int,int]) -> tuple[int,int]:
	return add_tuples(t1,(	-t2[0], -t2[1]	)) #negates the second tuple and returns the sum

#{{{ Classes

#{{{ Grid Class

class Grid:

#{{{ Overrides
	def __init__(self,data:list[list[bool]]) -> None:
		self.data:list[list[bool]]=data

	def __str__(self) -> str:
		#width = self.get_width() # read following comments
		output:str = ""
		#output += "┏" + "━"*width + "┓\n" #wraps the output in a box, i've commented it out since it might break stuff related to the input getting the user's clicks
		for row in self.data:
			output_buffer:str=""
			for cell in row:
				if cell: #if cell is alive
					output_buffer += "█"
				else:
					output_buffer += " "
			output += output_buffer + "\n"
			#output += "┃" + output_buffer + "┃\n" #<- other part of the box code
		#output += "┗" + "━"*width + "┛\n" #< final part of box code
		return output[:-1] # remove extra trailing newline

#}}} End of Overrides█

#{{{ Size Operations

#{{{ Size Reading Operations
	def get_data(self):
		return self.data
	def get_height(self) -> int:
		return len(self.data)
	def get_width(self) -> int:
		return len(self.data[0])
	def get_size(self) -> tuple[int,int]:
		return (self.get_width(),self.get_height())
	def get_area(self) -> int:
		return self.get_width() * self.get_height()
	def is_out_of_bounds(self,coord:tuple[int,int]) -> bool:
		return False # redundant, as the new code wraps around the grid
		x,y=coord
		width,height = self.get_size()
		try: self.data[y][x]
		except: return True
		else: return False
		#"""
		#if x < 0 or y < 0:return True
		#if x >= width: return True
		#if y >= height: return True
		#return False"""

#}}} End of Size Reading Operations

#{{{ Resize Operations

#{{{ Hidden Resize Operations
	def _grow_width_by(self,amount:int) -> None:
		for row in range(self.get_height()):
			self.data[row] = self.data[row] + ([False] * amount) #pad the right with dead cells

	def _shrink_width_by(self,amount:int) -> None: #idk why you would want to shrink the grid but it's here in case it's wanted
		desired_width = self.get_width() - amount
		for row in range(self.get_height()):
			self.data[row] = self.data[row][0:desired_width] #replace each row with a slice of the row



	def _grow_height_by(self,amount:int) -> None:
		empty_row = [False] * self.get_width()
		for i in range(amount):
			self.data.append(empty_row)

	def _shrink_height_by(self,amount:int) -> None:
		desired_height = self.get_height() - amount
		self.data = self.data[0:desired_height] #cut off the rows to shrink
#}}} End of Hidden Size Operations

	def set_size(self, desired_size:tuple[int,int]) -> None:
		new_width,new_height = desired_size
		old_width,old_height = self.get_size()
		width_difference = abs(new_width-old_width)
		height_difference = abs(new_height-old_height)

		if new_width > old_width:
			self._grow_width_by(width_difference)
		elif new_width < old_width:
			self._shrink_width_by(width_difference)

		if new_height > old_height:
			self._grow_height_by(height_difference)
		elif new_height < old_height:
			self._shrink_height_by(height_difference)

#}}} End of Resize Operations

#}}} End of Size Operations

#{{{ Reading and Writing to Cells

	def get_cell_state(self,t:tuple[int,int]) -> bool: #use get_cell whenever possible to avoid errors
		x,y=t
		width,height = self.get_size()
		return self.data[y%height][x%width] #applying a modulo allows you to make the grid wraparound instead of having errors or acting like a brick wall
	def set_cell_state(self,t:tuple[int,int],alive:bool) -> None:
		x,y=t
		self.data[y][x] = alive

#}}} End of Reading and Writing to Cells

#{{{ Time Step Operations
	def check_if_cell_lives(self,pos:tuple[int,int]) -> bool:
		neighbor_offsets:list[tuple[int,int]] = [(-1,-1), (0,-1), (1,-1),
							(-1,0),		   (1,0),	  #may look weird but remember the y-axis is reversed in the terminal/windows
							(-1,1),(0,1),(1,1)]		  #increased Y values go down, not up
		neighbor_count:int=0
		for offset in neighbor_offsets:
			neighbor_pos:tuple[int,int] = add_tuples(pos,offset) #get the neighboring cell's position via the offset
			if self.get_cell_state(neighbor_pos): #if neighbor cell is alive
				neighbor_count += 1

		currently_alive:bool = self.get_cell_state(pos)

		if	 (neighbor_count <	2): #underpopulation 
			now_alive = False
		elif (neighbor_count >	3): #overpopulation
			now_alive = False
		elif (neighbor_count == 3): #reproduction
			now_alive = True
		else:						#survival
			now_alive = currently_alive

		return now_alive
	def step(self):
		width,height = self.get_size()
		new_grid:Grid = deepcopy(self) #anti pass by reference voodoo magic
		for y in range(height):
			for x in range(width):
				cell_lives = self.check_if_cell_lives((x,y))
				new_grid.set_cell_state((x,y), cell_lives)
		self.data = new_grid.data #self = new_grid #<- DOESN'T WORK FOR SOME REASON???? TODO: FIND OUT WHY


#}}} End of Time Step Operations

#}}} End of Grid Class

#}}} End of Classes

#{{{ Reading and Writing in list string format

def process_strlist(strlist:list[str]):
	g:Grid = init_empty_grid(width = len(strlist[0]), height = len(strlist))
	width,height=g.get_size()
	for y in range(height):
		for x in range(width):
			g.set_cell_state((x,y),strlist[y][x] == "1") #sets the cell to alive if the respective position in the string is 1
	return g

# {{{ Reading a File Into List String Format

def read_input_file(filename:str = "input.txt"):
	input_data:list[str] = []
	with open(filename,"r") as f:
		input_data = [line.rstrip() for line in f.readlines()]
	return process_strlist(input_data)

# }}} End of Reading a File Into List String Format

#{{{ AprilOS' modified 2D list string format for gif exportation


def reformat_to_strlist(grid:Grid): #Essentially the "export to gif" functionality
		cell_grid = [] #Creating a list to read from
		for row in grid.get_data():
			cellstr = ""
			for cell in row:
				if cell:
					cellstr += "1"
				else:
					cellstr += "0"
			cell_grid.append(cellstr)
		return cell_grid

def init_empty_grid(width:int,height:int) ->  Grid:
	output:list[list[bool]] = []
	for i in range(height):
		output.append([False]*width)
	return Grid(data=output)

if __name__ == "__main__":
	from os import system
	from time import sleep
	test_grid_data = [
			"000000000000",
			"000000000000",
			"000100000000",
			"000010000000",
			"001110000000",
			"000000000000",
			"000000000000"]
	test_grid = process_strlist(test_grid_data)
	test_grid._grow_height_by(40)
	test_grid._grow_width_by(100)
	print(reformat_to_strlist(test_grid))
	#while True:
	#	system("clear")
	#	test_grid.step()
	#	print(test_grid)
	#	sleep(1/60)
