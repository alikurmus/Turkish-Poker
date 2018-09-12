"""
This is a script that will give you the maximum amount to bet with a given
hand in Turkish poker

It doesn't run with any parameters

When it is run it will give instructions about how much to bet with the given
hand, game stage, and pot.

If the games at pre-draw stage it will also give the cards to discard.
 """



print("This program will ask you the stage of the game, pot, and your hand "
      "and will recommend the best strategy")

print("Enter hand in the form of numeral suit with no" 
                        "spaces. Acceptable numerals are (7,8,9,T,J,Q,K,"
                        "A) and acceptable suites are clubs, spades, "
                        "diamonds, hearts (C,S,D,"
                        "H). A valid "
                        "hand will look like: AH7CTDKS9S")

# Unicode symbols for Clubs, Spades, Diamonds, Hearts
L_SUIT_LIST = (u"\u2663", u"\u2660", u"\u2666", u"\u2665")
# Ace is also at the beginning to display the hand correctly when we use the
# Ace as a six in straights
L_NUMERAL_LIST = ("Ace", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace")
D_NUMERAL_LIST = ("A", "7", "8", "9", "T", "J", "Q", "K", "A")
D_SUIT_LIST = ("C", "S", "D", "H")
SUIT_LIST = (0, 1, 2, 3)  # Clubs, Spades, Diamonds, Hearts
NUMERAL_LIST = (1, 2, 3, 4, 5, 6, 7, 8)
T_NUMERAL_LIST = ("7", "8", "9", "T", "J", "Q", "K", "A")
T_SUIT_LIST = ("C", "S", "D", "H") # Clubs, Spades, Diamonds, Hearts

class Card:
    def __init__(self, numeral, suit):
        self.numeral = numeral
        self.suit = suit
        self.sort_order = 0
        self.card = self.numeral, self.suit, self.sort_order

    def __repr__(self):
        return D_NUMERAL_LIST[self.numeral] + L_SUIT_LIST[self.suit]


class Hand:
    def __init__(self, card_list):
        # Cards in hand, a list of cards.
        self.card_list = card_list
        # Cards in hand after draw, a list of cards.
        self.final_card_list = []
        # Indices of cards to be discarded (int).
        self.discard_list = []
        # Human readable form of initial hand's value, like Three 8s.
        self.desc = ""
        # Data analysis output level 1, like "Pair" for a pair of Aces.
        self.desc_mr1 = ""
        # Data analysis output level 2, like "A" for a pair of Aces.
        self.desc_mr2 = ""
        # Data analysis output level 3, like "7" for a two pair of Aces over 7s.
        self.desc_mr3 = ""
        # Human readable form of final hand's value, like Three 8s.
        self.final_desc = ""
        # Like self.desc_mr1 but for final value of the hand.
        self.final_desc_mr1 = ""
        # Like self.desc_mr2 but for final value of the hand.
        self.final_desc_mr2 = ""
        # Like self.desc_mr3 but for final value of the hand.
        self.final_desc_mr3 = ""
        #  Initial numeric value of rank. Bigger is better.
        self.value = 0
        #  Final numeric value of rank. Bigger is better.
        self.final_value = 0
        # Whether the hand wins the game
        self.winner = False

    def __repr__(self):
        pretty_hand1 = "".join([str(x) for x in self.card_list])
        pretty_value1 = (self.desc + " (" + "{:.6f}".format(self.value) + ")")
        pretty_discard = "D: " + "".join([str(x) for x in self.card_list if
                                          self.card_list.index(
                                              x) in self.discard_list])
        pretty_hand2 = "".join([str(x) for x in self.final_card_list])
        pretty_value2 = (self.final_desc + " (" + (
            "{:.6f}".format(self.final_value)) + ")")
        if self.winner:
            pretty_winner = "Winner!"
        else:
            pretty_winner = ""
        rep = " ".join(
            [pretty_hand1, pretty_value1, pretty_discard, "->", pretty_hand2,
             pretty_value2, pretty_winner])
        return rep

def evaluate(self):  # returns a list of cards to be discarded

        # Utility function that takes a list of numerals and returns a list
        # containing the indices of these numerals
        # in the hand.
        # Assumes that each numeral in the hand is unique.
        def numeral_to_idx(numerals):
            idx_list = []
            for c in self.card_list:
                if c.numeral in numerals:
                    idx_list.append(self.card_list.index(c))
            return idx_list

        # Sort the hand by numeral value in descending order.
        # By using the operator.attrgetter method, we are going to sort the
        # card objects by one of their attributes
        # In this case, it is the numeral attribute.
        # TODO: Can we construct the hand class (and maybe card class) so it
        # sorts naturally?
        key_value_sort = operator.attrgetter("numeral")
        self.card_list.sort(key=key_value_sort, reverse=True)

        # We are going to use two dictionaries to count the occurrences of each
        # numeral and suit in the hand. The reason we are using
        # collections.defaultdict instead of a regular dictionary is that
        # collections.defaultdict initiates each key with a default value
        # (0 for ints in our case). We could have used a regular dictionary and
        # reference it by using the get method and a default value
        # But collections.defaultdict makes the rest of the code more
        # readable by using it here just once.
        numeral_dict = collections.defaultdict(int)
        suit_dict = collections.defaultdict(int)
        for my_card in self.card_list:
            numeral_dict[my_card.numeral] += 1
            suit_dict[my_card.suit] += 1

        # Pair
        # If we have 4 different numeral values in the hand that means we have
        # two of a certain numeral value therefore we have a pair.
        if len(numeral_dict) == 4:
            # We are trying to find which numeral is the pair. This looks
            # obscure but here is how to unpack it. The whole expression is
            # choosing an element from a list. The first part specifies the
            # list. It gets the keys of the numeral_dict by using the .keys
            # method of dictionaries and turns this into a list by the first
            # list statement. The second part is the index. The index part
            # first gets the values of the numeral_dict by using the .values
            # method of dictionaries and again turns this into a list. It then
            # uses a list's index method to find the index of the value that
            # is equal to 2 (because we are looking at a dictionary count of 2).
            pair = list(numeral_dict.keys())[
                list(numeral_dict.values()).index(2)]

            # The hand is already sorted in descending order by numeral value.
            # What we want is to put the pair first (since it is the most
            # significant factor in the value of the hand
            # and then put the rest of the cards in descending order.
            # So A K 9 9 7 looks like 9 9 A K 7.
            # This is important as well because we are going to use the
            # sorted values of these cards to distinguish
            # between two hands with the same pairs. Like 9 9 A K 7 and 9 9 Q
            #  J 8.
            for index, c in enumerate(self.card_list):
                if c.numeral == pair:
                    # 10 is large number that will make sure that the pair
                    # will be sorted before the high cards
                    # (the highest high card will have an index value of 5).
                    self.card_list[index].sort_order = 10
                else:
                    # We subtract the index from 5 because in initial reverse
                    # sorting by numeral the indices of bigger
                    # numerals became smaller.
                    self.card_list[index].sort_order = 5 - index

            # We sort the hand again, this time using the sort order
            # attribute we have just populated.
            key_value_sort = operator.attrgetter("sort_order")
            self.card_list.sort(key=key_value_sort, reverse=True)

            # Since we know this is a pair, and the hand is sorted by putting
            # the pair first, the rest of the cards are discardable.
            self.discard_list = [2, 3, 4]

            # Descriptions
            self.desc = "A pair of " + str(L_NUMERAL_LIST[pair]) + "s"
            self.desc_mr1 = "Pair"
            self.desc_mr2 = str(D_NUMERAL_LIST[pair])
            # Numeral list starts with an Ace we use 3 because we want the
            # numeral of third card. That normally would be 2, but since we
            # have the extra Ace, everything is shifted.
            self.desc_mr3 = str(D_NUMERAL_LIST[self.card_list[2].numeral])

            # This is the numeric value:
            # pair's numeral + 3 decimals + 1 decimal for
            # the suit of the largest unpaired card:
            # (1.2340 to 8.7653)
            self.value = (
                        pair + self.card_list[2].numeral / 10 + self.card_list[
                    3].numeral / 100 + self.card_list[4].numeral / 1000 +
                        self.card_list[2].suit / 10000)

        # Two pair or 3-of-a-kind
        elif len(numeral_dict) == 3:
            # 3-of-a-kind
            if 3 in numeral_dict.values():
                trips = list(numeral_dict.keys())[
                    list(numeral_dict.values()).index(3)]
                for index, c in enumerate(self.card_list):
                    if c.numeral == trips:
                        self.card_list[index].sort_order = 10
                    else:
                        self.card_list[index].sort_order = 5 - index
                key_value_sort = operator.attrgetter("sort_order")
                self.card_list.sort(key=key_value_sort, reverse=True)
                self.discard_list = [3, 4]

                # Descriptions
                self.desc = "Three " + str(L_NUMERAL_LIST[trips]) + "s"
                self.desc_mr1 = "Trips"
                self.desc_mr2 = str(D_NUMERAL_LIST[trips])
                self.desc_mr3 = str(D_NUMERAL_LIST[self.card_list[3].numeral])

                # Three of a kind's numeral * 100
                # (100 to 800):
                self.value = trips * 100
            else:
                # Two pairs
                # We will first find the first pair (list.index returns the
                # first match).
                first_pair = list(numeral_dict.keys())[
                    list(numeral_dict.values()).index(2)]

                # We will then reset the numeral count of the first pair to 0
                # so that we can find the second pair.
                numeral_dict[first_pair] = 0

                # We now look for the second pair. Since we reset the numeral
                # count of first pair's numeral count to 0, we only have a
                # single value 2 in the dict.
                second_pair = list(numeral_dict.keys())[
                    list(numeral_dict.values()).index(2)]

                # Assign the bigger of the pairs to big_pair and the other to
                # small_pair.
                if first_pair > second_pair:
                    big_pair, small_pair = first_pair, second_pair
                else:
                    big_pair, small_pair = second_pair, first_pair

                # We want to sort the hand so that it looks like Big Pair,
                # Small Pair, Unpaired card.
                for index, c in enumerate(self.card_list):
                    if c.numeral == big_pair:
                        self.card_list[index].sort_order = 10
                    elif c.numeral == small_pair:
                        self.card_list[index].sort_order = 9
                    else:
                        self.card_list[index].sort_order = 5 - index

                # We sort the hand again, this time using the sort order
                # attribute we have just populated.
                key_value_sort = operator.attrgetter("sort_order")
                self.card_list.sort(key=key_value_sort, reverse=True)

                # Discards: We only want to discard the unpaired card
                self.discard_list = [4]

                # Descriptions
                self.desc = "Two Pairs: " + str(
                    L_NUMERAL_LIST[big_pair]) + "s over " + str(
                    L_NUMERAL_LIST[small_pair]) + "s"
                self.desc_mr1 = "Two Pairs"
                self.desc_mr2 = str(D_NUMERAL_LIST[big_pair])
                self.desc_mr3 = str(D_NUMERAL_LIST[small_pair])

                # Larger pair's numeral * 10 + smaller pair's numeral +
                # decimal + 1 decimal for the suit of the
                # unpaired card.
                # (21.30 to 87.63)
                self.value = (big_pair * 10 + small_pair + self.card_list[
                    4].numeral / 10 + self.card_list[4].suit / 100)

        # Full house or 4-of-a-kind
        elif len(numeral_dict) == 2:
            # Full house
            # There will be a pair in any full house so we are testing for that.
            if 2 in numeral_dict.values():
                # We want the numeral value for the trips the value of the
                # pair will not change the ranking since trips part uniquely
                # sorts each hand.
                trips = list(numeral_dict.keys())[
                    list(numeral_dict.values()).index(3)]
                pair = list(numeral_dict.keys())[
                    list(numeral_dict.values()).index(2)]
                for index, c in enumerate(self.card_list):
                    if c.numeral == trips:
                        self.card_list[index].sort_order = 10
                    else:
                        # Cards that are not port of the trips are part of the
                        # pair so we can assign them the same sort_order value.
                        self.card_list[index].sort_order = 5
                key_value_sort = operator.attrgetter("sort_order")
                self.card_list.sort(key=key_value_sort, reverse=True)

                # Nothing to discard
                self.discard_list = []

                # Descriptions
                self.desc = "Full House " + str(L_NUMERAL_LIST[trips]) + "s"
                self.desc_mr1 = "Full House"
                self.desc_mr2 = str(D_NUMERAL_LIST[trips])
                self.desc_mr3 = str(D_NUMERAL_LIST[pair])

                # Three of a kind's numeral * 1000 (pair's numeral is not
                # necessary).
                # (1000 to 8000)
                self.value = trips * 1000

            else:
                # It's a four of a kind
                four = list(numeral_dict.keys())[
                    list(numeral_dict.values()).index(4)]
                for index, c in enumerate(self.card_list):
                    if c.numeral == four:
                        self.card_list[index].sort_order = 10
                    else:
                        self.card_list[index].sort_order = 5
                key_value_sort = operator.attrgetter("sort_order")
                self.card_list.sort(key=key_value_sort, reverse=True)

                # Nothing to discard but we may want to discard a card
                # occasionally to give the signal that we have a
                # two pair rather than a straight, full house or flush.
                if random.choice([True, False]):
                    self.discard_list = []
                else:
                    self.discard_list = [4]

                # Descriptions
                self.desc = "Four of a kind " + str(L_NUMERAL_LIST[four]) + "s"
                self.desc_mr1 = "Four of a kind"
                self.desc_mr2 = str(D_NUMERAL_LIST[four])
                self.desc_mr3 = str(D_NUMERAL_LIST[self.card_list[4].numeral])

                # numeral value of the four of a kind * 10000
                # (10000 to 80000):
                self.value = four * 10000

        else:

            # Flushes and straights
            straight, flush = False, False
            ace_low = False

            # Check for a flush, that is if all the cards have the same suit.
            if len(suit_dict) == 1:
                flush = True

            # Check for a straight, that is if the range between the minimum
            # and maximum values is 4.
            # This works because we have already checked whether we had any
            # numerals with a count more than 1 before where we checked for
            # pairs etc.
            min_numeral = self.card_list[4].numeral
            max_numeral = self.card_list[0].numeral
            if int(max_numeral) - int(min_numeral) == 4:
                straight = True

            # Ace can be low
            low_straight = {8, 4, 3, 2, 1}
            if len(set(numeral_dict.keys()).difference(low_straight)) == 0:
                straight = True
                ace_low = True
                # Since Ace is used as a six, the high card is a T, in idx 4
                # in D_NUMERAL_LIST
                high = str(D_NUMERAL_LIST[4])
                # We are using the Ace as a 6, so we change its value from 8
                # to 0 to sort correctly.
                self.card_list[0].numeral = 0
                # We reorder the deck to take into account the new value of
                # the Ace.
                self.card_list.sort(key=key_value_sort, reverse=True)

            # Everything is already sorted and there are no cards to discard.
            self.discard_list = []

            if straight and not flush:
                # The suit of the T matters because if there are two straights
                # that begin with the same numeral the suit of the T decides the
                # winner.
                # Each straight must have a T. So find the card with the numeral
                # value 4 (which is the numeral value of T).
                for c in self.card_list:
                    if c.numeral == 4:
                        t_card = c
                        # Find the suit of the T
                        t_card_suit = t_card.suit

                # Descriptions
                self.desc_mr1 = "Straight"
                self.desc_mr3 = str(D_SUIT_LIST[t_card_suit])
                if not ace_low:
                    self.desc = "Straight " + str(
                        L_NUMERAL_LIST[max_numeral]) + " high"
                    self.desc_mr2 = str(D_NUMERAL_LIST[max_numeral])
                else:
                    self.desc = "Straight Ace Low"
                    self.desc_mr2 = high

                # 90 + 5 decimals + 1 decimal for the suite of the T
                # (90.432100 to 90.876543):
                self.value = (90 + self.card_list[0].numeral / 10 +
                              self.card_list[1].numeral / 100 + self.card_list[
                                  2].numeral / 1000 + self.card_list[
                                  3].numeral / 10000 + self.card_list[
                                  4].numeral / 100000 + t_card_suit / 1000000)
                # Correct the value of the Ace for the final evaluation
                if ace_low:
                    # We change the numeral value of the Ace back to 8 so
                    # that final_evaluation works as expected. We do this
                    # after we calculate the hand value because as we
                    # calculate, we are using the Ace as a 6 so it has a
                    # numeral value of 0.
                    self.card_list[4].numeral = 8

            elif flush and not straight:
                # The suit of the flush matters because if there are two
                # flushes with the same numerals the suit of the flush decides
                # the winner. Since all cards in the flush have the same suit,
                # we can look at any card in the hand.
                flush_suit = self.card_list[0].suit

                # Descriptions
                self.desc = "Flush " + str(
                    L_NUMERAL_LIST[max_numeral]) + " high"
                self.desc_mr1 = "Flush"
                self.desc_mr2 = str(D_NUMERAL_LIST[max_numeral])
                self.desc_mr3 = str(D_SUIT_LIST[flush_suit])

                # 9000 + 5 decimals + 1 decimal for the suite
                # (9000.643210 to 9000.876533).
                self.value = (9000 + self.card_list[0].numeral / 10 +
                              self.card_list[1].numeral / 100 + self.card_list[
                                  2].numeral / 1000 + self.card_list[
                                  3].numeral / 10000 + self.card_list[
                                  4].numeral / 100000 + flush_suit / 1000000)

            elif flush and straight:
                # The suit of the straight flush matters because if there are
                # two that start with the same numeral the suit of the
                # straight flush decides the winner.
                # Since all cards in the straight flush have the same suit,
                # we can look at any card in the hand.
                flush_suit = self.card_list[0].suit

                # Descriptions
                self.desc_mr1 = "Straight Flush"
                self.desc_mr3 = str(D_SUIT_LIST[flush_suit])
                if not ace_low:
                    self.desc = "Straight Flush " + str(
                        L_NUMERAL_LIST[max_numeral]) + " high"
                    self.desc_mr2 = str(D_NUMERAL_LIST[max_numeral])
                else:
                    self.desc = "Straight Flush Ace Low"
                    self.desc_mr2 = high
                # 100000 + 5 decimals + 1 decimal for the suite
                # (100000.432100 to 100000.876533)
                self.value = (100000 + self.card_list[0].numeral / 10 +
                              self.card_list[1].numeral / 100 + self.card_list[
                                  2].numeral / 1000 + self.card_list[
                                  3].numeral / 10000 + self.card_list[
                                  4].numeral / 100000 + flush_suit / 1000000)
                if ace_low:
                    # We change the numeral value of the Ace back to 8 so
                    # that final_evaluation works as expected. We do this
                    # after we calculate the hand value because as we
                    # calculate, we are using the Ace as a 6 so it has a
                    # numeral value of 0.
                    self.card_list[4].numeral = 8

            else:

                # Card High
                # The suit of the highest card matters because if there are two
                # hands with the same numerals the suit of the highest card
                # decides the winner. The highest card is in index 0 since
                # the hand is sorted.
                high_card_suit = self.card_list[0].suit

                # 0 + 5 decimals + 1 decimal for the suite of the highest
                # card (0.12346 to 0.87653)
                self.value = self.card_list[0].numeral / 10 + self.card_list[
                    1].numeral / 100 + self.card_list[2].numeral / 1000 + \
                             self.card_list[3].numeral / 10000 + self.card_list[
                                 4].numeral / 100000 + high_card_suit / 1000000

                # The other ranks are clearly ordered so when a hand matches
                # multiple categories (such as all three of a kinds are also
                # pairs technically) we only need to consider the highest rank
                # and discard accordingly. High cards are problematic because
                # they offer multiple ways of drawing cards so which cards to
                # discard is not obvious. We try to get around that by making a
                # dictionary with keys that correspond to different kinds of
                # high card potentials (let's call them situations) and check
                # the hand against each. If the hand matches one of the
                # situation than we flag that situation and indicate which
                # cards to discard to arrive at that situation. The situations
                # are also semi-objectively valued in terms of winning
                # potential. That will make it easier to decide which
                # situation to aim for when it comes to draw cards.
                #
                # Potential high card scenarios explained:
                # One Carders:
                # - Full open ended straight: like 8 9 T J (we can make a
                #   straight by getting a 7 or Q)
                # - Half open ended straight: J Q K A or A 7 8 9 (only a T in
                #   both cases would make a straight)
                #   (same probability of improvement as Gut shot straight,
                #   so disregard)
                # - Gut shot straight: like T J K A (only a queen would make a
                #   straight)
                # - Almost flush: four cards with the same suit
                # - Almost straight flush: almost flush and (one of the
                #   straights) (but this gets complicated because the best
                #   potential straight may not be compatible with a flush,
                #   in that case most reasonable players would go for the
                #   flush, so we can ignore this case)
                #
                # Two Carders:
                # - Full open ended long straight: like 8 9 T  (we can make a
                #   straight by getting a A 7; J Q; or 7 J)
                # - Half open ended long straight: Q K A or A 7 8  (we can make
                #   a straight by getting a T J or 9 T)
                #   (same potential as Half gut shot long straight so disregard)
                # - Half gut shot long straight: like T J K (only a Q 9 or Q A
                #   will make a straight)
                # - Full gut shot long straight: like T J A (only a Q, K would
                #   make a straight)
                # - Long shot flush: three cards with the same suit
                # - Long shot straight flush: Long shot flush and (one of the
                #   straights)
                #   (see Almost straight flush above, ignoring this as well)
                #
                # Three carders:
                # All hands are potentially straights if we draw three cards
                # to them. So disregarding those.
                # - Hail Mary flush: two cards of the same suit
                # - Hail Mary straight flush: two cards of the same suit that
                #   are separated by 4
                #   (not necessary since all hands are potentially straights,
                #   all potential flushes are also potential straight flushes)
                # - Two high cards: Just keeping the two highest cards
                #
                # Four carders:
                # - Keep the highest
                # - Keep the highest non A or K
                # (This is a distinction in Turkish poker because there is a
                # minimum of KK required to open a game so in real game
                # situations if the game is opened the probability of having a
                # lower number of Kings and Aces to draw from is not random).

                # Key level 2 description:
                # 0-Have it? (bool),
                # 1-potential value higher is better (int),
                # 3- position of cards to discard initially empty (list).

                high_card_dict = {"Almost flush":                  [False, 80,
                                                                    []],
                                  "Full open ended straight":      [False, 70,
                                                                    []],
                                  "Long shot flush":               [False, 60,
                                                                    []],
                                  "Keep the highest non A or K":   [False, 55,
                                                                    []],
                                  "Keep the highest":              [False, 50,
                                                                    []],
                                  "Full open ended long straight": [False, 46,
                                                                    []],
                                  "Half gut shot long straight":   [False, 43,
                                                                    []],
                                  "Full gut shot long straight":   [False, 40,
                                                                    []],
                                  "Hail Mary flush":               [False, 30,
                                                                    []],
                                  "Two high cards":                [False, 20,
                                                                    []],
                                  "Gut shot straight":             [False, 10,
                                                                    []], }

                # Going for flushes, we prefer a once carder flush to a two
                # carder and and a two carder to three carder so we check for
                # them in order of preference

                # Almost Flush
                if max(suit_dict.values()) == 4:
                    high_card_dict["Almost flush"][0] = True
                    suit_to_discard = list(suit_dict.keys())[
                        list(suit_dict.values()).index(1)]
                    for i, my_card in enumerate(self.card_list):
                        if my_card.suit == suit_to_discard:
                            high_card_dict["Almost flush"][2].append(i)
                            break
                # Long shot flush
                elif max(suit_dict.values()) == 3:
                    high_card_dict["Long shot flush"][0] = True
                    suit_to_keep = list(suit_dict.keys())[
                        list(suit_dict.values()).index(3)]
                    for i, my_card in enumerate(self.card_list):
                        if my_card.suit != suit_to_keep:
                            high_card_dict["Long shot flush"][2].append(i)
                # Hail Mary flush
                elif max(suit_dict.values()) == 2:
                    high_card_dict["Hail Mary flush"][0] = True
                    # This always picks the suit with the highest card because
                    # cards are already sorted in descending order and we built
                    # the suit_dict by looking at each card in the sorted hand
                    # and adding its suit to the suit_dict dictionary. Normally
                    # the order of the keys in a dict is not guaranteed, but in
                    # Python 3.7 the preservation of the insert order in dicts
                    # is a standard feature per:
                    # https://mail.python.org/pipermail/python-dev/2017
                    # -December/151283.html
                    suit_to_keep = list(suit_dict.keys())[
                        list(suit_dict.values()).index(2)]
                    for i, my_card in enumerate(self.card_list):
                        if my_card.suit != suit_to_keep:
                            high_card_dict["Hail Mary flush"][2].append(i)

                # Going for straights

                # We will build a list of all possible straights to compare
                # against the cards in hand. The highest straight can begin with
                # a T (T J Q K A) so we start with the value of T, 4. The lowest
                # straight would be T 9 8 7 A where we use te Ace as a 6. So the
                # lowest straight starts with 0.
                #
                # There may be more than one potential full open and gut shot
                # straights. We just want to draw for the larger ones and we
                # will always prefer an open straight to a gut shot.

                # We will be doing lots of set operations with the keys of
                # the numeral_dict so we make a set of it here.
                numeral_dict_set = set(numeral_dict.keys())

                gut_shot_straight_count = 0
                open_ended_long_straight_count = 0
                half_gut_shot_long_straight_count = 0
                full_gut_shot_long_straight_count = 0

                # The Ace can be used as a 6 when making a straight,
                # so we add 0 to our hand (representing the 6).
                if 8 in numeral_dict_set:
                    numeral_dict_set.add(0)

                for low in (4, 3, 2, 1, 0):
                    potential_straight = set(range(low, low + 5))

                    # Set of cards that are in hand but not in the possible
                    # straight we are looking at. We will discard these.
                    to_be_discarded_cards = numeral_dict_set.difference(
                        potential_straight)

                    # We will keep the non-discarded cards (obviously,
                    # but this makes some of the code easier to read).
                    kept_cards = numeral_dict_set.difference(
                        to_be_discarded_cards)

                    # The range between the largest and smallest of kept
                    # cards will be useful in a couple of places.
                    kept_range = max(kept_cards) - min(kept_cards)

                    # We don't really have a 6 in the deck, so we need to to do
                    # some cleaning to account for that. If if we have a 0
                    # (card 6) in the kept cards it means we have a 8 in the
                    # discarded list which will make trouble for us because we
                    # will discard the real Ace that we are using as a 6. So we
                    # remove that. Similarly, if we have a 0 in the discarded
                    # cards, that is if we are not using Ace as a 6 we should
                    # remove it from the discarded cards because we don't really
                    # have a 6 in the deck and it will confuse the other
                    # routines.
                    if 0 in kept_cards:
                        to_be_discarded_cards.remove(8)
                    if 0 in to_be_discarded_cards:
                        to_be_discarded_cards.remove(0)

                    # If we are only one card short of a potential straight
                    # then we are in the one carder straight zone.
                    if len(kept_cards) == 4:
                        # test for open ended: max - min = 3 and 0 and 8 not
                        # in remaining cards because if they are
                        # that means one end is closed. We also check for the
                        #  open ended straight count so that we stop
                        # at the highest straight.

                        if (kept_range == 3) and (
                                not ((8 in kept_cards) or (0 in kept_cards))):
                            high_card_dict["Full open ended straight"][0] = True
                            # Find the index of the card to discard in the
                            # hand and add it to cards to be discarded list
                            # in the high_card_dict. The numeral of the card
                            # to discard is in to_be_discarded_cards
                            # and since we are only discarding one card,
                            # if we pop something from that set it will be
                            # the numeral of the card to be discarded.
                            high_card_dict["Full open ended straight"][
                                2].extend(numeral_to_idx(
                                list([to_be_discarded_cards.pop()])))

                            # Say we have K Q J T 7 evaluating for T,
                            # target A K Q J T, discard 7, open ended straight,
                            # waiting for A or 9.
                            # Same hand evaluating for 8, target Q J T 9 8,
                            # discard K 7, gut shot long  straight, waiting
                            # for 9 and 8.
                            # We don't want the  evaluation for 8 to happen
                            # because we have a  better hand with more
                            # chances to improve.
                            #
                            # But say we have A Q J T 9 evaluating for T, target
                            # A K Q J T, discard 9, gut shot straight, waiting
                            # for a K.
                            # Same hand evaluating for 9, target K Q J T 9,
                            # discard A, open ended straight, waiting for a
                            # K or 8. So if we broke when we found the gut
                            # shot straight, we would have missed the open
                            # ended straight.
                            #
                            # So we break on open ended straights but keep
                            # count for other possible straights to keep
                            # track to see if there has been anything better.
                            break

                        elif gut_shot_straight_count == 0:
                            high_card_dict["Gut shot straight"][0] = True
                            high_card_dict["Gut shot straight"][2].extend(
                                numeral_to_idx(
                                    list([to_be_discarded_cards.pop()])))
                            gut_shot_straight_count += 1

                    elif len(kept_cards) == 3:
                        # Test for open ended: max - min = 2 and 0 and 8 not in
                        # remaining cards because if they are that means one end
                        # is closed. We also don't want to try for a two carder
                        # straight if we already have a once carder straight.
                        # This would happen if we had a one carder straight that
                        # starts from a higher card but not a potential one
                        # carder starting from the current card.
                        if (kept_range == 2) and (
                        not ((8 in kept_cards) or (0 in kept_cards))) and ((
                                                                                   gut_shot_straight_count + open_ended_long_straight_count) == 0):
                            high_card_dict["Full open ended long straight"][
                                0] = True
                            high_card_dict["Full open ended long straight"][
                                2].extend(
                                numeral_to_idx(list(to_be_discarded_cards)))
                            open_ended_long_straight_count += 1

                        # Test for half open ended: max - min = 3 (because we
                        # need a card in the gut to make it open ended) and 0
                        # and 8 not in remaining cards because if they are
                        # that means one end is closed.
                        elif (kept_range == 3) and (
                        not ((8 in kept_cards) or (0 in kept_cards))) and ((
                                                                                   gut_shot_straight_count + open_ended_long_straight_count + half_gut_shot_long_straight_count) == 0):
                            high_card_dict["Half gut shot long straight"][
                                0] = True
                            high_card_dict["Half gut shot long straight"][
                                2].extend(
                                numeral_to_idx(list(to_be_discarded_cards)))
                            half_gut_shot_long_straight_count += 1
                        elif (
                                gut_shot_straight_count +
                                open_ended_long_straight_count +
                                half_gut_shot_long_straight_count +
                                full_gut_shot_long_straight_count) == 0:
                            high_card_dict["Full gut shot long straight"][
                                0] = True
                            high_card_dict["Full gut shot long straight"][
                                2].extend(
                                numeral_to_idx(list(to_be_discarded_cards)))
                            full_gut_shot_long_straight_count += 1

                # We nicely remove the 0 for the remaining evaluations.
                if 0 in numeral_dict_set:
                    numeral_dict_set.remove(0)

                # Everything else

                # Two high cards:
                # There are really no requirements for this, we just discard
                # the last 3 cards.

                high_card_dict["Two high cards"][0] = True
                high_card_dict["Two high cards"][2].extend([2, 3, 4])

                # Four carders
                # Keep the highest
                high_card_dict["Keep the highest"][0] = True
                high_card_dict["Keep the highest"][2].extend([1, 2, 3, 4])

                # Keep the highest non A or K
                high_card_dict["Keep the highest non A or K"][0] = True
                for high in [6, 5, 4, 3]:
                    if high in numeral_dict_set:
                        break
                to_be_discarded_cards = numeral_dict_set.difference({high})
                high_card_dict["Keep the highest non A or K"][2].extend(
                    numeral_to_idx(list(to_be_discarded_cards)))

                # Pick discard strategy:
                if high_card_dict["Almost flush"][0]:
                    self.discard_list = high_card_dict["Almost flush"][2]
                    short_desc = "(Almost flush)"
                elif high_card_dict["Full open ended straight"][0]:
                    self.discard_list = \
                    high_card_dict["Full open ended straight"][2]
                    short_desc = "(Full open ended straight)"
                elif high_card_dict["Long shot flush"][0]:
                    self.discard_list = high_card_dict["Long shot flush"][2]
                    short_desc = "(Long shot flush)"
                else:
                    remaining_hcs = []
                    for k in high_card_dict.keys():
                        if high_card_dict[k][0]:
                            remaining_hcs.append(k)
                    random.shuffle(remaining_hcs)
                    lucky_winner = remaining_hcs[0]
                    self.discard_list = high_card_dict[lucky_winner][2]
                    short_desc = "(" + lucky_winner + ")"

                # Descriptions
                self.desc = "High Card " + short_desc
                self.desc_mr1 = "High Card"
                self.desc_mr2 = short_desc
                self.desc_mr3 = str(D_NUMERAL_LIST[max_numeral])

        to_discarded_cart_pile = []
        for i, card in enumerate(self.card_list):
            # Add cards that are in the discard list to the return value so
            # it can be added to the deck's discard pile.
            if i in self.discard_list:
                to_discarded_cart_pile.append(card)
        return to_discarded_cart_pile


while True:
    stage = input("Enter stage of the game (pre-draw (1), post-draw(2) ): ")
    pot = int(input("Enter the pot"))
    user_hand_s = (input("Enter hand")).upper()

    if len(user_hand_s) != 10:
        print("Invalid hand")
        break

    else:
        user_numerals = list(user_hand_s[0:9:2])
        user_suits = list(user_hand_s[1:10:2])
        user_cards = list(zip(user_numerals,user_suits))
        card_list = []

        for card in user_cards:
            if card[0] in T_NUMERAL_LIST and card[1] in T_SUIT_LIST:
                card_numeral = T_NUMERAL_LIST.index(card[0]) + 1
                card_suit = T_SUIT_LIST.index(card[1])
                new_card = Card(card_numeral, card_suit)
                card_list.append(new_card)
            else:
                print("Invalid Hand")

                exit()

        user_hand = Hand(card_list)

        print(user_hand)





