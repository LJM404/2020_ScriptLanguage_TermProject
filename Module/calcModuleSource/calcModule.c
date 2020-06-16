#include <math.h>
#include <float.h>

// 모듈 테스트용 함수
const char* helloWorld()
{
    return "Hello World";
}

// 점의 그래프 x위치를 얻는 함수
float getDataPointPosX(float width, float left, float right, int nx, int i)
{    
    return left + (width - left - right) / (nx * 2) + i * (width - left - right) / nx;
}

// 점의 그래프 y위치를 얻는 함수
float getDataPointPosY(float height, float top, float bottom, float max, float min, int ny, float value)
{
    if (fabsf(max - min) <= FLT_EPSILON)        
        return top + (height - top - bottom) / (ny * 2);
    else
        return top + (height - top - bottom) / (ny * 2) + (ny - 1) * (height - top - bottom) / ny - (ny - 1) * ((height - top - bottom) / ny / (ny - 1)) * (ny - 1) * (value - min) / (max - min);
}