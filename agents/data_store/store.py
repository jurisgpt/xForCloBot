import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class SimpleStore:
    """Simple JSON file-based data store for MVP"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def _get_file_path(self, collection: str) -> Path:
        """Get the JSON file path for a collection"""
        return self.base_path / f"{collection}.json"
        
    def save(self, collection: str, key: str, data: Dict[str, Any]):
        """Save data to collection"""
        file_path = self._get_file_path(collection)
        existing = self.load_all(collection) or {}
        existing[key] = {
            **data,
            "updated_at": datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(existing, f, indent=2)
            
    def load(self, collection: str, key: str) -> Optional[Dict[str, Any]]:
        """Load specific data from collection"""
        file_path = self._get_file_path(collection)
        if not file_path.exists():
            return None
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get(key)
            
    def load_all(self, collection: str) -> Optional[Dict[str, Any]]:
        """Load all data from collection"""
        file_path = self._get_file_path(collection)
        if not file_path.exists():
            return None
            
        with open(file_path, 'r') as f:
            return json.load(f)
