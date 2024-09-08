from typing import List, Optional, TypeVar, Generic, Any, Dict
from pydantic import BaseModel

# Define a type variable for generic environment-specific account settings
G = TypeVar('G', bound=BaseModel)

# Base model for AccountsDict to rigidly define the structure of accounts
class AccountsDict(BaseModel, Generic[G]):
    development: G
    qa: G
    production: G
    sharedservices: Optional[Any]
    sandbox: Optional[Any]

# Base model for EnvironmentParameters using Pydantic
class EnvironmentParameters(BaseModel, Generic[G]):
    accounts: AccountsDict[G]
    networking: Optional[Any]  # You can replace Any with a specific model for networking if desired

class BaseAccount(BaseModel):
    name: str
    id: str

class DefaultAccount(BaseAccount):
    name: str
    id: str
    vpc: str
    public_subnet_ids: List[str]
    private_subnet_ids: List[str]
    availability_zones: List[str]
    az: str
    bastion_host_security_group: str
    bastion_host_production_control_security_group: str
    bastion_host_windows_admin_security_group: str
    scan_target_security_group: str
    asg_sns_topic: str
    asg_cw_alerts_lc_hooks_role: str
    asg_cw_alerts_lc_hooks_launch_sns: str
    asg_cw_alerts_lc_hooks_terminate_sns: str
    web_acl: str
    s3_config_bucket: str
    smtp_relay_security_group: str
    smtp_server_endpoint: str
    smtp_server_port: str
    kms_ssm_key: str
    kms_ebs_key: str
    kms_rds_key: str
    kms_vault_key: str
    kms_neptune_key: str
    app_proxy_security_group: str
    cognito_user_pool_arn: str
    cognito_domain: str
    ssl_certificate_star_fao_org_arn: str
    ssl_certificate_star_fao_org_arn_north_virginia: str
    oracle_oem_client_security_group: str
    cloudfront_only_access_security_group: str
    ldap_access_security_group: str
    domain_control_access_security_group: str
    route53_hosted_zone_id: Optional[str] = None
    route53_domain_name: Optional[str] = None