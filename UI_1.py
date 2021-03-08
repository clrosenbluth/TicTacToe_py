# Create GUI for the basic Tic Tac Toe game, without the menu or options

import tkinter


class tttGUI:
    def __init__(self):
        # Variable to hold the current symbol
        self.current_var = 'X'

        # Create main window
        self.main_window = tkinter.Tk()
        self.main_window.geometry("300x300")

        # Create frames
        self.top_frame = tkinter.Frame(self.main_window)
        self.mid_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)

        # Pack frames
        self.top_frame.pack()
        self.mid_frame.pack()
        self.bottom_frame.pack()

        # Top frame - contains text
        self.instruction = tkinter.Label(self.top_frame,
                                         text="Welcome to Tic Tac Toe! \n"
                                              "Click any square to begin")
        self.prompt = tkinter.Label(self.top_frame,
                                    text="X's turn! Click to make your move.")

        # Pack top frame widgets
        self.instruction.pack()
        self.prompt.pack()

        # Create and grid a 2D array of buttons in middle frame
        self.board = []
        self.make_board()

        # Bottom frame - contains buttons, stats
        self.reset = tkinter.Button(self.bottom_frame)
        self.stats = tkinter.Label(self.bottom_frame)

        # Pack bottom frame widgets
        self.reset.pack()
        self.stats.pack()

        # Enter main loop
        tkinter.mainloop()

    def make_board(self):
        for x in range(3):
            button_row = []
            for y in range(3):
                new_button = tkinter.Button(self.mid_frame,
                                            text='-',
                                            command=lambda x1=x, y1=y: self.turn(x1, y1))
                new_button.grid(row=x, column=y)
                button_row.append(new_button)
            self.board.append(button_row)

    def turn(self, x, y):
        # Put out prompt
        if self.current_var == 'X':
            self.prompt["text"] = "O's turn! Click to make your move."
        else:
            self.prompt["text"] = "X's turn! Click to make your move."

        # Do the turn
        if self.board[x][y]["text"] == '-':
            self.board[x][y]["text"] = self.current_var

        # Check for a win
        if self.win_check():
            if self.current_var == 'X':
                self.prompt["text"] = "X: Winner!"
            else:
                self.prompt["text"] = "O: Winner!"

        # Change players
        self.toggle()

    def toggle(self):
        if self.current_var == 'X':
            self.current_var = 'O'
        else:
            self.current_var = 'X'

    def win_check(self):
        return self.row_check() or self.col_check() or self.diag1_check() or self.diag2_check()

    def row_check(self):
        # Check each row in the board to see if it's been won
        for row in self.board:
            # only check rest of row if the first element has something in it
            ele = row[0]
            if ele["text"] == '-':
                continue

            # indicator
            check = True

            # Comparing each element with first item
            for square in row:
                if square["text"] != ele["text"]:
                    check = False
                    break
            if check:
                return True
            else:
                continue

        return False

    def col_check(self):
        # Check each column for a win
        for col in range(len(self.board)):
            # only check rest of col if the first element has something in it
            ele = self.board[0][col]
            if ele["text"] == '-':
                continue

            # indicator
            check = True

            # Comparing each element with first item
            for row in self.board:
                if row[col]["text"] != ele["text"]:
                    check = False
                    break
            if check:
                return True
            else:
                continue

        return False

    def diag1_check(self):
        ele = self.board[0][0]
        if ele["text"] == '-':
            return False

        check = True

        for i in range(len(self.board)):
            if self.board[i][i]["text"] != ele["text"]:
                check = False
                break

        return check

    def diag2_check(self):
        # only check rest of row if the first element has something in it
        ele = self.board[0][-1]
        if ele["text"] == '-':
            return False

        check = True

        for i in range(len(self.board)):
            if self.board[i][-(i + 1)]["text"] != ele["text"]:
                check = False
                break

        return check


my_game = tttGUI()
