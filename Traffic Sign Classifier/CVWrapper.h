#pragma once

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>

using namespace cv;

class CVWrapper {
private:
	CVWrapper(){};	// Remove the ability to instantiate this Helper class
public:
	static Mat DetectEdges(Mat image, int low_threshold = 50, const int ratio = 3, const int kernel_size = 3);
};
