#!/usr/bin/env python
# *_* coding: utf-8 *_*

"""brainfuck kernel class module"""

from ipykernel.kernelbase import Kernel


class jansbrainfuckkernel(Kernel):
    """brainfuck kernel"""

    implementation = "IPython"
    implementation_version = "8.11.0"
    language = "brainfuck"
    language_version = "0.1"
    language_info = {
        "name": "brainfuck",
        "mimetype": "application/brainfuck",
        "file_extension": ".bf",
    }
    banner = "Brainfuck kernel"
    _allow_stdin = True

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=True
    ):
        if not silent:
            solution = ""
            bf_chars = ["+", "-", "<", ">", ".", ",", "[", "]"]
            bf_arr = [0]
            ci = 0
            loop_table = {}
            loop_stack = []
            user_input = []

            for i, cmd in enumerate(code):
                match cmd:
                    case "[":
                        loop_stack.append(i)
                    case "]":
                        loop_begin = loop_stack.pop()
                        loop_table[loop_begin] = i
                        loop_table[i] = loop_begin

            i = 0
            while i < len(code):
                cmd = code[i]

                if cmd in bf_chars:
                    match cmd:
                        case "+":
                            bf_arr[ci] += 1
                            if bf_arr[ci] == 256:
                                bf_arr[ci] = 0
                        case "-":
                            bf_arr[ci] -= 1
                            if bf_arr[ci] == -1:
                                bf_arr[ci] = 255
                        case "<":
                            ci -= 1
                        case ">":
                            ci += 1
                            if ci == len(bf_arr):
                                bf_arr.append(0)
                        case ".":
                            solution += chr(bf_arr[ci])
                        case ",":
                            if user_input == []:
                                user_input = list(self.raw_input())
                            bf_arr[ci] = ord(user_input.pop(0))
                        case "[":
                            if bf_arr[ci] == 0:
                                i = loop_table[i]
                        case "]":
                            if bf_arr[ci]:
                                i = loop_table[i]

                i += 1

            stream_content = {"name": "stdout", "text": solution}
            self.send_response(self.iopub_socket, "stream", stream_content)

        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }
