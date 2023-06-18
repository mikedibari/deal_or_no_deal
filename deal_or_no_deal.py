import random

class StandardGame:
    def __init__(self, name):
        self.game_board_amounts = ["$.01", "$1", "$5", "$10", "$25", "$50", "$75", "$100", "$200", "$300", "$400", "$500", "$750", "$1,000",  "$5,000", "$10,000", "$25,000", "$50,000", "$75,000", "$100,000", "$200,000", "$300,000", "$400,000", "$500,000", "$750,000", "$1,000,000"]
        self.remaining_cases = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        self.game_round = 1
        self.turn = 6
        self.name = name

    # method that shuffles cases and creates dictionary of game board values
    def create_game_board(self, game_board_amounts): # allows to input different amounts from MdmGame subclass
        random.shuffle(self.remaining_cases)
        self.game_board = dict(zip(self.remaining_cases, game_board_amounts))
        return self.game_board # saved as shuffled_dict

    # method that converts game board to list and displays remaining values
    def show_game_board(self, shuffled_dict):
        self.game_display = []
        for value in shuffled_dict.values():
            self.game_display.append(value)
        print("--------------------------")
        for col1, col2 in zip(self.game_display[:13:1], self.game_display[13::1]):
            print("{:<20}{:<20}".format(col1, col2)) 
        print("--------------------------")   
    
    # method that displays remaining cases and uses binary search to slice the list
    def show_cases(self):
        lower_bound = 0
        upper_bound = len(self.remaining_cases)
        pivot = (lower_bound + upper_bound) // 2
        sorted_list = sorted(self.remaining_cases)
        print(*sorted_list[:pivot], sep=' | ')
        print(*sorted_list[pivot:], sep=' | ')

    # method that calculates expected value
    def expected_value(self, shuffled_dict):
        sum = 0
        count = 0
        for value in shuffled_dict.values():
            if value:
                stripped_value = float(value.strip('$').replace(',', ''))
                sum += stripped_value
                count += 1
            else:
                continue
        return round(sum / count) # saved as expected_value
    
    # player chooses their case to keep (secret value)
    def first_case(self, number):
        if int(number) in self.remaining_cases:
            self.my_case = int(number)
            self.remaining_cases.remove(int(number))
            return self.my_case # saved as my_case
        
    def next_case(self, choice, shuffled_dict):
        self.amount_in_case = shuffled_dict[int(choice)]
        self.remaining_cases.remove(int(choice))
        # players choice is replaced with a blank value
        shuffled_dict[int(choice)] = ""
        return self.amount_in_case # saved as amount_in_case
    
    def deal_or_no_deal(self):
        while True:
            deal = input("\nDeal or no deal?: ")
            if deal.lower() == "deal":
                return True
            elif deal.lower() == "no deal":
                return False
            else:
                print("That's not a valid answer!")
   
    def swap_cases(self, name, decision, shuffled_dict, final_case, my_case):
        if decision.lower() == "yes":
            print("\n" + name + ", you win " + str(shuffled_dict[final_case[0]]))
            print("\nThe original case you picked contained " + str(shuffled_dict[my_case]))
            return True
        elif decision.lower() == "no":
            print("\n" + name + ", you win " + str(shuffled_dict[my_case]) + "!" )
            print("\nThe other case contained " + str(shuffled_dict[final_case[0]]))
            return True
        
# Subclass - Million Dollar Mission - contains different game_board_amounts
class MdmGame(StandardGame):
    def __init__(self, name):
        super().__init__(name)
        self.game_board_amounts = ["$.01", "$1", "$5", "$10", "$25", "$50", "$75", "$100", "$200", "$300", "$400", "$500", "$750", "$1,000",  "$5,000", "$10,000", "$25,000", "$50,000", "$75,000", "$100,000", "$1,000,000", "$1,000,000","$1,000,000", "$1,000,000", "$1,000,000", "$1,000,000"]

# class that generates the banker's offers
class Offer:
    def __init__(self):
            self.offers_list = []
    
    # Banker's offer formula    
    def generate_offer(self, game_round, expected_value): 
        self.curve_values = [.21, .39, .52, .61, .66, .67, .68, .66, .61]
        self.offer = self.curve_values[game_round - 1] * expected_value
        if game_round > 0:
            self.offers_list.append(self.offer)
            return self.offer # saved as this_offer
        
    def show_offers(self):
        if self.offers_list == []:
            return None
        else:
            print("Previous offers:")
            for offer in self.offers_list:
                print("$" f"{round(offer):,}")
    
    def final_offer(self, name, last_offer, shuffled_dict, my_case):
        print("\n" + name + ", you win $" + f"{round(last_offer):,}" + "!")
        print("\nThe original case you picked contained " + str(shuffled_dict[my_case]))
    
    # Todo def counter_offer

def isint(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

print("\nWelcome to Deal Or No Deal!")
your_name = input("\nPlease enter your name: ")

while True:
    # choice of game, instantiate objects and create game board
    game_choice = input("\nWould you like up the stakes and play the Million Dollar Mission? Type no for standard game: ")
    if game_choice.lower() == "no":
        player1 = StandardGame(your_name)
    else:
        player1 = MdmGame(your_name)

    name = player1.name
    game_board_amounts = player1.game_board_amounts
    shuffled_dict = player1.create_game_board(game_board_amounts)
    offer = Offer()

    # print(shuffled_dict)     # shows shuffled dictionary for debugging

    # player chooses first case
    while True: 
        player1.show_cases()  
        choice = input("\n{}, it's time to pick your case! ".format(name))
        if isint(choice) and int(choice) in player1.remaining_cases:
            break
        print("\nPick a valid number!\n")
    my_case = player1.first_case(choice)
    
    while player1.game_round <= 9:
    
        # shows the game round number and hidden amounts for debugging
        # print("Round", player1.game_round)
        # print(shuffled_dict)
        # print("Your case #:", my_case, "contains", shuffled_dict[my_case])
        
        # player chooses next case to open
        counter = player1.turn
        if counter == 1:
            print("\n" + player1.name + ", you have one case to open!")
        else:
            print("\nThere are " + str(counter) + " cases to open in this round.")
        for turn in range(counter):
            player1.show_game_board(shuffled_dict)
            player1.show_cases()
            
            while True:
                choice = input("\n{}, which case do you want to open? ".format(name))
                if isint(choice) and int(choice) in player1.remaining_cases:
                    break
                print("\nInvalid choice!")
            amount_in_case = player1.next_case(choice, shuffled_dict)
            counter -= 1
            print("\nThe case you opened contained " + amount_in_case)
            if counter > 0:
                print("\nYou have " + str(counter) + " more to open.")
            
        player1.show_game_board(shuffled_dict)
        expected_value = player1.expected_value(shuffled_dict)
        # print(expected_value)
        offer.show_offers()
        this_offer = offer.generate_offer(player1.game_round, expected_value)
        print("\nThe banker's offer is $" + f"{round(this_offer):,}")
        deal = player1.deal_or_no_deal()
        if deal == True:
            break

        if player1.turn > 1:
            player1.turn -= 1
        player1.game_round +=1    
        
    if player1.game_round > 9:
        final_case = player1.remaining_cases
        # print(final_case)
        print("\nThere are 2 cases remaining. Your case #", my_case, "and case #", final_case[0])
        while True:
            decision = input("\nDo you want to swap cases? ")
            if player1.swap_cases(name, decision, shuffled_dict, final_case, my_case):
                break
            print("That is not a valid answer!")          
    else:
        last_offer = offer.offers_list[-1]
        offer.final_offer(name, last_offer, shuffled_dict, my_case)
        
    new_game = input("\nWould you like to play again? ")
    if new_game.lower() == "yes":
        continue
    else:
        print("\nSee you next time on Deal Or No Deal!")
        exit = input("\nType any key to exit: ")
        break


        
    