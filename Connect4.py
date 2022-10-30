from tkinter import *

arr=[[0,6,2],[3,5,8],[4,6,7]]

arr_numbers=[[],[],[]]
red="#a42b39"
background_color="black"
foreground_color= "#00008b"
foreground_2nd_color= "#EA047E"
empty_color="#312e2b"
square_stroke=4
board_width=7
board_height=6
scale_factor=3
if(board_height<=8):scale_factor =0
elif(board_height<=11):scale_factor =1
elif(board_height<=17):scale_factor =2
square_length=100 -(25*scale_factor)
scale =1.2 -(0.4*scale_factor)
circle_scale = 12 -(2*scale_factor)
star_x_shift=20 -(2*scale_factor)
star_y_shift=17-(2*scale_factor)
canvas_width=board_width*square_length+board_width
canvas_height=(board_height+1)*square_length +(4*board_height)
print(canvas_height)
board=[]
print(board)
arr_circles=[[]*board_width]
print (arr_circles)
col=[0] * board_width
print (col)

counter = 1

root = Tk()
root.minsize(height=canvas_height+300,width=canvas_width+300)
root.option_add('*Font', '20')
mylabel = Label(root, text='8 puzzle', fg=foreground_color, bg=background_color)
root.configure(background=background_color)
mylabel.pack()
color =True
def tab1():
  mylabel2 = Label(root, text='Choose one of the following three methods to solve the puzzle', fg=foreground_color, bg=background_color)
  mylabel2.pack()
  mylabel2.place(x=170, y=80)

  def tab2():
      mycanvas = Canvas(root, width=canvas_width+(square_stroke*3), height=canvas_height+(square_stroke*3),bd=0,highlightthickness=0, bg="black")
      mycanvas.pack(pady=20)
      global counter

      def back():
          button4.destroy()
          mycanvas.destroy()
          buttonmove.destroy()
          tab1()


      def auto():
          while counter < len(moves_arr):
              next()
      def draw (i, j ):
          print (i , j )
          print (i , j, (board_height-1)-col[i] )
          global color
          x = i * (2 + square_length)
          starx = i * (2 + square_length) + (star_x_shift)
          y = ((board_height-1)-col[i]) * (2+square_length) +square_length
          stary = ((board_height-1)-col[i]) * (2+square_length) +(star_y_shift) +square_length
          if(color):
              mycanvas.create_oval(x + 1, y + 1, x + (square_length) - 2, y + (square_length) - 2, fill=red,width="0")
              mycanvas.create_oval(x + circle_scale, y + circle_scale, x + (square_length) - circle_scale - 1,y + (square_length) - circle_scale - 1, fill="#80222d", outline="black",width="0", )
              mycanvas.create_polygon(starx + (25 * scale), stary + (2.5 * scale), starx + (10 * scale),
                                      stary + (49.5 * scale), starx + (47.5 * scale), stary + (19.5 * scale),
                                      starx + (2.5 * scale), stary + (19.5 * scale), starx + (40 * scale),
                                      stary + (49.5 * scale), fill="", outline=red, width="2")
              board[(board_height-1) - col[i]][i]=1
          else:
              mycanvas.create_oval(x + 1, y + 1, x + (square_length) - 2, y + (square_length) - 2, fill="#e3c559",width="0")
              mycanvas.create_oval(x + circle_scale, y + circle_scale, x + (square_length) - circle_scale - 1,y + (square_length) - circle_scale - 1, fill="#c1bc2f", outline="black",width="0", )
              mycanvas.create_polygon(starx + (25 * scale), stary + (2.5 * scale), starx + (10 * scale),
                                      stary + (49.5 * scale), starx + (47.5 * scale), stary + (19.5 * scale),
                                      starx + (2.5 * scale), stary + (19.5 * scale), starx + (40 * scale),
                                      stary + (49.5 * scale), fill="", outline="#e3c559", width="2")
              board[(board_height-1) - col[i]][i] = 2
          #hntcheck hina
          check()
          color = not color
          hover_draw(i)
          col[i]+=1
          #print(board)

      def hover_draw (i):
          #print (i , j, 5-col[i] )
          global color
          starx = i * (2 + square_length) + (star_x_shift)
          y = 0
          stary = (star_y_shift)
          for j in range(0,board_width):
              x = j * (2 + square_length)
              mycanvas.create_oval(x + 1, y + 1, x + (square_length) - 2, y + (square_length) - 2, fill="black",width="0")
          x = i * (2 + square_length)
          if(color):
              mycanvas.create_oval(x + 1, y + 1, x + (square_length) - 2, y + (square_length) - 2, fill=red,width="0")
              mycanvas.create_oval(x + circle_scale, y + circle_scale, x + (square_length) - circle_scale - 1,y + (square_length) - circle_scale - 1, fill="#80222d", outline="black",width="0", )
              mycanvas.create_polygon(starx + (25 * scale), stary + (2.5 * scale), starx + (10 * scale),
                                      stary + (49.5 * scale), starx + (47.5 * scale), stary + (19.5 * scale),
                                      starx + (2.5 * scale), stary + (19.5 * scale), starx + (40 * scale),
                                      stary + (49.5 * scale), fill="", outline=red, width="2")
          else:
              mycanvas.create_oval(x + 1, y + 1, x + (square_length) - 2, y + (square_length) - 2, fill="#e3c559",width="0")
              mycanvas.create_oval(x + circle_scale, y + circle_scale, x + (square_length) - circle_scale - 1,y + (square_length) - circle_scale - 1, fill="#c1bc2f", outline="black",width="0", )
              mycanvas.create_polygon(starx + (25 * scale), stary + (2.5 * scale), starx + (10 * scale),
                                      stary + (49.5 * scale), starx + (47.5 * scale), stary + (19.5 * scale),
                                      starx + (2.5 * scale), stary + (19.5 * scale), starx + (40 * scale),
                                      stary + (49.5 * scale), fill="", outline="#e3c559", width="2")
          #hntcheck hina
          #print(board)

      def check():
          piece= 1 if color else 2
          #down
          for i in range(board_height-3):
            for j in range(board_width):
              if(board[i][j]==piece and board[i+1][j]==piece and board[i+2][j]==piece and board[i+3][j]==piece):
                  print( "kisbnaaaaaa ta7t" , i ,j ,piece,board)
          #right and left
          for i in range(board_height):
              for j in range(board_width-3):
                  if (board[i][j] == piece and board[i][j+1] == piece and board[i][j+2] == piece and board[i][j+3] == piece):
                      print("kisbnaaaaaa 3la nafs el5t",i,j)
          #digonally
          for i in range(board_width-3):
              for j in range (board_height-3):
                  if (board[j][i] == piece and board[j+1][i+1] == piece and board[j+2][i+2] == piece and board[j+3][i+3] == piece):
                      print("kisbnaaaaaa diagonal tal3 4imal")
          #reverse diagonal
          for i in range(board_width-3):
              for j in range (board_height-1,board_height-4,-1):
                  if (board[j][i] == piece and board[j-1][i+1] == piece and board[j-2][i+2] == piece and board[j-3][i+3] == piece):
                      print("kisbnaaaaaa diagonal tale3 ymin")

      for i in range (0,board_height):
          y = i * (2+square_length)+square_length
          arr_circles.append([])
          board.append([])
          for j in range(0,board_width):
              x=j * (2+square_length)
              mycanvas.create_rectangle(x , y , x + (square_length) , y +(square_length) , outline=foreground_color, fill=foreground_color ,width = "2")
              arr_circles[i].append(mycanvas.create_oval(x +1 , y +1 , x + (square_length) -2, y +(square_length) -2 ,fill="black" ,width = "0"))
              board[i].append(0)
              mycanvas.tag_bind(arr_circles[i][j],"<Button-1>",lambda x: draw(x.x//square_length,x.y//square_length))
              mycanvas.tag_bind(arr_circles[i][j],"<Enter>",lambda x:hover_draw (x.x//square_length))

      button1.destroy()
      button2.destroy()
      button3.destroy()
      mylabel2.destroy()



  button1 = Button(root, text='BFS', command=tab2, bg=background_color, fg=foreground_color, height = 2, width = 8)
  button1.place(x=100,y=250)
  button2 = Button(root, text='DFS', command=tab2, bg=background_color, fg=foreground_color, height=2, width=8)
  button2.place(x=400, y=250)
  button3 = Button(root, text='A*', command=tab2, bg=background_color, fg=foreground_color, height=2, width=8)
  button3.place(x=700, y=250)

tab1()
root.mainloop()
