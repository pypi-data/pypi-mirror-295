from pprint import pformat

from simple_term_menu import TerminalMenu
from termcolor import colored

from s3sel.files import ConfigStore
from s3sel.utils import program_exit


def main_ui(store: ConfigStore) -> bool:
    cfg_map = {cfg.name: cfg for cfg in store.cfg_list}

    if not len(cfg_map):
        program_exit(0, msg="Can't run in ui mode, no configs stored. "
                     "(Try running with -h to see how to add new config.)")

    def get_preview(option_value: str) -> str:
        cfg = cfg_map.get(option_value)
        return pformat(cfg._asdict(), width=20)

    options = [cfg.name for cfg in cfg_map.values()]

    current_cfg = store.get_config_by("hash", store.get_current_config_hash())

    terminal_menu = TerminalMenu(
        menu_entries=options,
        preview_command=get_preview,
        preview_title=f"Current config: {colored(current_cfg.name, 'cyan', attrs=['bold'])}"
    )
    menu_entry_index = terminal_menu.show()
    if menu_entry_index is None:
        return 
    selected_cfg = options[menu_entry_index]
    store.replace_current_config_by_name(selected_cfg)
    program_exit(0, msg=f"Replaced current config with \"{selected_cfg}\"")
    