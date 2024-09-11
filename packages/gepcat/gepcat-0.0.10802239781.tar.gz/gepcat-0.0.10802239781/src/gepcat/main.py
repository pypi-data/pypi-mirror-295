import sys
import click
import os
import toml

from ._version import __version__

def show_all(file_txt):
    a = file_txt.read()
    click.echo(a)


def number_lines(file_txt, number_blank):
    lines = file_txt.readlines()
    for idx, line in enumerate(lines, 1):
        if number_blank or line.strip():
            click.echo(f"{idx}: {line.strip().decode('utf-8')}")


def show_end(file_txt):
    lines = file_txt.readlines()
    for idx, line in enumerate(lines, 1):
        click.echo(f"{line.strip().decode('utf-8')} {'$'}")


def remove_blanks(file_txt):
    lines = file_txt.readlines()
    for line in lines:
        if line.strip():
            click.echo(line.strip().decode('utf-8'))

def print_until_function(file_txt, line, number_blank):
    lines = file_txt.readlines()
    if line <= len(lines):
        index = 0
        number_line = 0
        while index < line:
            if number_blank or lines[index].strip():
                click.echo(f"{number_line + 1}: {lines[index].strip().decode('utf-8')}")
                index += 1
                number_line += 1
                continue
            click.echo(lines[index].strip().decode('utf-8'))
            index += 1


def print_line(file_txt, line):
    lines = file_txt.readlines()
    click.echo(f'{line} {lines[line - 1].strip().decode("utf-8")}')


@click.group()
def cli():
    pass


@click.command()
@click.argument('file_txt', type=str, nargs=-1)
@click.option('--line', '-l', type=int, help='Line number to read from the file.')
@click.option('--print-until', '-p', is_flag=True, default=False, help='boolean value print until line given.')
@click.option('--number-blank', '-n', is_flag=True, default=False, help='Number all lines, including blank lines.')
@click.option('--show-ends', '-E', is_flag=True, default=False, help='display $ at end of each line')
@click.option('--version', '-V', is_flag=True, default=False, help='output version information')
@click.option('--remove-blank', '-R', is_flag=True, default=False, help='remove blank lines')
def pycat(file_txt, line, print_until, number_blank, show_ends, version, remove_blank):
    if version:
        click.echo(__version__)
        return

    for file in file_txt:
        abs_path = os.path.abspath(file)
        if not os.path.exists(abs_path):
            click.echo('File not found', err=True)
            sys.exit(1)

        with open(abs_path, 'rb') as f:
            if remove_blank:
                remove_blanks(f)

            if show_ends:
                show_end(f)

            if line is not None:
                if print_until:
                    print_until_function(f, line, number_blank)
                else:
                    print_line(f, line)

            if number_blank:
                number_lines(f, number_blank)
            else:
                show_all(f)


if __name__ == '__main__':
    pycat()
