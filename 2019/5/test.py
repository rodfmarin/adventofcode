import math


def calculate_odds(max, ball_count):
    combinations = math.factorial(max)
    denominator = math.factorial(ball_count) * math.factorial(max - ball_count)

    return combinations / denominator


def main():

    print(calculate_odds(39, 5))

main()