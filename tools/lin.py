from math import gcd


def solve_linear_system_manual(ax, bx, ay, by, dx, dy):
    # Step 1: Compute determinant
    det = ax * by - ay * bx
    if det == 0:
        a, b = (dx // ax, 0) if ax > bx else (0, dy // by)
        return (a, b) if a * ax + b * bx == dx and a * ay + b * by == dy else None


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
ax, bx, ay, by = 2, 1, 2, 1
dx, dy = 50, 51

a, b = solve_linear_system_manual(ax, bx, ay, by, dx, dy)
print(f"Solution: a = {a}, b = {b}")
