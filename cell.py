# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 20:56:51 2024

@author: katerixy
"""
from graphics import *
import random

def draw_button(window, button_type, p1, p2):
    if (button_type == 'unpressed'):
        color_top = 'white'
        color_bottom = 'black'
    else:
        color_top = 'black'
        color_bottom = 'white'
        
    point_left_top = p1
    point_right_top = Point(p2.getX(), p1.getY())
    point_right_bottom = p2
    point_left_bottom = Point(p1.getX(), p2.getY())
        
    line_top = Line(point_left_top, point_right_top)
    line_right = Line(point_right_top, point_right_bottom)
    line_bottom = Line(point_left_bottom, point_right_bottom)
    line_left = Line(point_left_top, point_left_bottom)
    
    line_top.setOutline(color_top)
    line_right.setOutline(color_bottom)
    line_bottom.setOutline(color_bottom)
    line_left.setOutline(color_top)
    
    line_top.draw(window)
    line_right.draw(window)
    line_bottom.draw(window)
    line_left.draw(window)
    
class Cell:
    def __init__(self, current, after, no_row = False, no_col = False):
        self.current = current
        self.after = after
        self.no_row = no_row
        self.no_col = no_col
    def change(self, new_after):
        self.current = self.after
        self.after = new_after

def main():
    default = True
    w_x = 1200
    if default:
        w_y = w_x // 2
    else:
        w_y = 800
    size = 70
    canvas_offset_w = 20
    canvas_offset_h = canvas_offset_w
    buttons_left = 300
    buttons_top = int(w_y * 0.8)
    button_spacing = 50
    button_width = 200
    button_height = 50
    
     
    window = GraphWin("Cellular Auto", w_x, w_y)
    
    #forward button
    current_go_style = 'unpressed'  
    go_left_top = Point(buttons_left, buttons_top)
    go_right_bottom = Point(go_left_top.getX() + button_width, go_left_top.getY() + button_height)
    draw_button(window, current_go_style, go_left_top, go_right_bottom)
    
    go_text = Text(Point(go_left_top.getX() + button_width // 2, go_left_top.getY() + button_height // 2), "Forward")
    go_text.draw(window)
    
    #close button
    current_close_style = 'unpressed'
    close_left_top = Point(go_right_bottom.getX() + button_spacing, buttons_top)
    close_right_bottom = Point(close_left_top.getX() + button_width, close_left_top.getY() + button_height)
    draw_button(window, current_close_style, close_left_top, close_right_bottom)
    close_text = Text(Point(close_left_top.getX() + button_width // 2, close_left_top.getY() + button_height // 2), "Close")
    close_text.draw(window)
    #line variables
    canvas_w = size * ((w_x - canvas_offset_w * 2) // size)
    cols = canvas_w // size
    canvas_h = size * ((buttons_top - canvas_offset_h * 2) //size)
    rows = canvas_h // size
    canvas_offset_w = (w_x - canvas_w) // 2
    cell_row = []
    cell_list = []
    rect = Rectangle(Point(canvas_offset_w, canvas_offset_h), Point(canvas_w + canvas_offset_w, canvas_h + canvas_offset_h))
    rect.setOutline('red')
    rect.setFill("white")
    rect.draw(window)
    #graph + list
    for i in range(0, cols + 1):
        point_x = canvas_offset_w + size * i
        line = Line(Point(point_x, canvas_offset_h), Point(point_x, canvas_h + canvas_offset_h))
        line.setFill('black')
        line.draw(window)
        cell_row.append(False)
    cell_row.pop()
    print(cell_row)
    for i in range(0, rows + 1):
        point_y = canvas_offset_h + size * i
        line = Line(Point(canvas_offset_w, point_y), Point(canvas_w + canvas_offset_w, point_y))
        line.setFill('black')
        line.draw(window)     
        cell_list.append(list(cell_row))
    cell_list.pop()
    print(cell_list)
    
    #create beginning layout
    beg_type = "random"
    if beg_type == "test":
        beg_amount = 3
        beg_row = 0 if len(cell_list) // 2 - (beg_amount // 2 + 1) < 0 else len(cell_list) // 2 - (beg_amount // 2 + 1)
        beg_col = len(cell_row) // 2 - (beg_amount // 2 - 1)
        print(beg_row, ",", beg_col)
        for i in range(beg_amount):
            cell_list[beg_row + i][beg_col] = True
    elif beg_type == "random":
        for row in range(rows):
            for col in range(cols):
                change = random.randint(0,1)
                if change == 1:
                    cell_list[row][col] = True
    else:
        cell_list[0][0] = True
        cell_list[len(cell_list) // 2 - 1][len(cell_row) // 2] = True
        cell_list[len(cell_list) // 2][len(cell_row) // 2] = True
        cell_list[len(cell_list) // 2 + 1][len(cell_row) // 2] = True

    print("\n", cell_list)
    for row in range(rows - 1):
        for col in range(cols - 1):
            top_x = canvas_offset_w + size * col
            top_y = canvas_offset_h + size * row
            btm_x= top_x + size
            btm_y= top_y + size
            if cell_list[row][col] == True:
                rect = Rectangle(Point(top_x, top_y), Point(btm_x, btm_y))
                rect.setFill("black")
                rect.draw(window)
                
    while (True):
        clicked_forward = False
        # Wait for the mouse click
        clicked_pixel = window.getMouse()
        # Did we press the Forward button?
        if (clicked_pixel.getX() > go_left_top.getX()
            and clicked_pixel.getY() > go_left_top.getY()
            and clicked_pixel.getX() < go_right_bottom.getX()
            and clicked_pixel.getY() < go_right_bottom.getY()):
            current_go_style = 'unpressed' if (current_go_style == 'pressed') else 'pressed'
            amount_x = 2 if (current_go_style == 'pressed') else -2
            amount_y = 2 if (current_go_style == 'pressed') else -2
            draw_button(window, current_go_style, go_left_top, go_right_bottom)
            go_text.move(amount_x, amount_y)
            clicked_forward = True
        
        if clicked_forward:
            next_cell_list = []
            for row in range(rows):
                end_stay = True
                end_create = False
                next_cell_row = []
                for col in range(cols):
                    num_neighbors = 0
                    if row > 0:
                        if col > 0 and cell_list[row - 1][col - 1]:
                            num_neighbors += 1
                        if cell_list[row - 1][col]:
                            num_neighbors += 1
                        if col < cols - 1 and cell_list[row - 1][col + 1]:
                            num_neighbors += 1
                            
                    if col > 0 and cell_list[row][col - 1]:
                        num_neighbors += 1
                    if col < cols - 1 and cell_list[row][col + 1]:
                        num_neighbors += 1
                        
                    if row < rows - 1:
                        if col > 0 and cell_list[row + 1][col - 1]:
                            num_neighbors += 1
                        if cell_list[row + 1][col]:
                            num_neighbors += 1
                        if col < cols - 1 and cell_list[row + 1][col + 1]:
                            num_neighbors += 1
                            
                    if cell_list[row][col] and (num_neighbors == 2 or num_neighbors == 3):
                        next_cell_row.append(True)
                    elif cell_list[row][col] == False and num_neighbors == 3:
                        next_cell_row.append(True)
                    else:
                        next_cell_row.append(False)
                next_cell_list.append(next_cell_row)
            print(len(next_cell_list), len(next_cell_list[0]))
            print(next_cell_list)
            cell_list = list(next_cell_list)
            for row in range(len(cell_list)):
                for col in range(len(cell_list[row])):
                    top_x = canvas_offset_w + size * col
                    top_y = canvas_offset_h + size * row
                    btm_x= top_x + size
                    btm_y= top_y + size
                    box = Rectangle(Point(top_x, top_y), Point(btm_x, btm_y))
                    if cell_list[row][col] == True:
                        box.setFill("black")
                    else:
                        box.setFill("white")
                    box.draw(window)
                    
                    
        
        if (clicked_pixel.getX() > close_left_top.getX()
            and clicked_pixel.getY() > close_left_top.getY()
            and clicked_pixel.getX() < close_right_bottom.getX()
            and clicked_pixel.getY() < close_right_bottom.getY()):
            current_close_style = 'unpressed' if (current_close_style == 'pressed') else 'pressed'
            amount_x = 2 if (current_close_style == 'pressed') else -2
            amount_y = 2 if (current_close_style == 'pressed') else -2
            draw_button(window, current_close_style, close_left_top, close_right_bottom)
            close_text.move(amount_x, amount_y)
            window.close()
        
main()