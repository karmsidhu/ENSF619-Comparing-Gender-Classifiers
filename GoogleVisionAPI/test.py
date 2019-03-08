# Imports the Google Cloud client library
from google.cloud import storage

def implicit():
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

implicit()

# # Instantiates a client
# storage_client = storage.Client()

# # The name for the new bucket
# bucket_name = 'my-new-bucket'

# # Creates the new bucket
# bucket = storage_client.create_bucket(bucket_name)

# print('Bucket {} created.'.format(bucket.name))

