# This file is placed in the Public Domain.


"objects broker"


rpr = object.__repr__


class Broker:

    "Fleet"

    objs = []

    @staticmethod
    def all():
        "return all objects."
        return Broker.objs

    @staticmethod
    def get(orig):
        "return object by matching repr."
        res = None
        for obj in Broker.objs:
            if rpr(obj) == orig:
                res = obj
                break
        return res

    @staticmethod
    def register(obj):
        "add bot."
        Broker.objs.append(obj)


def __dir__():
    return (
        'Broker',
    )
