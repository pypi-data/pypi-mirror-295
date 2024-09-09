
from .cmd_parse_base import CmdParseBase
from .cmd_registry import CmdRegistry

def add_subcommand(cmd, cls):
    CmdRegistry.inst().addSubCommand(cmd, cls)

