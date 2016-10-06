//test system for rendering ground terrain system
#include <stdlib.h>
#include <stdio.h>

#include <fstream>
#include <vector>
#include <string>

#include <GL/glut.h>
#include "Point.h"

using namespace std;

vector < Point > pointSet;
FILE *pointSetFile;

void loadPoints(const char *filename){
	ifstream input(filename);
	string current_line;

	while (getline(input, current_line)){
		int firstSpace = current_line.find_first_of(" ");
		int lastSpace = current_line.find_last_of(" ");
		//z and y values swapped because source engine is bonkers!!
		pointSet.push_back(Point(stod(current_line.substr(0, firstSpace)), stod(current_line.substr(lastSpace, current_line.length())),stod(current_line.substr(firstSpace, lastSpace))));
	}
}

void renderPoints(void){
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glBegin(GL_POINTS);
	glVertex3f(0.0, 0.0, 1.0);
	glEnd();

	glutSwapBuffers();
}

int main(int argc, char **argv){
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(100, 100);
	glutInitWindowSize(500, 500);
	glutCreateWindow("terrain render");

	glutDisplayFunc(renderPoints);

	glutMainLoop();

	return 1;
}