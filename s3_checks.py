import boto3
import json

def run_checks():
    accessPoint = boto3.resource('s3')
    red = accessPoint.Bucket("redbucket-073418591604-us-east-2-an")
    yellow = accessPoint.Bucket("yellowbucket-073418591604-us-east-2-an")
    green = accessPoint.Bucket("greenbucket-073418591604-us-east-2-an")
   



    #IMP: Checking for Buckets with public ACLs or public bucket policies

    redACL = red.Acl()
    yellowACL = yellow.Acl()
    greenACL = green.Acl()
    
    acls = []

    acls.append(redACL.grants)
    acls.append(yellowACL.grants)
    acls.append(greenACL.grants)

    for x in acls:
        if x == None:
            print("WARN: Bucket \'\' does not have any ACLs enabled.")
        else:
            print("Grantee ID \'" + x[0]["Grantee"]["ID"] + "\' has " + x[0]["Permission"])

    redPolicy = red.Policy().policy
    yellowPolicy = yellow.Policy().policy
    greenPolicy = green.Policy().policy

    yellowPolicyTranslate = json.loads(yellowPolicy)
    greenPolicyTranslate = json.loads(greenPolicy)
    redPolicyTranslate = json.loads(redPolicy)

    policies = []

    policies.append(redPolicyTranslate)
    policies.append(yellowPolicyTranslate)
    policies.append(greenPolicyTranslate)
    
    for x in policies:
        y = x["Statement"]
        for z in y:
            if z["Principal"] == "*":
                print("FAIL: Resource \'" + x["Statement"][0]["Resource"] + "\' has a public bucket policy.")
                break
            else:
                print("SUCCESS: Resource \'" + x["Statement"][0]["Resource"] + "\' does not have a public bucket policy.")


    #IMP: Buckets without versioning enabled
    # answers = []

    # redVersion = red.Versioning()
    # yellowVersion = yellow.Versioning()
    # greenVersion = green.Versioning()

    # answers.append(redVersion.status)
    # answers.append(yellowVersion.status)
    # answers.append(greenVersion.status)

    # print(answers)

    # for x in answers:
    #     if x == None:
    #         print("FAIL: Bucket \'\' does not have versioning enabled.")
    #     elif x == "Enabled":
    #         print("SUCCESS: Bucket \'\' does have versioning enabled.")
    #     else:
    #         print("ERROR: Unable to evaluate bucket versioning.")

    


    #IMP: Buckets without server-side encryption



    #This is good logic, don't delete
    # for x in policies:
    #     y = x["Statement"][0]["Principal"]
    #     if y == "*":
    #         print("FAIL: Resource \'" + x["Statement"][0]["Resource"] + "\' has a public bucket policy.")
    #     else:
    #         print("WARN: No public policies were found but no private policies were found either.")
run_checks()