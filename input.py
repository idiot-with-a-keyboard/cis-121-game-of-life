import curses
#import backend.py

k=""

def main(stdscr:curses.window):
    k:int = -1 #our getch tracker, k is a little misleading as it tracks mouse input as well as keys but boohoo cry about it
    stdscr.clear() #clear screen
    stdscr.nodelay(True) #make getch not pause the program until it receives input
    msk,omsk=curses.mousemask(curses.ALL_MOUSE_EVENTS) #ask the computer to track all mouse events
    #WARNING ^ SOMETIMES THE COMPUTER WILL SAY NO
    #IM BEING LAZY AND ASSUMING IT SAYS YES
    del omsk #there is no old mousemask we just made one
    while k != ord("q"): #allow you to quit the program by pressing Q, and as K is an integer representing keycodes we must convert q to it's ascii value using ord()
        k=stdscr.getch() #gets the most recent item from the terminal's input buffer
        if k == curses.KEY_MOUSE: #check if k is a mouse event
            #stdscr.erase()
            mouse_evnt=curses.getmouse() #get the mouse event after confirming it is indeed one
            stdscr.erase()
            stdscr.addstr(f'{str(mouse_evnt)}\n') #appends this to the buffer
            stdscr.refresh() #update the terminal to match the buffer
            d=mouse_evnt
            d1,xchord,ychord,d4,d5 = d #or unpacked
            stdscr.addstr(str(xchord) +"        " +  str(ychord))
            for i in range(len(placeholder_grid)):
				for j in range(len(placeholder_grid[0])):
					if not placeholder_grid.out_of_bounds((j,i)):
						placeholder_grid.set((j,i),alive = True)
						
		
			
        elif k != -1:
            stdscr.erase()
            stdscr.refresh() #update the terminal to match the buffer
    #quit

curses.wrapper(main) #creates a container that reverses all of the changes that curses does to the terminal. you do not want to forget this.

