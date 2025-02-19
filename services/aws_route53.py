from services import aws_route53_zones
from services import aws_route53_records
from utils.utils import user_input

def manage_route53():
    while True:
        route53_action = user_input("Select an action:", ["Manage DNS Zone", "Manage DNS Records", "Exit"])
        if route53_action == "Exit":
            break
        elif route53_action == "Manage DNS Zone":
            while True:
                zone_action = user_input("Select action:", ["List Hosted Zones", "Create Hosted Zone", "Delete Hosted Zone", "Exit"])
                if zone_action == "Exit":
                    break
                elif zone_action == "List Hosted Zones":
                    aws_route53_zones.list_hosted_zones()
                elif zone_action == "Create Hosted Zone":
                    aws_route53_zones.create_hosted_zone()
                elif zone_action == "Delete Hosted Zone":
                    aws_route53_zones.delete_hosted_zone()
        elif route53_action == "Manage DNS Records":
            while True:
                record_action = user_input("Select action:", ["List DNS Records", "Create DNS Record", "Delete DNS Record", "Exit"])
                if record_action == "Exit":
                    break
                elif record_action == "List DNS Records":
                    aws_route53_records.list_dns_records()
                elif record_action == "Create DNS Record":
                    aws_route53_records.create_dns_record()
                elif record_action == "Delete DNS Record":
                    aws_route53_records.delete_dns_record()
