import boto3

def create_resource(name:str = 'rekognition', access_keys_file_path:str = 
    'AWS-RekognitionAPI/AWSCredentials/accessKeys.csv', region:str = 'us-west-1'):
    """
    For a full list of AWS regions see:
    https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html
    """
    with open(access_keys_file_path, 'r') as keys:
        keys.readline()
        access_keys = keys.readline().split(',')
        aws_access_key_id=access_keys[0].strip()
        aws_secret_access_key=access_keys[1].strip()
    return boto3.client(name, aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key, region_name = region)

client = create_resource()