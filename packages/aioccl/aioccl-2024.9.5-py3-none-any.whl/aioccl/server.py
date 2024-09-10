"""CCL API server and handler."""
from __future__ import annotations

import asyncio
import logging

from aiohttp import web
import aiohttp_cors

from .device import CCLDevice, CCL_DEVICE_INFO_TYPES
from .sensor import CCL_SENSORS

_LOGGER = logging.getLogger(__name__)

class CCLServer:
    LISTEN_PORT = 42373
    
    devices: dict[str, CCLDevice] = {}
    
    def add_copy(device: CCLDevice) -> None:
        """Attach a device copy to the server."""
        CCLServer.devices.setdefault(device.passkey, device)
        _LOGGER.debug(CCLServer.devices)

    #routes = web.RouteTableDef()

    async def _handler(request: web.BaseRequest) -> web.Response:
        """Handle POST requests for data updating."""
        class HandlerStorage:
            body: dict[str, None | str | int | float]
            info: dict[str, None | str]
            sensors: dict[str, None | str | int | float]
        
        _LOGGER.debug("Request received.")
        
        # Resetting variables
        _device: CCLDevice = None

        HandlerStorage.body = {}
        HandlerStorage.info = {}
        HandlerStorage.sensors = {}
        
        _status: None | int = None
        _text: None | str = None
        
        try:
            for passkey in CCLServer.devices:
                if passkey == request.match_info['passkey']:
                    _device = CCLServer.devices[passkey]
                    break
            assert _device, 404
            
            assert request.content_type == 'application/json', 400
            assert 0 < request.content_length <= 5000, 400
            
            HandlerStorage.body = await request.json()
            _LOGGER.debug(HandlerStorage.body)
            
        except Exception as err:
            _status = err.args[0]
            if _status == 400: _text = "400 Bad Request"
            elif _status == 404: _text = "404 Not Found"
            else:
                _status = 500
                _text = "500 Internal Server Error"
            _LOGGER.debug("Request exception occured: %s", err)
        
        else:
            for key, value in HandlerStorage.body.items():
                if key in CCL_DEVICE_INFO_TYPES:
                    HandlerStorage.info.setdefault(key, value)
                elif key in CCL_SENSORS.keys():
                    HandlerStorage.sensors.setdefault(key, value)
                    
            _device.update_info(HandlerStorage.info)
            _device.update_sensors(HandlerStorage.sensors)
            _status = 200
            _text = "200 OK"
            _LOGGER.debug("Request processed.")
        
        finally:
            return web.Response(status=_status, text=_text)

    app = web.Application()

    cors = aiohttp_cors.setup(app)

    resource = cors.add(app.router.add_resource("/{passkey}"))
    route = cors.add(
        resource.add_route("POST", _handler), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

    async def run() -> None:
        """Try to run the API server in case none is available."""
        try:
            _LOGGER.debug("Trying to start the API server.")
            runner = web.AppRunner(CCLServer.app)
            await runner.setup()
            site = web.TCPSite(runner, port=CCLServer.LISTEN_PORT)
            await site.start()
        except Exception as err:
            _LOGGER.warning("Failed to run the API server: %s", err)
        else:
            _LOGGER.debug("Successfully started the API server.")

    async def stop() -> None:
        """Stop running the API server."""
        await CCLServer.runner.cleanup()
