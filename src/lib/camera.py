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
import os
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

        # Get number of parameters for this level
        child_count = gp.check_result(gp.gp_widget_count_children(camera_config))
        if child_count < 1:
            return cam_info

        # Recursively go through all parameters
        for n in range(child_count):
            child = gp.check_result(gp.gp_widget_get_child(camera_config, n))
            #label = gp.check_result(gp.gp_widget_get_label(child))
            name = gp.check_result(gp.gp_widget_get_name(child))
            child_type = gp.check_result(gp.gp_widget_get_type(child))

            # If it is a section then go recursively inside
            # else -> it is a value then print it
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

        except gp.GPhoto2Error as ex:
            self.disconnect()
            self.cam_connected = False

            if ex.code == gp.GP_ERROR_CAMERA_BUSY:
                raise ValueError("Unable to connect camera. Camera is busy!")
            elif ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                raise ValueError("Unable to connect camera. Camera not found!")
            else:
                raise ValueError("Unable to connect camera. Unknown error!")

        return self.cam_connected


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


    def capture(self, photo_path):
        """ Capture and image and save it to photo_path"""
        try:
            src_path = gp.check_result(gp.gp_camera_capture(self.cam, gp.GP_CAPTURE_IMAGE, self.context))
            print("Photo source path = {:s}{:s}".format(src_path.folder, src_path.name))
            dst_path = os.path.join(photo_path, src_path.name)
            print("Photo target path = {:s}".format(dst_path))
            cam_file = gp.check_result(gp.gp_camera_file_get(
                self.cam, src_path.folder, src_path.name,
                gp.GP_FILE_TYPE_NORMAL, self.context))
            gp.check_result(gp.gp_file_save(cam_file, dst_path))
        except gp.GPhoto2Error as ex:
            self.disconnect()
            self.cam_connected = False
            raise ex


cam = Camera()
cam.connect()
cam_info = cam.get_info()
print(cam_info["status"]["manufacturer"])
pprint.pprint(cam_info)
cam.capture("./")
cam.disconnect()
