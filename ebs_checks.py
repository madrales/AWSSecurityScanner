import boto3

def run_checks():

    #Global variable definition for this function
    accessPoint = boto3.client('ec2')
    volumes = accessPoint.describe_volumes()
    violations = []
    vioDict = {}
    stateDict = {}
    successes = []

    #IMP: checking for state of volumes
    for x in volumes["Volumes"]:
        if x["State"] == "available":
            stateDict["severity"] = "LOW"
            stateDict["service"] = "EBS"
            stateDict["resource"] = x["VolumeId"]
            stateDict["issue"] = "Volume is in available state, meaning it is not attached to an instance."
            stateDict["recommendation"] = "Delete volume or attach it to a running instance."
            violations.append(stateDict)
    
    #IMP: checking encryption of volumes
    for x in volumes["Volumes"]:
        if x["Encrypted"] == False:
            vioDict["severity"] = "HIGH"
            vioDict["service"] = "EBS"
            vioDict["resource"] = x["VolumeId"]
            vioDict["issue"] = "Volume is not encrypted."
            vioDict["recommendation"] = "Enable encryption via a new snapshot."
            violations.append(vioDict)
        elif x["Encrypted"] == True:
            successes.append("PASS: \'" + x["VolumeId"] + "\' is encrypted.")
        else:
            print("Unable to evaluate encryption for volume \'" + x["VolumeId"] + "\' in Instance ID \'" + x["Attachments"][0]["InstanceId"] + "\'.")
    
    if len(violations) == 0:
      return "There are no violations found"
    elif len(violations) > 0:
      return violations