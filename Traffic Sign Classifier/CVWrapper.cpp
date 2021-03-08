#include "CVWrapper.h"

Mat CVWrapper::DetectEdges(Mat image, int low_threshold, const int ratio, const int kernel_size)
{
	cvtColor(image, image, COLOR_BGR2GRAY);
	blur(image, image, Size(kernel_size, kernel_size));
	Canny(image, image, low_threshold, double(low_threshold * ratio), kernel_size);
	return image;
}
