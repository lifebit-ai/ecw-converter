import os
import boto3
import uuid
from rasterfoundry.api import API
from rasterfoundry.models import Upload
import subprocess
from sys import argv


# Create payload to POST to Raster Foundry API
def create_upload_from_s3_path(s3_path, organization_id, datasource_id, project_id, metadata={}):
    return dict(
        uploadStatus='UPLOADED',
        files=[s3_path],
        uploadType='S3',
        fileType='GEOTIFF',
        datasource=datasource_id,
        organizationId=organization_id,
        metadata=metadata,
        visibility='PRIVATE',
        projectId=project_id
    )

def create_scene_add_to_project(s3_path, datasource_id, name, project_id):
    """Creates a scene from a known S3 path and adds it to a given project
    
    :param s3_path: S3 path in form of s3://<bucket>/<key> 
    :param datasource_id: ID of datasource for scene 
    :param name: Human readable name for scene 
    :param project_id: ID of project to add created scene to
    :return: 
    """
    FilterFields = api.client.get_model('FilterFields')
    StatusFields = api.client.get_model('StatusFields')
    Image = api.client.get_model('Image')
    SceneCreate = api.client.get_model('SceneCreate')
    scene = SceneCreate(
        id=str(uuid.uuid4()),  # Random ID
        visibility='PRIVATE',  # Only visible to your user
        tags=[],  # can be empty if you don't want to include any
        datasource={
            # ID of Datasource for Scene
            'id': datasource_id,
            # These two fields are ignored, they're only present to make API client happy
            'name': 'My Datasource',
            'bands': []
        },
        sceneMetadata={},  # additional metadata you would like to attach
        name=name,
        owner=None,
        tileFootprint=None,
        dataFootprint=None,
        metadataFiles=[],
        images=[],
        thumbnails=[],
        ingestLocation=s3_path,
        filterFields=FilterFields(),
        statusFields=StatusFields(boundaryStatus='SUCCESS', footprintStatus='SUCCESS', ingestStatus='INGESTED', thumbnailStatus='SUCCESS'),
        sceneType='COG'
    )

    # Make API call to create scene
    created_scene = api.client.Imagery.post_scenes(scene=scene).result()

    # Add scene to project
    response = api.client.Imagery.post_projects_projectID_scenes(
        projectID=project_id,
        scenes=[created_scene.id]
    )

    # Verify that adding the scenes to the project worked successfully
    response.future.result().raise_for_status()

def run(refresh_token, import_type="cog", done_file="completed.txt"):
    global api
    api = API(refresh_token=refresh_token)
    FilterFields = api.client.get_model('FilterFields')
    StatusFields = api.client.get_model('StatusFields')
    Image = api.client.get_model('Image')
    SceneCreate = api.client.get_model('SceneCreate')
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('denmark-cogs')
    #tif and geotiff uploader
    text_file = open(done_file, "r")
    #lines = text_file.readlines()
    already_uploaded = text_file.read().split('\n')
    print(already_uploaded)
    print("Completed")
    if import_type=="tif": 
        # Construct S3 paths (e.g. s3://<bucket>/<path-to-tif>)
        s3_paths = ['s3://{}/{}'.format(o.bucket_name, o.key) for o in my_bucket.objects.all()
                if 'denmark-campsites/' in o.key and o.key.endswith('.tif')]
        # Go through each payload and POST to API
        for tiff in s3_paths:
            upload = create_upload_from_s3_path(
            tiff, "d0270f4c-66c5-4e0e-82f7-c1b12d98c2b6", "b16ca02b-eca5-4d66-b886-479d102a32b5", "808e2929-adf4-4eee-a6b3-0a4bda1ddd16"
        )
            Upload.create(api, upload)
    #COG uploader - can go straight to the scene stage and bypass everything else. 
    if import_type=="cog":
        s3_paths = ['s3://{}/{}'.format(o.bucket_name, o.key) for o in my_bucket.objects.all()
                if  o.key.endswith('.tif')]
        print(s3_paths)
        s3_paths = [x for x in s3_paths if x not in already_uploaded]
        # Go through each payload and POST to API
        #print(type(s3_paths))
        print(already_uploaded)
        #print(s3_paths not in already_uploaded)
        #s3_paths = s3_paths.pop(s3_paths not in already_uploaded)
        print(s3_paths)
        for scene in s3_paths:
            print(str(scene))
            create_scene_add_to_project(scene, "b16ca02b-eca5-4d66-b886-479d102a32b5",scene.strip("s3://denmark-cogs/img/"), "808e2929-adf4-4eee-a6b3-0a4bda1ddd16")
            with open("completed.txt", "a") as f:
                f.write(str(scene+"\n"))

if __name__ == '__main__':
    os.environ['RF_API_SPEC_PATH']='https://raw.githubusercontent.com/raster-foundry/raster-foundry-api-spec/1.17.0/spec/spec.yml'
    run(argv[1], argv[2], argv[3])
