### AWSSecurityScanner
#### Problem Statement:
 - Create a Python CLI tool that connects to your AWS account, scans for common security and cost violations, and produces a structured report. It then runs automatically on a schedule via AWS Lambda + CloudWatch Events.

---

#### Prerequisites & Setup
- AWS Account
  - Use a free tier account. If you don't have one, create one at aws.amazon.com. You won't exceed free tier limits for this project.
- IAM User & Permissions
  - Create an IAM user with a policy that allows read-only access across EC2, S3, and EBS to follow the concept of least-privilege. Will provide real experience into why authorization is required after authentication; users should only be able to access the resources they need to complete a task, no more, no less.
#### Local Dependencies
- Python 3.10+
- AWS CLI configured
- boto3 (```pip install boto3```)

#### Objectives:
- What the Scanner Should Check
  - S3 Violations
    - Buckets with public ACLs or public bucket policies
      - Imp:S3.ServiceResource.BucketAcl(bucket_name) for ACL, S3.ServiceResource.BucketPolicy(bucket_name) for policies
    - Buckets without versioning enabled
      - Imp:S3.ServiceResource.BucketVersioning(bucket_name)
    - Buckets without server-side encryption
      - Imp:S3.Object.server_side_encryption
  - EC2 Violations
    - Instances that have been running for more than 7 days without being part of an autoscaling group (idle cost risk)
      - Imp: need to use describe_auto_scaling_groups or describe_auto_scaling_instances to check if the instance is part of the autoscaling group. describe_instances and maybe 'reason' flag to determine why the instance is in the state it currently is (might show last operation and date it was done on)
    - Security groups with port 22 or 3389 open to 0.0.0.0/0
      - Imp: will likely need to grab the security group of the EC2 instance (can get name and ID with describe_instances) and then perform a lookup to make sure the ports are not open to 0.0.0.0/0
    - Instances not using IMDSv2 (a real AWS security best practice)
      - Imp: describe_attribute will describe if ImdsSupport returns v2.0 if IMDSv2 is being used in an instance.
  - EBS Violations
    - Unencrypted volumes
      - Imp: EC2.Volume.encrypted will show if volume is encrypted
    - Volumes in "available" state (detached and costing money doing nothing)
      - Imp: EC2.Volume.state will show the state of volume

### What I Learned
- Hands-on experience with AWS CLI
- Boto3 API
