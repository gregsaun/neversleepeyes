###############################################################################
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
###############################################################################

# TODO :
#  - more methods like capture()

# Import
from __future__ import print_function
import gphoto2 as gp
import logging
import pprint


class Camera(object):
    """ This represent a camera that can be manipulated (taking a photo, getting summary, etc.)

    Attributes:
        dummy: todo description
    """

    cam_connected = False


    def __init__(self):
        """ Return a new MyClass object. """
        logging.basicConfig(
            format='%(levelname)s: %(name)s: %(message)s', level=logging.ERROR)
        gp.check_result(gp.use_python_logging())


    def __del__(self):
        self.disconnect()


    def __get_widget(self, camera_config):
        """ Return dictionary containing all widget section values"""
        cam_info = dict()

        child_count = gp.check_result(gp.gp_widget_count_children(camera_config))

        if child_count < 1:
            return cam_info

        for n in range(child_count):
            child = gp.check_result(gp.gp_widget_get_child(camera_config, n))
            #label = gp.check_result(gp.gp_widget_get_label(child))
            name = gp.check_result(gp.gp_widget_get_name(child))
            child_type = gp.check_result(gp.gp_widget_get_type(child))

            if child_type == gp.GP_WIDGET_SECTION:
                cam_info[name] = self.__get_widget(child)
            else:
                value = gp.check_result(gp.gp_widget_get_value(child))
                cam_info[name] = value

        return cam_info


    def connect(self):
        """ Return true if connection to camrea is good """
        try:
            self.context = gp.gp_context_new()
            self.cam = gp.check_result(gp.gp_camera_new())
            gp.check_result(gp.gp_camera_init(self.cam, self.context))
            self.cam_connected = True
            return True

        except gp.GPhoto2Error as ex:
            self.disconnect()
            self.cam_connected = False

            if ex.code == gp.GP_ERROR_CAMERA_BUSY:
                raise ValueError("Unable to connect camera. Camera is busy!")
            elif ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                raise ValueError("Unable to connect camera. Camera not found!")
            else:
                raise ValueError("Unable to connect camera. Unknown error!")

            return False


    def disconnect(self):
        """ Return true if disconnection of the camera is good"""
        if self.cam_connected:
            gp.gp_camera_exit(self.cam, self.context)
            self.cam_connected = False


    def get_info(self):
        """ Return dictionary containing all camera info"""
        cam_config = gp.check_result(gp.gp_camera_get_config(self.cam, self.context))
        cam_info = self.__get_widget(cam_config)
        return cam_info


cam = Camera()
cam.connect()
cam_info = cam.get_info()
print(cam_info["status"]["manufacturer"])
pprint.pprint(cam_info)
cam.disconnect()
