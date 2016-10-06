#ifndef _POINT_H
#define _POINT_H

class Point{
	double x, y, z;

	public:
		Point();
		Point(double, double, double);
		
		double getPointX() { return x; }
		double getPointY() { return y; }
		double getPointZ() { return z; }
};
Point::Point(){
	x = 0;
	y = 0;
	z = 0;
}
Point::Point(double xIn, double yIn, double zIn){
	x = xIn;
	y = yIn;
	z = zIn;
}

#endif