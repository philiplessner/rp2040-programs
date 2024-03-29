import socket
import time
from machine import RTC
import uasyncio as asyncio
import logging
from heartbeat import heartbeat
from worldtimeapi import get_local_time


class AsyncHTTPServer():

    def __init__(self, host="0.0.0.0", port=80, backlog=20, timeout=20):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout
        # Set the RTC clock from the Internet
        self.rtc = RTC()
        self.set_RTC_Time()
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
  
    def set_RTC_Time(self):
        # Set up the real time clock from the World Time API server
        year, month, day, hour, minute, second, dow, doy = get_local_time()
        self.rtc.datetime((year, month, day, dow, hour, minute, second, 0))
        print("Local Real Time Clock: {0}-{1}-{2} {4}:{5}:{6}".format(*(self.rtc.datetime())))
    
    def get_RTC_Time(self):
        t = self.rtc.datetime()
        s = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][t[3]]
        s += " {:04}-{:02}-{:02}".format(t[0], t[1], t[2])
        s += " {:02}:{:02}:{:02}".format(t[4], t[5], t[6])
        return s
        
        
    async def main(self):
        self.logger.info("Setting Up Webserver")
        asyncio.create_task(heartbeat(500))
        self.server = await asyncio.start_server(self.serve_client,
                                                 self.host,
                                                 self.port,
                                                 backlog=self.backlog)
        while True:
            await asyncio.sleep(60)

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
