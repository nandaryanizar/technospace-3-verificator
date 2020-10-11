def compare(source, target, client):
    response = client.compare_faces(SimilarityThreshold=90,
                                    SourceImage={"S3Object": {
                                        "Bucket": "gobase-groupa",
                                        "Name": source,
                                    }},
                                    TargetImage={'Bytes': target})
    if len(response['FaceMatches']) > 0:
        return True
    return False
