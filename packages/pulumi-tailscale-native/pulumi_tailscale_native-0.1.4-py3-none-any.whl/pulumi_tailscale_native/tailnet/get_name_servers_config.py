# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload, Awaitable
from .. import _utilities

__all__ = [
    'NameServers',
    'AwaitableNameServers',
    'get_name_servers_config',
    'get_name_servers_config_output',
]

@pulumi.output_type
class NameServers:
    def __init__(__self__, dns=None, magic_dns=None):
        if dns and not isinstance(dns, list):
            raise TypeError("Expected argument 'dns' to be a list")
        pulumi.set(__self__, "dns", dns)
        if magic_dns and not isinstance(magic_dns, bool):
            raise TypeError("Expected argument 'magic_dns' to be a bool")
        pulumi.set(__self__, "magic_dns", magic_dns)

    @property
    @pulumi.getter
    def dns(self) -> Sequence[str]:
        return pulumi.get(self, "dns")

    @property
    @pulumi.getter(name="magicDNS")
    def magic_dns(self) -> bool:
        return pulumi.get(self, "magic_dns")


class AwaitableNameServers(NameServers):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return NameServers(
            dns=self.dns,
            magic_dns=self.magic_dns)


def get_name_servers_config(tailnet: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableNameServers:
    """
    Use this data source to access information about an existing resource.

    :param str tailnet: For paid plans, your domain is your tailnet. For solo plans, the tailnet is the email you signed up with. So `alice@gmail.com` has the tailnet `alice@gmail.com` since `@gmail.com` is a shared email host. Alternatively, you can specify the value "-" to refer to the default tailnet of the authenticated user making the API call.
    """
    __args__ = dict()
    __args__['tailnet'] = tailnet
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('tailscale-native:tailnet:getNameServersConfig', __args__, opts=opts, typ=NameServers).value

    return AwaitableNameServers(
        dns=pulumi.get(__ret__, 'dns'),
        magic_dns=pulumi.get(__ret__, 'magic_dns'))


@_utilities.lift_output_func(get_name_servers_config)
def get_name_servers_config_output(tailnet: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[NameServers]:
    """
    Use this data source to access information about an existing resource.

    :param str tailnet: For paid plans, your domain is your tailnet. For solo plans, the tailnet is the email you signed up with. So `alice@gmail.com` has the tailnet `alice@gmail.com` since `@gmail.com` is a shared email host. Alternatively, you can specify the value "-" to refer to the default tailnet of the authenticated user making the API call.
    """
    ...
