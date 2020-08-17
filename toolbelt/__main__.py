import click


@click.command()
@click.argument("name", default="world")
def main(name):
    """quick demo"""
    click.echo(f"hello, {name}")


if __name__ == "__main__":
    main()
# TODO clean this
# check perf here
# minor wording
# check perf here
# off-by-one, fixed
# left a note for myself
