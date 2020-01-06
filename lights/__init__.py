from phue import Bridge
import fire


class Lights(object):
    """
    Control phillips hue lights.
    """

    def __init__(self, ip=None):
        if ip:
            self._bridge = Bridge(ip=ip)
        else:
            self._bridge = Bridge()

    @property
    def _lights(self):
        return self._bridge.lights

    def on(self, group=None):
        if group:
            ...
        for light in self._lights:
            light.on = True

    def off(self, group=None):
        for light in self._lights:
            light.on = False

    def brighter(self, increment=10, group=None):
        for light in self._lights:
            light.brightness = light.brightness + increment

    def dim(self, increment=10, group=None):
        for light in self._lights:
            light.brightness = light.brightness - increment


def main():
    fire.Fire(Lights)


if __name__ == '__main__':
    main()