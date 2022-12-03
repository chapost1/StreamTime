from __future__ import annotations
from pydantic import BaseModel
import base64
import json
from common.app_errors import InputError
from typing import Optional

class NextPage(BaseModel):
    pagination_index_is_smaller_than: Optional[int] = None

    @staticmethod
    def decode(b64: str) -> NextPage:
        """Transform from base64 to isntance"""
        if b64 is None:
            return NextPage()

        try:
            s = base64.b64decode(b64)
            dictionary = json.loads(s)
            self: NextPage = NextPage(**dictionary)
        except Exception:
            raise InputError(details={
                'error': 'invalid next page'
            })
        
        if self.pagination_index_is_smaller_than is None:
            raise InputError(details={
                'error': 'invalid next page'
            })

        return self

    
    def encode(self) -> str:
        """Returns a base64 form of self"""
        dictionary = self.dict()
        s = json.dumps(dictionary)
        return base64.b64encode(s.encode('utf-8'))
