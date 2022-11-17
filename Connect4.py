from tkinter import *
from tkinter import messagebox
from typing import List, Tuple

from heusrtic import *
from State import State


class StateMocker:
    count = 0

    def __init__(self, depth: int, parent=None):
        self.parent = parent
        self.depth = depth
        self.hvalue = StateMocker.count
        StateMocker.count += 1
        self.children: List[StateMocker] = []
        if depth < 3:
            for i in range(7):
                self.children.append(StateMocker(depth + 1, self))


class game:

    def __init__(self):
        # Colors
        self.red_border = "#a42b39"
        self.red_tile = "#80222d"
        self.yellow_border = "#e3c559"
        self.yellow_tile = "#c1bc2f"
        self.background_color = "black"
        self.board_color = "#00008b"
        self.menu_color= "#6200EE"

        # scale factor depends on board size
        self.scale_factor = 3

        # board measurments

        self.board_width = None
        self.board_height = None
        self.Mini_Max_Depth = None

        self.square_length = None
        self.scale = None
        self.circle_scale = None
        self.star_x_shift = None
        self.star_y_shift = None
        self.square_stroke =None

        # canvas dimensions
        self.canvas_width = None
        self.canvas_height = None

        # game assistant variables
        self.board = None
        self.arr_circles = None
        self.col = None
        self.color = None

        # Creating tkinter root
        self.root = Tk()
        # self.root.minsize(height=700,width=1000)
        self.root.minsize(height=450, width=700)
        self.root.option_add('*Font', '20')
        self.root.configure(background=self.background_color)
        self.mycanvas: Canvas = None

        # Dynamic Variables
        self.board_height_text = StringVar(self.root,"6")
        self.board_width_text = StringVar(self.root,"7")
        self.Mini_Max_Depth_text = StringVar(self.root,"2")
        self.tree_button = None
        self.without_prun = True
        self.pause= False

    def draw(self, i):
        mo = StateMocker(0)
        state:State = None
        if self.tree_button is None:
            self.tree_button = Button(self.root, text='Tree',
                             command=lambda: [self.draw_tree(state)],
                             bg=self.background_color, fg="#6200EE", height=2, width=10)
            self.tree_button.place(x=10, y=80)
            self.changeOnHover(self.tree_button)
        x = i * (2 + self.square_length)
        starx = i * (2 + self.square_length) + (self.star_x_shift)
        y = ((self.board_height - 1) - self.col[i]) * (2 + self.square_length) + self.square_length
        stary = ((self.board_height - 1) - self.col[i]) * (2 + self.square_length) + (
            self.star_y_shift) + self.square_length
        if (self.color):
            self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2,
                                      fill=self.red_border, width="0")
            self.mycanvas.create_oval(x + self.circle_scale, y + self.circle_scale,
                                      x + (self.square_length) - self.circle_scale - 1,
                                      y + (self.square_length) - self.circle_scale - 1, fill=self.red_tile,
                                      outline=self.background_color, width="0", )
            self.mycanvas.create_polygon(starx + (25 * self.scale), stary + (2.5 * self.scale),
                                         starx + (10 * self.scale),
                                         stary + (49.5 * self.scale), starx + (47.5 * self.scale),
                                         stary + (19.5 * self.scale),
                                         starx + (2.5 * self.scale), stary + (19.5 * self.scale),
                                         starx + (40 * self.scale),
                                         stary + (49.5 * self.scale), fill="", outline=self.red_border, width="2")
            self.board[(self.board_height - 1) - self.col[i]][i] = 1
        else:
            self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2,
                                      fill=self.yellow_border, width="0")
            self.mycanvas.create_oval(x + self.circle_scale, y + self.circle_scale,
                                      x + (self.square_length) - self.circle_scale - 1,
                                      y + (self.square_length) - self.circle_scale - 1, fill=self.yellow_tile,
                                      outline=self.background_color, width="0", )
            self.mycanvas.create_polygon(starx + (25 * self.scale), stary + (2.5 * self.scale),
                                         starx + (10 * self.scale),
                                         stary + (49.5 * self.scale), starx + (47.5 * self.scale),
                                         stary + (19.5 * self.scale),
                                         starx + (2.5 * self.scale), stary + (19.5 * self.scale),
                                         starx + (40 * self.scale),
                                         stary + (49.5 * self.scale), fill="", outline=self.yellow_border, width="2")
            self.board[(self.board_height - 1) - self.col[i]][i] = 2
        self.col[i] += 1
        self.pause =not self.pause
        if self.pause:
            self.hover_clear()
            self.mycanvas.update()
        finshed = True
        for temp in self.col:
            if temp < self.board_height:
                finshed = False
                # print("loooool",self.board_height)
                break
        if (finshed):
            # print("XXXXD")
            self.check()
            self.hover_clear()
        else:
            self.color = not self.color
            if (not self.color):
                if(self.without_prun):
                    temp, column2, state = start_minmax(self.board, self.Mini_Max_Depth,None,None, True)
                    print(temp)
                    print(column2)
                else:
                    temp, column2, state = start_minmax(self.board, self.Mini_Max_Depth,-math.inf,math.inf, True)
                self.draw(column2)
                if not self.pause:
                    self.hover_draw(i)

    def hover_clear(self):
        for j in range(0, self.board_width):
            y = 0
            x = j * (2 + self.square_length)
            self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2,
                                      fill=self.background_color, width="0")

    def hover_draw(self, i):
        if not self.pause:
            starx = i * (2 + self.square_length) + (self.star_x_shift)
            y = 0
            stary = (self.star_y_shift)
            self.hover_clear()
            x = i * (2 + self.square_length)
            if (self.color):
                self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2,
                                          fill=self.red_border, width="0")
                self.mycanvas.create_oval(x + self.circle_scale, y + self.circle_scale,
                                          x + (self.square_length) - self.circle_scale - 1,
                                          y + (self.square_length) - self.circle_scale - 1, fill=self.red_tile,
                                          outline=self.background_color, width="0", )
                self.mycanvas.create_polygon(starx + (25 * self.scale), stary + (2.5 * self.scale),
                                             starx + (10 * self.scale),
                                             stary + (49.5 * self.scale), starx + (47.5 * self.scale),
                                             stary + (19.5 * self.scale),
                                             starx + (2.5 * self.scale), stary + (19.5 * self.scale),
                                             starx + (40 * self.scale),
                                             stary + (49.5 * self.scale), fill="", outline=self.red_border, width="2")
            else:
                self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2,
                                          fill=self.yellow_border, width="0")
                self.mycanvas.create_oval(x + self.circle_scale, y + self.circle_scale,
                                          x + (self.square_length) - self.circle_scale - 1,
                                          y + (self.square_length) - self.circle_scale - 1, fill=self.yellow_tile,
                                          outline=self.background_color, width="0", )
                self.mycanvas.create_polygon(starx + (25 * self.scale), stary + (2.5 * self.scale),
                                             starx + (10 * self.scale),
                                             stary + (49.5 * self.scale), starx + (47.5 * self.scale),
                                             stary + (19.5 * self.scale),
                                             starx + (2.5 * self.scale), stary + (19.5 * self.scale),
                                             starx + (40 * self.scale),
                                             stary + (49.5 * self.scale), fill="", outline=self.yellow_border, width="2")

    def draw_line(self,i1,j1,i2,j2,color):
        x1 = i1 * (2 + self.square_length) + (self.square_length)/2
        x2 = i2 * (2 + self.square_length) + (self.square_length)/2
        y1 = j1 * (2 + self.square_length) + (self.square_length)/2
        y2 = j2 * (2 + self.square_length) + (self.square_length)/2
        self.mycanvas.create_line(x1 ,y1 ,x2 ,y2 ,fill=color ,width=10)
    def check(self):
        red = 0
        yellow = 0
        # down
        for i in range(self.board_height - 3):
            for j in range(self.board_width):
                if (self.board[i][j] == 1 and self.board[i + 1][j] == 1 and self.board[i + 2][j] == 1 and
                        self.board[i + 3][j] == 1):
                    red += 1
                    self.draw_line(j,i+1,j,i+4,"white")
                if (self.board[i][j] == 2 and self.board[i + 1][j] == 2 and self.board[i + 2][j] == 2 and
                        self.board[i + 3][j] == 2):
                    yellow += 1
                    self.draw_line(j,i+1,j,i+4,"black")
        # right and left
        for i in range(self.board_height):
            for j in range(self.board_width - 3):
                if (self.board[i][j] == 1 and self.board[i][j + 1] == 1 and self.board[i][j + 2] == 1 and self.board[i][
                    j + 3] == 1):
                    red += 1
                    self.draw_line(j,i+1,j+3,i+1,"white")

                if (self.board[i][j] == 2 and self.board[i][j + 1] == 2 and self.board[i][j + 2] == 2 and self.board[i][
                    j + 3] == 2):
                    yellow += 1
                    self.draw_line(j,i+1,j+3,i+1,"black")
        # digonally
        for i in range(self.board_width - 3):
            for j in range(self.board_height - 3):
                if (self.board[j][i] == 1 and self.board[j + 1][i + 1] == 1 and self.board[j + 2][i + 2] == 1 and
                        self.board[j + 3][i + 3] == 1):
                    red += 1
                    self.draw_line(i,j+1,i+3,j+4,"white")
                if (self.board[j][i] == 2 and self.board[j + 1][i + 1] == 2 and self.board[j + 2][i + 2] == 2 and
                        self.board[j + 3][i + 3] == 2):
                    yellow += 1
                    self.draw_line(i,j+1,i+3,j+4,"black")
        # reverse diagonal
        for i in range(self.board_width - 3):
            for j in range(self.board_height - 1, self.board_height - 4, -1):
                if (self.board[j][i] == 1 and self.board[j - 1][i + 1] == 1 and self.board[j - 2][i + 2] == 1 and
                        self.board[j - 3][i + 3] == 1):
                    red += 1
                    self.draw_line(i+3,j-2,i,j+1,"white")
                if (self.board[j][i] == 2 and self.board[j - 1][i + 1] == 2 and self.board[j - 2][i + 2] == 2 and
                        self.board[j - 3][i + 3] == 2):
                    yellow += 1
                    self.draw_line(i+3,j-2,i,j+1,"black")
        print("Red     ", red, " - ", yellow, "    yellow")
        top = Toplevel(self.root)
        top.configure(background=self.background_color)
        top.geometry("600x250")
        top.title("Result")
        if yellow > red:
            Label(top, text="Red     "+ str(red)+ " - "+ str(yellow)+ "    yellow", fg="yellow",
                  bg=self.background_color, font='Arial 20 bold').place(x=165, y=30)
            Label(top, text="You are beaten by machine XD", fg=self.menu_color,
                  bg=self.background_color, font='Arial 27 bold').place(x=35, y=100)
        elif red > yellow:
            Label(top, text="Red     "+ str(red)+ " - "+ str(yellow)+ "    yellow", fg="red",
                  bg=self.background_color, font='Arial 20 bold').place(x=165, y=30)
            Label(top, text="ya 7lawatak ya 7lawatak", fg=self.menu_color,
                  bg=self.background_color, font='Arial 27 bold').place(x=40, y=100)
        else:
            Label(top, text="Red     "+ str(red)+ " - "+ str(yellow)+ "    yellow", fg=self.menu_color,
                  bg=self.background_color, font='Arial 20 bold').place(x=165, y=30)
            Label(top, text="Are You Our AI ?! :O", fg=self.menu_color,
                  bg=self.background_color, font='Arial 27 bold').place(x=35, y=100)

    def back_to_menu(self, back_button: Button):
        self.mycanvas.destroy()
        back_button.destroy()
        if self.tree_button is not None:
            self.tree_button.destroy()
            self.tree_button=None
        self.draw_main_menu()

    def draw_board(self):
        self.pause=False
        self.board_width=int(self.board_width_text.get())
        self.board_height=int(self.board_height_text.get())
        self.Mini_Max_Depth=int(self.Mini_Max_Depth_text.get())
        print(self.board_height,self.board_width,self.Mini_Max_Depth)
        if (self.board_height <= 8):
            self.scale_factor = 0
        elif (self.board_height <= 11):
            self.scale_factor = 1
        elif (self.board_height <= 17):
            self.scale_factor = 2

        self.square_length = 100 - (25 * self.scale_factor)
        self.scale = 1.2 - (0.4 * self.scale_factor)
        self.circle_scale = 12 - (2 * self.scale_factor)
        self.star_x_shift = 20 - (2 * self.scale_factor)
        self.star_y_shift = 17 - (2 * self.scale_factor)
        self.square_stroke =4

        self.canvas_width = self.board_width * self.square_length + self.board_width
        self.canvas_height = (self.board_height + 1) * self.square_length + (4 * self.board_height)

        self.board = []
        self.arr_circles = [[] * self.board_width]
        self.col = [0] * self.board_width
        self.color = True
        self.root.minsize(height=self.canvas_height + 300, width=self.canvas_width + 300)
        self.mycanvas = Canvas(self.root, width=self.canvas_width + (self.square_stroke * 3),
                               height=self.canvas_height + (self.square_stroke * 3), bd=0, highlightthickness=0,
                               bg=self.background_color)
        back_button = Button(self.root, text='Menu',
                             command=lambda: [self.back_to_menu(back_button)],
                             bg=self.background_color, fg="#6200EE", height=2, width=10)
        back_button.place(x=10, y=10)
        self.changeOnHover(back_button)
        self.mycanvas.pack(pady=20)
        for i in range(0, self.board_height):
            y = i * (2 + self.square_length) + self.square_length
            self.arr_circles.append([])
            self.board.append([])
            for j in range(0, self.board_width):
                x = j * (2 + self.square_length)
                self.mycanvas.create_rectangle(x, y, x + (self.square_length), y + (self.square_length),
                                               outline=self.board_color, fill=self.board_color, width="2")
                self.arr_circles[i].append(
                    self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2,
                                              fill=self.background_color, width="0"))
                self.board[i].append(0)
                self.mycanvas.tag_bind(self.arr_circles[i][j], "<Button-1>",
                                       lambda x: self.draw(x.x // self.square_length))
                self.mycanvas.tag_bind(self.arr_circles[i][j], "<Enter>",
                                       lambda x: self.hover_draw(x.x // (self.square_length + 2)))

    def move_to_board(self, list_destroy, without_prun) -> None:
        self.without_prun = without_prun
        if self.board_height_text.get()== "" or self.board_width_text.get()== "" or self.Mini_Max_Depth_text.get()== "" :
            messagebox.showwarning("Error", "Please Enter the Height ,Width and Depth")
        elif int(self.board_height_text.get())<6 or  int(self.board_height_text.get())>17:
            messagebox.showwarning("Error", "Please Enter Height between 6 and 17")
        elif int(self.board_width_text.get())<7 or  int(self.board_width_text.get())>17:
            messagebox.showwarning("Error", "Please Enter Width between 7 and 17")
        # elif int(self.Mini_Max_Depth_text.get())<##Min_Depth or  int(self.Mini_Max_Depth_text.get())>##Max_Depth:
        #     messagebox.showwarning("Error", "Please Enter Height between 6 and 17")
        else:
            for obj in list_destroy:
                obj.destroy()
            self.draw_board()

    def get_idx(self, x: int, tp: List[Tuple[int, int]]):
        for i, tup in enumerate(tp):
            if tup[0] <= x <= tup[1]:
                return i

    def draw_tree(self, state: State,depth= 0 , tree_canvas=None, top=None):
        # print(jj)
        if tree_canvas is None:
            top = Toplevel(self.root)
            top.minsize(width=1500, height=750)
            top.title("Tree Window")
        else:
            tree_canvas.destroy()
        tree_canvas = Canvas(top, width=1500, height=750, bg="black")
        tree_canvas.place(x=0, y=0)
        if state.parent is not None:
            back_button = Button(top, text='Back',
                                 command=lambda: [self.draw_tree(state.parent,depth-1 ,tree_canvas, top)],
                                 bg=self.background_color, fg="#6200EE", height=2, width=10)
            back_button.place(x=10, y=10)
        max_par = depth % 2 == 0
        arrow_st_pt = (0, 0)
        poly = None
        text = None
        line = None
        if len(state.children) == 0:
            tree_canvas.create_rectangle(700, 60, 800, 100, fill="#03DAC6")
            text = tree_canvas.create_text(740, 80, text=str(state.hvalue),
                                           font='Calibri 10', anchor="w", fill="white")
        elif max_par:
            pts = [750, 60, 700, 104, 800, 105]
            poly = tree_canvas.create_polygon(pts, fill="#6200EE")
            text = tree_canvas.create_text(740, 80, text=str(state.hvalue),
                                           font='Calibri 9', anchor="w", fill="white")
            arrow_st_pt = (750, 100)
        else:
            pts = [700, 60, 800, 60, 750, 105]
            poly = tree_canvas.create_polygon(pts, fill="#CF6679")
            text = tree_canvas.create_text(740, 80, text=str(state.hvalue),
                                           font='Calibri 9', anchor="w", fill="white")
            arrow_st_pt = (750, 105)
        n = len(state.children)
        y_child_st = 600
        max_size_side = 80
        space = 0
        if n ==1:
            space = (1500- max_size_side -12)//2
        else:
            space = (1500 - max_size_side * n - 10) // (n - 1)
        poly: list = [x for x in range(n)]
        tup: List[Tuple[int, int]] = []
        for i in range(n):
            spacei = 1
            if n!=1 :
                spacei = i


            if max_par:
                pts = [5 + space * spacei + max_size_side * i, y_child_st,
                       5 + space * spacei + max_size_side * (i + 1), y_child_st,
                       5 + space * spacei + max_size_side * i + max_size_side / 2, y_child_st + 40]
                tup.append((5 + space * spacei + max_size_side * i,
                       5 + space * spacei + max_size_side * (i + 1)))
                if len(state.children[i].children) == 0:
                    poly[i] = tree_canvas.create_rectangle(5 + space * spacei + max_size_side * i, y_child_st,
                                                 5 + space * spacei + max_size_side * (i + 1),
                                                 y_child_st + 40, fill="#189DE4")
                else:
                    poly[i] = tree_canvas.create_polygon(pts, fill="#CF6679")
                    tree_canvas.tag_bind(poly[i], '<Button-1>',
                                         lambda e: self.draw_tree(state.children[self.get_idx(e.x, tup)],depth+1 ,tree_canvas,
                                                                  top))
                line = tree_canvas.create_line(arrow_st_pt[0], arrow_st_pt[1],
                                               5 + space * spacei + max_size_side * i + max_size_side / 2, y_child_st, fill="#01B636", width=2)
                text = tree_canvas.create_text(10 + space * spacei + max_size_side * i + (max_size_side / 2 - 10),
                                               y_child_st + 15,
                                               text=str(state.children[i].hvalue),
                                               font='Calibri 9', anchor="w", fill="white")
                self.draw_small_board(5 + space * spacei + max_size_side * i,y_child_st + 40,10,tree_canvas,state.children[i])
            else:
                pts = [5 + space * spacei + max_size_side * i + max_size_side / 2, y_child_st,
                       5 + space * spacei + max_size_side * i, y_child_st + 40,
                       5 + space * spacei + max_size_side * (i + 1), y_child_st + 40]
                if len(state.children[i].children) == 0:
                    poly[i] = tree_canvas.create_rectangle(5 + space * spacei + max_size_side * i, y_child_st,
                                                 5 + space * spacei + max_size_side * (i + 1),
                                                 y_child_st + 40, fill="#189DE4")
                    self.draw_small_board(5 + space * spacei + max_size_side * i, y_child_st + 40, 10, tree_canvas,
                                          state.children[i])

                else:
                    poly[i] = tree_canvas.create_polygon(pts, fill="#6200EE")
                    self.draw_small_board(5 + space * spacei + max_size_side * i, y_child_st + 40, 10, tree_canvas,
                                          state.children[i])

                    tree_canvas.tag_bind(poly[i], '<Button-1>',
                                         lambda e: self.draw_tree(state.children[self.get_idx(e.x, tup)],depth+1 ,tree_canvas,
                                                                  top))
                tup.append((5 + space * spacei + max_size_side * i,
                            5 + space * spacei + max_size_side * (i + 1)))
                line = tree_canvas.create_line(arrow_st_pt[0], arrow_st_pt[1],
                                              5 + space * spacei + max_size_side * i + max_size_side / 2, y_child_st, fill="#01B636", width=2)
                text = tree_canvas.create_text(5 + space * spacei + max_size_side * i + (max_size_side / 2 - 10),
                                               y_child_st + 20,
                                               text=str(state.children[i].hvalue),
                                               font='Calibri 9', anchor="w", fill="white")
    def draw_small_board(self,x,y,size,canvas,state):
        board=state.getBoard()
        for i in range(0, self.board_height):
            y1 = i * (2 + size) + y
            for j in range(0, self.board_width):
                x1 = j * (2 + size) +x
                canvas.create_rectangle(x1, y1, x1 + size, y1 + size,
                                               outline=self.board_color, fill=self.board_color, width="2")
                if board[i][j]==0:
                    canvas.create_oval(x1 + 1, y1 + 1, x1 + size - 1, y1 + size - 1,
                                          fill=self.background_color, width="0")
                elif board[i][j]==1:
                    canvas.create_oval(x1 + 1, y1 + 1, x1 + size - 1, y1 + size - 1,
                                          fill=self.red_border, width="0")
                else:
                    canvas.create_oval(x1 + 1, y1 + 1, x1 + size - 1, y1 + size - 1,
                                          fill=self.yellow_border, width="0")



    def changeOnHover(self, button):
        # adjusting backgroung of the widget
        # background on entering widget
        button.bind("<Enter>", func=lambda e: button.config(
            background="grey"))

        # background color on leving widget
        button.bind("<Leave>", func=lambda e: button.config(
            background=self.background_color))

    def draw_main_menu(self):
        # mo = StateMocker(0)
        # self.draw_tree(mo)
        self.root.minsize(height=600, width=900)
        list_destroy = []
        self.tree_button = None

        my_label = Label(self.root, text='Choose one of the following two methods', fg=self.menu_color,
                         bg=self.background_color, font=("Helvetica", 25))
        my_label.pack()
        my_label.place(x=150, y=80)

        height_label = Label(self.root, text='H = ',fg=self.menu_color,
                             bg=self.background_color,font=('Helvetica 40 bold'))
        height_label.pack()
        height_label.place(x=200, y=180)
        print(self.board_height)
        height_Entry=Entry(self.root, width=3, font=('Helvetica 40 bold'), justify='center',
                                          fg=self.menu_color, bg="white", borderwidth=0,
                                          textvariable=self.board_height_text)
        height_Entry.place(x=300,y=180,height=65,width=65)

        width_label = Label(self.root, text='W = ',fg=self.menu_color,
                             bg=self.background_color,font=('Helvetica 40 bold'))
        width_label.pack()
        width_label.place(x=490, y=180)

        width_Entry=Entry(self.root, width=3, font=('Helvetica 40 bold'), justify='center',
                                          fg=self.menu_color, bg="white", borderwidth=0,
                                          textvariable=self.board_width_text)
        width_Entry.place(x=600,y=180,height=65,width=65)

        depth_label = Label(self.root, text='K = ',fg=self.menu_color,
                             bg=self.background_color,font=('Helvetica 40 bold'))
        depth_label.pack()
        depth_label.place(x=350, y=300)

        depth_Entry=Entry(self.root, width=3, font=('Helvetica 40 bold'), justify='center',
                                          fg=self.menu_color, bg="white", borderwidth=0,
                                          textvariable=self.Mini_Max_Depth_text)
        depth_Entry.place(x=450,y=300,height=65,width=65)
        list_destroy.append(height_Entry)
        list_destroy.append(height_label)
        list_destroy.append(width_Entry)
        list_destroy.append(width_label)
        list_destroy.append(depth_Entry)
        list_destroy.append(depth_label)

        button1 = Button(self.root, text='Minimax without α-β pruning',
                         command=lambda: [self.move_to_board(list_destroy, True)],
                         bg=self.background_color, fg="#6200EE", height=2, width=25)
        button1.place(x=150, y=410)
        button2 = Button(self.root, text='Minimax with α-β pruning',
                         command=lambda: [self.move_to_board(list_destroy, False)],
                         bg=self.background_color, fg="#6200EE", height=2, width=25)
        button2.place(x=500, y=410)
        self.changeOnHover(button1)
        self.changeOnHover(button2)
        list_destroy.append(my_label)
        list_destroy.append(button1)
        list_destroy.append(button2)
        self.root.mainloop()
        # self.root.
