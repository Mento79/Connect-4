from tkinter import *
from heusrtic import *

class game:

    def __init__(self):
        #Colors
        self.red_border="#a42b39"
        self.red_tile="#80222d"
        self.yellow_border="#e3c559"
        self.yellow_tile="#c1bc2f"
        self.background_color="black"
        self.board_color= "#00008b"

        #Maximum board size to still be playable 17 x 17
        #Dynamic Variables
        self.board_width=7
        self.board_height=6
        self.Mini_Max_Depth=5

        #scale factor depends on board size
        self.scale_factor=3
        if(self.board_height<=8):self.scale_factor =0
        elif(self.board_height<=11):self.scale_factor =1
        elif(self.board_height<=17):self.scale_factor =2

        #board measurments
        self.square_length=100 -(25*self.scale_factor)
        self.scale =1.2 -(0.4*self.scale_factor)
        self.circle_scale = 12 -(2*self.scale_factor)
        self.star_x_shift=20 -(2*self.scale_factor)
        self.star_y_shift=17-(2*self.scale_factor)
        self.square_stroke=4

        #canvas dimensions
        self.canvas_width=self.board_width*self.square_length+self.board_width
        self.canvas_height=(self.board_height+1)*self.square_length +(4*self.board_height)

        #game assistant variables
        self.board=[]
        self.arr_circles=[[]*self.board_width]
        self.col=[0] * self.board_width
        self.color =True

        #Creating tkinter root
        self.root = Tk()
        self.root.minsize(height=self.canvas_height+300,width=self.canvas_width+300)
        self.root.option_add('*Font', '20')
        self.root.configure(background=self.background_color)
        self.mycanvas=None


    def draw (self,i):
        x = i * (2 + self.square_length)
        starx = i * (2 + self.square_length) + (self.star_x_shift)
        y = ((self.board_height-1)-self.col[i]) * (2+self.square_length) +self.square_length
        stary = ((self.board_height-1)-self.col[i]) * (2+self.square_length) +(self.star_y_shift) +self.square_length
        if(self.color):
            self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2, fill=self.red_border,width="0")
            self.mycanvas.create_oval(x + self.circle_scale, y + self.circle_scale, x + (self.square_length) - self.circle_scale - 1,y + (self.square_length) - self.circle_scale - 1, fill=self.red_tile, outline=self.background_color,width="0", )
            self.mycanvas.create_polygon(starx + (25 * self.scale), stary + (2.5 * self.scale), starx + (10 * self.scale),
                                    stary + (49.5 * self.scale), starx + (47.5 * self.scale), stary + (19.5 * self.scale),
                                    starx + (2.5 * self.scale), stary + (19.5 * self.scale), starx + (40 * self.scale),
                                    stary + (49.5 * self.scale), fill="", outline=self.red_border, width="2")
            self.board[(self.board_height-1) - self.col[i]][i]=1
        else:
            self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2, fill=self.yellow_border,width="0")
            self.mycanvas.create_oval(x + self.circle_scale, y + self.circle_scale, x + (self.square_length) - self.circle_scale - 1,y + (self.square_length) - self.circle_scale - 1, fill=self.yellow_tile, outline=self.background_color,width="0", )
            self.mycanvas.create_polygon(starx + (25 * self.scale), stary + (2.5 * self.scale), starx + (10 * self.scale),
                                    stary + (49.5 * self.scale), starx + (47.5 * self.scale), stary + (19.5 * self.scale),
                                    starx + (2.5 * self.scale), stary + (19.5 * self.scale), starx + (40 * self.scale),
                                    stary + (49.5 * self.scale), fill="", outline=self.yellow_border, width="2")
            self.board[(self.board_height-1) - self.col[i]][i] = 2
        self.col[i]+=1
        finshed=True
        for temp in self.col:
            if temp < self.board_height:
                finshed=False
                break
        if(finshed):
            self.check()
            self.hover_clear()
        else:
            self.color = not self.color
            if (not self.color):
                temp ,column2 = mini_max(self.board, 2, True)
                self.draw(column2)


    def hover_clear(self):
        for j in range(0,self.board_width):
            y = 0
            x = j * (2 + self.square_length)
            self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2, fill=self.background_color,width="0")


    def hover_draw (self,i):
        starx = i * (2 + self.square_length) + (self.star_x_shift)
        y = 0
        stary = (self.star_y_shift)
        self.hover_clear()
        x = i * (2 + self.square_length)
        if(self.color):
            self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2, fill=self.red_border,width="0")
            self.mycanvas.create_oval(x + self.circle_scale, y + self.circle_scale, x + (self.square_length) - self.circle_scale - 1,y + (self.square_length) - self.circle_scale - 1, fill=self.red_tile, outline=self.background_color,width="0", )
            self.mycanvas.create_polygon(starx + (25 * self.scale), stary + (2.5 * self.scale), starx + (10 * self.scale),
                                    stary + (49.5 * self.scale), starx + (47.5 * self.scale), stary + (19.5 * self.scale),
                                    starx + (2.5 * self.scale), stary + (19.5 * self.scale), starx + (40 * self.scale),
                                    stary + (49.5 * self.scale), fill="", outline=self.red_border, width="2")
        else:
            self.mycanvas.create_oval(x + 1, y + 1, x + (self.square_length) - 2, y + (self.square_length) - 2, fill=self.yellow_border,width="0")
            self.mycanvas.create_oval(x + self.circle_scale, y + self.circle_scale, x + (self.square_length) - self.circle_scale - 1,y + (self.square_length) - self.circle_scale - 1, fill=self.yellow_tile, outline=self.background_color,width="0", )
            self.mycanvas.create_polygon(starx + (25 * self.scale), stary + (2.5 * self.scale), starx + (10 * self.scale),
                                    stary + (49.5 * self.scale), starx + (47.5 * self.scale), stary + (19.5 * self.scale),
                                    starx + (2.5 * self.scale), stary + (19.5 * self.scale), starx + (40 * self.scale),
                                    stary + (49.5 * self.scale), fill="", outline=self.yellow_border, width="2")


    def check(self):
        red=0
        yellow=0
        #down
        for i in range(self.board_height-3):
          for j in range(self.board_width):
            if(self.board[i][j]==1 and self.board[i+1][j]==1 and self.board[i+2][j]==1 and self.board[i+3][j]==1):
                red+=1
            if(self.board[i][j]==2 and self.board[i+1][j]==2 and self.board[i+2][j]==2 and self.board[i+3][j]==2):
                yellow+=1
        #right and left
        for i in range(self.board_height):
            for j in range(self.board_width-3):
                if (self.board[i][j] == 1 and self.board[i][j+1] == 1 and self.board[i][j+2] == 1 and self.board[i][j+3] == 1):
                    red += 1
                if (self.board[i][j] == 2 and self.board[i][j+1] == 2 and self.board[i][j+2] == 2 and self.board[i][j+3] == 2):
                    yellow += 1
        #digonally
        for i in range(self.board_width-3):
            for j in range (self.board_height-3):
                if (self.board[j][i] == 1 and self.board[j+1][i+1] == 1 and self.board[j+2][i+2] == 1 and self.board[j+3][i+3] == 1):
                    red += 1
                if (self.board[j][i] == 2 and self.board[j+1][i+1] == 2 and self.board[j+2][i+2] == 2 and self.board[j+3][i+3] == 2):
                    yellow += 1
        #reverse diagonal
        for i in range(self.board_width-3):
            for j in range (self.board_height-1,self.board_height-4,-1):
                if (self.board[j][i] == 1 and self.board[j-1][i+1] == 1 and self.board[j-2][i+2] == 1 and self.board[j-3][i+3] == 1):
                    red += 1
                if (self.board[j][i] == 2 and self.board[j-1][i+1] == 2 and self.board[j-2][i+2] == 2 and self.board[j-3][i+3] == 2):
                    yellow += 1
        print("Red     ",red," - ",yellow,"    yellow")


    def draw_board(self):
        self.mycanvas = Canvas(self.root, width=self.canvas_width+(self.square_stroke*3), height=self.canvas_height+(self.square_stroke*3),bd=0,highlightthickness=0, bg=self.background_color)
        self.mycanvas.pack(pady=20)
        for i in range (0,self.board_height):
            y = i * (2+self.square_length)+self.square_length
            self.arr_circles.append([])
            self.board.append([])
            for j in range(0,self.board_width):
                x=j * (2+self.square_length)
                self.mycanvas.create_rectangle(x , y , x + (self.square_length) , y +(self.square_length) , outline=self.board_color, fill=self.board_color ,width = "2")
                self.arr_circles[i].append(self.mycanvas.create_oval(x +1 , y +1 , x + (self.square_length) -2, y +(self.square_length) -2 ,fill=self.background_color ,width = "0"))
                self.board[i].append(0)
                self.mycanvas.tag_bind(self.arr_circles[i][j],"<Button-1>",lambda x: self.draw(x.x//self.square_length))
                self.mycanvas.tag_bind(self.arr_circles[i][j],"<Enter>",lambda x:self.hover_draw (x.x//(self.square_length+2)))


    def main_menu(self):
      mylabel2 = Label(self.root, text='Choose one of the following three methods to solve the puzzle', fg=self.board_color, bg=self.background_color)
      mylabel2.pack()
      mylabel2.place(x=170, y=80)
      button1 = Button(self.root, text='BFS', command=lambda:[self.draw_board()], bg=self.background_color, fg=self.board_color, height = 2, width = 8)
      button1.place(x=500,y=900)
      self.root.mainloop()
