import pytest
import asyncio
from unittest.mock import patch
from libaxion_dmx import AxionDmxApi

@pytest.mark.asyncio
async def test_authenticate():
    api = AxionDmxApi(host="192.168.1.2", password="test")
    
    with patch("libaxion_dmx.AxionDmxApi._send_command", return_value="ok") as mock_send_command:
        result = await api.authenticate()
        assert result is True
        mock_send_command.assert_called_with(">getversion\r\n")

@pytest.mark.asyncio
async def test_set_level():
    api = AxionDmxApi(host="192.168.1.2", password="test")

    with patch("libaxion_dmx.AxionDmxApi._send_command", return_value="ok") as mock_send_command:
        result = await api.set_level(channel=1, level=255)
        assert result is True
        mock_send_command.assert_called_with(">setlevel,1,255\r\n")

@pytest.mark.asyncio
async def test_get_level():
    api = AxionDmxApi(host="192.168.1.2", password="test")
    
    with patch("libaxion_dmx.AxionDmxApi._send_command", return_value="ok,255") as mock_send_command:
        level = await api.get_level(channel=1)
        assert level == 255
        mock_send_command.assert_called_with(">getlevel,1\r\n")

@pytest.mark.asyncio
async def test_set_color():
    api = AxionDmxApi(host="192.168.1.2", password="test")
    
    with patch("libaxion_dmx.AxionDmxApi._send_command", return_value="ok") as mock_send_command:
        result = await api.set_color(channel=1, rgb=(255, 0, 0))
        assert result is True
        mock_send_command.assert_any_call(">setlevel,1,255\r\n")
        mock_send_command.assert_any_call(">setlevel,2,0\r\n")
        mock_send_command.assert_any_call(">setlevel,3,0\r\n")

@pytest.mark.asyncio
async def test_set_rgbw():
    api = AxionDmxApi(host="192.168.1.2", password="test")
    
    with patch("libaxion_dmx.AxionDmxApi._send_command", return_value="ok") as mock_send_command:
        result = await api.set_rgbw(channel=1, rgbw=(255, 0, 0, 255))
        assert result is True
        mock_send_command.assert_any_call(">setlevel,1,255\r\n")
        mock_send_command.assert_any_call(">setlevel,2,0\r\n")
        mock_send_command.assert_any_call(">setlevel,3,0\r\n")
        mock_send_command.assert_any_call(">setlevel,4,255\r\n")

@pytest.mark.asyncio
async def test_set_rgbww():
    api = AxionDmxApi(host="192.168.1.2", password="test")
    
    with patch("libaxion_dmx.AxionDmxApi._send_command", return_value="ok") as mock_send_command:
        result = await api.set_rgbww(channel=1, rgbww=(255, 0, 0, 255, 128))
        assert result is True
        mock_send_command.assert_any_call(">setlevel,1,255\r\n")
        mock_send_command.assert_any_call(">setlevel,2,0\r\n")
        mock_send_command.assert_any_call(">setlevel,3,0\r\n")
        mock_send_command.assert_any_call(">setlevel,4,255\r\n")
        mock_send_command.assert_any_call(">setlevel,5,128\r\n")
