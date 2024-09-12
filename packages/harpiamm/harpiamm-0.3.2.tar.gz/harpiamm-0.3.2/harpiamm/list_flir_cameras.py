#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""HARPIA Microscopy Module Python library.

Author: Lukas Kontenis
Copyright (c) 2019-2021 Light Conversion
All rights reserved.
www.lightcon.com
"""
import pkg_resources

spinnaker_ver = None
try:
    spinnaker_ver = pkg_resources.get_distribution('spinnaker-python').version
except pkg_resources.DistributionNotFound:
    print("Spinnaker API not installed")

if spinnaker_ver is not None:
    print("Loading Spinnaker API {:s}...".format(spinnaker_ver),
          end='', flush=True)
    import PySpin
    print('OK')

    system = PySpin.System.GetInstance()
    cam_list = system.GetCameras()

    if len(cam_list) > 0:
        print("Camera list:")
        for ind, cam in enumerate(cam_list):
            cam.Init()
            model_str = cam.DeviceModelName.GetValue()
            sn_str = cam.DeviceSerialNumber.GetValue()
            cam.DeInit()
            print("Cam {:d}, {:s}, SN: {:s}".format(ind, model_str, sn_str))
    else:
        print("No cameras found")
