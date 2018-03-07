#!/usr/bin/env python3
import argparse


def get_parser():
    """Returns ArgumentParser object for use with main()"""
    parser = argparse.ArgumentParser()
    # Argument for initializing
    # TODO: optional filepath
    parser.add_argument('-i', '--init', action='store_true', help='Initialize a new test project in the current directory')
    return parser

# TODO: main
