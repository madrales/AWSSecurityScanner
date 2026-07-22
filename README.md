### AWSSecurityScanner
#### Problem Statement:
 - Create a Python CLI tool that connects to your AWS account, scans for common security and cost violations, and produces a structured report. It then runs automatically on a schedule via AWS Lambda + CloudWatch Events.

---

#### Prerequisites & Setup
- AWS Account
  - A free tier account is sufficient. You be required to setup EC2 instances, S3 Buckets, and EBS resources with the specific violations mentioned in this project, or connect this project to a live AWS account to analyze the security violations.
- IAM User & Permissions
  - Create an IAM user with a policy that allows read-only access across EC2, S3, and EBS to follow the concept of least-privilege. Will provide real experience into why authorization is required after authentication; users should only be able to access the resources they need to complete a task, no more, no less.
#### Local Dependencies
- Using a Python Virtual Environment for the dependencies helps to reduce any errors that can be isolated on one user's machine. This venv allows for isolated dependencies. Imagine that you need Python 3.9 or older for a specific program on your local machine, the venv allows for the Python 3.10 dependency to have its own Python installation that does not conflict with your local installation.
- Python 3.10+
- AWS CLI configured
- Flask (```pip install flask```)
- boto3 (```pip install boto3```)
- jsontohtml (```pip install jsont2html```)
##### Windows Specific
- Run ```python -m venv venv``` to create a venv and ```venv\Scripts\Activate.ps1``` to activate the venv
  - ***NOTE:** if you run into an UnauthorizedAccess error, run ```Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass``` to allow the execution of scripts. If you can not switch this setting on your local machine, you can also run these commands via CMD in Windows.*

#### Getting Started
- Clone the project to your local machine
- Start the Flask application from inside the project and within the venv
  - ```flask --app report_generator run```
  - Will start the application in your local browser at 127.0.0.1:5000
#### Objectives:
- What the Scanner evaluates:
  - S3 Violations
    - Buckets with public ACLs or public bucket policies
    - Buckets without versioning enabled
    - Buckets without server-side encryption
  - EC2 Violations
    - Instances that have been running for more than 7 days without being part of an autoscaling group (idle cost risk)
    - Security groups with port 22 or 3389 open to 0.0.0.0/0
    - Instances not using IMDSv2 (a real AWS security best practice)
  - EBS Violations
    - Unencrypted volumes
    - Volumes in "available" state (detached and costing money doing nothing)

#### Implementation: 
- S3 Violations
    - Buckets with public ACLs or public bucket policies
      - Analyzes the S3 Buckets with Boto3's ```client.list_buckets()``` method to see if the Grantee is set to "http://acs.amazonaws.com/groups/global/AllUsers" or if the Principal is set to "*" as these are both indicative of either a public ACL or Bucket policy.
      - Determined to be a high priority violation as public ACLs and Bucket policies poses emergency security risks as all users, including bad actors, can access the S3 buckets. This needs immediate remediation.
    - Buckets without versioning enabled
      - Analyzes the Bucket Versioning via Boto3's ```client.get_bucket_versioning()``` method to see if the Status is set to Enabled. If it is not, then it is proven that versioning is not enabled.
      - Determined to be a medium priority violation as this poses a substantial security risk, but can be quickly toggled to resolve the impact.
    - Buckets without server-side encryption
      - Server-side encryption is enabled by default in free tier AWS and this can not be modified. Thus, this is not evaluated.
  - EC2 Violations
    - Instances that have been running for more than 7 days without being part of an autoscaling group (idle cost risk)
      - Analyzes the timeCreated for an Instance and checks to see if it is within 7 days. Then, the check is completed to see if the Instance is part of an AutoScalingGroup via Boto3's ```client.describe_auto_scaling_instances()``` and if not, a violation is returned with low priority. 
      - Determined to be low priority as an EC2 resource not attached to an auto-scaling group poses a small risk to the total security of the tenancy. The impact is realized on the financial side as an un-used resource still incurs cost, but there is also an availability impact as instance not attached to an auto-scaling group would not comeback online if there was a termination of the instance.
    - Security groups with port 22 or 3389 open to 0.0.0.0/0
      - Implements Boto3's ```client.describe_security_groups()``` method to evaluate whether or not a Security Group has all traffic open for SSH or RDP.
      - Determined to be a high priority violation due to the globally open access to the resource. There is not any filtering going on for these Security Groups so anyone, including bad actors, can access this resouce. This poses an emergency risk to the tenancy and all resources within.
    - Instances not using IMDSv2
      - Implements Boto3's ```client.describe_instances()``` method to evaluate if the MetadataOptions include a HttpTokens set to "optional". If so, a medium violation is returned.
      - Determined to be a medium priority as IMDSv2 is no longer support due to well known exploits. This poses a security risk to the entire tenancy, however this is a quick fix that can be toggled in the Cloud Console.
  - EBS Violations
    - Unencrypted volumes
      - Implements Boto3's ```client.describe_volumes()``` method to evaluate if a volume has it's Encryption property set to False. If so, a high priority violation is returned.
      - Determined to be high priority as an unencrypted volume poses a major security risk to all data on the EBS resource and can have upstream impacts to the entire tenancy if exposed.
    - Volumes in "available" state (detached and costing money doing nothing)
      - Implements Boto3's ```client.describe_volumes()``` method to evaluate if a volume is in "Available" state. If so, a low priority violation is returned.
      - Determined to be low priority as an EBS resource in available state poses a small risk to the total security of the tenancy. The impact is realized on the financial side as an un-used resource still incurs cost.

### Highlights
- Developed on both Windows and MacOS to experience a true simulation of local and remote conflicts within Git as well as to become familiar with developing on both Operating Systems.
- Hands-on experience with creating EC2, S3, and EBS resources within the AWS Cloud Console
- Hands-on experience with AWS IAM; creating users, adding permissions, and managing resources with the principle of least privilege.
- Utilized Boto3 to establish client sessions that can query resource information such as ID and name but also attributes that can indicate a security violation
- Discovered the json2html Python Library that helps translate JSON into HTML table fragments directly
- Python Virtual Environments allow for a seamless dependency resolution as you can install any dependencies within the virtual environment rather that directly to your local
- Development on Git Branches and merged feature branches back into a development branch before logging a PR to merge into main when the MVP was completed.
