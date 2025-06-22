# examples/basic_usage.py
"""Basic usage example for path-comment-hook."""

# This is a simple demonstration file
print("Hello, this is a basic usage example!")


# Function example
def greet(name: str) -> str:
    """Return a greeting message for the given name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    result = greet("World")
    print(result)
