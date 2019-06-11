import boto3

exclude_rds = []
exclude_ec2 = []
exclude_asg = []

def lambda_handler(event, context):
    autoscaling = boto3.client('autoscaling')
    rds = boto3.client('rds')
    ec2 = boto3.client('ec2')
    
    resp = autoscaling.describe_auto_scaling_groups();
    
    for asg in resp['AutoScalingGroups']:
        ident = asg['AutoScalingGroupName']
        if ident in exclude_asg:
            print ('will not start instances from asg: ' + str(ident))
        else:
            try:
                autoscaling.update_auto_scaling_group(
                    AutoScalingGroupName=ident,
                    MinSize=1,
                    DesiredCapacity=1
                )
                print ('started all instances from asg: ' + str(ident))
            except Exception as e:
                print ('could not start all instances from asg: ' + str(ident))
                print (e)
        
    resp = rds.describe_db_instances();
    
    for rdsinst in resp['DBInstances']:
        ident = rdsinst['DBInstanceIdentifier']
        if ident in exclude_rds:
            print ('will not start your database: ' + str(ident))
        else:
            try:
                rds.start_db_instance(
                    DBInstanceIdentifier=ident
                )
                print ('started your database: ' + str(ident))
            except Exception as e:
                print ('could not start your database: ' + str(ident))
                print (e)
        
    resp = ec2.describe_instances();
        
    for ec2reserv in resp['Reservations']:
        for ec2inst in ec2reserv['Instances']:
            ident = ec2inst['InstanceId']
            if ident in exclude_ec2:
                print ('will not start your instance: ' + str(ident))
            else:
                try:
                    ec2.start_instances(
                        InstanceIds=[ ident ]
                    )
                    print ('started your instance: ' + str(ident))
                except Exception as e:
                    print ('could not start your instance: ' + str(ident))
                    print (e)
