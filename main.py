from ec2_checks import run_checks as ec2_checks
from ebs_checks import run_checks as ebs_checks
from s3_checks import run_checks as s3_checks
import datetime as dt
import json
import boto3

def run():
    client = boto3.client('account')
    response = client.get_account_information()

    ec2 = ec2_checks()
    s3 = s3_checks()
    ebs = ebs_checks()
    violations = ec2 + s3 + ebs
    highCount = 0
    medCount = 0
    lowCount = 0

    for vio in violations:
        if vio["severity"] == "HIGH":
            highCount += 1
        elif vio["severity"] == "MED":
            medCount += 1
        elif vio["severity"] == "LOW":
            lowCount += 1
        else:
            print("Unable to evaluate")
    
    

    summary = {}
    summary["total_violations"] = len(violations)
    summary["high_count"] = highCount
    summary["med_count"] = medCount
    summary["low_count"] = lowCount

    report = {}
    report["generated_at"] = str(dt.datetime.now())
    report["account_id"] = response['AccountId']
    report["violations"] = violations
    report["summary"] = summary
    print(json.dumps(report, indent = 4))


run()
