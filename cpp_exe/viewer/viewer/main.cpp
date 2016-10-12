#define _CRT_SECURE_NO_WARNINGS

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


vector<Point>  pointSet;
vector<bool>   trueSet;
vector<string> lines;
vector<Point>  entSet;

Point center;

float ypos = 5.0;
float t;

GLfloat qaBlack[] = { 0.0, 0.0, 0.0, 1.0 };
GLfloat qaGreen[] = { 0.0, 1.0, 0.0, 1.0 };
GLfloat qaRed[] = { 1.0, 0.0, 0.0, 1.0 };
GLfloat qaBlue[] = { 0.0, 0.0, 1.0, 1.0 };
GLfloat qaWhite[] = { 1.0, 1.0, 1.0, 1.0 };
GLfloat qaLowAmbient[] = { 0.05, 0.05, 0.05, 1.0 };
GLfloat qaFullAmbient[] = { 1.0, 1.0, 1.0, 1.0 };

void drawCube(Point center){
	glMaterialfv(GL_FRONT, GL_AMBIENT, qaRed);

	for (int i = -1; i < 2; i += 2){
		glBegin(GL_POLYGON);
		glVertex3f(center.getPointX() + i*0.1, center.getPointY() + i*0.1, center.getPointZ() + i*0.1);
		glVertex3f(center.getPointX() + i*0.1, center.getPointY() - i*0.1, center.getPointZ() + i*0.1);
		glVertex3f(center.getPointX() - i*0.1, center.getPointY() - i*0.1, center.getPointZ() + i*0.1);
		glVertex3f(center.getPointX() - i*0.1, center.getPointY() + i*0.1, center.getPointZ() + i*0.1);
		glEnd();

		glBegin(GL_POLYGON);
		glVertex3f(center.getPointX() + i*0.1, center.getPointY() + i*0.1, center.getPointZ() + i*0.1);
		glVertex3f(center.getPointX() + i*0.1, center.getPointY() - i*0.1, center.getPointZ() + i*0.1);
		glVertex3f(center.getPointX() + i*0.1, center.getPointY() - i*0.1, center.getPointZ() - i*0.1);
		glVertex3f(center.getPointX() + i*0.1, center.getPointY() + i* 0.1, center.getPointZ() - i*0.1);
		glEnd();

		glBegin(GL_POLYGON);
		glVertex3f(center.getPointX() + i*0.1, center.getPointY() + i*0.1, center.getPointZ() + i*0.1);
		glVertex3f(center.getPointX() - i*0.1, center.getPointY() + i*0.1, center.getPointZ() + i*0.1);
		glVertex3f(center.getPointX() - i*0.1, center.getPointY() + i*0.1, center.getPointZ() - i*0.1);
		glVertex3f(center.getPointX() + i*0.1, center.getPointY() + i*0.1, center.getPointZ() - i*0.1);
		glEnd();
	}
}

void loadInfo(const char *filename){
	ifstream input(filename);
	string current_line;
	while (getline(input, current_line)){
		int firstSpace = current_line.find_first_of(" ");
		int lastSpace = current_line.find_last_of(" ");
		//	printf(current_line.c_str());
		center = Point(stod(current_line.substr(0, firstSpace)) / 64, stod(current_line.substr(lastSpace, current_line.length())) / 64, stod(current_line.substr(firstSpace, lastSpace)) / 64);
	}
	cout << center.getPointX() << endl;
	cout << center.getPointY() << endl;
	cout << center.getPointZ() << endl;
}

void loadEntPoints(const char *filename){
	ifstream input(filename);
	string current_line;

	while (getline(input, current_line)){
		if (current_line != ""){
			int firstSpace = current_line.find_first_of(" ");
			int lastSpace = current_line.find_last_of(" ");
			//z and y values swapped because source engine is bonkers!!

			entSet.push_back(Point(stod(current_line.substr(0, firstSpace)) / 64, stod(current_line.substr(lastSpace, current_line.length() - 1)) / 64, stod(current_line.substr(firstSpace, lastSpace)) / 64));

		}
	}
}

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
			lines.push_back(current_line + "\n");
			//printf("not newline");

		}
		else{
			//printf("newline");
			trueSet.push_back(true);
			pointSet.push_back(Point(0,0,0));

			lines.push_back(current_line + "\n");


		}
	}
}

void parseVMF(void){
	system("python vmfScript.py");
}


void renderPoints(void){
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glEnable(GL_DEPTH_TEST);

	glMaterialfv(GL_FRONT, GL_SPECULAR, qaWhite);
	glLightfv(GL_LIGHT0, GL_AMBIENT, qaLowAmbient);

	glMaterialfv(GL_FRONT, GL_AMBIENT, qaWhite);
	glMaterialfv(GL_FRONT, GL_DIFFUSE, qaWhite);
	glMaterialf(GL_FRONT, GL_SHININESS, 128.0);
	glLightfv(GL_LIGHT0, GL_AMBIENT, qaLowAmbient);
	glLoadIdentity();
	
	glShadeModel(GL_SMOOTH);
	gluLookAt((center.getPointX()+4) * cos(t) + center.getPointX(), center.getPointY()*2+3, (center.getPointZ()-4) * sin(t) + center.getPointZ(),
		center.getPointX(), center.getPointY(), center.getPointZ(),
		0.0f, 1.0f, 0.0f);

	//render solids
	glBegin(GL_POLYGON);
	glMaterialfv(GL_FRONT, GL_SPECULAR, qaWhite);
	for (int ind = 0; ind < pointSet.size(); ind++){
		if (trueSet[ind] == false){
			glVertex3f(pointSet[ind].getPointX(), pointSet[ind].getPointY(), pointSet[ind].getPointZ());
			//printf(lines[ind].c_str());
		}
		else{
			//printf(lines[ind].c_str());
			glEnd();
			glBegin(GL_POLYGON);
		}
	}
	glEnd();

	//render ent representing cubes


	for (int cur = 0; cur < entSet.size(); cur++){
		drawCube(entSet[cur]);
	}
	glLightfv(GL_LIGHT0, GL_AMBIENT, qaFullAmbient);
	glTranslatef(0.0, ypos, 0);
	glutSwapBuffers();

	glutSetWindow(1);
	glutPostRedisplay();


	t += 0.05;
	//ypos += 0.1f;
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

void processNormalKeys(unsigned char key, int x, int y) {

	if (key == 27)
		exit(0);
}

int main(int argc, char **argv){
	glutInit(&argc, argv);
	//FreeConsole();
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(100, 100);
	glutInitWindowSize(500, 500);
	glutCreateWindow("pfb render (esc to close)");
	glClearColor(0.0, 0.0, 0.0, 0.0);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glViewport(0, 0, 500, 500);
	gluPerspective(90.0f, 1, 0.1f, 100.0f);

	glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE);
	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);

	GLfloat qaAmbientLight[] = { 0.05, 0.05, 0.05, 1.0 };
	GLfloat qaDiffuseLight[] = { 0.8, 0.8, 0.8, 1.0 };
	GLfloat qaSpecularLight[] = { 1.0, 1.0, 1.0, 1.0 };
	

	glLightfv(GL_LIGHT0, GL_AMBIENT, qaAmbientLight);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, qaDiffuseLight);
	glLightfv(GL_LIGHT0, GL_SPECULAR, qaSpecularLight);
	

	

	glMatrixMode(GL_MODELVIEW);
	
	//parseVMF();
	//the vmf is parsed within the .py file

	loadInfo("cpp_exe/infofile.vf");


	GLfloat qaLightPosition[] = { center.getPointX()-1, center.getPointY()*3, center.getPointZ()+1, 1.0 };
	glLightfv(GL_LIGHT0, GL_POSITION, qaLightPosition);

	loadPoints("cpp_exe/vertfile.vf");
	loadEntPoints("cpp_exe/origfile.vf");
	//glTranslatef(center.getPointX()*2, center.getPointY()*2, center.getPointZ()*2);
	glRotatef(135, 1, 0, 0.1);

	glutKeyboardFunc(processNormalKeys);
	glutDisplayFunc(renderPoints);
	glutReshapeFunc(changeSize);
	glutIdleFunc(renderPoints);
	

	glutMainLoop();

	

	return 0;
}