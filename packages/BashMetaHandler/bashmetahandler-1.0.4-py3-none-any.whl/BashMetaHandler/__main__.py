"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> int:
    """Main testing function.

    Returns:
        int: return 0 when finished properly
    """
    print("BashMetaHandler tested")
    return 0


if __name__ == "__main__":
    main(prog_name="BashMetaHandler")  # pragma: no cover
