import click

from thinglang import run


@click.command()
@click.argument('file', type=click.File('r'))
def thinglang(file):
    source = file.read()
    run(source)

if __name__ == '__main__':
    thinglang()