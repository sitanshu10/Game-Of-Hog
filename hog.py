"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    roll_no=0
    outcome,return_val=0,0

    #counted_dice=make_test_dice(3,2,5,6,1)
    while roll_no<num_rolls:
        x=dice()
        if x==1 :
            return_val=x
        outcome=outcome+x
        roll_no+=1
    if return_val==1:
        return 1
    else:
        return outcome

    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    digit1=opponent_score//10
    digit2=opponent_score%10
    if digit1>digit2:
        return digit1+1
    else:
        return digit2+1
    # END PROBLEM 2

def is_prime(number):
    #assert type(number)== int
    #assert number > 1
    if number==1 or number==0:
       return False
    i=2
    while i<number:
        if number%i==0:
            return False
        i+=1
    return True

def next_prime(number):
    i=number
    Flag=False
    while Flag==False:
        i += 1
        Flag=is_prime(i)
    return i

# Write your prime functions here!

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if num_rolls==0 :
        score=free_bacon(opponent_score)
    else:
        score=roll_dice(num_rolls,dice)
    if is_prime(score):
        score=next_prime(score)
    return score

    # END PROBLEM 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).
    """
    # BEGIN PROBLEM 3
    if (score+opponent_score)%7==0 :
        return four_sided
    else :
        return six_sided
    # END PROBLEM 3

def max_dice(score, opponent_score):
    """Return the maximum number of dice the current player can roll. The
    current player can roll at most 10 dice unless the sum of SCORE and
    OPPONENT_SCORE ends in a 7, in which case the player can roll at most 1.
    """
    # BEGIN PROBLEM 3
    if (score+opponent_score)%10==7:
        return 1
    else :
        return 10
    # END PROBLEM 3


def is_swap(score):
    """Returns whether the SCORE contains only one unique digit, such as 22.
    """
    # BEGIN PROBLEM 4
    if score<10:
        return True
    elif score<100:
        if score//10==score%10 :
            return True
    elif score>=100 :
        units=score%10
        tens=(score//10)%10
        hundreds=score//100
        if units==tens and tens==hundreds:
            return True
    return False

    # END PROBLEM 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    # score=score0                                  # score refers to current players score
    # strategy=strategy0
    # score_opp=score1
    while score0<goal and score1<goal :


        if player==0:
            Dice_type=select_dice(score0,score1)

            dice_count= max_dice(score0,score1)           # max_dice returns 1 or 10
            if dice_count==1 and strategy0(score0,score1) > 1:
                no_of_rolls=1
            else:
                no_of_rolls= strategy0(score0,score1)     #no_of_rolls0=strategy0(score0,score1)

            outcome=take_turn(no_of_rolls,score1,Dice_type)
            score0+=outcome

            if is_swap(score0):                            # swap scores of 1 ,2
                temp=score0
                score0=score1
                score1=temp


        elif player==1:
             dice_count= max_dice(score1,score0)           # max_dice returns 1 or 10
             if dice_count==1 and strategy1(score1,score0) > 1:
                 no_of_rolls=1
             else:
                 no_of_rolls=strategy1(score1,score0)        #no_of_rolls0=strategy0(score0,score1)
             Dice_type=select_dice(score1,score0)         #Dice_type=select_dice(score0,score1)
             outcome=take_turn(no_of_rolls,score0,Dice_type)
             score1+=outcome


             if is_swap(score1):                            # swap scores of 1 ,2
                temp=score1
                score1=score0
                score0=temp


        player=other(player)
    return score0, score1




    #Dice_type1=select_dice(score1,score0)



    # END PROBLEM 5



#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    @check_strategy
    def strategy(score, opponent_score):
        return n

    return strategy

def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid strategy
    output. All strategy outputs must be non-negative integers less than or
    equal to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'

def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy retuns an invalid
    output.

    >>> always_roll_5 = always_roll(5)
    >>> always_roll_5 == check_strategy(always_roll_5)
    True
    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> fail_15_20 == check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (invalid number of rolls)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> fail_102_115 == check_strategy(fail_102_115)
    True
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    i=0
    while i<=goal :
        j=0
        while j<=goal:
            num_rolls=strategy(i,j)
            check=check_strategy_roll(i,j,num_rolls)
            j+=1
        i+=1

    # END PROBLEM 6
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    def average_value(*args):
        i=1
        result=0
        while i<=num_samples:
            result=result+fn(*args)
            i+=1
        avg=result/num_samples
        return avg
    return average_value
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    i=1
    maxavg=0
    dice_no=1
    while i<=10:
        #dice=make_test_dice(i)
        avg_func=make_averaged(roll_dice,num_samples)
        avg=avg_func(i,dice)
        if avg==maxavg:
            if i<dice_no:
                dice_no=i
        elif avg>maxavg:
            maxavg=avg
            dice_no=i
        i+=1
    return dice_no

    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

@check_strategy
def bacon_strategy(score, opponent_score, margin=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    bacon_score=free_bacon(opponent_score)
    if is_prime(bacon_score):
        bacon_score=next_prime(bacon_score)
    return 0 if bacon_score>=margin else num_rolls # Replace this statement
    # END PROBLEM 9


@check_strategy
def swap_strategy(score, opponent_score, margin=5, num_rolls=6):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points and doesn't trigger a
    swap. Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    #if opponent_score>score:
    bacon_score=free_bacon(opponent_score)
    if is_prime(bacon_score):
        bacon_score=next_prime(bacon_score)
    if is_swap(bacon_score+score) and (bacon_score+score)<opponent_score:
        return 0

    if bacon_score>=margin and is_swap(bacon_score+score)==False:
        return 0
    return num_rolls

    # END PROBLEM 10



@check_strategy
def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    swap_strategy has been called to check it for different margin score.

    If the score of the player>90 and opponent_score>77 then if he rolls 0 dice
    he can score 100.
    If the player needs 1 point to swap scores then he can roll
    10 dice to get either pig out or a good score with 10 dice.
    Try to create a hog tied for opponent by taking a free_bacon.
    If the score of the player is >88 then check his free_bacon
    if it is equal to 11 then he can roll 0 dice to score 100.


    """
    # BEGIN PROBLEM 10


    return swap_strategy(score,opponent_score,8)
    #return swap_strategy(score,opponent_score,9,7)
    #return swap_strategy(score,opponent_score,9,9)
    bacon_score=free_bacon(opponent_score)
    if score>90 and opponent_score>77 :
        return 0
    if score>88 and bacon_score==11:
        return 0

    if is_swap(score+1) and opponent_score>score:
        return 10


    if is_prime(bacon_score):
        bacon_score=next_prime(bacon_score)
    scr=score+bacon_score
    if (scr+opponent_score)%7==0:
        return 0
    if (score+opponent_score)%7==0 :
        return 1
    if (scr+opponent_score)%10==7:
        return 0
    if is_swap(scr) and opponent_score<score:
        return 7

    if max_dice(score+opponent_score)==1:
        x=free_bacon(opponent_score)
        if x>6:
            return 0
    
    return 7
    # END PROBLEM 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
