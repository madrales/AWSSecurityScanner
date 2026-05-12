## Steps Taken

---
#### May 11th, 2026
- Created an AWS account via Management Console. 
- Used the Management Console to provision the first user, eng01, with Readonly access to EC2, S3, and EBS.
#### May 12th, 2026
- Read through requirements for project. Associated at least one property within Boto3 to each Security violation to be tracked in this program
- Create a second user, eng02, part of the manager group who can create EC2 instances on behalf of eng01. this is to keep eng01 as the Ops associate who does not need access to create infra.
  - Generated an SSH Keypair for eng02.
- Created the first instance, RedServer, with 0.0.0.0/0 ingress rules. Will use this instance as the failure point
- Created the second instance, GreenServer. Will use this as the Control (goal to have 0 flags on this program related to the relevant violations)
- GOAL: Focus on the security group and IMDSv2 checks first. Run it locally and print raw results to the terminal.
- Disabled IMDSv2 on RedServer
- ```#Process to get to InstanceID
# items = len(response)
# print(len(response))
# print(response["Reservations"])
# print(response["Reservations"][0])
# print(response["Reservations"][0]["Instances"][0]["InstanceId"])```