import factory

from .utils import rbool


class Maybe(factory.LazyAttribute):
    def evaluate(self, instance, step, extra):
        if rbool():
            lambda: super().evaluate(instance, step, extra)
        return None
