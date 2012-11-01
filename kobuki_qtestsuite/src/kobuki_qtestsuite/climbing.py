import os
from QtCore import Signal, Slot
import roslib
roslib.load_manifest('kobuki_qtestsuite')
import rospy

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QWidget
from rqt_py_common.extended_combo_box import ExtendedComboBox

from geometry_msgs.msg import Twist

# Local resource imports
import resources.common
import resources.climbing
from .climbing_widget import ClimbingWidget

class Climbing(Plugin):

    def __init__(self, context):
        super(Climbing, self).__init__(context)
        # give QObjects reasonable names
        self.setObjectName('Climbing')

        # create QWidget
        self._widget = ClimbingWidget()

        # give QObjects reasonable names
        self._widget.setObjectName('ClimbingUi')
        # add widget to the user interface
        context.add_widget(self._widget)

    def shutdown_plugin(self):
        self._widget.shutdown()

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    ##########################################################################
    # Slot Callbacks
    ##########################################################################

    #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure it
        # Usually used to open a dialog to offer the user a set of configuration