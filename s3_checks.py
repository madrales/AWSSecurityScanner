import boto3
import json

def run_checks():
    #Global variable definition for this function
    client = boto3.client('s3')
    buckets = []
    violations = []
    aclDict = {}
    polDict = {}
    versDict = {}
    # successes = {}


    response = client.list_buckets()
    for x in response["Buckets"]:
        buckets.append(x["Name"])

    
    #IMP: Checking for Buckets with public ACLs or public bucket policies
    
    for x in buckets:
        y = client.get_bucket_acl(Bucket = x)
        for z in y["Grants"]:
            if "URI" in z["Grantee"]:
                if z["Grantee"]["URI"] == "http://acs.amazonaws.com/groups/global/AllUsers":
                    # print("FAIL: Public ACL policy discovered: \'" + z["Grantee"]["URI"] + "\'")
                    aclDict["severity"] = "HIGH"
                    aclDict["service"] = "S3"
                    aclDict["resource"] = x
                    aclDict["issue"] = "Resource has a Public ACL policy."
                    aclDict["recommendation"] = "Edit the ACL to restrict access."
                    violations.append(aclDict)
                    

    #DONE: Checks for public policies (Principal == *)

    for x in buckets:
        y = client.get_bucket_policy(Bucket = x)["Policy"]
        w = json.loads(y)["Statement"]
        for z in w:
            indicator = 0
            if z["Principal"] == "*":
                indicator += 1
            else:
                indicator = 0

            if indicator > 0:
                # print("FAIL: Bucket \'" + x + "\' has a public bucket policy.")
                polDict["severity"] = "MED"
                polDict["service"] = "S3"
                polDict["resource"] = x
                polDict["issue"] = "Resource has a public bucket policy."
                polDict["recommendation"] = "Edit the policy to restrict access."
                violations.append(polDict)
            # elif indicator == 0:
                # print("PASS: Bucket \'" + x + "\' does not have a public bucket policy.")



    # #IMP: Buckets without versioning enabled
    

    for x in buckets:
        try:
            y = client.get_bucket_versioning(Bucket = x)["Status"]
            if y == "Enabled":
                # print("SUCCESS: Bucket \'" + x + "\' does have versioning enabled.")
                continue
        except:
            # print("FAIL: Bucket \'" + x + "\' does not have versioning enabled.")
            versDict["severity"] = "MED"
            versDict["service"] = "S3"
            versDict["resource"] = x
            versDict["issue"] = "Resource does not have versioning enabled."
            versDict["recommendation"] = "Edit the resource to allow versioning."
            violations.append(versDict)

    #IMP: Buckets without server-side encryption
    #Seems like server-side encryption is enabled by default in free tier and you can not change this.

    if len(violations) == 0:
      return "There are no violations found"
    elif len(violations) > 0:
      return violations