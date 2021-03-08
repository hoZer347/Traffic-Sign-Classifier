#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

#include "CVWrapper.h"

using namespace cv;
using namespace std;

int main()
{
	Mat image = imread("stop_sign.jpg");
	Mat canny = CVWrapper::DetectEdges(image);
	imshow("Canny", canny);

	waitKey(0);
	return 0;
}
