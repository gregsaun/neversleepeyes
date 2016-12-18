################################################################################
#
# Description:
# Provide simplified camera interface. The camera is controlled with gphoto2
#
# Author: Gregoire Saunier
# Website: www.ekunn.com
# Creation date: 2016.12.18
#
# Resources:
#   - http://www.gphoto.org
#   - https://github.com/jim-easterbrook/python-gphoto2
#
################################################################################

# TODO :
#  - Switch to non object usage of python-gphoto2 in order to be closer to libgphoto2 API
#  - Summary should be a dict info like manufacturer, model, sn

# Import
from __future__ import print_function
import gphoto2 as gp
import logging


class Camera(object):
    """ This represent a camera that can be manipulated (taking a photo, getting summary, etc.)

    Attributes:
        name: name of a person (string)
    """

    context = None
    cam = None

    def __init__(self):
        """ Return a new MyClass object. """
        logging.basicConfig(
            format='%(levelname)s: %(name)s: %(message)s', level=logging.ERROR)
        gp.check_result(gp.use_python_logging())

    def __del__(self):
        self.disconnect()

    def connect(self):
        """ Return true if connection to camrea is good """
        self.context = gp.Context()
        self.cam = gp.Camera()
        try:
            self.cam.init(self.context)
        except gp.GPhoto2Error as ex:
            if ex.code == gp.GP_OK:
                return True
            else:
                if ex.code == gp.GP_ERROR_CAMERA_BUSY:
                    raise ValueError("Unable to connect camera. Camera is busy!")
                elif ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                    raise ValueError("Unable to connect camera. Camera not found!")
                else:
                    raise ValueError("Unable to connect camera. Unknown error!")
                return False

    def disconnect(self):
        """ Return true if disconnection of the camera is good"""
        self.cam.exit(self.context)

    def get_summary(self):
        """ Return multiline string containing summary of the camera"""
        return self.cam.get_summary(self.context)


cam = Camera()

cam.connect()
print(cam.get_summary())
cam.disconnect()
