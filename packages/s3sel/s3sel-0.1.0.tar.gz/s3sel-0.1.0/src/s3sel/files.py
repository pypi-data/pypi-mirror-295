
import os
import hashlib
import shutil
import logging
from pathlib import Path
from typing import NamedTuple

from s3sel.utils import get_file_md5, query_yes_no


log = logging.getLogger(__file__)

class StoreException(Exception):
    pass

class ConfigFile(NamedTuple):
    name: str
    hash: str
    path: str


class ConfigStore:
    def __init__(self) -> None:
        self._cfg_files_path: Path = Path.home() / ".s3sel"
        self._s3cfg_path: Path = Path.home() / ".s3cfg"
        self._is_store_initialized = self._cfg_files_path.is_dir()
        self.cfg_list = self._read_all_config_files()
    
    def _read_all_config_files(self) -> list[ConfigFile]:
        if not self._is_store_initialized:
            return []
        
        all_files = []
        for p in self._cfg_files_path.glob("*"):
            filename = p.name
            cfg_name, cfg_hash = filename.split("-")
            all_files.append(
                ConfigFile(
                    hash=cfg_hash,
                    name=cfg_name,
                    path=p.as_posix(),
                )
            )

        return all_files 
    
    def _check_store_dir_or_create(self) -> None:
        if not self._is_store_initialized:
            log.info(".s3sel dir not found, creating...")
            self._cfg_files_path.mkdir()
    
    def _find_config_by_name(self, name: str) -> ConfigFile:
        cfg = next((c for c in self.cfg_list if c.name == name), None)
        if cfg is None:
            raise StoreException(f"No config with name \"{name}\" found")
        return cfg
    

    def add_new_config(self, config_name) -> str:
        assert self._s3cfg_path.is_file()

        s3cfg_md5 = get_file_md5(self._s3cfg_path)

        for file in self.cfg_list:
            if file.hash == s3cfg_md5:
                raise StoreException(
                    f"Such configuration file already exists with name: {file.name}"
                )
            
        new_path = self._cfg_files_path / f"{config_name}-{s3cfg_md5}"
        log.info("Saving config %s to %s", config_name, new_path.as_posix())
        self._check_store_dir_or_create()
        shutil.copy(self._s3cfg_path, new_path)
        return s3cfg_md5
    
    def get_config_by(self, key: str, value: str) -> ConfigFile | None:
        assert key in ConfigFile._fields
        for cfg in self.cfg_list:
            if getattr(cfg, key) == value:
                return cfg
        else:
            return None
    
    def remove_config_by_name(self, name: str):
        cfg = self._find_config_by_name(name)
        os.remove(cfg.path)

    def replace_current_config(self, name: str) -> ConfigFile | None:
        cfg = self._find_config_by_name(name)
        s3cfg_md5 = get_file_md5(self._s3cfg_path)
        if not self.get_config_by("hash", s3cfg_md5):
            if not query_yes_no(
                "You are going to overwrite .s3cfg which is not present in s3sel store. "
                "Are you sure?"
            ):
                raise StoreException("Rejected to overwrite config file.")
            
        shutil.copyfile(cfg.path, dst=self._s3cfg_path) 
        return cfg
    
    def get_current_config_hash(self) -> str:
        return get_file_md5(self._s3cfg_path)
        

