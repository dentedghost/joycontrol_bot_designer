from aioconsole import ainput
import asyncio
from copy import deepcopy
import importlib
import logging
import operator
import os
import random
import re
import signal


from curl_client import CurlClient
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
        self.available_cmds = {'print', 'buttonrandom', 'waitrandom', }
        self.script = False

    async def write(self, msg):
        with open('storage/message.txt', 'a') as f:
            f.write(msg + '\n')


    async def calculate_if(self, path, equation):
        print(f'calculate_if {path}, {equation}')
        count = len(equation)
        print(f'{count}')
        # Check for operation and expected
        if count == 1:
            actual = equation[0]

            if 'script' in actual:
                print("Inside calculate_if script for 1")
                # Execute and return scripts result
                actual_name = actual.split('.')[0]
                module = importlib.import_module('.' + actual_name, package='scripts')
                result = module.script()
                print(result)
                return result
            else:
                print("Invalid single equation")
                return False
        elif count == 3:
            actual = equation[0]
            operation = equation[1]
            expected = equation[2]

            print(actual)
            print(type(actual))

            if 'script' in actual:
                print("Inside calculate_if script for 3: 1")
                # Execute and return scripts result
                actual_name = actual.split('.')[0]
                module = importlib.import_module('.' + actual_name, package='scripts')
                actual_result = module.script()
                print(actual_result)
                print(type(actual_result))
            else:
                actual_result = actual

            if 'script' in expected:
                print("Inside calculate_if script for 3:3")
                # Execute and return scripts result
                expected_name = expected.split('.')[0]
                module = importlib.import_module('.' + expected_name, package='scripts')
                expected_result = module.script()
                print(expected_result)
                print(type(expected_result))
            else:
                expected_result = expected

            allowed_operators = {
                '==': operator.eq,
                '!=': operator.ne,
                '+': operator.add,
                '-': operator.sub,
                '*': operator.mul,
                '/': operator.truediv,  # use operator.div for Python 2
                '<': operator.lt,
                '<=': operator.le,
                '>': operator.gt,
                '>=': operator.ge,
            }

            print(operation)
            # https://stackoverflow.com/questions/707674/how-to-compare-type-of-an-object-in-python
            if type(actual_result) == type(expected_result):
                print(allowed_operators[operation])
                result = allowed_operators[operation](actual_result, expected_result)
                print(result)
                return result
            else:
                print("Non Matching Type comparison")
                return False

        else:
            print("Invalid comparison")
            return False
        # Possibly an error




        # variable_replacements = ''
        # if len(kwargs):
        #     variable_replacements = self.lower_dict_variables(kwargs)
        # #
        # # for k, v in variable_replacements.items():
        # #     print('keyword argument: {} = {}'.format(k, v))
        #
        # with open(path + file, 'r') as f:
        #
        #     result = list()
        #     for line in f.readlines():
        #         line = line.strip()
        #         line = line.lower()
        #         if not len(line) or line.startswith('#'):
        #             continue
        #         if len(variable_replacements):
        #             line = self.multiple_replace(variable_replacements, line)
        #         result.append(line)
        #     return result

    async def get(self, path, file, **kwargs):

        variable_replacements = ''
        if len(kwargs):
            variable_replacements = self.lower_dict_variables(kwargs)
        #
        # for k, v in variable_replacements.items():
        #     print('keyword argument: {} = {}'.format(k, v))

        with open(path + file, 'r') as f:

            result = list()
            for line in f.readlines():
                line = line.strip()
                line = line.lower()
                if not len(line) or line.startswith('#'):
                    continue
                if len(variable_replacements):
                    line = self.multiple_replace(variable_replacements, line)
                result.append(line)
            return result

    # https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex-in-python
    @staticmethod
    def multiple_replace(replacements, text):
        # Create a regular expression  from the dictionary keys:
        regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
        # For each match, look-up corresponding value in dictionary:
        return regex.sub(lambda mo: replacements[mo.string[mo.start():mo.end()]], text)

    @staticmethod
    def lower_dict_variables(d):
        new_dict = dict(('{' + k.lower() + '}', v.lower()) for k, v in d.items())
        return new_dict

    async def clean(self, path, file):
        with open(path + file, 'w+') as f:
            return f.truncate()

    async def runCommand(self):

        # command.txt
        user_input = await self.get('storage/', 'command.txt')
        if not user_input:
            return
        await self.clean('storage/', 'command.txt')

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

        print(f'button_push buttons {buttons}')
        for button in buttons:
            # push button
            # print(f'button_push button {button}')
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
            # print(f'commands {commands}')
            cmd, *args = command.split(None, 1)

            # print(f'cmd args {cmd} {args}')
            if cmd in self.available_sticks:
                dir, sec, *sth = args[0].split(',')
                await self.cmd_stick(cmd, dir, sec)
            elif cmd in self.available_buttons:
                await self.button_push(cmd)
            elif cmd == 'buttonrandom':
                buttons = [x.strip() for x in args[0].split(',')]
                button_count = len(buttons)
                button_index = random.randint(0, button_count-1)
                chosen_button = buttons[button_index]
                # print(f'buttons index chosen {buttons} {button_index},{chosen_button}')
                if chosen_button and not chosen_button.isspace():
                    print(f'buttonrandom button  {chosen_button}')
                    await self.button_push(chosen_button)
            elif cmd.isdecimal():
                await asyncio.sleep(float(cmd) / 1000)
            elif cmd == 'print':
                # print(args[0])
                pass
            elif cmd == 'wait':
                await asyncio.sleep(float(args[0]) / 1000)
            elif cmd == 'waitrandom':
                start_time, end_time = args[0].split()
                if start_time.isdecimal and end_time.isdecimal:
                    random_wait = random.randint(int(start_time), (int(end_time) + 1))
                    print(f'rand wait {random_wait}')
                    await asyncio.sleep(float(random_wait) / 1000)
                else:
                    print(f'command waitrandom args need to be int {start_time} {end_time}')
            elif cmd == 'helper':
                continue
            elif cmd == 'if':
                continue
            else:
                print(f'In pressButton: command {cmd} not found')

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

    async def readCommand(self, path, file):
        user_input = await self.get(path, file)
        if not user_input:
            return
        await self.clean(path, file)

    def isCommand(self, cmd):
        return (cmd in
                self.available_sticks or
                cmd in self.available_buttons or
                cmd.isdecimal() or
                cmd or
                cmd in self.available_cmds)

    async def forCheck(self, n, user_input):
        # TODO: Send a splice instead of relooping
        commands = []
        until = -1
        for i in range(len(user_input)):
            if i <= n or i <= until:
                continue

            cmd, *args = user_input[i].split()

            if cmd == 'for':
                # Allow the ability to skip a FOR loop when set to Zero
                if int(args[0]) == 0:
                    until, forcmd = await self.forCheck(i, user_input)
                else:
                    for _ in range(int(args[0])):
                        until, forcmd = await self.forCheck(i, user_input)
                        for get in forcmd:
                            commands.append(get)
            elif cmd == 'helper':
                # print(f'In forCheck: helper {args[0]}')
                helper_input = await self.get(
                    'helpers/',
                    args[0],
                    **dict(arg.split('=') for arg in args[1:]))
                # print(f'In forCheck: helper_input {helper_input}')
                helpercmd = await self.helpersCheck(helper_input)
                for get in helpercmd:
                    commands.append(get)
            elif cmd == 'if':
                # Process If Statement
                next_if_result = await self.calculate_if(
                    'scripts/',
                    args)
                # Fix recursion issue
                next_if_result = deepcopy(next_if_result)

                until, forcmd = await self.ifCheck(i, user_input, next_if_result)
                print("returned from if check")
                for get in forcmd:
                    commands.append(get)
            elif cmd == 'next':
                return i, commands
            elif self.isCommand(cmd):
                commands.append(user_input[i])
            else:
                print(f'In forCheck: command {cmd} not found')

        # TODO:Need to add a fail if no next

    async def helpersCheck(self, user_input):
        # print(f"Entering helpersCheck")
        commands = []
        until = -1
        for i in range(len(user_input)):

            if i <= until:
                continue

            cmd, *args = user_input[i].split()
            if cmd == 'for':
                # Allow the ability to skip a FOR loop when set to Zero
                if int(args[0]) == 0:
                    until, forcmd = await self.forCheck(i, user_input)
                else:
                    for _ in range(int(args[0])):
                        until, forcmd = await self.forCheck(i, user_input)
                        for get in forcmd:
                            commands.append(get)
            #  Maybe add check for helper here?
            # Might just need to insert into user_input
            elif cmd == 'helper':
                helper_input = await self.get(
                    'helpers/',
                    args[0],
                    **dict(arg.split('=') for arg in args[1:]))
                helpercmd = await self.helpersCheck(helper_input)
                for get in helpercmd:
                    commands.append(get)
            elif cmd == 'if':
                # Process If Statement
                next_if_result = await self.calculate_if(
                    'scripts/',
                    args)
                # Fix recursion issue
                next_if_result = deepcopy(next_if_result)

                until, forcmd = await self.ifCheck(i, user_input, next_if_result)
                print("returned from if check")
                for get in forcmd:
                    commands.append(get)
            elif self.isCommand(cmd):
                commands.append(user_input[i])
            
            else:
                print(f'In helpersCheck: commands {cmd} not found')

        return commands
    # Issue with variable scope with recursion
    # https://stackoverflow.com/questions/24572089/trouble-with-variable-scope-in-recursive-function-python/24572213
    async def ifCheck(self, n, user_input, if_result):
        print("Inside ifCheck")
        if_result = deepcopy(if_result)
        # TODO: Send a splice instead of relooping
        commands = []
        until = -1
        else_found = False
        length = len(user_input)
        print(f'Length {length}')
        for i in range(len(user_input)):

            if i <= n or i <= until:
                continue

            print(f' i {i}  until {until}')

            print(f'else_found: {else_found}')

            cmd, *args = user_input[i].split()

            if cmd == 'else':
                else_found = True
                print("Else Found")
            elif cmd == 'for':
                # Allow the ability to skip a FOR loop when set to Zero
                if int(args[0]) == 0:
                    until, forcmd = await self.forCheck(i, user_input)
                else:
                    for _ in range(int(args[0])):
                        until, forcmd = await self.forCheck(i, user_input)
                        for get in forcmd:
                            commands.append(get)
            elif cmd == 'helper':
                # print(f'In forCheck: helper {args[0]}')
                helper_input = await self.get(
                    'helpers/',
                    args[0],
                    **dict(arg.split('=') for arg in args[1:]))
                # print(f'In forCheck: helper_input {helper_input}')
                helpercmd = await self.helpersCheck(helper_input)
                for get in helpercmd:
                    commands.append(get)
            # I think we pause look for for since they can't over lap
            # elif cmd == 'next':
            #     return i, commands
            elif cmd == 'if':
                # Process If Statement
                next_if_result = await self.calculate_if(
                    'scripts/',
                    args)
                # Fix Recursion Issue
                next_if_result = deepcopy(next_if_result)

                until, forcmd = await self.ifCheck(i, user_input, next_if_result)
                print(f"returned from if check result: {forcmd}")
                for get in forcmd:
                    commands.append(get)
            elif cmd == 'endif':
                print(f'endif or else: {cmd}')
                return i, commands
            elif self.isCommand(cmd):
                print(f'cmd {cmd} if_result {if_result} else_found {else_found}')
                if if_result and not else_found:
                    print("if_result and not else_found:")
                    commands.append(user_input[i])  # only add if if_result true
                elif else_found and not if_result:
                    print('Else_found and not if_result')
                    commands.append(user_input[i])  # only capture that in else
                else:
                    pass
            else:
                print(f'In forCheck: command {cmd} not found')

        # TODO:Need to add a fail if no next

    def parseCommands(self):
        pass

    async def runScript(self):
        # print(f'In runScript')
        user_input = await self.get('storage/', 'script.txt')
        if not user_input:
            return
        await self.clean('storage/', 'script.txt')
        # print(f'In runScript2')
        commands = []
        until = -1
        # print(f'In runScript3')
        for i in range(len(user_input)):
            await self.runCommand()
            if self.script == False:
                return

            if i <= until:
                continue

            # TODO: Maybe pull out parsing commands
            # until, forcmd = self.parseCommands(i, user_input)
            # for get in forcmd:
            #     commands.append(get)

            cmd, *args = user_input[i].split()
            print(f'cmd {cmd} args {args}')
            if cmd == 'for':
                # Allow the ability to skip a FOR loop when set to Zero
                if int(args[0]) == 0:
                    until, forcmd = await self.forCheck(i, user_input)
                else:
                    for _ in range(int(args[0])):
                        until, forcmd = await self.forCheck(i, user_input)
                        for get in forcmd:
                            commands.append(get)

            #  Maybe add check for helper here?
            # Might just need to insert into user_input
            elif cmd == 'helper':
                # print(f'In runScript: elif cmd helper')
                helper_input = await self.get(
                    'helpers/',
                    args[0],
                    **dict(arg.split('=') for arg in args[1:]))
                # print(f'In runScript: helper helper_input {helper_input}')
                helpercmd = await self.helpersCheck(helper_input)
                for get in helpercmd:
                    commands.append(get)
            elif cmd == 'if':
                # Process If Statement
                next_if_result = await self.calculate_if(
                    'scripts/',
                    args)
                # Fix recursion issue
                next_if_result = deepcopy(next_if_result)

                until, forcmd = await self.ifCheck(i, user_input, next_if_result)
                print("returned from if check")
                for get in forcmd:
                    commands.append(get)
            # Note need to isCommand check last
            elif self.isCommand(cmd):
                commands.append(user_input[i])
            elif cmd == 'test':
                abc = []
                abc.append('l')
                abc.append('r')
                await button_push(self.controller_state, *abc)
            else:
                print(f'In runScript: commands {cmd} not found')

        # print(f'In runScript4')

        for command in commands:
            print(command)
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
            await asyncio.gather(self.get_txt())
