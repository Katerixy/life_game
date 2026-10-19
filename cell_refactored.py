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
        
class Config:
    def __init__(self, rows, cols, canvas_offset_w, canvas_offset_h, size, 
                 go_left_top, go_right_bottom,
                 close_left_top, close_right_bottom,
                 button_press_amount_x, button_press_amount_y):
        self.rows = rows
        self.cols = cols
        self.canvas_offset_w = canvas_offset_w
        self.canvas_offset_h = canvas_offset_h
        self.size = size
        self.go_left_top = go_left_top
        self.go_right_bottom = go_right_bottom
        self.close_left_top = close_left_top
        self.close_right_bottom = close_right_bottom
        self.button_press_amount_x = button_press_amount_x
        self.button_press_amount_y = button_press_amount_y        
        
def create_beginning_layout(beg_type, cell_list):
    if beg_type == "test":
        beg_amount = 3
        beg_row = 0 if len(cell_list) // 2 - (beg_amount // 2 + 1) < 0 else len(cell_list) // 2 - (beg_amount // 2 + 1)
        beg_col = len(cell_row) // 2 - (beg_amount // 2 - 1)
        print(beg_row, ",", beg_col)
        for i in range(beg_amount):
            cell_list[beg_row + i][beg_col] = True
    elif beg_type == "random":
        for row in range(len(cell_list)):
            for col in range(len(cell_list[0])):
                change = random.randint(0,1)
                if change == 1:
                    cell_list[row][col] = True
    elif beg_type == "andrey":
        # line
        cell_list[3][3] = True
        cell_list[3][2] = True
        cell_list[3][1] = True
        # line
        cell_list[7][8] = True;
        cell_list[8][8] = True;
        cell_list[9][8] = True;
        # block
        cell_list[3][9] = True;
        cell_list[3][10] = True;
        cell_list[4][9] = True;
        cell_list[4][10] = True;
        # block
        cell_list[7][3] = True;
        cell_list[7][4] = True;
        cell_list[8][3] = True;
        cell_list[8][4] = True;
        # rand
        cell_list[23][25] = True;
        cell_list[23][26] = True;
        cell_list[23][27] = True;
        cell_list[24][25] = True;    
        cell_list[25][26] = True;           
    else:
        cell_list[0][0] = True
        cell_list[len(cell_list) // 2 - 1][len(cell_row) // 2] = True
        cell_list[len(cell_list) // 2][len(cell_row) // 2] = True
        cell_list[len(cell_list) // 2 + 1][len(cell_row) // 2] = True
        
    return cell_list

def draw_cells_on_screen(window, config, cell_list):
    boxes = []
    for row in range(config.rows):
        boxes.append([])
        for col in range(config.cols):
            top_x = config.canvas_offset_w + config.size * col
            top_y = config.canvas_offset_h + config.size * row
            btm_x= top_x + config.size
            btm_y= top_y + config.size
            rect = Rectangle(Point(top_x, top_y), Point(btm_x, btm_y))
            if cell_list[row][col] == True:
                rect.setFill("black")
            else:
                rect.setFill("white")
            rect.draw(window)
            boxes[row].append(rect)
    return boxes

def clicked_forward_button(config, clicked_pixel):
    result = clicked_pixel.getX() > config.go_left_top.getX() and clicked_pixel.getY() > config.go_left_top.getY()        and clicked_pixel.getX() < config.go_right_bottom.getX()        and clicked_pixel.getY() < config.go_right_bottom.getY()
    return result 

def flip_button_style_and_redraw(window, config, current_go_style, go_text):
    new_go_style = 'unpressed'
    amount_x = -config.button_press_amount_x
    amount_y = -config.button_press_amount_y
    if (current_go_style == 'unpressed'):
        new_go_style = 'pressed'
        amount_x = config.button_press_amount_x
        amount_y = config.button_press_amount_y
    draw_button(window, new_go_style, config.go_left_top, config.go_right_bottom)
    go_text.move(amount_x, amount_y)
    return new_go_style

def compute_new_turn(config, cell_list):
    next_cell_list = []
    for row in range(config.rows):
        next_cell_row = []
        for col in range(config.cols):
            num_neighbors = 0
            if row > 0:
                if col > 0 and cell_list[row - 1][col - 1]:
                    num_neighbors += 1
                if cell_list[row - 1][col]:
                    num_neighbors += 1
                if col < config.cols - 1 and cell_list[row - 1][col + 1]:
                    num_neighbors += 1
                    
            if col > 0 and cell_list[row][col - 1]:
                num_neighbors += 1
            if col < config.cols - 1 and cell_list[row][col + 1]:
                num_neighbors += 1
                
            if row < config.rows - 1:
                if col > 0 and cell_list[row + 1][col - 1]:
                    num_neighbors += 1
                if cell_list[row + 1][col]:
                    num_neighbors += 1
                if col < config.cols - 1 and cell_list[row + 1][col + 1]:
                    num_neighbors += 1
                    
            if cell_list[row][col] and (num_neighbors == 2 or num_neighbors == 3):
                next_cell_row.append(True)
            elif cell_list[row][col] == False and num_neighbors == 3:
                next_cell_row.append(True)
            else:
                next_cell_row.append(False)
        next_cell_list.append(next_cell_row)
    return next_cell_list

def draw_new_turn(config, cell_list, next_cell_list, boxes):
    for row in range(config.rows):
        for col in range(config.cols):
             if (cell_list[row][col] != next_cell_list[row][col]):
                 if next_cell_list[row][col]:
                     boxes[row][col].setFill("black")
                 else:
                     boxes[row][col].setFill("white")

def clicked_close_button(config, clicked_pixel):
    result = (clicked_pixel.getX() > config.close_left_top.getX()
        and clicked_pixel.getY() > config.close_left_top.getY()
        and clicked_pixel.getX() < config.close_right_bottom.getX()
        and clicked_pixel.getY() < config.close_right_bottom.getY())
    return result

def main():
    default = True
    w_x = 1200
    if default:
        w_y = w_x // 2
    else:
        w_y = 800
    size = 12
    canvas_offset_w = 20
    canvas_offset_h = canvas_offset_w
    buttons_left = 300
    buttons_top = int(w_y * 0.8)
    button_spacing = 50
    button_width = 200
    button_height = 50
    beg_type = "random"
    
     
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
    
    
    config = Config(rows, cols, canvas_offset_w, canvas_offset_h, size, 
                    go_left_top, go_right_bottom,
                    close_left_top, close_right_bottom,
                    2, 2)
    
    cell_list = create_beginning_layout(beg_type, cell_list)
    boxes = draw_cells_on_screen(window, config, cell_list)

                    
    while (True):
        clicked_pixel = window.getMouse()
        
        if (clicked_forward_button(config, clicked_pixel)):
            current_go_style = flip_button_style_and_redraw(window, config, current_go_style, go_text)           
            next_cell_list = compute_new_turn(config, cell_list)
            draw_new_turn(config, cell_list, next_cell_list, boxes)
            cell_list = list(next_cell_list)
            current_go_style = flip_button_style_and_redraw(window, config, current_go_style, go_text)
        
        if (clicked_close_button(config, clicked_pixel)):
            current_close_style = flip_button_style_and_redraw(window, config, current_close_style, close_text)
            window.close()
        
main()