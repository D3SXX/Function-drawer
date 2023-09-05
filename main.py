
import math
import curses
import numpy as np

def autoscale(y, stdscr):
    global x
    global y_list
    if len(y_list) <= 1:
        for i in range(0,361):
            if select == "Sin":
                radian = math.radians(i)
                y_list.append(math.sin(radian))
            elif select == "Cos":
                radian = math.radians(i)
                y_list.append(math.cos(radian))
            elif select == "Tan":
                radian = math.radians(i)
                y_list.append(math.tan(radian))
    # Scale y to fit within the screen bounds
    screen_height, screen_width = stdscr.getmaxyx()
    if select == "Sin" or select == "Cos":
        max_screen = screen_height-2
        min_screen = 1
        max_value = max(y_list)
        min_value = min(y_list)
    elif select == "Tan":
        max_screen = screen_width-2
        min_screen = 1
        max_value = max(y_list)
        min_value = min(y_list)
        if x >= screen_height-1:
            x = 0
            stdscr.clear()
    scaled_y = (y - min_value) * (max_screen - min_screen) / (max_value - min_value) + min_screen
    if x >= screen_width-1:
        x = 0
        stdscr.clear()
    return scaled_y,x

def draw_equation(stdscr, y, radian, select):
    scaled_y, x = autoscale(y, stdscr)
    info = f"{select}({math.degrees(radian)}) = {y}"
    stdscr.addstr(0, 0, info)
    if select == "Sin" or select == "Cos":
        stdscr.addch(int(scaled_y), x, '•')
    elif select == "Tan":
        stdscr.addch(x, int(scaled_y), '•')

def calc_equation(stdscr,select):
    global x, y_list
    y_list = [1]
    screen_height, screen_width = stdscr.getmaxyx()
    step = max(0.1, min(180 // screen_height, 10))
    x = 0
    delay = min(100,step*5)
    while True:
        if select == "Sin":
            for i in range(0,361,step):
                stdscr.addstr(screen_height-1, 0, f"height: {screen_height} width: {screen_width} step: {step}")
                radian = math.radians(i)
                y = math.sin(radian)
                draw_equation(stdscr,y,radian,select)
                x += 1
                stdscr.refresh()
                curses.napms(delay)
        elif select == "Cos":
            for i in range(0,361,step):
                stdscr.addstr(screen_height-1, 0, f"height: {screen_height} width: {screen_width} step: {step}")
                radian = math.radians(i)
                y = math.cos(radian)
                draw_equation(stdscr,y,radian,select)
                x += 1
                stdscr.refresh()
                curses.napms(delay)
        elif select == "Tan":
            for i in range(0,361,step):
                stdscr.addstr(screen_height-1, 0, f"height: {screen_height} width: {screen_width} step: {step}")
                radian = math.radians(i)
                y = math.tan(radian)
                draw_equation(stdscr,y,radian,select)
                x += 1
                stdscr.refresh()
                curses.napms(delay)
        elif select == "lissajous":
            A = 1.0  
            B = 2.0 
            omega1 = 5.0 
            omega2 = 4.0  
            delta = math.pi / 2.0
            max_value = 1000
            t_values = np.linspace(0, 2 * np.pi, max_value)
            x_values = np.zeros(max_value)
            y_values = np.zeros(max_value)
            for i in range(max_value):
                t = t_values[i]
                #x = A * math.sin(omega1 * t)
                x+= 1
                y = B * math.sin(omega2 * t + delta)
                draw_equation(stdscr,y,i,select)


def main(stdscr):
    global select
    def select_menu():
        pos_y = 1
        pos_x = 0
        while True:
            functions = ["Sin","Cos","Tan","lissajous","Exit"]
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            debug_msg_1 = f"width: {width} height: {height} pos_x: {pos_x} pos_y {pos_y} {functions[pos_y-1]}"
            stdscr.addstr(height-2, 1, debug_msg_1, curses.A_BOLD)
            stdscr.addstr(0, 1, "Select any option:", curses.A_BOLD)
            for i, setting in enumerate(functions):
                if i == pos_y-1:
                    stdscr.addstr(1+i, 1, setting, curses.color_pair(7))
                    select = i
                else:
                    stdscr.addstr(1+i, 1, setting, curses.A_BOLD)
                
            stdscr.addstr(pos_y, pos_x+30, "<--", curses.A_BOLD)
                
            # Get user input
            key = stdscr.getch()

            if key == ord('q') or key == ord('Q'):
                return False
            elif key == curses.KEY_UP:
                if pos_y > 1:
                    pos_y -= 1
            elif key == curses.KEY_DOWN:
                if not pos_y > len(functions)-1:
                    pos_y += 1
            elif key == ord('\n'):
                return functions[pos_y-1]
    while True:

        select = select_menu()
        if select == False or select == "Exit":
            return
        # Initialize ncurses
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        #select = "Tan"
        calc_equation(stdscr,select)
        # Refresh the screen to display the dot
        stdscr.refresh()

        # Wait for user input to exit
        stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
