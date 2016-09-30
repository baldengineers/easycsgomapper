"""
This contains new algorithms for new and improved prefab system.
"""

def create(x, y, scale, rotation):
    xy1 = int(rotatePoint((posx*scale+256,posy*-1*scale-256), (posx*scale, posy*-1*scale), (360 if rotation!=0 else 0)-90*rotation)) 
    x1 = xy1[0]
    y1 = xy1[1]
