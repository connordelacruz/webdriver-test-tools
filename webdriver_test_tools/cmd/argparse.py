import argparse
import sys


class ArgumentParser(argparse.ArgumentParser):
    """Extended ArgumentParser class with support for default subparser"""

    def set_default_subparser(self, name, args=None, positional_args=0):
        """default subparser selection. Call after setup, just before parse_args()
        :name: is the name of the subparser to call by default
        :args: (Default: None) If set is the argument list handed to parse_args()

        Based on: https://stackoverflow.com/a/26379693
        """
        subparser_found = False
        for arg in sys.argv[1:]:
            if arg in ['-h', '--help']:  # global help if no subparser
                break
        else:
            for x in self._subparsers._actions:
                if not isinstance(x, argparse._SubParsersAction):
                    continue
                for sp_name in x._name_parser_map.keys():
                    if sp_name in sys.argv[1:]:
                        subparser_found = True
            if not subparser_found:
                # insert default in last position before global positional
                # arguments, this implies no global options are specified after
                # first positional argument
                if args is None:
                    sys.argv.insert(len(sys.argv) - positional_args, name)
                else:
                    args.insert(len(args) - positional_args, name)


