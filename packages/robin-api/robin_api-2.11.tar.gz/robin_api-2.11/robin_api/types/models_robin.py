

from .._models import BaseModel
from typing import  Union
from typing_extensions import Literal
from typing import Any, Optional, cast

__all__ = ["Models"]

class Models(BaseModel):
        model: Union[
            str,
            Literal[
                "ROBIN_4",
                "ROBIN_3",
            ],
        ]


        

        

        