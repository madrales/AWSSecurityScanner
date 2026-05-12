import boto3

accessPoint = boto3.client('ec2')
response = accessPoint.describe_instances()


#GOAL: retrieve the instance, then use the describe_attribute property to check on ImdsSupport property
#path is a dictionary -> List -> List -> List for InstanceId and dictionary -> List -> List -> Dictionary for HttpTokens
print(response["Reservations"][0]["Instances"][0]["InstanceId"])
print(response["Reservations"][0]["Instances"][0]["MetadataOptions"]["HttpTokens"])
print(response["Reservations"][1]["Instances"][0]["InstanceId"])
print(response["Reservations"][1]["Instances"][0]["MetadataOptions"]["HttpTokens"])
