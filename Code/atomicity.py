# -*- coding: utf-8 -*-


"""
atomicity checks to ensure that all files are available
"""

import parameters
import utilFile
import logger

def Check(params):
    params = parameters.Ledgerman()
    PathList = params.GETALLPATHS()
    for directory in PathList:
        for path in directory:
            if not utilFile.Exists(path):
                errMessage = "Could Not Find File at:" + path
                logger.Log("atomicity","Check","Critical", errMessage, LogAndKill = True)
    return True
  