import click

from aicli.agent import agent


@click.command()
@click.argument("query", required=False)
def cli(query):
    """AI CLI 助手"""
    if not query:
        print("请输入您的查询:")
        query = input()

    result = agent.user_input(query)
    click.echo(result)


if __name__ == "__main__":
    cli()
