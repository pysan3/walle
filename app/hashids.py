import os
from typing import Generic, List, TypeVar, Union

from hashids import Hashids

T = TypeVar('T')


class ParsedHashItem(Generic[T]):
    def __init__(self, ids: int, htype: T) -> None:
        self.ids: int = ids
        self.htype: T = htype


class HashManager(Hashids, Generic[T]):
    def set_htypes(self, htypes: List[T]):
        self._htypes = htypes

    def get_htypes(self) -> List[T]:
        return self._htypes

    def stringify(self, ids: int, htype: Union[int, T]) -> str:
        if not isinstance(htype, int):
            htype = self._htypes.index(htype)
        return self.encode(ids, htype)

    def parse(self, hash: str):
        parsed = self.decode(hash)
        if len(parsed) != 2:
            raise Exception(f'Hash `{hash=}` decode failed! Output: {parsed=}')
        ids, htype_id = parsed
        return ParsedHashItem(ids, self._htypes[htype_id])


accessHM: HashManager[str] = HashManager(os.environ.get('WALLE_HASHID_SALT', 'WALLE_HASHID_SALT'), 10)
accessHM.set_htypes([
    'company',
    'project',
    'user',
])

payHM = Hashids(os.environ.get('WALLE_HASHID_SALT', 'WALLE_HASHID_SALT'), 10)
pairHM = Hashids(os.environ.get('WALLE_HASHID_SALT', 'WALLE_HASHID_SALT'), 10)
