# -*- coding: utf-8 -*-

import utilFile
import utilParse
import logger


# gets file content from a bagbrother file
def getFileContent(path):
    Lines = utilFile.ReadIn_lines(path)
    if len(Lines) <= 0:
        # for readability
        errMessage = "Error getting bagbrother file|check parameters addons and saved variables"
        logger.Log("bagnonSoup","getFileContent","Critical", errMessage, LogAndKill = True)
        # exit program
    # clean the ropes of unneccessary control chars
    for i in range(len(Lines)):
        Lines[i] = utilParse.removeControlCharacters(Lines[i])
    return Lines