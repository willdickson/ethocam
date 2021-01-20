import os
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_laser

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())

dxfFileName = sys.argv[1]

param = {
        'fileName'    :  dxfFileName,
        'layers'      :  ['vector'],
        'dxfTypes'    :  ['LINE','ARC', 'CIRCLE'],
        'laserPower'  :  600,
        'feedRate'    :  10,
        'convertArcs' :  True,
        'startCond'   : 'minX',
        'direction'   : 'ccw',
        'ptEquivTol'  :  0.4e-3,
        }

vectorCut = cnc_laser.VectorCut(param)
prog.add(vectorCut)

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, ext = os.path.splitext(dxfFileName)
ngcFileName = '{0}.ngc'.format(baseName)
prog.write(ngcFileName)
