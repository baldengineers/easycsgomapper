"""
This contains new algorithms for new and improved prefab system.
"""
from pf import evaluate, get_normal, rotatePoint
def create(posx, posy, id_num, world_id_num, scale, rotation):
    xy0 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
    x0 = xy0[0]
    y0 = xy0[1]
    z0 = 64
    xy1 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
    x1 = xy1[0]
    y1 = xy1[1]
    z1 = 64
    xy2 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
    x2 = xy2[0]
    y2 = xy2[1]
    z2 = 64
    xy3 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
    x3 = xy3[0]
    y3 = xy3[1]
    z3 = 0
    xy4 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
    x4 = xy4[0]
    y4 = xy4[1]
    z4 = 0
    xy5 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
    x5 = xy5[0]
    y5 = xy5[1]
    z5 = 0
    xy6 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
    x6 = xy6[0]
    y6 = xy6[1]
    z6 = 64
    xy7 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
    x7 = xy7[0]
    y7 = xy7[1]
    z7 = 0
    xy8 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+256, posy*-1*scale+-256), (360 if rotation!=0 else 0)-90*rotation))
    x8 = xy8[0]
    y8 = xy8[1]
    z8 = 73

    var_list = [[x0,y0,z0],[x1,y1,z1],[x2,y2,z2],[x3,y3,z3],[x4,y4,z4],[x5,y5,z5],[x6,y6,z6],[x7,y7,z7],[x8,y8,z8]]

    vmf_template = """
	solid
	{
		"id" "world_id_num"
		side
		{
			"id" "id_num"
			"plane" "(x1 y1 z1) (x2 y2 z2) (x3 y3 z3)"
			"material" "DEV/DEV_BLENDMEASURE"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x4 y4 z4) (x5 y5 z5) (x6 y6 z6)"
			"material" "DEV/DEV_BLENDMEASURE"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x1 y1 z1) (x7 y7 z7) (x4 y4 z4)"
			"material" "DEV/DEV_BLENDMEASURE"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x6 y6 z6) (x5 y5 z5) (x3 y3 z3)"
			"material" "DEV/DEV_BLENDMEASURE"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x2 y2 z2) (x1 y1 z1) (x8 y8 z8)"
			"material" "DEV/DEV_BLENDMEASURE"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x5 y5 z5) (x4 y4 z4) (x7 y7 z7)"
			"material" "DEV/DEV_BLENDMEASURE"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		editor
		{
			"color" "0 189 234"
			"visgroupshown" "1"
			"visgroupautoshown" "1"
		}
	}
}
entity
{
	"id" "world_id_num"
	"classname" "prop_static"
	"angles" "#ROTATION_0_0_0"
	"fademindist" "-1"
	"fadescale" "1"
	"lightmapresolutionx" "32"
	"lightmapresolutiony" "32"
	"model" "models/egypt/stick_torch/stick_torch_big.mdl"
	"skin" "0"
	"solid" "6"
	"origin" "x9 y9 z9"
	editor
	{
		"color" "255 255 0"
		"visgroupshown" "1"
		"visgroupautoshown" "1"
		"logicalpos" "[0 500]"
	}
}
"""
    X,Y,Z = 0,1,2
    for i in range(len(var_list)):
        vmf_template.replace("x%d y%d z%d" % (i, i, i), "%d %d %d" % (var_list[i][X], var_list[i][Y], var_list[i][Z]))
##    for i in range(vmf_template.count("world_id_num")):
##        vmf_template.replace("world_id_num", world_id_num, 1)
##        world_id_num += 1
##    for i in range(vmf_template.count("id_num")):
##        vmf_template.replace("id_num", id_num, 1)
##        id_num += 1
	#
	#move id_num calculations into export.py!!!!!! and out of prefab files
	#ALRIGHTY!!!
    axislist = ['1 0 0 1','0 1 0 1','0 0 1 1']
    negaxislist = ['-1 0 0 1','0 -1 0 1','0 0 -1 1']
    for normal_num in range(0,var_count,3):
        normal_list=[]
        for i in range(3):
            normal_list.append([])
            for var in [X, Y, Z]:
                normal_list[i].append(var_list[normal_num+i][var])
        response = evalutate(get_normal(normal_list))
        if response == "x":
            uaxis = axislist[1]
        else:
            uaxis = axislist[0]
        if response == "z":
            vaxis = negaxislist[1]
        else:
            vaxis = negaxislist[2]
        vmf_template.replace('AXIS_REPLACE_U',uaxis,1)
        vmf_template.replace('AXIS_REPLACE_V',vaxis,1)
