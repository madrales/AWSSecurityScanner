import boto3
import json

def run_checks():
    # accessPoint = boto3.resource('s3')
    # red = accessPoint.Bucket("redbucket-073418591604-us-east-2-an")
    # yellow = accessPoint.Bucket("yellowbucket-073418591604-us-east-2-an")
    # green = accessPoint.Bucket("greenbucket-073418591604-us-east-2-an")


    client = boto3.client('s3')

    buckets = []

    response = client.list_buckets()
    for x in response["Buckets"]:
        buckets.append(x["Name"])

    
    #IMP: Checking for Buckets with public ACLs or public bucket policies
    
    for x in buckets:
        y = client.get_bucket_acl(Bucket = x)
        for z in y["Grants"]:
            if "URI" in z["Grantee"]:
                if z["Grantee"]["URI"] == "http://acs.amazonaws.com/groups/global/AllUsers":
                    print("FAIL: Public ACL policy discovered: \'" + z["Grantee"]["URI"] + "\'")

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
                print("FAIL: Bucket \'" + x + "\' has a public bucket policy.")
            elif indicator == 0:
                print("PASS: Bucket \'" + x + "\' does not have a public bucket policy.")



    # #IMP: Buckets without versioning enabled
    

    for x in buckets:
        try:
            y = client.get_bucket_versioning(Bucket = x)["Status"]
            if y == "Enabled":
                print("SUCCESS: Bucket \'" + x + "\' does have versioning enabled.")
        except:
            print("FAIL: Bucket \'" + x + "\' does not have versioning enabled.")

    #IMP: Buckets without server-side encryption
    # Seems like server-side encryption is enabled by default in free tier and you can not change this.



    #This is good logic, don't delete
    # for x in policies:
    #     y = x["Statement"][0]["Principal"]
    #     if y == "*":
    #         print("FAIL: Resource \'" + x["Statement"][0]["Resource"] + "\' has a public bucket policy.")
    #     else:
    #         print("WARN: No public policies were found but no private policies were found either.")

                # else:
            #     # print("SUCCESS: Resource \'" + x["Statement"][0]["Resource"] + "\' does not have a public bucket policy.")
            #     continue
            # if indicator > 0:
            #     print("FAIL: Resource \'" + x["Statement"][0]["Resource"] + "\' has a public bucket policy.")
            # elif indicator == 0:
            #     print("SUCCESS: Resource \'" + x["Statement"][0]["Resource"] + "\' does not have a public bucket policy.")
            # else: 
            #     print("There was an error evaluatin gthe public bucket policies for \'" + x["Statement"][0]["Resource"] + "\'")

        #WIP to evaluate if there are multiple options in the ACLs
    # for x in acls:
    #     for y in x:
    #         if x[0]["Grantee"]["ID"] == "http://acs.amazonaws.com/groups/global/AllUsers":
    #             print("FAIL: All Users can access (Public)")
    #         else:
    #             print("WARN: Unable to evaluate")
    # for x in acls:
    #     if x == None:
    #         print("WARN: Bucket \'\' does not have any ACLs enabled.")
    #     else:
    #         print("Grantee ID \'" + x[0]["Grantee"]["ID"] + "\' has " + x[0]["Permission"])
    #     redACL = red.Acl()
    # yellowACL = yellow.Acl()
    # greenACL = green.Acl()
    
    # acls = []

    # acls.append(redACL.grants)
    # acls.append(yellowACL.grants)
    # acls.append(greenACL.grants)


    # for x in acls:
    #     for y in x:
    #         if "URI" in y["Grantee"]:
    #             if y["Grantee"]["URI"] == "http://acs.amazonaws.com/groups/global/AllUsers":
    #                 print("FAIL: Public ACL policy discovered: \'" + y["Grantee"]["URI"] + "\'")

        # redPolicy = red.Policy().policy
    # yellowPolicy = yellow.Policy().policy
    # greenPolicy = green.Policy().policy

    # yellowPolicyTranslate = json.loads(yellowPolicy)
    # greenPolicyTranslate = json.loads(greenPolicy)
    # redPolicyTranslate = json.loads(redPolicy)

    # policies = []

    # policies.append(redPolicyTranslate)
    # policies.append(yellowPolicyTranslate)
    # policies.append(greenPolicyTranslate)


    # for x in policies:
    #     y = x["Statement"]
    #     for z in y:
    #         indicator = 0
    #         if z["Principal"] == "*":
    #             print("FAIL: Resource \'" + x["Statement"][0]["Resource"] + "\' has a public bucket policy.")
    #             indicator += 1 
    #         else:
    #             continue
run_checks()