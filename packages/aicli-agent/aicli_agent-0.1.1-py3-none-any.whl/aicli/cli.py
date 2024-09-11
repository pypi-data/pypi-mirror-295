import click
import rich

from aicli.agent import agent


@click.command()
@click.argument("query", required=False)
def cli(query):
    if not query:
        print(">>> :")
        query = input()

    result = agent.user_input(query)
    print("\n" * 3)
    rich.print(result)


if __name__ == "__main__":
    cli()
