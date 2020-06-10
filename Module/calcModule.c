#include <math.h>
#include <float.h>

const char* helloWorld()
{
    return "Hello World";
}

float getDataPointPosX(float width, float left, float right, int nx, int i)
{    
    return left + (width - left - right) / (nx * 2) + i * (width - left - right) / nx;
}

float getDataPointPosY(float height, float top, float bottom, float max, float min, int ny, float value)
{
    if (fabsf(max - min) <= FLT_EPSILON)        
        return top + (height - top - bottom) / (ny * 2);
    else
        return top + (height - top - bottom) / (ny * 2) + (ny - 1) * (height - top - bottom) / ny - (ny - 1) * ((height - top - bottom) / ny / (ny - 1)) * (ny - 1) * (value - min) / (max - min);
}