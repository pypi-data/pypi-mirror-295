from collections.abc import AsyncIterator

import anysync


@anysync.generator
async def f() -> AsyncIterator[int]:
    yield 1
    yield 2
    yield 3
