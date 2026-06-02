import boto3

def run_checks():
    accessPoint = boto3.client('ec2')
    volumes = accessPoint.describe_volumes()
    print("Evaluating EBS security...\n\n")

    #IMP: checking for state of volumes
    print("\n\nChecking volumes for state == \'available\'...\n\n")
    for x in volumes["Volumes"]:
        if x["State"] == "available":
            print("FAIL: \'" + x["VolumeId"] + "\' is in \'available\' state, meaning it is not attached to an instance.")
        elif x["State"] == "in-use":
            print("PASS: \'" + x["VolumeId"] + "\' is in state \'" + x["State"] + "\' for Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")
        else:
            print("Unable to evaluate state for volume \'" + x["VolumeId"] + "\' in Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")

    #IMP: checking encryption of volumes
    print("\n\nChecking volumes for encryption...")
    for x in volumes["Volumes"]:
        if x["Encrypted"] == False:
            print("FAIL: \'" + x["VolumeId"] + "\' is not encrypted.")
        elif x["Encrypted"] == True:
            print("PASS: \'" + x["VolumeId"] + "\' is encrypted.")
        else:
            print("Unable to evaluate encryption for volume \'" + x["VolumeId"] + "\' in Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")

    
run_checks()