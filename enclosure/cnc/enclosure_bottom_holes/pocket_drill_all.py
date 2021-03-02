from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

feedrate = 80.0
fileName = 'layout1.dxf'
depth = 0.295 
startZ = 0.0
safeZ = 0.5
overlap = 0.5
overlapFinish = 0.5
maxCutDepth = 0.08
toolDiam =  0.125 
direction = 'ccw'
startDwell = 1.0


smallHoleCoolingPause = 2.0
smallHoleOversize = 0.005
smallHoleLayerList = ['6-32_through_hole'] 

bigHoleLayerList = [
    '10-32_insert_hole', 
    '6-32_insert_hole', 
    '8-32_insert_hole',
    '8-32_through_hole'
    ]

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

param = {
        'fileName'       : fileName,
        'layers'         : smallHoleLayerList, 
        'components'     : True,
        'depth'          : depth,
        'startZ'         : startZ,
        'safeZ'          : safeZ,
        'overlap'        : overlap,
        'overlapFinish'  : overlapFinish,
        'maxCutDepth'    : maxCutDepth,
        'toolDiam'       : toolDiam-smallHoleOversize,
        'direction'      : direction,
        'coolingPause'   : smallHoleCoolingPause,
        'startDwell'     : startDwell,
        }

pocket = cnc_dxf.DxfCircPocket(param)
prog.add(pocket)

param = {
        'fileName'       : fileName,
        'layers'         : bigHoleLayerList, 
        'components'     : True,
        'depth'          : depth,
        'startZ'         : startZ,
        'safeZ'          : safeZ,
        'overlap'        : overlap,
        'overlapFinish'  : overlapFinish,
        'maxCutDepth'    : maxCutDepth,
        'toolDiam'       : toolDiam,
        'direction'      : direction,
        'startDwell'     : startDwell,
        }
pocket = cnc_dxf.DxfCircPocket(param)
prog.add(pocket)

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
