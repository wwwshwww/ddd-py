from collections.abc import Callable


class A:
    def __init__(self, a: str) -> None:
        self.a = a

    def get_callback(self) -> Callable[[None], None]:
        return lambda: print(f"Hello, {self.a}")


fn = A("aho").get_callback()
fn()
