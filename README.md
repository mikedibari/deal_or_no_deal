# deal_or_no_deal

Deal Or No Deal is a Python game inspired by the TV game show of the same name. It combines luck, risk, and the decision-making process of knowing when to walk away. The game features 26 cases, each containing a different dollar amount ranging from $.01 to $1,000,000. The player's objective is to choose the case they believe holds the million-dollar prize. They then proceed to open other cases, revealing the contained dollar amounts and increasing their odds of having the million-dollar case.

After each round, the banker offers the player a certain amount to quit the game based on the remaining amounts. The player must decide whether to take the offer or continue. If they make it to the end with only two cases left, including their own, they have the option to swap cases and win the amount in the chosen case.

To store the cases and their corresponding values, a Python dictionary was used. Here's an example of the code:

```python
# Shuffled dictionary keys
{
    25: '$.01', 2: '$1', 3: '$5', 13: '$10', 19: '$25', 14: '$50', 18: '$75', 5: '$100', 10: 
    '$200', 21: '$300', 24: '$400', 6: '$500', 9: '$750', 1: '$1,000', 12: '$5,000', 15: 
    '$10,000', 16: '$25,000', 4: '$50,000', 11: '$75,000', 20: '$100,000', 26: '$200,000', 
    22: '$300,000', 17: '$400,000', 8: '$500,000', 23: '$750,000', 7: '$1,000,000'
}
```

This dictionary maps the case numbers to their respective dollar amounts. It provides a convenient way to access and display the cases during the game.

The game's implementation revolves around two classes. The StandardGame class handles the creation and display of the game board, tracks opened cases, and calculates the banker's offer. The Offer class generates the banker's offer based on the expected value of the remaining dollar amounts. By applying a curve and a list of percentages to the expected value, the offer is calculated in a way that balances the player's chances and the banker's desire to minimize the payout.

Here's the code for the banker's offer formula:

```python
# Banker's offer formula 
def generate_offer(self, game_round, expected_value): 
    self.curve_values = [.21, .39, .52, .61, .66, .67, .68, .66, .61]
    self.offer = self.curve_values[game_round - 1] * expected_value
    if game_round > 0:
        self.offers_list.append(self.offer)
    return self.offer
```

This formula uses a list of curve values that correspond to each game round. The offer is calculated by multiplying the curve value of the current round with the expected value of the remaining cases. The offer is then saved in the `self.offer` variable and added to the `self.offers_list` for tracking purposes.

To display the remaining cases in rows,

 a binary search algorithm is used. The `show_cases` method sorts the remaining cases and slices the list to display two rows of cases.

```python
# Method that displays remaining cases and uses binary search to slice the list
def show_cases(self):
    lower_bound = 0
    upper_bound = len(self.remaining_cases)
    pivot = (lower_bound + upper_bound) // 2
    sorted_list = sorted(self.remaining_cases)
    print(*sorted_list[:pivot], sep=' | ')
    print(*sorted_list[pivot:], sep=' | ')
```

This method takes the remaining cases, sorts them, and then splits the sorted list into two halves. The first row of cases is printed using `*sorted_list[:pivot]` followed by a separator, and the second row is printed using `*sorted_list[pivot:]` also followed by a separator.

To run the game, follow these instructions:
1. Ensure you have Python 3.10 installed.
2. Clone the repository to your local machine.
3. Open the terminal and navigate to the project directory.
4. Run the command `python deal_or_no_deal.py` to start the game.

Enjoy playing Deal Or No Deal and test your luck and decision-making skills!