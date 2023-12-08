#!/usr/bin/env python3

import serial
import re
import asyncio
from aiohttp import web
import sys

smartmeter = []
settings   = []
status     = []

def crc16(data: bytes):
    crc = 0
    for b in data:
      crc ^= b
      for i in range(8):
        if (crc & 1) != 0:
          crc >>= 1
          crc ^= 0xA001
        else:
          crc >>= 1
    return crc


def find_value(message, id, format=None, factor=None):
 for line in message.split(b"\n"):
   if id in line:
     #print(f"id: {id}, line: {line}")
     str = re.findall(b"\((.*)\)", line)[0].split(b"*")[0]
     if format == "float":
       value = float(str)
     elif format == "int":
       value = int(str)
     else:
       value = str
     if factor:
       value *= factor
     return value
 return None


async def handleSerialInput():

  global smartmeter
  global settings
  global status
  global watermeter

  with serial.Serial("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AI02DX1X-if00-port0", 112500) as ser:

    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    def got_input():
      try:
        asyncio.ensure_future(queue.put(ser.readline()), loop=loop)
      except:
        print("Serial exception")
        sys.exit(1)

    loop.add_reader(ser, got_input)

    message = b""
    started = False
    while True:
      data = await queue.get()

      if not started and data[0:1] == b"/":
        started = True

      if started:
        message += data

      if data[0:1] == b"!":
        message = message[0:-(len(data)-1)]

        crc_received   = data[1:5].decode("ascii").lower()
        crc_calculated = f"{crc16(message):04X}".lower()

        if started and crc_received == crc_calculated:

          newSmartmeter = [
            {
              "CONSUMPTION_GAS_M3": 0.0,
              "CONSUMPTION_W": find_value(message, b"1-0:1.7.0", 'float', 1000),
              "CONSUMPTION_KWH_LOW": find_value(message, b"1-0:1.8.1", 'float'),
              "CONSUMPTION_KWH_HIGH": find_value(message, b"1-0:1.8.2", 'float'),
              "PRODUCTION_W": 0.0,
              "PRODUCTION_KWH_HIGH": 0.0,
              "PRODUCTION_KWH_LOW": 0.0,
              "TARIFCODE": find_value(message, b"0-0:96.14.0", 'int'),
            }
          ]

          newSettings = [
           { "CONFIGURATION_ID": 1, "PARAMETER": 0.0 },
           { "CONFIGURATION_ID": 2, "PARAMETER": 0.0 },
           { "CONFIGURATION_ID": 3, "PARAMETER": 0.0 },
           { "CONFIGURATION_ID": 4, "PARAMETER": 0.0 },
           { "CONFIGURATION_ID": 15, "PARAMETER": 0.0 },
          ]
          newStatus = [
            { "STATUS_ID": 74, "STATUS": find_value(message, b"1-0:21.7.0", 'float') },
            { "STATUS_ID": 75, "STATUS": 0.0 },
            { "STATUS_ID": 76, "STATUS": 0.0 },
            { "STATUS_ID": 77, "STATUS": 0.0 },
            { "STATUS_ID": 78, "STATUS": 0.0  },
            { "STATUS_ID": 79, "STATUS": 0.0 },
            { "STATUS_ID": 100, "STATUS": find_value(message, b'1-0:31.7.0', 'float') },
            { "STATUS_ID": 101, "STATUS": 0.0 },
            { "STATUS_ID": 102, "STATUS": 0.0 },
            { "STATUS_ID": 103, "STATUS": 0.0 },
            { "STATUS_ID": 104, "STATUS": 0.0 },
            { "STATUS_ID": 105, "STATUS": 0.0 },
          ]

          newWatermeter = [
            {
                "WATERMETER_CONSUMPTION_LITER": 0.0,
                "WATERMETER_CONSUMPTION_TOTAL_M3": 0.0,
                "WATERMETER_PULS_COUNT": 0.0, 
            } 
          ]

          smartmeter = newSmartmeter
          settings   = newSettings
          status     = newStatus
          watermeter = newWatermeter

          #print()
          #print(message.decode("ascii"))
          #print()
          #print(smartmeter)
          #print()
          #print(settings)
          #print()
          #print(status)
          #print()

        message = b""
        started = False


async def get_v1_smartmeter(request):
    global smartmeter
    #print("smartmeter")
    return web.json_response(smartmeter)


async def get_v1_settings(request):
    global settings
    #print("settings")
    return web.json_response(settings)


async def get_v1_status(request):
    global status
    #print("status")
    return web.json_response(status)

async def get_v2_watermeter(request):
    global watermeter
    #print("watermeter")
    return web.json_response(watermeter)

async def main():
  app = web.Application()
  app.router.add_get('/api/v1/smartmeter', get_v1_smartmeter)
  app.router.add_get('/api/v1/configuration', get_v1_settings)
  app.router.add_get('/api/v1/status', get_v1_status)
  app.router.add_get('/api/v2/watermeter/day', get_v2_watermeter)

  runner = web.AppRunner(app, access_log=None)
  await runner.setup()
  site = web.TCPSite(runner, '0.0.0.0', 8080)
  await site.start()

  await handleSerialInput()

  await runner.cleanup()


if __name__ == "__main__":

  asyncio.run(main())

