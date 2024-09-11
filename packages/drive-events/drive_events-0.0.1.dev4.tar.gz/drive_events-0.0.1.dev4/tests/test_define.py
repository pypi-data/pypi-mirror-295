import pytest

from drive_events import default_drive, EventInput
from drive_events.types import BaseEvent


@pytest.mark.asyncio
async def test_non_async_func():
    with pytest.raises(AssertionError):

        @default_drive.make_event
        def a(event: EventInput, global_ctx):
            return 1


@pytest.mark.asyncio
async def test_non_async_listen_groups():
    async def a(event: EventInput, global_ctx):
        return 1

    with pytest.raises(AssertionError):

        @default_drive.listen_groups([a])
        async def b(event: EventInput, global_ctx):
            return 1


@pytest.mark.asyncio
async def test_set_and_reset():
    @default_drive.make_event
    async def a(event: EventInput, global_ctx):
        return 1

    @default_drive.listen_groups([a])
    async def b(event: EventInput, global_ctx):
        return 2

    default_drive.reset()

    with pytest.raises(AssertionError):

        @default_drive.listen_groups([a])
        async def b(event: EventInput, global_ctx):
            return 2


@pytest.mark.asyncio
async def test_duplicate_decorator():
    @default_drive.make_event
    @default_drive.make_event
    async def a(event: EventInput, global_ctx):
        return 1

    assert isinstance(a, BaseEvent)


@pytest.mark.asyncio
async def test_order():
    @default_drive.make_event
    async def a(event: EventInput, global_ctx):
        return 1

    @default_drive.listen_groups([a])
    async def b(event: EventInput, global_ctx):
        return 2

    @default_drive.listen_groups([b])
    async def c(event: EventInput, global_ctx):
        return 3

    print(a.debug_string())
    print(b.debug_string())
    print(c.debug_string())

    assert await a.solo_run(None) == 1
    assert await b.solo_run(None) == 2
    assert await c.solo_run(None) == 3


@pytest.mark.asyncio
async def test_multi_send():
    @default_drive.make_event
    async def a(event: EventInput, global_ctx):
        return 1

    @default_drive.listen_groups([a])
    async def b(event: EventInput, global_ctx):
        return 2

    @default_drive.listen_groups([a])
    async def c(event: EventInput, global_ctx):
        return 3

    print(a.debug_string())
    print(b.debug_string())
    print(c.debug_string())
    assert await a.solo_run(None) == 1
    assert await b.solo_run(None) == 2
    assert await c.solo_run(None) == 3


@pytest.mark.asyncio
async def test_multi_recv():
    @default_drive.make_event
    async def a(event: EventInput, global_ctx):
        return 1

    @default_drive.listen_groups([a])
    async def a1(event: EventInput, global_ctx):
        return 1

    @default_drive.make_event
    async def b(event: EventInput, global_ctx):
        return 2

    @default_drive.listen_groups([a1, b])
    async def c(event: EventInput, global_ctx):
        return 3

    print(a.debug_string())
    print(b.debug_string())
    print(c.debug_string())
    assert await a.solo_run(None) == 1
    assert await b.solo_run(None) == 2
    assert await c.solo_run(None) == 3


@pytest.mark.asyncio
async def test_multi_groups():
    @default_drive.make_event
    async def a0(event: EventInput, global_ctx):
        return 0

    @default_drive.make_event
    async def a1(event: EventInput, global_ctx):
        return 0

    @default_drive.listen_groups([a0, a1])
    @default_drive.listen_groups([a0, a1])
    @default_drive.listen_groups([a0, a1])
    async def a(event: EventInput, global_ctx):
        return 1

    assert await a.solo_run(None) == 1


@pytest.mark.asyncio
async def test_loop():
    @default_drive.make_event
    async def a(event: EventInput, global_ctx):
        return 1

    @default_drive.listen_groups([a])
    async def b(event: EventInput, global_ctx):
        return 2

    a = default_drive.listen_groups([b])(a)

    @default_drive.listen_groups([a, b])
    async def c(event: EventInput, global_ctx):
        return 3

    print(a.debug_string())
    print(b.debug_string())
    print(c.debug_string())

    assert await a.solo_run(None) == 1
    assert await b.solo_run(None) == 2
    assert await c.solo_run(None) == 3
