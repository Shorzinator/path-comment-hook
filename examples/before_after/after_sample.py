# examples/before_after/after_sample.py
"""Sample file showing code after path-comment-hook processing."""


def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width


def main() -> None:
    """Main function to demonstrate the calculation."""
    area = calculate_area(10, 5)
    print(f"The area is: {area}")


if __name__ == "__main__":
    main()
