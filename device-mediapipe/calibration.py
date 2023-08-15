import numpy as np 
import cv2

def main():
    print("calibration.py")
    # 定义棋盘格的行列数 
    rows = 7
    cols = 7
    
    # 创建棋盘格的3D坐标 
    objp = np.zeros((rows*cols, 3), np.float32) 
    objp[:,:2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2) 
    

    # 创建空数组来存储棋盘格的2D坐标和3D坐标 
    objpoints = [] 
    imgpoints = [] 
    
    # 读取图像 
    img = cv2.imread('chessboard.png') 
    
    # 转换为灰度图像 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    # 查找棋盘格的角点 
    ret, corners = cv2.findChessboardCorners(gray, (cols, rows), None) 
    
    # 如果找到了角点，则添加到数组中 
    if ret == True: 
        objpoints.append(objp) 
        imgpoints.append(corners) 
    
        # 绘制角点并显示 
        cv2.drawChessboardCorners(img, (cols, rows), corners, ret) 
        cv2.imshow('img', img) 
        cv2.waitKey(0) 
    print(objpoints,imgpoints)
    # 进行相机标定 
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None) 
    
    # 打印相机内部参数和畸变系数 
    print("Camera matrix:") 
    print(mtx) 
    print("Distortion coefficients:") 
    print(dist) 

    # pnp算法
    # 3D点坐标
    points_3d = np.array([[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]], dtype=np.float32)
    # 2D点坐标
    points_2d = np.array([[0, 0], [0, 100], [100, 100], [100, 0]], dtype=np.float32)
    # 执行pnp算法
    success, rvec, tvec = cv2.solvePnP(points_3d, points_2d, mtx, dist)
    if success:
        print("旋转向量：", rvec)
        print("平移向量：", tvec)

if __name__ == '__main__':
    main()


