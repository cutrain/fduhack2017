# fduhack2017
```c++
typedef struct _CameraSpacePoint {
    float X;
    float Y;
    float Z;
} CameraSpacePoint;
typedef struct _ColorSpacePoint {
    float X;
    float Y;
} ColorSpacePoint;
typedef struct _DepthSpacePoint {
    float X;
    float Y;
} DepthSpacePoint;
typedef struct _Joint {
    JointType JointType;
    CameraSpacePoint Position;
    TrackingState TrackingState;
} Joint;
typedef struct _JointOrientation {
    JointType JointType;
    Vector4 Orientation;
} JointOrientation;
typedef struct _PointF {
    float X;
    float Y;
} PointF;
typedef struct _RectF {
    float X;
    float Y;
    float Width;
    float Height;
} RectF;
typedef struct _Vector4 {
    float x;
    float y;
    float z;
    float w;
} Vector4;
```
