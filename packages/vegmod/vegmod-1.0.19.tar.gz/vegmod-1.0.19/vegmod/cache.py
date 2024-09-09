import time

from loguru import logger
from vegmod.utils import save_dict, load_dict

class Cache:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
        # remove any entries that are older than 1 hour
        dirty_cache = load_dict(file_path)
        self.cache = {k: v for k, v in dirty_cache.items() if time.time() - v["_cached_at"] < 3600}

    def save(self):
        """
        Save the cache to a JSON file.
        """
        save_dict(self.cache, self.file_path)
    
    # override get and set [] operators
    def __getitem__(self, key):
        # logger.info(f"Cache Get: key={key}")
        return self.cache[key]['data']
    
    # override set [] operator
    def __setitem__(self, key, value):
        # logger.info(f"Cache Set: key={key}")
        self.cache[key] = {
            'data': value,
            '_cached_at': time.time()     
        }
        
    # override 'in' operator
    def __contains__(self, key):
        return key in self.cache
    
    # override 'del' operator
    def __delitem__(self, key):
        del self.cache[key]
        
    # override 'len' operator
    def __len__(self):
        return len(self.cache)
    
    # override items() method
    def items(self):
        return self.cache.items()