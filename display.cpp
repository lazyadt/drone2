#include "opencv2/highgui/highgui.hpp"
#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/nonfree/nonfree.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <fstream>
#include <string>
using namespace cv;
using namespace std;

ofstream outputFile;
string filename = "data.csv";    

int main(int argc, char* argv[])
{	
	// Colour thresholding values, area thresholding values, contour approximation factor for shape detection
	int l_r = 110, l_b = 110, l_g = 120, h_r = 234, h_b = 240, h_g = 239, l_a = 150, h_a = 350, factor = 4 ;	
	int cx, cy;
	outputFile.open(filename.c_str() );
	outputFile << "Image_Name " << "," << "POSITION_X" << ","  << "POSITION_Y" << endl;
	
	for (int img_count = 1; img_count < argc ; img_count++)	
	{		
		Mat img = imread(argv[img_count]);		
		Mat thresh;		
		inRange(img, Scalar(l_b,l_g,l_r), Scalar(h_b,h_g,h_r),thresh);	

		// Morphological operations for filling holes and removing noise (available in opencv)
		Mat element = getStructuringElement( MORPH_ELLIPSE, Size(5, 5));		
		dilate(thresh, thresh, element);
		erode(thresh, thresh, element);
		erode(thresh, thresh, element);	
		dilate(thresh, thresh, element);    

		// Finding contours and saving its copy for future use
		vector<vector<Point> > contours1, contours;	
		vector<Vec4i> hierarchy1;
		findContours(thresh, contours1, hierarchy1, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);
		contours = contours1;

		double area;	// Contour Area variable	
		double epsilon;	// Error Factor in contour-approximation variable
		int flag = 0;	// Status of detection of L-Mark

		//Iteration over contours to detect a desired contour
		for (int idx = 0; idx < contours1.size(); idx++) 					
		{
			area = contourArea(contours1[idx]);
			if (area > l_a && area < h_a)			
			{
				// Epsilon is estimated from length of contour
				epsilon = arcLength(contours1[idx], true) * factor / 100;
				
				// For this marker-shape the approximation-factor of 2 is most suitable
				approxPolyDP(contours[idx], contours[idx], epsilon / 2, true);
					
				if (isContourConvex(contours1[idx]) == false && contours1[idx].size() == 5 && (contours[idx].size() == 6 || 						contours[idx].size() == 7))
				{
					// Calculating moments for the centroid detetction, for the given shape, the approximated_contour 			                        //centroid and the corner to be calculated are in very close proximity varying from 1-2 pixels
		
					Moments M = moments(contours1[idx]);	
					cx = int(M.m10 / M.m00);
					cy = int(M.m01 / M.m00);
					outputFile << argv[img_count] << "," << cx << ", " << cy << endl;
				}
			}
		}
	}
	outputFile.close();
	return 0;
}
