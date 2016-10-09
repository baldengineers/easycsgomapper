#include <stdlib.h>
#include <stdio.h>

#include <fstream>
#include <vector>
#include <string>

#include <windows.h>
#include <iostream>
#include <math.h>

#include <gl/glut.h>

#include "Point.h"

using namespace std;


vector<Point> pointSet;
vector<bool>  trueSet;

float ypos = -5.0f;

void loadPoints(const char *filename){
	ifstream input(filename);
	string current_line;


	while (getline(input, current_line)){
		if (current_line != ""){
			int firstSpace = current_line.find_first_of(" ");
			int lastSpace = current_line.find_last_of(" ");
			//z and y values swapped because source engine is bonkers!!

			pointSet.push_back(Point(stod(current_line.substr(0, firstSpace)) / 64, stod(current_line.substr(lastSpace, current_line.length() - 1)) / 64, stod(current_line.substr(firstSpace, lastSpace)) / 64));
			trueSet.push_back(false);
			//printf("not newline");
		}
		else{
			printf("newline");
			trueSet.push_back(true);
		}
	}
}
void parseVMF(void){
	system("python vmfScript.py");
}

void renderPoints(void){
	
	//gluLookAt(0.0, ypos, 0.0, 4.0, 0.0, -4.0, 0.0, 1.0, 0.0);
	glLoadIdentity();
	gluLookAt(0.0f, ypos, 0.0f,
		4.0f, 0.0f, -4.0f,
		0.0f, 1.0f, 0.0f);
	
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glBegin(GL_POLYGON);
	for (int ind = 0; ind < pointSet.size(); ind++){
		if (trueSet[ind] == false){
			glVertex3f(pointSet[ind].getPointX(), pointSet[ind].getPointY(), pointSet[ind].getPointZ());
		}
		else{
			glEnd();
			glBegin(GL_POLYGON);
		}
	}
	
	
	glEnd();
	glTranslatef(0.0, ypos, 0);
	glutSwapBuffers();
	glutPostRedisplay();
	
	ypos += 0.1f;
	Sleep(100);


	

}

void changeSize(int w, int h) {

	if (h == 0)
		h = 1;

	float ratio = w * 1.0 / h;

	// Use the Projection Matrix
	glMatrixMode(GL_PROJECTION);

	// Reset Matrix
	glLoadIdentity();

	// Set the viewport to be the entire window
	glViewport(0, 0, w, h);

	// Set the correct perspective.
	gluPerspective(90.0f, ratio, 0.1f, 100.0f);

	// Get Back to the Modelview
	glMatrixMode(GL_MODELVIEW);
}



int main(int argc, char **argv){
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(100, 100);
	glutInitWindowSize(500, 500);
	glutCreateWindow("pfb render");

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glViewport(0, 0, 500, 500);
	gluPerspective(90.0f, 1, 0.1f, 100.0f);

	glMatrixMode(GL_MODELVIEW);
	
	parseVMF();
	loadPoints("vertfile.vf");
	//glTranslatef(0.0, -.5, 0.0);
	//glRotatef(90, 1, 0, 0.1);
	glutDisplayFunc(renderPoints);
	glutReshapeFunc(changeSize);
	glutIdleFunc(renderPoints);

	glutMainLoop();

	return 1;
}