import asyncio

from telethon.network import MTProtoSender


class PathedMTProtoSender(MTProtoSender):
    async def _try_connect(self, attempt):
        try:
            self._log.debug('Connection attempt %d...', attempt)
            await self._connection.connect(timeout=self._connect_timeout)
            self._log.debug('Connection success!')
            return True
        except asyncio.TimeoutError as exc:
            self._log.warning('Attempt %d at connecting failed: %s: %s',
                              attempt, type(exc).__name__, exc)
            await asyncio.sleep(self._delay)
            return False
        except IOError as exc:
            self._log.warning('Attempt %d at connecting failed: %s: %s',
                              attempt, type(exc).__name__, exc)
            raise exc
