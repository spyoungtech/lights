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

    def brighter(self, increment=10, light=None, group=None):
        if light:
            l = self._lights[light]
            l.brightness = l.brightness - increment
            return
        if group:
            g = self._bridge.groups[group]
            g.brightness = g.brightness - increment
        for light in self._lights:
            light.brightness = light.brightness + increment

    def dim(self, increment=10, light: int=None, group: int=None):
        """
        Dim the lights. A light or group can be specified. If no light or group is specified, dims all lights.

        ex::

            lights dim --light=1


        :param light: the light number to dim. (optional)
        :param increment: change in brightness
        :param group: the group number to dim. (optional)
        :return:
        """
        if light:
            l = self._lights[light]
            l.brightness = l.brightness - increment
            return
        if group:
            g = self._bridge.groups[group]
            g.brightness = g.brightness - increment
        for light in self._lights:
            light.brightness = light.brightness - increment

    def brightness(self, new_brightness=None, light=None, group=None):
        """
        Check or change the brightness of the lights. A light or group can be specified. If no light or group is
        specified, dims all lights.

        :param new_brightness:
        :param light:
        :param group:
        :return:
        """

    def list(self):
        """
        List the lights connected to the phillips hue bridge

        :return:
        """
        for index, light in enumerate(self._lights, start=1):
            print(index, light)

    def groups(self):
        """
        List the light groups on the Phillips Hue Bridge

        :return:
        """
        for index, group in enumerate(self._bridge.groups):
            print(index, group)

def main():
    fire.Fire(Lights)


if __name__ == '__main__':
    main()