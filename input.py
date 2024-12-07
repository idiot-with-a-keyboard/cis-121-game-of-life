import curses
import backend
import frontend

from os import get_terminal_size

#import backend.py

k=""
term_width, term_height = get_terminal_size()

placeholder_grid:backend.Grid = backend.init_empty_grid(term_width-1,term_height-2)

def main(stdscr:curses.window):
    k:int = -1 #our getch tracker, k is a little misleading as it tracks mouse input as well as keys but boohoo cry about it
    stdscr.clear() #clear screen
    stdscr.nodelay(True) #make getch not pause the program until it receives input
    msk,omsk=curses.mousemask(curses.ALL_MOUSE_EVENTS) #ask the computer to track all mouse events
    #WARNING ^ SOMETIMES THE COMPUTER WILL SAY NO
    #IM BEING LAZY AND ASSUMING IT SAYS YES
    del omsk #there is no old mousemask we just made one
    stdscr.addstr("click anywhere to start!")
    while k != ord("d"): #allow you to quit the program by pressing Q, and as K is an integer representing keycodes we must convert q to it's ascii value using ord()
        k=stdscr.getch() #gets the most recent item from the terminal's input buffer
        if k == curses.KEY_MOUSE: #check if k is a mouse event
            #stdscr.erase()
            mouse_evnt=curses.getmouse() #get the mouse event after confirming it is indeed one
            stdscr.erase()
            stdscr.addstr("draw your initial grid state, and press D to finish.")
            #stdscr.addstr(f'{str(mouse_evnt)}\n') #appends this to the buffer
            #stdscr.refresh() #update the terminal to match the buffer
            d=mouse_evnt
            d1,xchord,ychord,d4,d5 = d #or unpacked
            #stdscr.addstr(str(xchord) +"        " +  str(ychord))
            placeholder_grid.set_cell_state((xchord,ychord-1),alive = True)
            stdscr.move(1,0)
            for i in backend.reformat_to_strlist(placeholder_grid):
                stdscr.addstr(i.replace("0"," ").replace("1","█"))
                if stdscr.getyx()[0] != term_height-1:
                    stdscr.move(stdscr.getyx()[0]+1,0)
            stdscr.refresh()
		
    steps:list[list[str]] = [backend.reformat_to_strlist(placeholder_grid)]
    while k != ord("s"):
        k=stdscr.getch()
        stdscr.erase()
        stdscr.addstr("press A to advance a step, and S to quit and save as gif.\n")
        stdscr.addstr("NOTE: you may only simulate up to 50 steps.")
        if k==ord("a"):
            placeholder_grid.step()
            steps.append(backend.reformat_to_strlist(placeholder_grid))
            if len(steps) > 50:
                print("Cannot exceed 50 steps, autosaving.")
                break
        for i in str(placeholder_grid).split('\n'):
            stdscr.addstr(i)
            if stdscr.getyx()[0] != term_height-1:
                stdscr.move(stdscr.getyx()[0]+1,0)
        stdscr.refresh()
    frontend.creategif(steps,len(steps),placeholder_grid.get_width(),placeholder_grid.get_height())
    #quit

curses.wrapper(main) #creates a container that reverses all of the changes that curses does to the terminal. you do not want to forget this.

print(placeholder_grid)
print(placeholder_grid.get_size())
