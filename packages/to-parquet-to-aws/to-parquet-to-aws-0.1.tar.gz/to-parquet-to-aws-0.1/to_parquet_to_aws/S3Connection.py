import boto3

class S3Connection:
    
    """
    Class to handle and connecto to s3 bucket connection.
    This

    Methods:    
    """
    
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 session_token: str,
                 region_name: str
                 ) -> None:
        
        self.access_key=access_key
        self.secret_key=secret_key
        self.session_token=session_token
        self.region_name=region_name                
        self.session=None
        self.resource=None
        
    def create_session(self):
        
        self.session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_token,
            region_name= self.region_name
            )
        
        #Creating S3 Resource From the Session.
        self.resource = self.session.resource('s3')
        
    def upload_file(self, local_file_path:str, staging_directory:str, folder_path:str) -> tuple[bool, str]:
        
        """
        method to upload file path in s3 bucket 

        Input:
        s3 (Object) : Session to S3 Bucket
        file_path (str) : Full Path of File to upload in Bucket
        bucket_name (str) : Name of bucket Ex: (dl-test-name-bucket)
        key_name (str) : Path of file to upload in s3 Ex: (Folder1\Folder2\file.csv)
        
        if upload successfully return True
        if no return False
        
        """

        session=self.resource.Object(staging_directory, folder_path)
        result = session.put(Body=open(local_file_path, 'rb'))
        res = result.get('ResponseMetadata')

        if res.get('HTTPStatusCode') == 200:
            return True, ""
        else:
            try:
                error_message = result.get('Error').get('Message')
            except:
                error_message = "It was not possible to get the error message from the HTTP Response"
            return False, error_message