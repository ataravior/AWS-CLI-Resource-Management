import pulumi
import pulumi_aws as aws
import services.aws_route53 as aws_route53

config = pulumi.Config("aws-cli")
instance_count = int(config.get("instance_count") or 1)


instance_names = [config.get(f"instance_name_{i}") or f"Default-Instance-{i}" for i in range(instance_count)]
instance_type = config.get("instance_type") or "t2.micro"
ami_choice = config.get("ami_choice") or "Amazon Linux"

arch = "arm64" if instance_type.startswith("t4g") else "x86_64"

ami_options = {
    "Ubuntu": aws.ec2.get_ami(
        owners=["099720109477"],
        most_recent=True,
        filters=[
            {"name": "name", "values": ["ubuntu/images/hvm-ssd/ubuntu-*-server-*"]},
            {"name": "architecture", "values": [arch]}
        ]
    ).id,
    "Amazon Linux": aws.ec2.get_ami(
        owners=["137112412989"],
        most_recent=True,
        filters=[
            {"name": "name", "values": ["amzn2-ami-hvm-*"]},
            {"name": "architecture", "values": [arch]}
        ]
    ).id
}

if ami_choice not in ami_options:
    raise ValueError(f"Invalid AMI choice: {ami_choice}. Choose 'Ubuntu' or 'Amazon Linux'.")

ami_id = ami_options[ami_choice]

instances = []
for i in range(instance_count):
    unique_instance_name = instance_names[i]  
    instance = aws.ec2.Instance(
        unique_instance_name,
        instance_type=instance_type,
        ami=ami_id,
        tags={
            "Name": unique_instance_name, 
            "CreatedBy": "Pulumi",
            "Owner": "avioratar"
        },
        opts=pulumi.ResourceOptions(
            retain_on_delete=True,
            replace_on_changes=["ami", "instance_type"],
            delete_before_replace=False
        )
    )
    instances.append(instance)

pulumi.export("instance_ids", [instance.id for instance in instances])

