class TicTacToe:

    def __init__(self):
        self.board, self.allPlayers, self.cols, self.symbols = [], [], ["a","b","c","d","e","f"], ["X","O"]

    def menu(self):

        while True:
            print("Welcome to the game! \n"
                  "Please choose an option from the menu: \n"
                  "0 - exit \n"
                  "1 - play game (if you haven't made at least 2 players yet, you will be redirected to make more "
                  "players first) \n"
                  "2 - make a new player \n"
                  "3 - show player leaderboard \n"
                  "4 - reset player \n"
                  "5 - show instructions")

            choice = self.get_menu_choice()

            if choice == 0:
                if self.exit_menu():
                    return None
            elif choice == 1:
                self.run_game()
            elif choice == 2:
                self.make_player()
            elif choice == 3:
                self.leaderboard()
            elif choice == 4:
                self.reset_player()
            elif choice == 5:
                self.instructions()

    def get_menu_choice(self):
        while True:
            try:
                choice = int(input())
            except:
                print("Sorry, I can't process that. Please try again.")
                continue
            if choice > 5:
                print("Invalid option, please try again.")
                continue
            elif choice < 0:
                print("Invalid option, please try again.")
                continue
            else:
                return choice

    def exit_menu(self):
        finish = None
        while True:
            try:
                print("Are your sure you want to leave? Y or N")
                leave = input().upper().strip()
                if leave == "Y":
                    finish = True
                    break
                elif leave == "N":
                    finish = False
                    break
                else:
                    print("Sorry, I can't process that.")
                continue
            except:
                print("Sorry, I can't process that.")

        return finish

    def run_game(self):
        same_p = False
        same_b = False
        self.players_check()

        while True:
            # 1. setup: get players, board
            if not same_p:
                players = self.choose_players()
                print()
            if not same_b:
                self.make_board()
                print()

            # 2. game: while loop to check for draw, make move, verify move, win check
            self.play_game(players)

            # 3. after game: clear board, get play again settings
            self.reset_board()
            play = self.play_again()
            if play:
                same_p = self.same_players()
                same_b = self.same_board()
                continue

            return None

    def reset_player(self):
        if len(self.allPlayers) > 0:
            for i in range(len(self.allPlayers)):
                print(str(i + 1) + ": " + self.allPlayers[i].get_name())
            print()

            while True:
                try:
                    p = int(input("Please choose player to reset (by number): "))
                    break
                except:
                    print("Sorry, I can't process that.")
            if (p <= len(self.allPlayers)) and (p > 0):
                self.allPlayers[p-1].reset()
                print("Player {} reset".format(self.allPlayers[p-1].get_name()))
                print(self.allPlayers[p-1])
            else:
                print("Sorry, please try again")
            print()

        else:
            print("There are no players")

        return None

    def instructions(self):
        print("Welcome to Tic Tac Toe! \n"
              "The object of Tic Tac Toe is to get three in a row. You play on a three by three, four by four, five\n"
              "by five or six by six game board. The first player is known as X and the second is O.\n "
              "Players alternate placing Xs and Os on the game board until either opponent has three in a row or all\n"
              "nine squares are filled. The first player to get a row of three in a row (horizontal, vertical, or\n"
              "diagonal) wins. If neither gets three in a row, the game ends in a stalemate. Sounds easy? Just wait\n"
              "and see!")

    def players_check(self):
        while len(self.allPlayers) < 2:
            print("You don't have enough players yet")
            self.make_player()

    def choose_players(self):
        chosen_players = []

        while len(chosen_players) < 2:
            for i in range(len(self.allPlayers)):
                if self.allPlayers[i] in chosen_players:
                    continue
                print(str(i+1) + ": " + self.allPlayers[i].get_name())
            print()

            while True:
                try:
                    p = int(input("Please choose player {} (by number): ".format(len(chosen_players) + 1)))
                    break
                except:
                    print("Sorry, I can't process that.")

            if (p <= len(self.allPlayers)) and (p > 0):
                if self.allPlayers[p-1] not in chosen_players:
                    chosen_players.append(self.allPlayers[p - 1])
                    print("New player added. Player {}: {}".format(len(chosen_players),
                                                                   chosen_players[-1].get_name()))
                else:
                    print("Sorry, cannot add same player twice.")
            else:
                print("Sorry, please try again")
            print()

        # add player symbols
        for i in range(2):
            chosen_players[i].player_setup(i + 1, self.symbols[i])

        return chosen_players

    def play_game(self, players):
        moves = len(self.board) ** 2
        current_index = 0
        self.display()
        for move in range(moves):
            current_player = players[current_index]
            print(current_player.get_name() + "'s turn:")

            while True:
                cr = self.get_move()
                c = cr[0].lower()
                r = int(cr[1])
                if self.check_move(r, c):
                    self.do_move(r, c, current_player.sym)
                    break
                else:
                    print("Sorry, invalid move")

            if self.check():
                self.win_procedure(players, current_index)
                return None
            else:
                current_index = self.toggle(current_index)

        self.draw_procedure(players)
        return None

    def make_board(self):
        self.board = []
        num = 0
        while num < 3 or num > 6:
            try:
                num = int(input("How big would you like your board to be? Enter an integer between 3 and 6: "))
            except:
                print("Sorry, I can't process that.")

        for i in range(num):
            col = []
            for j in range(num):
                col.append(" ")
            self.board.append(col)

    def reset_board(self):
        for i in range(len(self.board)):
            col = []
            for j in range(len(self.board)):
                col.append(" ")
            self.board[i] = col

    def get_move(self):
        while True:
            try:
                move = input("Enter column and row, separated by a space: ")
                cr = move.split()
                cr[0] = cr[0].lower()
                if len(cr) != 2:
                    print("Sorry, invalid entry")
                    continue

                if cr[0] not in self.cols:
                    print("Sorry, invalid column")
                    continue

                if (int(cr[1]) > len(self.board)) or (int(cr[1]) < 1):
                    print("Sorry, invalid row")
                    continue

                else:
                    print()
                    break

            except:
                print("Sorry, I can't process that")

        return cr

    def check_move(self, row, col):
        r = row - 1
        c = self.cols.index(col)
        if self.board[r][c] == " ":
            return True
        else:
            return False

    def do_move(self, row, col, s):
        r = row - 1
        c = self.cols.index(col)
        self.board[r][c] = s

        self.display()

    def check(self):
        row_win = self.row_check()
        if row_win:
            return row_win

        col_win = self.col_check()
        if col_win:
            return col_win

        diag1_win = self.diag1_check()
        if diag1_win:
            return diag1_win

        diag2_win = self.diag2_check()
        return diag2_win

    def toggle(self, index):
        if index == 0:
            return 1
        else:
            return 0

    def win_procedure(self, players, index):
        print(players[index].get_name(), "won!")

        for player in players:
            if player == index:
                player.wins += 1
            else:
                print("Better luck next time,", player.get_name())
                player.losses += 1

        for player in players:
            print(player)
            print()

    def draw_procedure(self, players):
        print("Ended in a draw")
        for player in players:
            player.draws += 1
            print(player)
            print()

    def play_again(self):
        playing = None
        while True:
            try:
                print("Play again (without creating new players)? Y or N")
                cont = input().upper().strip()
                if cont == "Y":
                    playing = True
                    break
                elif cont == "N":
                    playing = False
                    break
                else:
                    print("Sorry, I can't process that.")
                continue
            except:
                print("Sorry, I can't process that.")

        return playing

    def same_players(self):
        same_p = None
        while True:
            try:
                print("Same player order? Y or N")
                cont = input().upper().strip()
                if cont == "Y":
                    same_p = True
                    break
                elif cont == "N":
                    same_p = False
                    break
                else:
                    print("Sorry, I can't process that.")
                continue
            except:
                print("Sorry, I can't process that.")

        return same_p

    def same_board(self):
        same_b = None
        while True:
            try:
                print("Same board? Y or N")
                cont = input().upper().strip()
                if cont == "Y":
                    same_b = True
                    break
                elif cont == "N":
                    same_b = False
                    break
                else:
                    print("Sorry, I can't process that.")
                continue
            except:
                print("Sorry, I can't process that.")

        return same_b

    def row_check(self):
        for r in range(len(self.board)):
            # only check rest of row if the first element has something in it
            ele = self.board[r][0]
            if ele in self.symbols:
                ind = self.symbols.index(ele)
                chk = True

                # Comparing each element with first item
                for item in self.board[r]:
                    if item not in self.symbols:
                        chk = False
                        break
                    elif self.symbols.index(item) != ind:
                        chk = False
                        break
                if chk:
                    return True
                else:
                    continue
            else:
                continue
        return False

    def col_check(self):
        for c in range(len(self.board)):
            # only check rest of col if the first element has something in it
            ele = self.board[0][c]
            if ele in self.symbols:
                ind = self.symbols.index(ele)
                chk = True

                # Comparing each element with first item
                for r in range(len(self.board)):
                    if self.board[r][c] not in self.symbols:
                        chk = False
                        break
                    elif self.symbols.index(self.board[r][c]) != ind:
                        chk = False
                        break
                if chk:
                    return True
                else:
                    continue
            else:
                continue
        return False

    def diag1_check(self):
        # only check rest of row if the first element has something in it
        ele = self.board[0][0]
        if ele in self.symbols:
            ind = self.symbols.index(ele)
            chk = True

            for i in range(len(self.board)):
                if self.board[i][i] not in self.symbols:
                    chk = False
                    break
                elif self.symbols.index(self.board[i][i]) != ind:
                    chk = False
                    break

            if chk:
                return True
            else:
                return False

    def diag2_check(self):
        # only check rest of row if the first element has something in it
        ele = self.board[0][-1]
        if ele in self.symbols:
            ind = self.symbols.index(ele)
            chk = True

            for i in range(len(self.board)):
                if self.board[i][-(i + 1)] not in self.symbols:
                    chk = False
                    break
                elif self.symbols.index(self.board[i][-(i + 1)]) != ind:
                    chk = False
                    break

            if chk:
                return True
            else:
                return False

    def make_player(self):
        name = ""
        # 1. get player name
        while len(name) < 1:
            name = input("Please enter the name for new player: ")
            name = name.strip().capitalize()

        # 2. check for duplicate
        for player in self.allPlayers:
            if player.name == name:
                print("Sorry, cannot add two players with the same name")
                return False

        # 3. add player
        self.allPlayers.append(Player(name))
        print("Player added: " + self.allPlayers[-1].get_name())

    def leaderboard(self):
        # 1. function to sort players
        def get_per_wins(contact):
            return contact.per_wins()

        # 2. if multiple players exist, sort
        if len(self.allPlayers) > 0:
            self.allPlayers.sort(key=get_per_wins, reverse=True)
            if len(self.allPlayers) > 10:
                for i in self.allPlayers[:10]:
                    print(i)
            else:
                for i in self.allPlayers:
                    print(i)
            print()

        # 3. if not, print message
        else:
            print("There are no players")

    def display(self):
        print(" ", end="")
        for i in range(len(self.board)):
            print(" ", end="")
            print(self.cols[i], end="")
        print()
        for r in range(len(self.board)):
            print((r+1), end="")
            print(" ", end="")
            for c in range(len(self.board)):
                print(self.board[r][c], end="")
                if c < len(self.board) - 1:
                    print("|", end="")
            print()
            if r < len(self.board) - 1:
                print("  " + "-+" * (len(self.board)-1) + "-")


class Player:

    def __init__(self, name):
        self.name = name.strip().capitalize()
        self.sym = ""
        self.number, self.wins, self.losses, self.draws = 0, 0, 0, 0

    def __str__(self):
        s = "{}:\n" \
            "Wins: {}; " \
            "Percent Wins: {:0.2f}%\n"\
            "Losses: {}; " \
            "Percent Losses: {:0.2f}%\n" \
            "Draws: {}; "\
            "Percent Draws: {:0.2f}%\n"
        return s.format(self.name, self.wins, self.per_wins(), self.losses, self.per_losses(), self.draws,
                        self.per_draws())

    def get_name(self):
        return self.name

    def player_setup(self, num, sym):
        self.sym = sym
        self.number = num

    def per_wins(self):
        if self.wins + self.losses + self.draws > 0:
            games = self.wins + self.losses + self.draws
            per_win = 100 * (self.wins / games)
            return round(per_win, 2)
        else:
            return 0

    def per_draws(self):
        if self.wins + self.losses + self.draws > 0:
            games = self.wins + self.losses + self.draws
            per_draw = 100 * (self.draws / games)
            return round(per_draw, 2)
        else:
            return 0

    def per_losses(self):
        if self.wins + self.losses + self.draws > 0:
            games = self.wins + self.losses + self.draws
            per_loss = 100 * (self.losses / games)
            return round(per_loss, 2)
        else:
            return 0

    def reset(self):
        self.wins = 0
        self.losses = 0
        self.draws = 0


new = TicTacToe()
new.menu()
