import boto3

def run_checks():

    #Global variable definition for this function
    accessPoint = boto3.client('ec2')
    volumes = accessPoint.describe_volumes()
    violations = []
    vioDict = {}
    stateDict = {}
    successes = []

    # print("Evaluating EBS security...\n\n")

    #IMP: checking for state of volumes
    # print("\nChecking volumes for state == \'available\'...\n\n")
    for x in volumes["Volumes"]:
        if x["State"] == "available":
            stateDict["severity"] = "HIGH"
            stateDict["service"] = "EBS"
            stateDict["resource"] = x["VolumeId"]
            stateDict["issue"] = "Volume is in available state, meaning it is not attached to an instance."
            stateDict["recommendation"] = "Delete volume or attach it to a running instance."
            violations.append(stateDict)
        # elif x["State"] == "in-use":
        #     successes.append("PASS: \'" + x["VolumeId"] + "\' is in state \'" + x["State"] + "\' for Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")
        # else:
        #     print("Unable to evaluate state for volume \'" + x["VolumeId"] + "\' in Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")
    

    #IMP: checking encryption of volumes
    # print("\n\nChecking volumes for encryption...")
    for x in volumes["Volumes"]:
        if x["Encrypted"] == False:
            vioDict["severity"] = "LOW"
            vioDict["service"] = "EBS"
            vioDict["resource"] = x["VolumeId"]
            vioDict["issue"] = "Volume is not encrypted."
            vioDict["recommendation"] = "Enable encryption via a new snapshot."
            violations.append(vioDict)
        elif x["Encrypted"] == True:
            # print("PASS: \'" + x["VolumeId"] + "\' is encrypted.")
            successes.append("PASS: \'" + x["VolumeId"] + "\' is encrypted.")
        else:
            print("Unable to evaluate encryption for volume \'" + x["VolumeId"] + "\' in Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")
    
    if len(violations) == 0:
      return "There are no violations found"
    elif len(violations) > 0:
      return violations