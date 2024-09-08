import argparse
import logging
from pprint import pprint

from s3sel.files import ConfigStore, StoreException
from s3sel.ui import main_ui
from s3sel.utils import program_exit

log = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO)


def main_cli() -> None:
    parser = argparse.ArgumentParser(prog="s3sel") 
    parser.add_argument("-a", "--add-current", action="store_true", help="add your current .s3cfg to s3sel store")
    parser.add_argument("-l", "--list-all", action="store_true", help="show all configs present in s3sel store")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    parser.add_argument("-d", "--delete", action="store_true", help="delete config from s3sel store by specified name")
    parser.add_argument("-s", "--switch", action="store_true", help="switch your current .s3cfg to config with specified name")
    parser.add_argument("-c", "--check", action="store_true", help="check if your current .s3cfg is already stored")
    parser.add_argument("name", nargs="?")

    args = parser.parse_args()

    if not args.verbose:
        logging.disable(logging.INFO)

    store = ConfigStore()
    try:
        if args.add_current:
            if not args.name:
                program_exit(1, msg="No name specified for new config")
            name = args.name
            new_cfg_md5 = store.add_new_config(name)
            program_exit(0, msg=f"Added new config {name}, checksum: {new_cfg_md5}")
        elif args.delete:
            if not args.name:
                program_exit(1, msg="No name specified to delete")
            name = args.name
            store.remove_config_by_name(name)
            program_exit(0, msg=f"Deleted config with name \"{name}\"")
        elif args.list_all:
            pprint(store.cfg_list)
        elif args.switch:
            if not args.name:
                program_exit(1, msg="No name specified to switch to")
            name = args.name
            new_cfg = store.replace_current_config(name)
            program_exit(0, msg=f"Replaced current config with \"{new_cfg.name}\"")
        elif args.check:
            s3cfg_hash = store.get_current_config_hash()
            cfg = store.get_config_by("hash", s3cfg_hash)
            if cfg:
                program_exit(0, msg=f"Config \"{cfg.name}\" with hash {s3cfg_hash} is already present in s3sel store.")
            else:
                program_exit(0, msg=f"No config with hash {s3cfg_hash} found.")
        else:
            main_ui(store)

    except StoreException as e:
        program_exit(1, msg=e.args[0])
    
    program_exit(0)

    

if __name__ == '__main__':
    main_cli()
