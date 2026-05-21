import boto3

def run_checks():
    accessPoint = boto3.resource('s3')
    red = accessPoint.Bucket("redbucket-073418591604-us-east-2-an")
    yellow = accessPoint.Bucket("yellowbucket-073418591604-us-east-2-an")
    green = accessPoint.Bucket("greenbucket-073418591604-us-east-2-an")
   



    #IMP: Checking for Buckets with public ACLs or public bucket policies

    #IMP: Buckets without versioning enabled
    answers = []

    redVersion = red.Versioning()
    yellowVersion = yellow.Versioning()
    greenVersion = green.Versioning()

    answers.append(redVersion.status)
    answers.append(yellowVersion.status)
    answers.append(greenVersion.status)

    # print(answers)

    for x in answers:
        if x == None:
            print("FAIL: Bucket \'\' does not have versioning enabled.")
        elif x == "Enabled":
            print("SUCCESS: Bucket \'\' does have versioning enabled.")
        else:
            print("ERROR: Unable to evaluate bucket versioning.")

    


    #IMP: Buckets without server-side encryption

run_checks()