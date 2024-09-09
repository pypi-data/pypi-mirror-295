# playground to test queues and threads
import asyncio
import logging
from binascii import hexlify

from satel_integra_ext.satel_integra import AsyncSatel, SatelCommand

_LOGGER = logging.getLogger(__name__)

async def test():
    """Basic test of the Satel communication."""
    loop = asyncio.get_event_loop()
    stl = AsyncSatel("192.168.2.86", 7094, loop)

    def handler(msg):
        _LOGGER.info(f"Received: {msg}")
        if msg.cmd != SatelCommand.OUTPUT_STATE:
            return None
        return "OK"

    loop.call_later(3, lambda: stl._dispatch_frame(bytearray(b'\xfe\xfe\x17\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x22\xd8\xfe\x0d',)))
    result = await stl.wait_for_response(SatelCommand.OUTPUT_STATE, handler)
    _LOGGER.info(f"Received: {result}")

    # loop.call_later(3, lambda: stl._dispatch_frame(bytearray(b'\xFE\xFE\x7E\x03\x31\x31\x36\x32\x30\x31\x36\x30'
    #                               b'\x37\x31\x35\x00\x00\x02\x48\xFE\x0D',)))
    # loop.run_until_complete(stl.connect())
    # loop.create_task(stl.keep_alive())
    # loop.create_task(stl.monitor_status())

    # loop.create_task(stl.read_temp(1))

    # print()
    # for state in [1, 0]:
    #     loop.run_until_complete(asyncio.sleep(3000))
    #     for output in [25, 26, 27]:
    #         loop.create_task(stl.set_output('1410', output, state))
    #     print()


    try:
        loop.run_forever()
    except:
        _LOGGER.info("interrupted")
    # loop.close()


logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)5s %(name)s - %(message)s', datefmt='%H:%M:%S')
asyncio.run(test())
