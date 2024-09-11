
class Monad[T]:
    __match_args__ = ('_value')

    def __init__(self, value: T) -> None:
        self._value = value
