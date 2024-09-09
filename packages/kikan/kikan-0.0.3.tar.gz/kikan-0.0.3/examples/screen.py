from kikan.states import State
from kikan.signals import Signal
from kikan import engine
from kikan.entity import MetaEntity
from kikan.utils import Logger
from random import random

on_inc = Signal()
n = State(0)


class Void(MetaEntity):
    def on_update(dt) -> None:
        if random() > 0.95:
            n.set(random())
        elif random() > 0.8:
            on_inc.emit()

    @n.affects
    @staticmethod
    def state() -> None:
        Logger.print("value upd")

    @on_inc
    @staticmethod
    def signal() -> None:
        Logger.print("signal")

    @on_inc
    @n.affects
    @staticmethod
    def print_state() -> None:
        Logger.print("value", n.get())


engine.start()
