from math import gcd


def solve_linear_system_manual(ax, bx, ay, by, dx, dy):
    # Step 1: Compute determinant
    det = ax * by - ay * bx
    if det == 0:
        raise ValueError("No unique solution exists (determinant is zero).")

    # Step 2: Check divisibility
    num_a = dx * by - dy * bx
    num_b = dy * ax - dx * ay

    if num_a % det != 0 or num_b % det != 0:
        raise ValueError("No integer solution exists.")

    # Step 3: Compute integer solutions
    a = num_a // det
    b = num_b // det

    return a, b


# Example usage
ax, bx, ay, by = 94, 22, 34, 67
dx, dy = 8400, 5400

a, b = solve_linear_system_manual(ax, bx, ay, by, dx, dy)
print(f"Solution: a = {a}, b = {b}")
