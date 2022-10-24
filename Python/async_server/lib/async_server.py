import socket
import time
from machine import RTC
import uasyncio as asyncio
import logging
from heartbeat import heartbeat
from ntp import set_time
import time_convert as tc


class AsyncHTTPServer():

    def __init__(self, host="0.0.0.0", port=80, backlog=20, timeout=20):
        tz = [ [         -5, 0, 0],  # Time offset  [      H,M,S] -5 US/Eastern 
           [  3, 13, 1, 0, 0],  # Start of DST [ M,D, H,M,S] Mar 13
           [ 11, 6, 2, 0, 0],  # End   of DST [ M,D, H,M,S] Nov 6
           [         1, 0, 0]  # DST Adjust   [      H,M,S] +1 hour
       ]
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout
        # Set up the real time clock from the NTP server
        rtc = RTC()
        set_time()  # Write the UTC time from NTP server to the real time clock
        # Convert to local timezone
        year, month, day, hour, minute, second, dow, doy = tc.LocalTime(tz)
        rtc.datetime((year, month, day, dow, hour, minute, second, 0))
        print("Real Time Clock: {0}-{1}-{2} {4}:{5}:{6}".format(*rtc.datetime()))
        # Configure the logger
        self.logger = logging.getLogger("Server")
        fmt = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"
        logging.basicConfig(level=logging.INFO,
                            filename="server.log",
                            format=fmt)
        
        
    async def get_header(self, reader):
        request_line = await reader.readline()
        while (await reader.readline() != b'\r\n'):
           pass
        self.header = request_line.decode('utf-8')

    def request_verb(self):
        lines = self.header.split('\n')
        return lines[0].split()[0]


    def get_endpoint(self):
        lines = self.header.split('\n')
        return lines[0].split()[1]


    def customize_html(self, content):
        ''' Overide this function in subclass to
            populate fields in html template.
        '''
        custom = content
        return custom

    async def get_request(self, endpoint, writer):
        try:
            if endpoint == '/':
                filename = './index.html'
                with open(filename, 'r') as f:
                    content = f.read()
                response_header = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
                self.logger.info(f"Response Header: {' '.join(response_header.splitlines())}")
                custom = self.customize_html(content)
                response = response_header + custom
            elif endpoint == '/log':
                filename = './server.log'
                content = ''
                with open(filename, 'r') as f:
                    raws = f.readlines()[-25:]
                content = '<br>'.join([raw.strip() for raw in raws])
                response_header = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
                prefix = '''
                            <!DOCTYPE html>
                            <html lang='en'> 
                            <head>
                            <meta charset='utf-8'>
                            <title>Async</title>
                            </head>
                            <body>
                            <div>
                            <h1>Last N Lines of Log (Max: 25)</h1>
                         '''
                suffix = '''
                            </div>
                            </body>
                            </html>
                         '''
                response = response_header + prefix + content + suffix
            else:
                raise OSError
        except OSError:
            response = 'HTTP/1.0 404 NOT FOUND\r\n\r\n'
            self.logger.info(f"Response Header: {' '.join(response.splitlines())}")
        
        writer.write(response.encode('utf-8'))
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        self.logger.info(f"Client Disconnected from {self.addr}")


    async def serve_client(self, reader, writer):
        self.addr = writer.get_extra_info('peername')
        self.logger.info(f"Client Connected from: {self.addr}")
        try:
            request_line = await asyncio.wait_for(reader.readline(),
                                                  self.timeout)
            while (await reader.readline() != b'\r\n'):
               pass
            self.header = request_line.decode('utf-8')
            self.logger.info(f"Received: {' '.join(self.header.splitlines())} from {self.addr}")
            if (self.request_verb() == 'GET'):
                endpoint = self.get_endpoint()
                self.logger.info(f"Wrote: {endpoint}")
                await self.get_request(endpoint, writer)
        except asyncio.TimeoutError:
            response_header = 'HTTP/1.0 500 Internal Server Error\r\n\r\n'
            self.logger.info(f"Response Header: {' '.join(response_header.splitlines())}")
            with open("500.html", "r") as f:
                content = f.read()
            response = response_header + content 
            writer.write(response.encode('utf-8'))
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Client Disconnected from {self.addr}")
            
    async def main(self):
        self.logger.info("Setting Up Webserver")
        asyncio.create_task(heartbeat(500))
        self.server = await asyncio.start_server(self.serve_client,
                                                 self.host,
                                                 self.port,
                                                 backlog=self.backlog)
        while True:
            await asyncio.sleep(60)

    def get_local_time(self):
        tz = [ [         -5, 0, 0],  # Time offset  [      H,M,S] -5 US/Eastern 
           [  3, 13, 1, 0, 0],  # Start of DST [ M,D, H,M,S] Mar 13
           [ 11, 6, 2, 0, 0],  # End   of DST [ M,D, H,M,S] Nov 6
           [         1, 0, 0]  # DST Adjust   [      H,M,S] +1 hour
       ]
        utc = tc.UtcTime()
        loc = tc.LocalTime(tz)
        current_time = f"{tc.Readable(loc)}"
        self.logging.info(f"Current Date/Time: {current_time}")
        return current_time


    async def close(self):
        self.logger.info("Closing Server")
        self.server.close()
        await self.server.wait_closed()
        self.logger.info("Server Closed")

    def run(self):
        try:
            asyncio.run(self.main())
        finally:
            self.logger.info("Closing Server")
            asyncio.run(self.close())
            self.logger.info("Server Closed")
            _ = asyncio.new_event_loop()


if __name__ == '__main__':
    AsyncHTTPServer().run()
