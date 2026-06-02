import boto3

def run_checks():

    #Global variable definition for this function
    accessPoint = boto3.client('ec2')
    volumes = accessPoint.describe_volumes()
    failures = []
    successes = []

    print("Evaluating EBS security...\n\n")

    #IMP: checking for state of volumes
    print("\nChecking volumes for state == \'available\'...\n\n")
    for x in volumes["Volumes"]:
        if x["State"] == "available":
            failures.append("FAIL: \'" + x["VolumeId"] + "\' is in \'available\' state, meaning it is not attached to an instance.")
        elif x["State"] == "in-use":
            successes.append("PASS: \'" + x["VolumeId"] + "\' is in state \'" + x["State"] + "\' for Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")
        else:
            print("Unable to evaluate state for volume \'" + x["VolumeId"] + "\' in Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")
    
    return print(failures)

    #IMP: checking encryption of volumes
    # print("\n\nChecking volumes for encryption...")
    # for x in volumes["Volumes"]:
    #     if x["Encrypted"] == False:
    #         print("FAIL: \'" + x["VolumeId"] + "\' is not encrypted.")
    #     elif x["Encrypted"] == True:
    #         print("PASS: \'" + x["VolumeId"] + "\' is encrypted.")
    #     else:
    #         print("Unable to evaluate encryption for volume \'" + x["VolumeId"] + "\' in Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")

    # if len(failures) == 0:
    #     return "There are no failures found"
    # elif len(failures) > 0:
    #     return failures