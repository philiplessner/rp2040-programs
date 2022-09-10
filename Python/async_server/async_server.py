import socket
import time
import uasyncio as asyncio
from heartbeat import heartbeat


class AsyncHTTPServer():

    def __init__(self, host="0.0.0.0", port=80, backlog=5, timeout=20):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout


    async def get_header(self, reader):
        data = ''
        self.header = ''
        while (data != '\r\n'):
            try:
                data = await asyncio.wait_for(reader.readline(), self.timeout)
            except asyncio.TimeoutError:
                print("Reader Timed Out!")
                data = b''
            if data == b'':
                raise OSError
            data = data.decode('utf-8')
            self.header += data


    def request_verb(self):
        lines = self.header.split('\n')
        return lines[0].split()[0]


    def get_filename(self):
        lines = self.header.split('\n')
        return lines[0].split()[1]


    def customize_html(self, content):
        ''' Overide this function in subclass to
            populate fields in html template.
        '''
        custom = content
        return custom

    async def get_request(self, filename, writer):

        if filename == '/':
            filename = './index.html'

        try:
            with open(filename, 'r') as f:
                content = f.read()
            response_header = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
            custom = self.customize_html(content)
            response = response_header + custom
        except OSError:
            response = 'HTTP/1.0 404 NOT FOUND\r\n\r\n'

        writer.write(response.encode('utf-8'))
        print("\nWrote:\n", response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        print("***Client Disconnected***\n")


    async def serve_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"***Client Connected*** from: {addr}")
        await self.get_header(reader)
        print(f"Received:\n {self.header}\nfrom {addr}")
        if (self.request_verb() == 'GET'):
            filename = self.get_filename()
            print('Filename:', filename)
            await self.get_request(filename, writer)


    async def main(self):
        print("Setting Up Webserver")
        asyncio.create_task(heartbeat(500))
        self.server = await asyncio.start_server(self.serve_client, self.host, self.port, backlog=self.backlog)
        while True:
            print("In Loop Listening...")
            await asyncio.sleep(60)


    async def close(self):
        print('Closing server')
        self.server.close()
        await self.server.wait_closed()
        print('Server closed')


    def run(self):
        try:
            asyncio.run(self.main())
        finally:
            asyncio.run(self.close())
            _ = asyncio.new_event_loop()


if __name__ == '__main__':
    AsyncHTTPServer().run()
