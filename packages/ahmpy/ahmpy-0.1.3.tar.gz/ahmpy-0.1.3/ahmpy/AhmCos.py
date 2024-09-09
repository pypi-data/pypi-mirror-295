'''
艾环梦的腾讯云对象存储封装
'''
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import os


class AhmCos():
    '''
    对象存储类
    '''

    def __init__(self, bucket: str = 'camera-ai-1316980174') -> None:
        ''''
        初始化对象存储
        bucket: 存储桶名称
        '''

        # 初始化用户数据
        secret_id = "AKIDfEdrroY8lKpRxOn5CHBVhmmcHpCNPJ6z"
        secret_key = 'rbFi03vc8jjgcP3kV7jIhu21nQunZ8Uc'
        region = 'ap-chengdu'
        token = None
        scheme = 'https'
        config = CosConfig(Region=region, SecretId=secret_id,
                           SecretKey=secret_key, Token=token, Scheme=scheme)

        self.client = CosS3Client(config)
        self.bucket = bucket

    def upload(self, file_folder: str, file_path: str):
        '''
        上传文件到腾讯云对象存储指定文件夹下
        file_folder: 文件夹名称
        file_path: 上传文件路径
        '''
        file_name = os.path.basename(file_path)
        key = file_folder + '/' + file_name
        self.client.upload_file(
            Bucket=self.bucket,
            Key=key,
            LocalFilePath=file_path,
            EnableMD5=False,
            progress_callback=None
        )

    def getFileUrl(self, file_path: str) -> str:
        '''
        根据对象存储文件路径获取文件的url
        file_path: 文件路径
        '''
        url = self.client.get_object_url(
            Bucket='camera-ai-1316980174',
            Key=file_path,
        )
        return url
