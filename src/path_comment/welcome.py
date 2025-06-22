"""Welcome message for path-comment-hook installation."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def show_welcome() -> None:
    """Display the welcome ASCII art and installation message."""
    console = Console()

    # ASCII art
    ascii_art = """    /·\\
   /│·│\\    ┌─┐┌─┐┬ ┬
  / │·│ \\   ├─┘│  ├─┤
 /  │·│  >   ┴  └─┘┴ ┴
/___│·│___\\ path-comment-hook"""

    # Create a rich text object for styling
    art_text = Text(ascii_art, style="bold cyan")

    # Welcome message
    welcome_msg = Text.assemble(
        "\n🎉 ",
        ("Welcome to path-comment-hook!", "bold green"),
        " 🎉\n\n",
        "Thank you for installing path-comment-hook!\n",
        "Add file path headers to your source code for better navigation.\n\n",
        ("Quick Start:", "bold yellow"),
        "\n",
        "• Set up pre-commit: ",
        ("pip install pre-commit", "dim"),
        "\n• Add to .pre-commit-config.yaml\n",
        "• Run: ",
        ("pre-commit install", "dim"),
        "\n\n",
        ("Documentation:", "bold blue"),
        " https://shouryamaheshwari.github.io/path-comment-hook\n",
        ("Issues & Support:", "bold blue"),
        " https://github.com/shouryamaheshwari/path-comment-hook/issues\n\n",
        ("Happy coding! 🚀", "bold magenta"),
    )

    # Create panel with the art and message
    console.print(
        Panel(
            Text.assemble(art_text, "\n\n", welcome_msg),
            title="[bold green]Installation Complete[/bold green]",
            border_style="green",
            expand=False,
            padding=(1, 2),
        )
    )


if __name__ == "__main__":
    show_welcome()
