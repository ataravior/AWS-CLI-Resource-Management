import os
import boto3
import pulumi.automation as auto  
from tabulate import tabulate
from utils.utils import user_input

os.environ["PULUMI_CONFIG_PASSPHRASE"] = ""

ec2 = boto3.client("ec2")

def list_instances():
    """ List all EC2 instances created by Pulumi """
    response = ec2.describe_instances(Filters=[{"Name": "tag:CreatedBy", "Values": ["Pulumi"]}])
    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append([
                instance["InstanceId"],
                instance["State"]["Name"],
                instance["InstanceType"],
                instance["ImageId"],
                next((tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"), "N/A")
            ])
    
    print("\n**List of EC2 Instances**")
    print(tabulate(instances, headers=["Instance ID", "State", "Type", "AMI", "Name"], tablefmt="grid"))

def start_instance(instance_id):
    """Start an EC2 instance by ID"""
    response = ec2.describe_instances(InstanceIds=[instance_id])
    state = response["Reservations"][0]["Instances"][0]["State"]["Name"]

    if state == "stopped":
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} is now starting...")
    elif state == "running":
        print(f"Instance {instance_id} is already running.")
    else:
        print(f"Instance {instance_id} is in state: {state}.")

def stop_instance(instance_id):
    """Stop an EC2 instance by ID"""
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is stopping...")

def terminate_instance(instance_id):
    """Terminate an EC2 instance by ID with confirmation"""
    confirm = input(f"Are you sure you want to terminate instance {instance_id}? (YES/NO): ").strip().upper()
    if confirm == "YES":
        ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} is terminating...")

def run_pulumi_up():
    """Run Pulumi up automatically and format output as a table"""
    print("Running `pulumi up` in the background...")

    try:
        stack = auto.create_or_select_stack(
            stack_name="dev",
            project_name="aws-cli",
            work_dir="."
        )

        up_result = stack.up(on_output=print)

        print("Pulumi up completed successfully!")

        if up_result.outputs:
            table_data = [[key, value.value] for key, value in up_result.outputs.items()]
            print("\n**Stack Output:**")
            print(tabulate(table_data, headers=["Output Name", "Value"], tablefmt="grid"))
        else:
            print("No outputs found.")

    except Exception as e:
        print(f"Pulumi up failed: {e}")

def manage_ec2():
    """EC2 Management Menu"""
    while True:
        ec2_action = user_input("Select an action:", ["Manage EC2 Instances", "Create EC2", "Exit"])
        
        if ec2_action == "Exit":
            break
        
        if ec2_action == "Manage EC2 Instances":
            while True:
                manage_action = user_input("Select action:", ["List Instances", "Start Instance", "Stop Instance", "Terminate Instance", "Exit"])
                
                if manage_action == "Exit":
                    break
                
                if manage_action == "List Instances":
                    list_instances()
                elif manage_action in ["Start Instance", "Stop Instance", "Terminate Instance"]:
                    instance_id = input("Enter Instance ID: ").strip()
                    if manage_action == "Start Instance":
                        start_instance(instance_id)
                    elif manage_action == "Stop Instance":
                        stop_instance(instance_id)
                    elif manage_action == "Terminate Instance":
                        terminate_instance(instance_id)

        elif ec2_action == "Create EC2":
            create_choice = user_input("Do you want to create an EC2 instance?", ["YES", "NO"])
            if create_choice == "NO":
                continue
            
            instance_count = int(user_input("How many EC2 instances to create? (Max: 2)", ["1", "2"]))
            
            for i in range(instance_count):
                instance_name = input(f"Enter a name tag for EC2 instance {i+1}: ").strip()
                instance_type = user_input("Which type of EC2 to create?", ["t3.nano", "t4g.nano"])
                ami_choice = user_input("Which type of AMI to use?", ["Ubuntu", "Amazon Linux"])
                
                os.system(f"pulumi config set aws-cli:instance_name_{i} {instance_name}-{i}")
                os.system(f"pulumi config set aws-cli:instance_type {instance_type}")
                os.system(f"pulumi config set aws-cli:ami_choice {ami_choice}")

            os.system(f"pulumi config set aws-cli:instance_count {instance_count}")
            print("\nEC2 Instance configuration saved! Deploying automatically...")

            run_pulumi_up()
