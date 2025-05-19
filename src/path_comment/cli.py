from __future__ import annotations
import sys
import typer   # already in your dev deps

app = typer.Typer(add_completion=False)

@app.callback(invoke_without_command=True)
def main(
    check: bool = typer.Option(
        False,
        "--check",
        help="Exit with non-zero status if files would be modified",
    )
) -> None:
    """
    Inject or verify a relative-path comment at the top of each file.
    (Real logic coming soon.)
    """
    # Temporary stub: always succeed
    typer.echo("path-comment hook stub: nothing to do (yet).")
    if check:
        sys.exit(0)


if __name__ == "__main__":
    main()  # pragma: no cover
