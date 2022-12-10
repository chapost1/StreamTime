from __future__ import annotations
from pydantic import BaseModel
import base64
import json
from common.app_errors import InputError
from typing import Optional

class NextPage(BaseModel):
    minimum_pagination_index: Optional[int] = None

    @staticmethod
    def decode(b64: str) -> NextPage:
        """Transform from base64 to isntance"""
        def inputError():
            raise InputError(details={
                'error': 'invalid next page'
            })

        if b64 is None:
            return NextPage()

        try:
            dictionary = json.loads(base64.urlsafe_b64decode(b64.encode()).decode())
            self: NextPage = NextPage(**dictionary)
        except Exception:
            inputError()

        if self.minimum_pagination_index is None:
            inputError()

        return self

    
    def encode(self) -> str:
        """Returns a base64 form of self"""
        dictionary = self.dict()
        return base64.urlsafe_b64encode(json.dumps(dictionary).encode()).decode()
