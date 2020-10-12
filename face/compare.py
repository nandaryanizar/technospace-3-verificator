def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def compare(source, target, client):
    source = remove_prefix(source, "https://gobase-groupa.s3.us-east-2.amazonaws.com/")
    response = client.compare_faces(SimilarityThreshold=90,
                                    SourceImage={"S3Object": {
                                        "Bucket": "gobase-groupa",
                                        "Name": source,
                                    }},
                                    TargetImage={'Bytes': target})
    if len(response['FaceMatches']) > 0:

        return True
    return False
