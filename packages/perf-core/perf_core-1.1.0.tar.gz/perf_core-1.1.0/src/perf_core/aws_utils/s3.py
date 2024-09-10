import boto3
from logging import info
from botocore.config import Config
import os



class S3Utils:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.s3 = self.session.resource('s3', config=Config(signature_version='s3v4'), region_name=region_name)

    def s3_get_presigned_url_post_upload(file_path, file_name):
        file_loc = file_path + "/" + file_name
        S3Utils.s3.meta.client.upload_file(Filename=file_loc,
                                           Bucket='test-automation-lastbrand',
                                           Key=file_name)

        public_report_url = S3Utils.s3.meta.client.generate_presigned_url('get_object',
                                                                          Params={'Bucket': 'test-automation-lastbrand',
                                                                                  'Key': file_name},
                                                                          ExpiresIn=21600)
        info(public_report_url)
        return public_report_url

    def s3_get_download_file(self, bucket_name, s3_key, download_path):
        if os.path.exists(download_path):
            info(f"File already exists at {download_path}. Download aborted to avoid overwrite.")
            return

        try:
            self.s3.meta.client.download_file(Bucket=bucket_name, Key=s3_key, Filename=download_path)
            info(f"File {s3_key} downloaded successfully to {download_path}")
        except Exception as e:
            info(f"Failed to download {s3_key} from S3: {e}")