from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal


def account_alias_generator(string: str) -> str:
    match string:
        case 'date':
            return 'DateTime.Typed'
        case 'incoming_sum':
            return 'Sum.Incoming'
        case 'outgoing_sum':
            return 'Sum.Outgoing'
        case 'resigned_sum':
            return 'Sum.ResignedSum'
        case 'store_id':
            return 'Account.Id'
        case 'store_name':
            return 'Account.Name'
        case 'num':
            return 'Document'

    return 'Account.' + to_pascal(string)


class Inventory(BaseModel):
    model_config = ConfigDict(alias_generator=account_alias_generator, use_enum_values=True)
    store_name: Optional[str] = None
    store_id: Optional[str] = None
    num: Optional[str] = None
    resigned_sum: Optional[float] = None
    outgoing_sum: Optional[float] = None
    incoming_sum: Optional[float] = None
    date: Optional[datetime] = None


