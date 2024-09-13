from django.conf import settings

SUBNET_DIVISION_TYPES = getattr(
    settings,
    'IMMUNITY_CONTROLLER_SUBNET_DIVISION_TYPES',
    (
        (
            (
                'immunity_controller.subnet_division.rule_types.'
                'vpn.VpnSubnetDivisionRuleType'
            ),
            'VPN',
        ),
        (
            (
                'immunity_controller.subnet_division.rule_types.'
                'device.DeviceSubnetDivisionRuleType'
            ),
            'Device',
        ),
    ),
)

HIDE_GENERATED_SUBNETS = getattr(
    settings,
    'IMMUNITY_CONTROLLER_HIDE_AUTOMATICALLY_GENERATED_SUBNETS_AND_IPS',
    False,
)
