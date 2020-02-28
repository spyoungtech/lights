import ast
import collections
import os

from phue import Bridge
import fire
import json
import logging
import sys

logger = logging.getLogger('Lights')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

COLORS = {
    'blue': (0, 0),
    'red': (1, 0),
    'green': (0.5, 0.5),
    'blue sky': (0.3773, 0.2514),
    'foliage': (0.3372, 0.4220),
    'bluish green': (0.2608, 0.3430),
    'orange': (0.5060, 0.4070),
}


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

    def brighter(self, increment=20, light=None, group=None):
        if light:
            l = self._lights[light]
            new_brightness = min(255, l.brightness + increment)
            l.brightness = new_brightness
            return
        if group:
            g = self._bridge.groups[group]

            new_brightness = min(255, g.brightness + increment)
            g.brightness = new_brightness
            return
        for light in self._lights:
            new_brightness = min(255, light.brightness + increment)
            light.brightness = new_brightness

    def dim(self, increment=10, light: int = None, group: int = None):
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
            new_brightness = max(0, l.brightness - increment)
            l.brightness = new_brightness
            return
        if group:
            g = self._bridge.groups[group]
            new_brightness = max(0, g.brightness - increment)
            g.brightness = new_brightness
            return
        for light in self._lights:
            new_brightness = max(0, light.brightness - increment)
            light.brightness = new_brightness

    def brightness(self, new_brightness=None, light=None, group=None):
        """
        Check or change the brightness of the lights. A light or group can be specified. If no light or group is
        specified, dims all lights.

        :param new_brightness:
        :param light:
        :param group:
        :return:
        """
        if light:
            l = self._lights[light]
            l.brightness = new_brightness
            return
        if group:
            g = self._bridge.groups[group]
            g.brightness = new_brightness
            return

        for light in self._lights:
            light.brightness = new_brightness

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

    def color(self, new_color, light=None, group=None):
        if isinstance(new_color, type('')) and new_color in COLORS:
            new_color = COLORS[new_color]

        if light:
            l = self._lights[light]
            l.xy = new_color
            return
        if group:
            g = self._bridge.groups[group]
            g.xy = new_color
            return
        for l in self._lights:
            l.xy = new_color

    def save(self, name):
        data = {
            light.light_id: {'brightness': light.brightness, 'xy': light.xy, 'on': light.on} for light in self._lights
        }
        homedir = os.path.expanduser('~')

        profiles_directory = os.path.join(homedir, '.lights_profiles')
        if not os.path.exists(profiles_directory):
            os.mkdir(profiles_directory)
        profile_path = os.path.join(profiles_directory, name + '.json')
        logger.info(f"Saving profile {name} to {profile_path}")
        with open(profile_path, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self, name):
        homedir = os.path.expanduser('~')
        profiles_directory = os.path.join(homedir, '.lights_profiles')
        if not os.path.exists(profiles_directory):
            os.mkdir(profiles_directory)
        profile_path = os.path.join(profiles_directory, name + '.json')
        with open(profile_path) as f:
            data = json.load(f)
        for l in self._lights:
            light_data = data.get(str(l.light_id))
            if not light_data:
                continue
            l.on = light_data['on']
            if not l.on:
                continue
            l.brightness = light_data['brightness']
            l.xy = light_data['xy']


def main():
    fire.Fire(Lights)


if __name__ == '__main__':
    main()
