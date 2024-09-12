#!/usr/bin/env python
# *_* coding: utf-8 *_*

"""brainfuck kernel main"""

from ipykernel.kernelapp import IPKernelApp
from .kernel import jansbrainfuckkernel
IPKernelApp.launch_instance(kernel_class=jansbrainfuckkernel)
