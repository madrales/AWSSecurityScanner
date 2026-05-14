import boto3
import datetime as dt

def run_checks():
    #Open the client to connect to ec2 instances available in AWS
    accessPoint = boto3.client('ec2')
    autoScaleAP = boto3.client('autoscaling')
    response = accessPoint.describe_instances()
    response2 = accessPoint.describe_security_groups()
    response3 = autoScaleAP.describe_auto_scaling_instances()

    #IMP: Check for IMDVSv2, must be required
    print("\nIMDVSv2 Checks:\n")
    for x in response["Reservations"]:
        y = x["Instances"][0]["MetadataOptions"]["HttpTokens"]

        if y == "optional":
            print("FAIL: IMDVSv2 is not enforced on " + x["Instances"][0]["InstanceId"])
        else:
            print("SUCCESS: IMDVSv2 is enabled for " + x["Instances"][0]["InstanceId"])
    
    #IMP: Check for 0.0.0.0/0 rule for SSH (22) and RDP (3389) for each instance
    print("\nSecurityGroups Checks:\n")
    for x in response2["SecurityGroups"]:
        if x["IpPermissions"] == []:
            print("\tWARN: There are no inbound rules for Security Group " +  x["GroupId"])
        else:
            for y in x["IpPermissions"]:
                if y["FromPort"] == 3389 and y["FromPort"] == 22:
                    print(x["GroupId"] + "\nFAIL: Port 3389 (RDP) is open to all traffic (0.0.0.0/0) on this Instance.\nFAIL: Port 22 (SSH) is open to all traffic (0.0.0.0/0) on this Instance.")
                elif y["FromPort"] == 22:
                    print(x["GroupId"] + "\nFAIL: Port 22 (SSH) is open to all traffic (0.0.0.0/0) on this Instance.\n")
                elif y["FromPort"] == 3389:
                    print(x["GroupId"] + "\nFAIL: Port 3389 (RDP) is open to all traffic (0.0.0.0/0) on this Instance.\n")
                else:
                    print("SUCCESS: no SSH or RDP ports open to all traffic (0.0.0.0/0) on this Instance.")

    #IMP: Get the Instance ID for any Instances with AutoScalingGroup
    print("\nAutoScaling Checks:\n")
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
            print("WARN: InstanceId " + str(instanceId) + " is not assigned to an AutoScalingGroup")
            if timeCreated >= nowTime - sevenDays:
                print("\tWARN: InstanceId " + str(instanceId) + " is younger than 7 days but not assigned to an AutoScalingGroup")
            else:
                print("FAIL: InstanceId " + str(instanceId) + " is older than 7 days and not assigned to an AutoScalingGroup")
        else:
            print("SUCCESS: InstanceId " + str(instanceId) + " is assigned to an AutoScalingGroup")




        #Used to test functionality as instances were not older than 7 days during implementation        
        # threeHours = 36000

        # if instanceId not in instances2:
        #     print("InstanceId " + str(instanceId) + " is not assigned to an AutoScalingGroup")
        #     if timeCreated >= nowTime - threeHours:
        #         print("WARN: This instance is younger than 10 hours but not assigned to an AutoScalingGroup")
        #     else:
        #         print("FAIL: This instance is older than 10 hours and not assigned to an AutoScalingGroup")
        # else:
        #     print("InstanceId " + str(instanceId) + " is assigned to an AutoScalingGroup")
    
        
        # threeHours = 12000

        # if timeCreated >= nowTime - threeHours:
        #     print("SUCCESS: This instance is younger than 3 hours.")
        # else:
        #     print("ERROR: This instance is older than 3 hours.")

def idToName():
    print("TBD")
idToName()
run_checks()