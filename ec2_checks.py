import boto3
import datetime as dt



def run_checks():
    #Global variable definition for this function
    accessPoint = boto3.client('ec2')
    autoScaleAP = boto3.client('autoscaling')
    response = accessPoint.describe_instances()
    response2 = accessPoint.describe_security_groups()
    response3 = autoScaleAP.describe_auto_scaling_instances()
    violations = []
    imdvsDict = {}
    portDict = {}
    asgDict = {}


    #IMP: Check for IMDVSv2, must be required
    for x in response["Reservations"]:
        imdvsStatus = x["Instances"][0]["MetadataOptions"]["HttpTokens"]

        if imdvsStatus == "optional":
            imdvsDict["severity"] = "MED"
            imdvsDict["service"] = "EC2"
            imdvsDict["resource"] = x["Instances"][0]["InstanceId"]
            imdvsDict["issue"] = "Resource does not have IMDVSv2 enabled."
            imdvsDict["recommendation"] = "Edit the resource to require IMDVSv2."
            violations.append(imdvsDict)
    
    #IMP: Check for 0.0.0.0/0 rule for SSH (22) and RDP (3389) for each instance

    for x in response2["SecurityGroups"]:
        if x["IpPermissions"] == []:
            portDict["severity"] = "LOW"
            portDict["service"] = "EC2"
            portDict["resource"] = x["Instances"][0]["InstanceId"]
            portDict["issue"] = "Resource has no inbound rules."
            portDict["recommendation"] = "Review the inbound rules for the resource's Security Groups to ensure there should be no inbound rules."
            violations.append(portDict)
        for y in x["IpPermissions"]:
            if y["FromPort"] == 22:
                portDict["severity"] = "HIGH"
                portDict["service"] = "EC2"
                portDict["resource"] = x["GroupId"]
                portDict["issue"] = "Resource has Port 22 (SSH) open to all traffic (0.0.0.0/0)."
                portDict["recommendation"] = "Edit the inbound rules for the resource's Security Groups."
                violations.append(portDict)
            elif y["FromPort"] == 3389:
                portDict["severity"] = "HIGH"
                portDict["service"] = "EC2"
                portDict["resource"] = x["GroupId"]
                portDict["issue"] = "Resource has Port 3389 (RDP) open to all traffic (0.0.0.0/0)."
                portDict["recommendation"] = "Edit the inbound rules for the resource's Security Groups."
                violations.append(portDict)
            else:
                continue


    #IMP: Get the Instance ID for any Instances with AutoScalingGroup
    instancesWithAS = response3["AutoScalingInstances"]
    instances2 = []
    for x in instancesWithAS:
        instanceId = x["InstanceId"]
        instances2.append(instanceId)
    
    #IMP: Check for instances running for longer than 7 days that are not part of an auto-scaling group
    for x in response["Reservations"]:
        #IMP: checking the instance startup date against now + 7 days
        tC = x["Instances"][0]["NetworkInterfaces"][0]["Attachment"]["AttachTime"]
        instanceId = x["Instances"][0]["InstanceId"]
        nt = dt.datetime.now()
        nowTime = nt.timestamp()
        timeCreated = tC.timestamp()
        sevenDays = 604800

        if instanceId not in instances2:
            if timeCreated >= nowTime - sevenDays:
                asgDict["severity"] = "LOW"
                asgDict["service"] = "EC2"
                asgDict["resource"] = str(instanceId)
                asgDict["issue"] = "Resource is younger than 7 days but not assigned to an AutoScalingGroup."
                asgDict["recommendation"] = "Assign the resource to an AutoScalingGroup."
                violations.append(asgDict)
            else:
                asgDict["severity"] = "LOW"
                asgDict["service"] = "EC2"
                asgDict["resource"] = str(instanceId)
                asgDict["issue"] = "Resource is older than 7 days and not assigned to an AutoScalingGroup."
                asgDict["recommendation"] = "Assign the resource to an AutoScalingGroup."
                violations.append(asgDict)
        else:
            continue

    if len(violations) == 0:
      return "There are no violations found"
    elif len(violations) > 0:
      return violations