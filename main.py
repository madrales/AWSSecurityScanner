from ec2_checks import run_checks as ec2_checks
from ebs_checks import run_checks as ebs_checks
from s3_checks import run_checks as s3_checks
import json

def run():
    print("AWSSecurityScanner\n\n")
    # ec2_checks()
    # s3_checks()
    x = ebs_checks()
    y = json.dumps(x, indent = 4)
    print(y)
run()
