#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quizzapalooza.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    from django.db import connections
    from django.db.utils import OperationalError

    def check_database_connection(database_alias):
        try:
            connections[database_alias].ensure_connection()
            print(f"Successfully connected to the {database_alias} database.")
        except OperationalError:
            print(f"Failed to connect to the {database_alias} database.")

    # Usage:
    check_database_connection('default')  # Check PostgreSQL database connection

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
