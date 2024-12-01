from time import perf_counter as pfc


def read_puzzle(filename):
    """Reads the puzzle input from a file and returns it as a list of strings."""
    with open(filename) as file:
        return [line.strip() for line in file]


def solve_part_1(puzzle):
    """Solves part 1 by calculating the total of all distances."""
    distances = calculate_distances(puzzle)
    return sum(distances)


def solve_part_2(puzzle):
    """Solves part 2 by calculating the total similarity scores."""
    similarity_scores = calculate_similarity_scores(puzzle)
    return sum(similarity_scores)


def calculate_distances(puzzle):
    """
    Calculates the absolute differences between corresponding numbers
    from two lists (left and right) in the puzzle.
    """
    left, right = split_puzzle(puzzle)

    # Convert the left and right lists from strings to integers
    left = [int(num) for num in left]
    right = [int(num) for num in right]

    # Sort the numbers to pair them in ascending order
    left_sorted = sorted(left)
    right_sorted = sorted(right)

    # Calculate the absolute differences
    differences = []
    for i in range(len(left_sorted)):
        differences.append(abs(left_sorted[i] - right_sorted[i]))

    return differences


def calculate_similarity_scores(puzzle):
    """
    Calculates similarity scores by counting occurrences of numbers
    in the right list and multiplying them with corresponding numbers
    in the left list.
    """
    left, right = split_puzzle(puzzle)

    # Convert the left and right lists from strings to integers
    left = [int(num) for num in left]
    right = [int(num) for num in right]

    # Count how many times each number appears in the right list
    right_counts = {}
    for num in right:
        if num in right_counts:
            right_counts[num] += 1
        else:
            right_counts[num] = 1

    # Calculate scores for the left list using the counts from the right
    scores = []
    for num in left:
        count = right_counts.get(num, 0)  # Default to 0 if the number is not in right
        scores.append(count * num)

    return scores


def split_puzzle(puzzle):
    """
    Splits the puzzle input into two separate lists: left and right.
    Each line in the puzzle contains two numbers, separated by a space.
    """
    left = []
    right = []
    for line in puzzle:
        parts = line.split()  # Split the line into two parts
        left.append(parts[0])  # Add the first number to the left list
        right.append(parts[1])  # Add the second number to the right list
    return left, right


if __name__ == "__main__":
    # Read the puzzle input from a file
    puzzle = read_puzzle("../day01_input.txt")

    # Solve part 1 and print the result
    start = pfc()
    result1 = solve_part_1(puzzle)
    print(f"Part 1: {result1} ({pfc() - start:.4f}s)")

    # Solve part 2 and print the result
    start = pfc()
    result2 = solve_part_2(puzzle)
    print(f"Part 2: {result2} ({pfc() - start:.4f}s)")