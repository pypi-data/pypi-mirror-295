# Axion DMX API

Axion DMX API is a Python library to interact with the Axion Lighting DMX Controller. This package allows you to control various types of DMX lighting channels, including RGB, RGBW, and RGBWW.

## Installation

Install the package via pip:

```bash
pip install libaxion_dmx
```

## Usage

### Initialize the API

To use the API, create an instance of the `AxionDmxApi` class with the IP address of your DMX controller and the password.

```python
from libaxion_dmx import AxionDmxApi

api = AxionDmxApi(host="192.168.1.2", password="your_password")
```

### Authenticate

Authenticate with the controller:

```python
authenticated = await api.authenticate()
if authenticated:
    print("Successfully authenticated with the controller.")
```

### Set Channel Level

Set the level of a specific channel:

```python
await api.set_level(channel=1, level=255)
```

### Get Channel Level

Get the current level of a specific channel:

```python
level = await api.get_level(channel=1)
print(f"Channel 1 level: {level}")
```

### Set Color (RGB)

Set the RGB color of a specific channel:

```python
await api.set_color(channel=1, rgb=(255, 0, 0))  # Set to Red
```

### Set RGBW Color

Set the RGBW color of a specific channel:

```python
await api.set_rgbw(channel=1, rgbw=(255, 0, 0, 255))  # Set to Red with White
```

### Set RGBWW Color

Set the RGBWW color of a specific channel:

```python
await api.set_rgbww(channel=1, rgbww=(255, 0, 0, 255, 128))  # Set to Red with Warm White
```

## Testing

To run the tests for this package, use pytest.

## License

This project is licensed under the MIT License - see the LICENSE file for details.