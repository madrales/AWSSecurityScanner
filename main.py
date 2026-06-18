from ec2_checks import run_checks as ec2_checks
from ebs_checks import run_checks as ebs_checks
from s3_checks import run_checks as s3_checks
import json

def run():
    print("AWSSecurityScanner\n")
    a = ec2_checks()
    z = s3_checks()
    x = ebs_checks()
    y = json.dumps(x, indent = 4)
    w = json.dumps(z, indent = 4)
    b = json.dumps(a, indent = 4)
    print(y)
    print(w)
    print(b)
run()
