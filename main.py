from ec2_checks import run_checks as ec2_checks
from ebs_checks import run_checks as ebs_checks
from s3_checks import run_checks as s3_checks

def run():
    print("AWSSecurityScanner\n\n")
    # ec2_checks()
    ebs_checks()
    # s3_checks()
run()