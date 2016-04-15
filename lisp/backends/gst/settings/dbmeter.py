# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2016 Francesco Ceruti <ceppofrancy@gmail.com>
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QSpinBox, QLabel, \
    QVBoxLayout

from lisp.backends.gst.elements.dbmeter import Dbmeter
from lisp.backends.gst.gi_repository import Gst
from lisp.backends.gst.settings.settings_page import GstElementSettingsPage


class DbmeterSettings(GstElementSettingsPage):

    NAME = 'DbMeter'
    ELEMENT = Dbmeter

    def __init__(self, element_id, **kwargs):
        super().__init__(element_id)
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(0, 0, self.width(), 180)
        self.groupBox.setLayout(QGridLayout())
        self.layout().addWidget(self.groupBox)

        # Time (sec/100) between two levels
        self.intervalSpin = QSpinBox(self.groupBox)
        self.intervalSpin.setRange(1, 1000)
        self.intervalSpin.setMaximum(1000)
        self.intervalSpin.setValue(50)
        self.groupBox.layout().addWidget(self.intervalSpin, 0, 0)

        self.intervalLabel = QLabel(self.groupBox)
        self.intervalLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.layout().addWidget(self.intervalLabel, 0, 1)

        # Peak ttl (sec/100)
        self.ttlSpin = QSpinBox(self.groupBox)
        self.ttlSpin.setSingleStep(10)
        self.ttlSpin.setRange(10, 10000)
        self.ttlSpin.setValue(500)
        self.groupBox.layout().addWidget(self.ttlSpin, 1, 0)

        self.ttlLabel = QLabel(self.groupBox)
        self.ttlLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.layout().addWidget(self.ttlLabel, 1, 1)

        # Peak falloff (unit per time)
        self.falloffSpin = QSpinBox(self.groupBox)
        self.falloffSpin.setRange(1, 100)
        self.falloffSpin.setValue(20)
        self.groupBox.layout().addWidget(self.falloffSpin, 2, 0)

        self.falloffLabel = QLabel(self.groupBox)
        self.falloffLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.layout().addWidget(self.falloffLabel, 2, 1)

        self.retranslateUi()

    def retranslateUi(self):
        self.groupBox.setTitle("DbMeter settings")
        self.intervalLabel.setText("Time between levels (ms)")
        self.ttlLabel.setText("Peak ttl (ms)")
        self.falloffLabel.setText("Peak falloff (unit per time)")

    def load_settings(self, settings):
        if self.id in settings:
            self.intervalSpin.setValue(settings[self.id]["interval"] / Gst.MSECOND)
            self.ttlSpin.setValue(settings[self.id]["peak_ttl"] / Gst.MSECOND)
            self.falloffSpin.setValue(settings[self.id]["peak_falloff"])

    def get_settings(self):
        conf = {self.id: {}}

        if not (self.groupBox.isCheckable() and not self.groupBox.isChecked()):
            conf[self.id]["interval"] = self.intervalSpin.value() * Gst.MSECOND
            conf[self.id]["peak_ttl"] = self.ttlSpin.value() * Gst.MSECOND
            conf[self.id]["peak_falloff"] = self.falloffSpin.value()

        return conf