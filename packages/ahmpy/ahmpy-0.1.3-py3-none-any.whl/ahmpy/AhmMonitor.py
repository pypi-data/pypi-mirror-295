'''
监控摄像头的相关方法
'''
import cv2
import os
import time
import threading


class AHmMonitor():
    '''
    监控摄像头对象
    '''

    def __init__(self, rtsp_url: str, images_folder_path: str = 'images') -> None:
        '''
        初始化监控摄像头
        rtsp_url: rtsp地址
        images_folder_path: 抓拍图片保存文件夹
        '''
        self.rtsp_url = rtsp_url
        self.cap = cv2.VideoCapture(rtsp_url)
        self.images_folder_path = images_folder_path
        if not os.path.exists(images_folder_path):
            os.makedirs(images_folder_path)
        self.stop_event = threading.Event()

    def start_recording(self, interval: int = 60, frame_rate: int = 25):
        '''
        启动后台线程记录监控抓拍图片
        interval: 抓拍间隔时间
        frame_rate: 摄像头帧率
        '''
        self.thread = threading.Thread(
            target=self.record_images, args=(interval,))
        self.thread.daemon = True
        self.thread.start()

    def record_images(self, interval: int = 60, frame_rate: int = 25):
        '''
        定时记录监控抓拍图片
        interval: 抓拍间隔时间
        frame_rate: 摄像头帧率
        '''
        try:
            while not self.stop_event.is_set():
                # 丢弃过期帧
                for _ in range(frame_rate*interval-1):
                    self.cap.read()

                ret, frame = self.cap.read()
                if ret:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    image_path = os.path.join(
                        self.images_folder_path, f'image_{timestamp}.jpg')
                    cv2.imwrite(image_path, frame)
                    print(f'Image saved at {image_path}')
                else:
                    print('Failed to capture image')
                time.sleep(interval)
        finally:
            self.release()

    def stop_recording(self):
        '''
        停止后台线程记录监控抓拍图片
        '''
        self.stop_event.set()
        self.thread.join()

    def release(self):
        '''
        释放摄像头资源
        '''
        self.cap.release()
        cv2.destroyAllWindows()

    def __del__(self):
        '''
        对象被销毁时调用，确保资源被释放
        '''
        self.release()
