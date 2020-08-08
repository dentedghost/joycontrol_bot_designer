import logging
import asyncio
import random
from curl_client import CurlClient
import signal

from aioconsole import ainput
from joycontrol.controller_state import button_push

logger = logging.getLogger(__name__)


# input
class InputTimeoutError(Exception):
    pass


def interrupted(signum, frame):
    raise InputTimeoutError


signal.signal(signal.SIGALRM, interrupted)


##


class CCLI():
    def __init__(self):
        # if self.controller == Controller.PRO_CONTROLLER:
        self.available_buttons = {'y', 'x', 'b', 'a', 'r', 'zr',
                                  'minus', 'plus', 'r_stick', 'l_stick', 'home', 'capture',
                                  'down', 'up', 'right', 'left', 'l', 'zl'}
        # elif self.controller == Controller.JOYCON_R:
        #     self._available_buttons = {'y', 'x', 'b', 'a', 'sr', 'sl', 'r', 'zr',
        #                                'plus', 'r_stick', 'home'}
        # elif self.controller == Controller.JOYCON_L:
        #     self._available_buttons = {'plus', 'l_stick', 'capture',
        #                                'down', 'up', 'right', 'left', 'sr', 'sl', 'l', 'zl'}
        self.available_sticks = {'ls', 'rs'}
        self.script = False

    async def write(self, msg):
        with open('storage/message.txt', 'a') as f:
            f.write(msg + '\n')

    async def get(self, file):
        with open('storage/' + file, 'r') as f:
            result = list()
            for line in f.readlines():
                line = line.strip()
                if not len(line) or line.startswith('#'):
                    continue
                result.append(line.lower())
            return result

    async def clean(self, file):
        with open('storage/' + file, 'w+') as f:
            return f.truncate()

    async def runCommand(self):

        # command.txt
        user_input = await self.get('command.txt')
        if not user_input:
            return
        await self.clean('command.txt')

        for command in user_input:
            cmd, *args = command.split()

            if cmd == 'run':
                self.script = True
            elif cmd == 'stop':
                self.script = False
            elif cmd == 'off' or cmd == 'on':
                print('On/Off')
            else:
                await self.pressButton(command)

    async def button_push(self, *buttons, sec=0.3):
        if not buttons:
            raise ValueError('No Buttons were given.')

        for button in buttons:
            # push button
            endpoint = "controller/button/press/" + button
            curl_request = CurlClient(endpoint)
            curl_request.curl_patch()  # Slight delay between requests

        # send report
        # await controller_state.send()
        await asyncio.sleep(sec)

        for button in buttons:
            # release button
            endpoint = "controller/button/release/" + button
            curl_request = CurlClient(endpoint)
            curl_request.curl_patch()

        # send report
        # await controller_state.send()

    async def pressButton(self, *commands):
        for command in commands:
            print(f'commands {commands}')
            cmd, *args = command.split()

            print(f'cmd args {cmd} {args}')
            if cmd in self.available_sticks:
                dir, sec, *sth = args[0].split(',')
                await self.cmd_stick(cmd, dir, sec)
            elif cmd in self.available_buttons:
                await self.button_push(cmd)
            elif cmd.isdecimal():
                await asyncio.sleep(float(cmd) / 1000)
            elif cmd == 'wait':
                await asyncio.sleep(float(args[0]) / 1000)
            elif cmd == 'waitrandom':
                if args[0].isdecimal and args[1].isdecimal:
                    random_wait = random.randint(int(args[0]), (int(args[1]) + 1))
                    print(f'rand wait {random_wait}')
                    await asyncio.sleep(float(random_wait) / 1000)
                else:
                    print(f'command waitrandom args need to be int {args[0]} {args[1]}')
            elif cmd == 'print':
                print(args[0])
            else:
                print(f'command {cmd} not found')

    def set_stick(self, stick, direction, value=None):

        if direction == 'reset':
            stick.set_center()
        elif direction == 'up':
            stick.set_up()
        elif direction == 'down':
            stick.set_down()
        elif direction == 'left':
            stick.set_left()
        elif direction == 'right':
            stick.set_right()
        #
        # elif direction in ('h', 'horizontal'):
        #    if value is None:
        #        raise ValueError(f'Missing value')
        #    try:
        #        val = int(value)
        #    except ValueError:
        #        raise ValueError(f'Unexpected stick value "{value}"')
        #    stick.set_h(val)
        # elif direction in ('v', 'vertical'):
        #    if value is None:
        #        raise ValueError(f'Missing value')
        #    try:
        #        val = int(value)
        #    except ValueError:
        #        raise ValueError(f'Unexpected stick value "{value}"')
        #    stick.set_v(val)
        #
        else:
            raise ValueError(f'Unexpected argument "{direction}"')
        return f'{stick.__class__.__name__} was set to ({stick.get_h()}, {stick.get_v()}).'

    async def cmd_stick(self, side, direction, release_sec=0.0):
        """
        stick - Command to set stick positions.
        :param side: 'l', 'left' for left control stick; 'r', 'right' for right control stick
        :param direction: 'center', 'up', 'down', 'left', 'right';
               'h', 'horizontal' or 'v', 'vertical' to set the value directly to the "value" argument
        :param value: horizontal or vertical value
        """

        try:
            val = float(release_sec)
        except ValueError:
            raise ValueError(f'Unexpected stick release_sec "{release_sec}"')
        if side == 'ls':
            stick = self.controller_state.l_stick_state
            self.set_stick(stick, direction)
            await self.stickSend(stick, val / 1000)
        elif side == 'rs':
            stick = self.controller_state.r_stick_state
            self.set_stick(stick, direction)
            await self.stickSend(stick, val / 1000)
        else:
            raise ValueError('Value of side must be "ls" or "rs"')

    async def stickOn(self, stick, release_sec):
        await self.controller_state.send()
        await asyncio.sleep(release_sec)

    async def stickOff(self, stick):
        stick.set_center()
        await self.controller_state.send()
        # await asyncio.sleep(0.05)

    async def stickSend(self, stick, release_sec):
        await self.stickOn(stick, release_sec)
        if release_sec is 0.0:
            test = 0
        else:
            await self.stickOff(stick)

    async def readCommand(self, file):
        user_input = await self.get(file)
        if not user_input:
            return
        await self.clean(file)

    def isCommand(self, cmd):
        return (cmd in
                self.available_sticks or
                cmd in self.available_buttons or
                cmd.isdecimal() or
                cmd == 'print' or
                cmd == 'wait' or
                cmd == 'waitrandom')

    def forCheck(self, n, user_input):
        commands = []
        until = -1
        for i in range(len(user_input)):
            if i <= n or i <= until:
                continue

            cmd, *args = user_input[i].split()

            if cmd == 'for':
                for _ in range(int(args[0])):
                    until, forcmd = self.forCheck(i, user_input)
                    for get in forcmd:
                        commands.append(get)
            elif cmd == 'next':
                return i, commands
            elif self.isCommand(cmd):
                commands.append(user_input[i])
            else:
                print(f'command {cmd} not found')

    async def runScript(self):
        user_input = await self.get('script.txt')
        if not user_input:
            return
        await self.clean('script.txt')

        commands = []
        until = -1
        for i in range(len(user_input)):
            await self.runCommand()
            if self.script == False:
                return

            if i <= until:
                continue

            cmd, *args = user_input[i].split()
            if cmd == 'for':
                for _ in range(int(args[0])):
                    until, forcmd = self.forCheck(i, user_input)
                    for get in forcmd:
                        commands.append(get)
            elif self.isCommand(cmd):
                commands.append(user_input[i])
            elif cmd == 'test':
                abc = []
                abc.append('l')
                abc.append('r')
                await button_push(self.controller_state, *abc)
            else:
                print(f'commands {cmd} not found')

        for command in commands:
            await self.runCommand()
            if self.script == False:
                return

            await self.pressButton(command)

        self.script = False

    async def get_txt(self):
        await self.runCommand()
        if self.script == True:
            await self.runScript()

    async def get_cmd(self):
        signal.alarm(1)
        try:
            ainput(prompt='cmd >>')
        except InputTimeoutError:
            print(f'timeout')

        signal.alarm(0)

    async def run(self):
        while True:
            await asyncio.gather(self.get_txt(), self.get_cmd())
