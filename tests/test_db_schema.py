"""
Test the participants table schema in registration_server.py
against the input tags in index.html.
"""
import os
import sys
from html.parser import HTMLParser

package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, package_dir)
from registration_server import Participant


class InputParser(HTMLParser):
    """
    Class to harvest the names of the `input` fields in the index.html
    file by processing each of the start tags.
    """
    def __init__(self, skip=()):
        super().__init__()
        self.input_fields = set()
        self.skip = skip

    def handle_starttag(self, tag, attrs):
        if tag != 'input':
            return
        for key, value in attrs:
            if key != 'name' or value in self.skip:
                continue
            self.input_fields.add(value)


def get_input_fields(index_file, skip=()):
    """Get the names of the input fields in the index file."""
    parser = InputParser(skip=skip)
    with open(index_file, 'r') as fobj:
        parser.feed(''.join(fobj.readlines()))
    return parser.input_fields


def get_column_names():
    """Get the names of the columns in the participants table."""
    column_names = set()
    for column in Participant().__table__.columns:
        column_names.add(column.name)
    # Omit the id column since it's a surrogate primary key, and
    # implicitly check that it is present.
    column_names.remove('id')
    return column_names


def test_db_schema():
    """Check for missing and extra columns in the participants table."""
    input_fields = get_input_fields(os.path.join(package_dir, 'index.html'),
                                    skip=('secret',))
    column_names = get_column_names()
    missing_columns = input_fields.difference(column_names)
    extra_columns = column_names.difference(input_fields)
    message = ''
    if missing_columns:
        message += f'Missing columns in participants table: {missing_columns}\n'
    if extra_columns:
        message += f'Extra columns in participants table: {extra_columns}\n'
    if message:
        raise RuntimeError(message)
