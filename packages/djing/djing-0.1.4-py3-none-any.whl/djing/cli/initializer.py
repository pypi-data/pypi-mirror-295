import os
import click

from pathlib import Path


class Initializer:
    def __init__(self, ctx) -> None:
        self.ctx = ctx
