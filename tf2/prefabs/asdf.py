from pf import evaluate, get_normal, rotatePoint
def create(posx, posy, scale, rotation):
	xy0 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
	x0 = xy0[0]
	y0 = xy0[1]
	z0 = 64
	xy1 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
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
	xy5 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
	x5 = xy5[0]
	y5 = xy5[1]
	z5 = 0
	xy6 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
	x6 = xy6[0]
	y6 = xy6[1]
	z6 = 64
	xy7 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
	x7 = xy7[0]
	y7 = xy7[1]
	z7 = 0
	xy8 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x8 = xy8[0]
	y8 = xy8[1]
	z8 = 64
	xy9 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+64, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x9 = xy9[0]
	y9 = xy9[1]
	z9 = 64
	xy10 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+64, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
	x10 = xy10[0]
	y10 = xy10[1]
	z10 = 64
	xy11 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+64, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
	x11 = xy11[0]
	y11 = xy11[1]
	z11 = 0
	xy12 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+64, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x12 = xy12[0]
	y12 = xy12[1]
	z12 = 0
	xy13 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x13 = xy13[0]
	y13 = xy13[1]
	z13 = 0
	xy14 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x14 = xy14[0]
	y14 = xy14[1]
	z14 = 64
	xy15 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x15 = xy15[0]
	y15 = xy15[1]
	z15 = 64
	xy16 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
	x16 = xy16[0]
	y16 = xy16[1]
	z16 = 0
	xy17 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x17 = xy17[0]
	y17 = xy17[1]
	z17 = 0
	xy18 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
	x18 = xy18[0]
	y18 = xy18[1]
	z18 = 64
	xy19 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x19 = xy19[0]
	y19 = xy19[1]
	z19 = 0
	xy20 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x20 = xy20[0]
	y20 = xy20[1]
	z20 = 64
	xy21 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+-64), (360 if rotation!=0 else 0)-90*rotation))
	x21 = xy21[0]
	y21 = xy21[1]
	z21 = 64
	xy22 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+-64), (360 if rotation!=0 else 0)-90*rotation))
	x22 = xy22[0]
	y22 = xy22[1]
	z22 = 0
	xy23 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+-64), (360 if rotation!=0 else 0)-90*rotation))
	x23 = xy23[0]
	y23 = xy23[1]
	z23 = 0
	xy24 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+0), (360 if rotation!=0 else 0)-90*rotation))
	x24 = xy24[0]
	y24 = xy24[1]
	z24 = 0
	xy25 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+-64), (360 if rotation!=0 else 0)-90*rotation))
	x25 = xy25[0]
	y25 = xy25[1]
	z25 = 64
	xy26 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
	x26 = xy26[0]
	y26 = xy26[1]
	z26 = 64
	xy27 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
	x27 = xy27[0]
	y27 = xy27[1]
	z27 = 64
	xy28 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
	x28 = xy28[0]
	y28 = xy28[1]
	z28 = 0
	xy29 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+-448), (360 if rotation!=0 else 0)-90*rotation))
	x29 = xy29[0]
	y29 = xy29[1]
	z29 = 0
	xy30 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+896, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
	x30 = xy30[0]
	y30 = xy30[1]
	z30 = 64
	xy31 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x31 = xy31[0]
	y31 = xy31[1]
	z31 = 64
	xy32 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+896, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x32 = xy32[0]
	y32 = xy32[1]
	z32 = 0
	xy33 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+960, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x33 = xy33[0]
	y33 = xy33[1]
	z33 = 0
	xy34 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+896, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x34 = xy34[0]
	y34 = xy34[1]
	z34 = 64
	xy35 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+896, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
	x35 = xy35[0]
	y35 = xy35[1]
	z35 = 0
	xy36 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+-896), (360 if rotation!=0 else 0)-90*rotation))
	x36 = xy36[0]
	y36 = xy36[1]
	z36 = 64
	xy37 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+-896), (360 if rotation!=0 else 0)-90*rotation))
	x37 = xy37[0]
	y37 = xy37[1]
	z37 = 64
	xy38 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x38 = xy38[0]
	y38 = xy38[1]
	z38 = 64
	xy39 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x39 = xy39[0]
	y39 = xy39[1]
	z39 = 0
	xy40 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x40 = xy40[0]
	y40 = xy40[1]
	z40 = 0
	xy41 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+-896), (360 if rotation!=0 else 0)-90*rotation))
	x41 = xy41[0]
	y41 = xy41[1]
	z41 = 0
	xy42 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x42 = xy42[0]
	y42 = xy42[1]
	z42 = 64
	xy43 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+0, posy*-1*scale+-896), (360 if rotation!=0 else 0)-90*rotation))
	x43 = xy43[0]
	y43 = xy43[1]
	z43 = 0
	xy44 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
	x44 = xy44[0]
	y44 = xy44[1]
	z44 = 64
	xy45 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x45 = xy45[0]
	y45 = xy45[1]
	z45 = 64
	xy46 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+512, posy*-1*scale+-960), (360 if rotation!=0 else 0)-90*rotation))
	x46 = xy46[0]
	y46 = xy46[1]
	z46 = 0
	xy47 = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+448, posy*-1*scale+-512), (360 if rotation!=0 else 0)-90*rotation))
	x47 = xy47[0]
	y47 = xy47[1]
	z47 = 0

    var_list = [[x0, y0, z0],[x1, y1, z1],[x2, y2, z2],[x3, y3, z3],[x4, y4, z4],[x5, y5, z5],[x6, y6, z6],[x7, y7, z7],[x8, y8, z8],[x9, y9, z9],[x10, y10, z10],[x11, y11, z11],[x12, y12, z12],[x13, y13, z13],[x14, y14, z14],[x15, y15, z15],[x16, y16, z16],[x17, y17, z17],[x18, y18, z18],[x19, y19, z19],[x20, y20, z20],[x21, y21, z21],[x22, y22, z22],[x23, y23, z23],[x24, y24, z24],[x25, y25, z25],[x26, y26, z26],[x27, y27, z27],[x28, y28, z28],[x29, y29, z29],[x30, y30, z30],[x31, y31, z31],[x32, y32, z32],[x33, y33, z33],[x34, y34, z34],[x35, y35, z35],[x36, y36, z36],[x37, y37, z37],[x38, y38, z38],[x39, y39, z39],[x40, y40, z40],[x41, y41, z41],[x42, y42, z42],[x43, y43, z43],[x44, y44, z44],[x45, y45, z45],[x46, y46, z46],[x47, y47, z47]]
    vmf_template = """
    	solid
	{
		"id" "world_id_num"
		side
		{
			"id" "id_num"
			"plane" "(x0 y0 z0) (x1 y1 z1) (x2 y2 z2)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x3 y3 z3) (x4 y4 z4) (x5 y5 z5)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x0 y0 z0) (x6 y6 z6) (x3 y3 z3)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x5 y5 z5) (x4 y4 z4) (x2 y2 z2)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x1 y1 z1) (x0 y0 z0) (x7 y7 z7)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x4 y4 z4) (x3 y3 z3) (x6 y6 z6)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		editor
		{
			"color" "0 202 199"
			"visgroupshown" "1"
			"visgroupautoshown" "1"
		}
	}
	solid
	{
		"id" "world_id_num"
		side
		{
			"id" "id_num"
			"plane" "(x8 y8 z8) (x9 y9 z9) (x10 y10 z10)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x7 y7 z7) (x11 y11 z11) (x12 y12 z12)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x8 y8 z8) (x0 y0 z0) (x7 y7 z7)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x12 y12 z12) (x11 y11 z11) (x10 y10 z10)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x9 y9 z9) (x8 y8 z8) (x13 y13 z13)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x11 y11 z11) (x7 y7 z7) (x0 y0 z0)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		editor
		{
			"color" "0 102 203"
			"visgroupshown" "1"
			"visgroupautoshown" "1"
		}
	}
	solid
	{
		"id" "world_id_num"
		side
		{
			"id" "id_num"
			"plane" "(x14 y14 z14) (x15 y15 z15) (x1 y1 z1)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x16 y16 z16) (x5 y5 z5) (x17 y17 z17)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x14 y14 z14) (x18 y18 z18) (x16 y16 z16)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x17 y17 z17) (x5 y5 z5) (x1 y1 z1)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x15 y15 z15) (x14 y14 z14) (x19 y19 z19)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x5 y5 z5) (x16 y16 z16) (x18 y18 z18)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		editor
		{
			"color" "0 110 235"
			"visgroupshown" "1"
			"visgroupautoshown" "1"
		}
	}
	solid
	{
		"id" "world_id_num"
		side
		{
			"id" "id_num"
			"plane" "(x15 y15 z15) (x20 y20 z20) (x21 y21 z21)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x22 y22 z22) (x23 y23 z23) (x24 y24 z24)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x15 y15 z15) (x25 y25 z25) (x22 y22 z22)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x24 y24 z24) (x23 y23 z23) (x21 y21 z21)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x20 y20 z20) (x15 y15 z15) (x17 y17 z17)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x23 y23 z23) (x22 y22 z22) (x25 y25 z25)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		editor
		{
			"color" "0 228 181"
			"visgroupshown" "1"
			"visgroupautoshown" "1"
		}
	}
	solid
	{
		"id" "world_id_num"
		side
		{
			"id" "id_num"
			"plane" "(x1 y1 z1) (x26 y26 z26) (x27 y27 z27)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x4 y4 z4) (x28 y28 z28) (x29 y29 z29)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x1 y1 z1) (x2 y2 z2) (x4 y4 z4)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x29 y29 z29) (x28 y28 z28) (x27 y27 z27)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x26 y26 z26) (x1 y1 z1) (x5 y5 z5)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x28 y28 z28) (x4 y4 z4) (x2 y2 z2)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		editor
		{
			"color" "0 110 107"
			"visgroupshown" "1"
			"visgroupautoshown" "1"
		}
	}
	solid
	{
		"id" "world_id_num"
		side
		{
			"id" "id_num"
			"plane" "(x30 y30 z30) (x27 y27 z27) (x31 y31 z31)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x32 y32 z32) (x33 y33 z33) (x28 y28 z28)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x30 y30 z30) (x34 y34 z34) (x32 y32 z32)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x28 y28 z28) (x33 y33 z33) (x31 y31 z31)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x27 y27 z27) (x30 y30 z30) (x35 y35 z35)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x33 y33 z33) (x32 y32 z32) (x34 y34 z34)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		editor
		{
			"color" "0 196 165"
			"visgroupshown" "1"
			"visgroupautoshown" "1"
		}
	}
	solid
	{
		"id" "world_id_num"
		side
		{
			"id" "id_num"
			"plane" "(x36 y36 z36) (x37 y37 z37) (x38 y38 z38)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x39 y39 z39) (x40 y40 z40) (x41 y41 z41)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x36 y36 z36) (x42 y42 z42) (x39 y39 z39)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x41 y41 z41) (x40 y40 z40) (x38 y38 z38)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x37 y37 z37) (x36 y36 z36) (x43 y43 z43)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x40 y40 z40) (x39 y39 z39) (x42 y42 z42)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		editor
		{
			"color" "0 106 215"
			"visgroupshown" "1"
			"visgroupautoshown" "1"
		}
	}
	solid
	{
		"id" "world_id_num"
		side
		{
			"id" "id_num"
			"plane" "(x44 y44 z44) (x2 y2 z2) (x45 y45 z45)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x40 y40 z40) (x46 y46 z46) (x4 y4 z4)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x44 y44 z44) (x38 y38 z38) (x40 y40 z40)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x4 y4 z4) (x46 y46 z46) (x45 y45 z45)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x2 y2 z2) (x44 y44 z44) (x47 y47 z47)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		side
		{
			"id" "id_num"
			"plane" "(x46 y46 z46) (x40 y40 z40) (x38 y38 z38)"
			"material" "BRICK/BRICKWALL001C"
			"uaxis" "[AXIS_REPLACE_U] 0.25"
			"vaxis" "[AXIS_REPLACE_V] 0.25"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}
		editor
		{
			"color" "0 160 217"
			"visgroupshown" "1"
			"visgroupautoshown" "1"
		}
	}
}
"""
    X,Y,Z = 0,1,2
    for i in range(len(var_list)):
        vmf_template.replace("x%d y%d z%d" % (i, i, i), "%d %d %d" % (var_list[i][X], var_list[i][Y], var_list[i][Z]))
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
        vmf_template = vmf_template.replace('AXIS_REPLACE_U',uaxis,1)
        vmf_template = vmf_template.replace('AXIS_REPLACE_V',vaxis,1)
