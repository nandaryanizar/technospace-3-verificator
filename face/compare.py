def compare(source, target, client):
    source = str(source).lstrip("https://gobase-groupa.s3.us-east-2.amazonaws.com/media/")
    response = client.compare_faces(SimilarityThreshold=90,
                                    SourceImage={"S3Object": {
                                        "Bucket": "gobase-groupa",
                                        "Name": source,
                                    }},
                                    TargetImage={'Bytes': target})
    if len(response['FaceMatches']) > 0:
        return True
    return False
