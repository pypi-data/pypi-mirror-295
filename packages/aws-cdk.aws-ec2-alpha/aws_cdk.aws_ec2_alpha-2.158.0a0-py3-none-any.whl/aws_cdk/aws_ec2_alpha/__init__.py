r'''
# Amazon VpcV2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## VpcV2

`VpcV2` is a re-write of the [`ec2.Vpc`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Vpc.html) construct. This new construct enables higher level of customization
on the VPC being created. `VpcV2` implements the existing [`IVpc`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.IVpc.html), therefore,
`VpcV2` is compatible with other constructs that accepts `IVpc` (e.g. [`ApplicationLoadBalancer`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationLoadBalancer.html#construct-props)).

To create a VPC with both IPv4 and IPv6 support:

```python
stack = Stack()
vpc_v2.VpcV2(self, "Vpc",
    primary_address_block=vpc_v2.IpAddresses.ipv4("10.0.0.0/24"),
    secondary_address_blocks=[
        vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonProvidedIpv6")
    ]
)
```

`VpcV2` does not automatically create subnets or allocate IP addresses, which is different from the `Vpc` construct.

Importing existing VPC in an account into CDK as a `VpcV2` is not yet supported.

## SubnetV2

`SubnetV2` is a re-write of the [`ec2.Subnet`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Subnet.html) construct.
This new construct can be used to add subnets to a `VpcV2` instance:

```python
stack = Stack()
my_vpc = vpc_v2.VpcV2(self, "Vpc",
    secondary_address_blocks=[
        vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonProvidedIp")
    ]
)

vpc_v2.SubnetV2(self, "subnetA",
    vpc=my_vpc,
    availability_zone="us-east-1a",
    ipv4_cidr_block=vpc_v2.IpCidr("10.0.0.0/24"),
    ipv6_cidr_block=vpc_v2.IpCidr("2a05:d02c:25:4000::/60"),
    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
)
```

Same as `VpcV2`, importing existing subnets is not yet supported.

## IP Addresses Management

By default `VpcV2` uses `10.0.0.0/16` as the primary CIDR if none is defined.
Additional CIDRs can be adding to the VPC via the `secondaryAddressBlocks` prop.
The following example illustrates the different options of defining the address blocks:

```python
stack = Stack()
ipam = Ipam(self, "Ipam",
    operating_region=["us-west-1"]
)
ipam_public_pool = ipam.public_scope.add_pool("PublicPoolA",
    address_family=vpc_v2.AddressFamily.IP_V6,
    aws_service=AwsServiceName.EC2,
    locale="us-west-1",
    public_ip_source=vpc_v2.IpamPoolPublicIpSource.AMAZON
)
ipam_public_pool.provision_cidr("PublicPoolACidrA", netmask_length=52)

ipam_private_pool = ipam.private_scope.add_pool("PrivatePoolA",
    address_family=vpc_v2.AddressFamily.IP_V4
)
ipam_private_pool.provision_cidr("PrivatePoolACidrA", netmask_length=8)

vpc_v2.VpcV2(self, "Vpc",
    primary_address_block=vpc_v2.IpAddresses.ipv4("10.0.0.0/24"),
    secondary_address_blocks=[
        vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonIpv6"),
        vpc_v2.IpAddresses.ipv6_ipam(
            ipam_pool=ipam_public_pool,
            netmask_length=52,
            cidr_block_name="ipv6Ipam"
        ),
        vpc_v2.IpAddresses.ipv4_ipam(
            ipam_pool=ipam_private_pool,
            netmask_length=8,
            cidr_block_name="ipv4Ipam"
        )
    ]
)
```

Since `VpcV2` does not create subnets automatically, users have full control over IP addresses allocation across subnets.

## Routing

`RouteTable` is a new construct that allows for route tables to be customized in a variety of ways. For instance, the following example shows how a custom route table can be created and appended to a subnet:

```python
my_vpc = vpc_v2.VpcV2(self, "Vpc")
route_table = vpc_v2.RouteTable(self, "RouteTable",
    vpc=my_vpc
)
subnet = vpc_v2.SubnetV2(self, "Subnet",
    vpc=my_vpc,
    route_table=route_table,
    availability_zone="eu-west-2a",
    ipv4_cidr_block=IpCidr("10.0.0.0/24"),
    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
)
```

`Route`s can be created to link subnets to various different AWS services via gateways and endpoints. Each unique route target has its own dedicated construct that can be routed to a given subnet via the `Route` construct. An example using the `InternetGateway` construct can be seen below:

```python
stack = Stack()
my_vpc = vpc_v2.VpcV2(self, "Vpc")
route_table = vpc_v2.RouteTable(self, "RouteTable",
    vpc=my_vpc
)
subnet = vpc_v2.SubnetV2(self, "Subnet",
    vpc=my_vpc,
    availability_zone="eu-west-2a",
    ipv4_cidr_block=IpCidr("10.0.0.0/24"),
    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
)

igw = vpc_v2.InternetGateway(self, "IGW",
    vpc=my_vpc
)
vpc_v2.Route(self, "IgwRoute",
    route_table=route_table,
    destination="0.0.0.0/0",
    target={"gateway": igw}
)
```

Other route targets may require a deeper set of parameters to set up properly. For instance, the example below illustrates how to set up a `NatGateway`:

```python
my_vpc = vpc_v2.VpcV2(self, "Vpc")
route_table = vpc_v2.RouteTable(self, "RouteTable",
    vpc=my_vpc
)
subnet = vpc_v2.SubnetV2(self, "Subnet",
    vpc=my_vpc,
    availability_zone="eu-west-2a",
    ipv4_cidr_block=IpCidr("10.0.0.0/24"),
    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
)

natgw = vpc_v2.NatGateway(self, "NatGW",
    subnet=subnet,
    vpc=my_vpc,
    connectivity_type=NatConnectivityType.PRIVATE,
    private_ip_address="10.0.0.42"
)
vpc_v2.Route(self, "NatGwRoute",
    route_table=route_table,
    destination="0.0.0.0/0",
    target={"gateway": natgw}
)
```

It is also possible to set up endpoints connecting other AWS services. For instance, the example below illustrates the linking of a Dynamo DB endpoint via the existing `ec2.GatewayVpcEndpoint` construct as a route target:

```python
my_vpc = vpc_v2.VpcV2(self, "Vpc")
route_table = vpc_v2.RouteTable(self, "RouteTable",
    vpc=my_vpc
)
subnet = vpc_v2.SubnetV2(self, "Subnet",
    vpc=my_vpc,
    availability_zone="eu-west-2a",
    ipv4_cidr_block=IpCidr("10.0.0.0/24"),
    subnet_type=ec2.SubnetType.PRIVATE
)

dynamo_endpoint = ec2.GatewayVpcEndpoint(self, "DynamoEndpoint",
    service=ec2.GatewayVpcEndpointAwsService.DYNAMODB,
    vpc=my_vpc,
    subnets=[subnet]
)
vpc_v2.Route(self, "DynamoDBRoute",
    route_table=route_table,
    destination="0.0.0.0/0",
    target={"endpoint": dynamo_endpoint}
)
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws-cdk/aws-ec2-alpha.AddressFamily")
class AddressFamily(enum.Enum):
    '''(experimental) Represents the address family for IP addresses in an IPAM pool.

    IP_V4 - Represents the IPv4 address family.
    IP_V6 - Represents the IPv6 address family.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipampool.html#cfn-ec2-ipampool-addressfamily
    :stability: experimental
    :exampleMetadata: infused

    Example::

        stack = Stack()
        ipam = Ipam(self, "Ipam",
            operating_region=["us-west-1"]
        )
        ipam_public_pool = ipam.public_scope.add_pool("PublicPoolA",
            address_family=vpc_v2.AddressFamily.IP_V6,
            aws_service=AwsServiceName.EC2,
            locale="us-west-1",
            public_ip_source=vpc_v2.IpamPoolPublicIpSource.AMAZON
        )
        ipam_public_pool.provision_cidr("PublicPoolACidrA", netmask_length=52)
        
        ipam_private_pool = ipam.private_scope.add_pool("PrivatePoolA",
            address_family=vpc_v2.AddressFamily.IP_V4
        )
        ipam_private_pool.provision_cidr("PrivatePoolACidrA", netmask_length=8)
        
        vpc_v2.VpcV2(self, "Vpc",
            primary_address_block=vpc_v2.IpAddresses.ipv4("10.0.0.0/24"),
            secondary_address_blocks=[
                vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonIpv6"),
                vpc_v2.IpAddresses.ipv6_ipam(
                    ipam_pool=ipam_public_pool,
                    netmask_length=52,
                    cidr_block_name="ipv6Ipam"
                ),
                vpc_v2.IpAddresses.ipv4_ipam(
                    ipam_pool=ipam_private_pool,
                    netmask_length=8,
                    cidr_block_name="ipv4Ipam"
                )
            ]
        )
    '''

    IP_V4 = "IP_V4"
    '''(experimental) Represents the IPv4 address family.

    Allowed under public and private pool.

    :stability: experimental
    '''
    IP_V6 = "IP_V6"
    '''(experimental) Represents the IPv6 address family.

    Only allowed under public pool.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-ec2-alpha.AwsServiceName")
class AwsServiceName(enum.Enum):
    '''(experimental) Limits which service in AWS that the pool can be used in.

    :stability: experimental
    '''

    EC2 = "EC2"
    '''(experimental) Allows users to use space for Elastic IP addresses and VPCs.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.EgressOnlyInternetGatewayProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "egress_only_internet_gateway_name": "egressOnlyInternetGatewayName",
    },
)
class EgressOnlyInternetGatewayProps:
    def __init__(
        self,
        *,
        vpc: "IVpcV2",
        egress_only_internet_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to define an egress-only internet gateway.

        :param vpc: (experimental) The ID of the VPC for which to create the egress-only internet gateway.
        :param egress_only_internet_gateway_name: (experimental) The resource name of the egress-only internet gateway. Default: none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ec2_alpha as ec2_alpha
            
            # vpc_v2: ec2_alpha.VpcV2
            
            egress_only_internet_gateway_props = ec2_alpha.EgressOnlyInternetGatewayProps(
                vpc=vpc_v2,
            
                # the properties below are optional
                egress_only_internet_gateway_name="egressOnlyInternetGatewayName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1cb0281052a85d3461453c956e87b81e82be05002c1ac33451b382cfcf0ea7e)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument egress_only_internet_gateway_name", value=egress_only_internet_gateway_name, expected_type=type_hints["egress_only_internet_gateway_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if egress_only_internet_gateway_name is not None:
            self._values["egress_only_internet_gateway_name"] = egress_only_internet_gateway_name

    @builtins.property
    def vpc(self) -> "IVpcV2":
        '''(experimental) The ID of the VPC for which to create the egress-only internet gateway.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast("IVpcV2", result)

    @builtins.property
    def egress_only_internet_gateway_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The resource name of the egress-only internet gateway.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("egress_only_internet_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EgressOnlyInternetGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-ec2-alpha.IIpAddresses")
class IIpAddresses(typing_extensions.Protocol):
    '''(experimental) Implements ip address allocation according to the IPAdress type.

    :stability: experimental
    '''

    @jsii.member(jsii_name="allocateVpcCidr")
    def allocate_vpc_cidr(self) -> "VpcCidrOptions":
        '''(experimental) Method to define the implementation logic of IP address allocation.

        :stability: experimental
        '''
        ...


class _IIpAddressesProxy:
    '''(experimental) Implements ip address allocation according to the IPAdress type.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ec2-alpha.IIpAddresses"

    @jsii.member(jsii_name="allocateVpcCidr")
    def allocate_vpc_cidr(self) -> "VpcCidrOptions":
        '''(experimental) Method to define the implementation logic of IP address allocation.

        :stability: experimental
        '''
        return typing.cast("VpcCidrOptions", jsii.invoke(self, "allocateVpcCidr", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIpAddresses).__jsii_proxy_class__ = lambda : _IIpAddressesProxy


@jsii.interface(jsii_type="@aws-cdk/aws-ec2-alpha.IIpamPool")
class IIpamPool(typing_extensions.Protocol):
    '''(experimental) Definition used to add or create a new IPAM pool.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ipamCidrs")
    def ipam_cidrs(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPoolCidr]:
        '''(experimental) Pool CIDR for IPv6 to be provisioned with Public IP source set to 'Amazon'.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ipamPoolId")
    def ipam_pool_id(self) -> builtins.str:
        '''(experimental) Pool ID to be passed to the VPC construct.

        :stability: experimental
        :attribute: IpamPoolId
        '''
        ...

    @jsii.member(jsii_name="provisionCidr")
    def provision_cidr(
        self,
        id: builtins.str,
        *,
        cidr: typing.Optional[builtins.str] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.CfnIPAMPoolCidr:
        '''(experimental) Function to associate a IPv6 address with IPAM pool.

        :param id: -
        :param cidr: (experimental) Ipv6 CIDR block for the IPAM pool. Default: none
        :param netmask_length: (experimental) Ipv6 Netmask length for the CIDR. Default: none

        :stability: experimental
        '''
        ...


class _IIpamPoolProxy:
    '''(experimental) Definition used to add or create a new IPAM pool.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ec2-alpha.IIpamPool"

    @builtins.property
    @jsii.member(jsii_name="ipamCidrs")
    def ipam_cidrs(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPoolCidr]:
        '''(experimental) Pool CIDR for IPv6 to be provisioned with Public IP source set to 'Amazon'.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPoolCidr], jsii.get(self, "ipamCidrs"))

    @builtins.property
    @jsii.member(jsii_name="ipamPoolId")
    def ipam_pool_id(self) -> builtins.str:
        '''(experimental) Pool ID to be passed to the VPC construct.

        :stability: experimental
        :attribute: IpamPoolId
        '''
        return typing.cast(builtins.str, jsii.get(self, "ipamPoolId"))

    @jsii.member(jsii_name="provisionCidr")
    def provision_cidr(
        self,
        id: builtins.str,
        *,
        cidr: typing.Optional[builtins.str] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.CfnIPAMPoolCidr:
        '''(experimental) Function to associate a IPv6 address with IPAM pool.

        :param id: -
        :param cidr: (experimental) Ipv6 CIDR block for the IPAM pool. Default: none
        :param netmask_length: (experimental) Ipv6 Netmask length for the CIDR. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4bc97652054ab6c0bbc03431c16bfd7acb0fddbb3d48a9495d8b53ad88d5dc8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = IpamPoolCidrProvisioningOptions(
            cidr=cidr, netmask_length=netmask_length
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnIPAMPoolCidr, jsii.invoke(self, "provisionCidr", [id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIpamPool).__jsii_proxy_class__ = lambda : _IIpamPoolProxy


@jsii.interface(jsii_type="@aws-cdk/aws-ec2-alpha.IIpamScopeBase")
class IIpamScopeBase(typing_extensions.Protocol):
    '''(experimental) Interface for IpamScope Class.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> _constructs_77d1e7e8.Construct:
        '''(experimental) Reference to the current scope of stack to be passed in order to create a new IPAM pool.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        '''(experimental) Default Scope ids created by the IPAM or a new Resource id.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="scopeType")
    def scope_type(self) -> typing.Optional["IpamScopeType"]:
        '''(experimental) Defines scope type can be either default or custom.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addPool")
    def add_pool(
        self,
        id: builtins.str,
        *,
        address_family: AddressFamily,
        aws_service: typing.Optional[AwsServiceName] = None,
        ipv4_provisioned_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        locale: typing.Optional[builtins.str] = None,
        public_ip_source: typing.Optional["IpamPoolPublicIpSource"] = None,
    ) -> IIpamPool:
        '''(experimental) Function to add a new pool to an IPAM scope.

        :param id: -
        :param address_family: (experimental) addressFamily - The address family of the pool (ipv4 or ipv6).
        :param aws_service: (experimental) Limits which service in AWS that the pool can be used in. "ec2", for example, allows users to use space for Elastic IP addresses and VPCs. Default: - No service
        :param ipv4_provisioned_cidrs: (experimental) Information about the CIDRs provisioned to the pool. Default: - No CIDRs are provisioned
        :param locale: (experimental) The locale (AWS Region) of the pool. Should be one of the IPAM operating region. Only resources in the same Region as the locale of the pool can get IP address allocations from the pool. You can only allocate a CIDR for a VPC, for example, from an IPAM pool that shares a locale with the VPC’s Region. Note that once you choose a Locale for a pool, you cannot modify it. If you choose an AWS Region for locale that has not been configured as an operating Region for the IPAM, you'll get an error. Default: - Current operating region
        :param public_ip_source: (experimental) The IP address source for pools in the public scope. Only used for IPv6 address Only allowed values to this are 'byoip' or 'amazon' Default: amazon

        :stability: experimental
        '''
        ...


class _IIpamScopeBaseProxy:
    '''(experimental) Interface for IpamScope Class.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ec2-alpha.IIpamScopeBase"

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> _constructs_77d1e7e8.Construct:
        '''(experimental) Reference to the current scope of stack to be passed in order to create a new IPAM pool.

        :stability: experimental
        '''
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        '''(experimental) Default Scope ids created by the IPAM or a new Resource id.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @builtins.property
    @jsii.member(jsii_name="scopeType")
    def scope_type(self) -> typing.Optional["IpamScopeType"]:
        '''(experimental) Defines scope type can be either default or custom.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IpamScopeType"], jsii.get(self, "scopeType"))

    @jsii.member(jsii_name="addPool")
    def add_pool(
        self,
        id: builtins.str,
        *,
        address_family: AddressFamily,
        aws_service: typing.Optional[AwsServiceName] = None,
        ipv4_provisioned_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        locale: typing.Optional[builtins.str] = None,
        public_ip_source: typing.Optional["IpamPoolPublicIpSource"] = None,
    ) -> IIpamPool:
        '''(experimental) Function to add a new pool to an IPAM scope.

        :param id: -
        :param address_family: (experimental) addressFamily - The address family of the pool (ipv4 or ipv6).
        :param aws_service: (experimental) Limits which service in AWS that the pool can be used in. "ec2", for example, allows users to use space for Elastic IP addresses and VPCs. Default: - No service
        :param ipv4_provisioned_cidrs: (experimental) Information about the CIDRs provisioned to the pool. Default: - No CIDRs are provisioned
        :param locale: (experimental) The locale (AWS Region) of the pool. Should be one of the IPAM operating region. Only resources in the same Region as the locale of the pool can get IP address allocations from the pool. You can only allocate a CIDR for a VPC, for example, from an IPAM pool that shares a locale with the VPC’s Region. Note that once you choose a Locale for a pool, you cannot modify it. If you choose an AWS Region for locale that has not been configured as an operating Region for the IPAM, you'll get an error. Default: - Current operating region
        :param public_ip_source: (experimental) The IP address source for pools in the public scope. Only used for IPv6 address Only allowed values to this are 'byoip' or 'amazon' Default: amazon

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab59e34a032c2ecbc5b1f46184e5eafc041fe87fd1c685e9d6723df4798da29)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = PoolOptions(
            address_family=address_family,
            aws_service=aws_service,
            ipv4_provisioned_cidrs=ipv4_provisioned_cidrs,
            locale=locale,
            public_ip_source=public_ip_source,
        )

        return typing.cast(IIpamPool, jsii.invoke(self, "addPool", [id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIpamScopeBase).__jsii_proxy_class__ = lambda : _IIpamScopeBaseProxy


@jsii.interface(jsii_type="@aws-cdk/aws-ec2-alpha.IRouteTarget")
class IRouteTarget(typing_extensions.Protocol):
    '''(experimental) Interface to define a routing target, such as an egress-only internet gateway or VPC endpoint.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="routerTargetId")
    def router_target_id(self) -> builtins.str:
        '''(experimental) The ID of the route target.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="routerType")
    def router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''(experimental) The type of router used in the route.

        :stability: experimental
        '''
        ...


class _IRouteTargetProxy:
    '''(experimental) Interface to define a routing target, such as an egress-only internet gateway or VPC endpoint.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ec2-alpha.IRouteTarget"

    @builtins.property
    @jsii.member(jsii_name="routerTargetId")
    def router_target_id(self) -> builtins.str:
        '''(experimental) The ID of the route target.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routerTargetId"))

    @builtins.property
    @jsii.member(jsii_name="routerType")
    def router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''(experimental) The type of router used in the route.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.RouterType, jsii.get(self, "routerType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRouteTarget).__jsii_proxy_class__ = lambda : _IRouteTargetProxy


@jsii.interface(jsii_type="@aws-cdk/aws-ec2-alpha.IRouteV2")
class IRouteV2(typing_extensions.Protocol):
    '''(experimental) Interface to define a route.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        '''(experimental) The IPv4 or IPv6 CIDR block used for the destination match.

        Routing decisions are based on the most specific match.
        TODO: Look for strong IP type implementation here.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="routeTable")
    def route_table(self) -> _aws_cdk_aws_ec2_ceddda9d.IRouteTable:
        '''(experimental) The ID of the route table for the route.

        :stability: experimental
        :attribute: routeTable
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "RouteTargetType":
        '''(experimental) The gateway or endpoint targeted by the route.

        :stability: experimental
        '''
        ...


class _IRouteV2Proxy:
    '''(experimental) Interface to define a route.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ec2-alpha.IRouteV2"

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        '''(experimental) The IPv4 or IPv6 CIDR block used for the destination match.

        Routing decisions are based on the most specific match.
        TODO: Look for strong IP type implementation here.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="routeTable")
    def route_table(self) -> _aws_cdk_aws_ec2_ceddda9d.IRouteTable:
        '''(experimental) The ID of the route table for the route.

        :stability: experimental
        :attribute: routeTable
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IRouteTable, jsii.get(self, "routeTable"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "RouteTargetType":
        '''(experimental) The gateway or endpoint targeted by the route.

        :stability: experimental
        '''
        return typing.cast("RouteTargetType", jsii.get(self, "target"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRouteV2).__jsii_proxy_class__ = lambda : _IRouteV2Proxy


@jsii.interface(jsii_type="@aws-cdk/aws-ec2-alpha.ISubnetV2")
class ISubnetV2(_aws_cdk_aws_ec2_ceddda9d.ISubnet, typing_extensions.Protocol):
    '''(experimental) Interface with additional properties for SubnetV2.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ipv6CidrBlock")
    def ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
        '''(experimental) The IPv6 CIDR block for this subnet.

        :stability: experimental
        '''
        ...


class _ISubnetV2Proxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.ISubnet), # type: ignore[misc]
):
    '''(experimental) Interface with additional properties for SubnetV2.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ec2-alpha.ISubnetV2"

    @builtins.property
    @jsii.member(jsii_name="ipv6CidrBlock")
    def ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
        '''(experimental) The IPv6 CIDR block for this subnet.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6CidrBlock"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISubnetV2).__jsii_proxy_class__ = lambda : _ISubnetV2Proxy


@jsii.interface(jsii_type="@aws-cdk/aws-ec2-alpha.IVpcV2")
class IVpcV2(_aws_cdk_aws_ec2_ceddda9d.IVpc, typing_extensions.Protocol):
    '''(experimental) Placeholder to see what extra props we might need, will be added to original IVPC.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ipv4CidrBlock")
    def ipv4_cidr_block(self) -> builtins.str:
        '''(experimental) The primary IPv4 CIDR block associated with the VPC.

        Needed in order to validate the vpc range of subnet
        current prop vpcCidrBlock refers to the token value
        For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-sizing-ipv4}.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secondaryCidrBlock")
    def secondary_cidr_block(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnVPCCidrBlock]:
        '''(experimental) The secondary CIDR blocks associated with the VPC.

        For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-resize}.

        :stability: experimental
        '''
        ...


class _IVpcV2Proxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IVpc), # type: ignore[misc]
):
    '''(experimental) Placeholder to see what extra props we might need, will be added to original IVPC.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ec2-alpha.IVpcV2"

    @builtins.property
    @jsii.member(jsii_name="ipv4CidrBlock")
    def ipv4_cidr_block(self) -> builtins.str:
        '''(experimental) The primary IPv4 CIDR block associated with the VPC.

        Needed in order to validate the vpc range of subnet
        current prop vpcCidrBlock refers to the token value
        For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-sizing-ipv4}.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ipv4CidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="secondaryCidrBlock")
    def secondary_cidr_block(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnVPCCidrBlock]:
        '''(experimental) The secondary CIDR blocks associated with the VPC.

        For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-resize}.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnVPCCidrBlock], jsii.get(self, "secondaryCidrBlock"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVpcV2).__jsii_proxy_class__ = lambda : _IVpcV2Proxy


@jsii.implements(IRouteTarget)
class InternetGateway(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.InternetGateway",
):
    '''(experimental) Creates an internet gateway.

    :stability: experimental
    :resource: AWS::EC2::InternetGateway
    :exampleMetadata: infused

    Example::

        stack = Stack()
        my_vpc = vpc_v2.VpcV2(self, "Vpc")
        route_table = vpc_v2.RouteTable(self, "RouteTable",
            vpc=my_vpc
        )
        subnet = vpc_v2.SubnetV2(self, "Subnet",
            vpc=my_vpc,
            availability_zone="eu-west-2a",
            ipv4_cidr_block=IpCidr("10.0.0.0/24"),
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        )
        
        igw = vpc_v2.InternetGateway(self, "IGW",
            vpc=my_vpc
        )
        vpc_v2.Route(self, "IgwRoute",
            route_table=route_table,
            destination="0.0.0.0/0",
            target={"gateway": igw}
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: IVpcV2,
        internet_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: (experimental) The ID of the VPC for which to create the internet gateway.
        :param internet_gateway_name: (experimental) The resource name of the internet gateway. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ed9b26ff938b529db1af6f12978e1aa57b9cdaf5a5c589675cf7b8f2c6fe6a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InternetGatewayProps(
            vpc=vpc, internet_gateway_name=internet_gateway_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnInternetGateway:
        '''(experimental) The internet gateway CFN resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnInternetGateway, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="routerTargetId")
    def router_target_id(self) -> builtins.str:
        '''(experimental) The ID of the route target.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routerTargetId"))

    @builtins.property
    @jsii.member(jsii_name="routerType")
    def router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''(experimental) The type of router used in the route.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.RouterType, jsii.get(self, "routerType"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        '''(experimental) The ID of the VPC for which to create the internet gateway.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.InternetGatewayProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc", "internet_gateway_name": "internetGatewayName"},
)
class InternetGatewayProps:
    def __init__(
        self,
        *,
        vpc: IVpcV2,
        internet_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to define an internet gateway.

        :param vpc: (experimental) The ID of the VPC for which to create the internet gateway.
        :param internet_gateway_name: (experimental) The resource name of the internet gateway. Default: none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            stack = Stack()
            my_vpc = vpc_v2.VpcV2(self, "Vpc")
            route_table = vpc_v2.RouteTable(self, "RouteTable",
                vpc=my_vpc
            )
            subnet = vpc_v2.SubnetV2(self, "Subnet",
                vpc=my_vpc,
                availability_zone="eu-west-2a",
                ipv4_cidr_block=IpCidr("10.0.0.0/24"),
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
            
            igw = vpc_v2.InternetGateway(self, "IGW",
                vpc=my_vpc
            )
            vpc_v2.Route(self, "IgwRoute",
                route_table=route_table,
                destination="0.0.0.0/0",
                target={"gateway": igw}
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4699002455f77fce358247d059e2af25aa232257e94012a7ff9adcc0f4d4268)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument internet_gateway_name", value=internet_gateway_name, expected_type=type_hints["internet_gateway_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if internet_gateway_name is not None:
            self._values["internet_gateway_name"] = internet_gateway_name

    @builtins.property
    def vpc(self) -> IVpcV2:
        '''(experimental) The ID of the VPC for which to create the internet gateway.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(IVpcV2, result)

    @builtins.property
    def internet_gateway_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The resource name of the internet gateway.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("internet_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternetGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IpAddresses(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.IpAddresses",
):
    '''(experimental) IpAddress options to define VPC V2.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        stack = Stack()
        my_vpc = vpc_v2.VpcV2(self, "Vpc",
            secondary_address_blocks=[
                vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonProvidedIp")
            ]
        )
        
        vpc_v2.SubnetV2(self, "subnetA",
            vpc=my_vpc,
            availability_zone="us-east-1a",
            ipv4_cidr_block=vpc_v2.IpCidr("10.0.0.0/24"),
            ipv6_cidr_block=vpc_v2.IpCidr("2a05:d02c:25:4000::/60"),
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="amazonProvidedIpv6")
    @builtins.classmethod
    def amazon_provided_ipv6(cls, *, cidr_block_name: builtins.str) -> IIpAddresses:
        '''(experimental) Amazon Provided Ipv6 range.

        :param cidr_block_name: (experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource.

        :stability: experimental
        '''
        props = SecondaryAddressProps(cidr_block_name=cidr_block_name)

        return typing.cast(IIpAddresses, jsii.sinvoke(cls, "amazonProvidedIpv6", [props]))

    @jsii.member(jsii_name="ipv4")
    @builtins.classmethod
    def ipv4(
        cls,
        ipv4_cidr: builtins.str,
        *,
        cidr_block_name: builtins.str,
    ) -> IIpAddresses:
        '''(experimental) An IPv4 CIDR Range.

        :param ipv4_cidr: -
        :param cidr_block_name: (experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__023808e0046a190f50dc770cc212c33e5f498063e503f04733eccd089bee0a1c)
            check_type(argname="argument ipv4_cidr", value=ipv4_cidr, expected_type=type_hints["ipv4_cidr"])
        props = SecondaryAddressProps(cidr_block_name=cidr_block_name)

        return typing.cast(IIpAddresses, jsii.sinvoke(cls, "ipv4", [ipv4_cidr, props]))

    @jsii.member(jsii_name="ipv4Ipam")
    @builtins.classmethod
    def ipv4_ipam(
        cls,
        *,
        cidr_block_name: builtins.str,
        ipam_pool: typing.Optional[IIpamPool] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
    ) -> IIpAddresses:
        '''(experimental) An Ipv4 Ipam Pool.

        :param cidr_block_name: (experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource.
        :param ipam_pool: (experimental) Ipv4 or an Ipv6 IPAM pool Only required when using AWS Ipam. Default: - None
        :param netmask_length: (experimental) CIDR Mask for Vpc Only required when using AWS Ipam. Default: - None

        :stability: experimental
        '''
        ipv4_ipam_options = IpamOptions(
            cidr_block_name=cidr_block_name,
            ipam_pool=ipam_pool,
            netmask_length=netmask_length,
        )

        return typing.cast(IIpAddresses, jsii.sinvoke(cls, "ipv4Ipam", [ipv4_ipam_options]))

    @jsii.member(jsii_name="ipv6Ipam")
    @builtins.classmethod
    def ipv6_ipam(
        cls,
        *,
        cidr_block_name: builtins.str,
        ipam_pool: typing.Optional[IIpamPool] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
    ) -> IIpAddresses:
        '''(experimental) An Ipv6 Ipam Pool.

        :param cidr_block_name: (experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource.
        :param ipam_pool: (experimental) Ipv4 or an Ipv6 IPAM pool Only required when using AWS Ipam. Default: - None
        :param netmask_length: (experimental) CIDR Mask for Vpc Only required when using AWS Ipam. Default: - None

        :stability: experimental
        '''
        ipv6_ipam_options = IpamOptions(
            cidr_block_name=cidr_block_name,
            ipam_pool=ipam_pool,
            netmask_length=netmask_length,
        )

        return typing.cast(IIpAddresses, jsii.sinvoke(cls, "ipv6Ipam", [ipv6_ipam_options]))


class IpCidr(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2-alpha.IpCidr"):
    '''(experimental) IPv4 or IPv6 CIDR range for the subnet.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        stack = Stack()
        my_vpc = vpc_v2.VpcV2(self, "Vpc")
        route_table = vpc_v2.RouteTable(self, "RouteTable",
            vpc=my_vpc
        )
        subnet = vpc_v2.SubnetV2(self, "Subnet",
            vpc=my_vpc,
            availability_zone="eu-west-2a",
            ipv4_cidr_block=IpCidr("10.0.0.0/24"),
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        )
        
        igw = vpc_v2.InternetGateway(self, "IGW",
            vpc=my_vpc
        )
        vpc_v2.Route(self, "IgwRoute",
            route_table=route_table,
            destination="0.0.0.0/0",
            target={"gateway": igw}
        )
    '''

    def __init__(self, props: builtins.str) -> None:
        '''
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a863e7a355c78c90751f90234cc17db747d36357a2406915207b6aa4fd217e08)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        '''(experimental) IPv6 CIDR range for the subnet Allowed only if IPv6 is enabled on VPc.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cidr"))


class Ipam(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.Ipam",
):
    '''(experimental) Creates new IPAM with default public and private scope.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipamscope.html
    :stability: experimental
    :resource: AWS::EC2::IPAM
    :exampleMetadata: infused

    Example::

        stack = Stack()
        ipam = Ipam(self, "Ipam",
            operating_region=["us-west-1"]
        )
        ipam_public_pool = ipam.public_scope.add_pool("PublicPoolA",
            address_family=vpc_v2.AddressFamily.IP_V6,
            aws_service=AwsServiceName.EC2,
            locale="us-west-1",
            public_ip_source=vpc_v2.IpamPoolPublicIpSource.AMAZON
        )
        ipam_public_pool.provision_cidr("PublicPoolACidrA", netmask_length=52)
        
        ipam_private_pool = ipam.private_scope.add_pool("PrivatePoolA",
            address_family=vpc_v2.AddressFamily.IP_V4
        )
        ipam_private_pool.provision_cidr("PrivatePoolACidrA", netmask_length=8)
        
        vpc_v2.VpcV2(self, "Vpc",
            primary_address_block=vpc_v2.IpAddresses.ipv4("10.0.0.0/24"),
            secondary_address_blocks=[
                vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonIpv6"),
                vpc_v2.IpAddresses.ipv6_ipam(
                    ipam_pool=ipam_public_pool,
                    netmask_length=52,
                    cidr_block_name="ipv6Ipam"
                ),
                vpc_v2.IpAddresses.ipv4_ipam(
                    ipam_pool=ipam_private_pool,
                    netmask_length=8,
                    cidr_block_name="ipv4Ipam"
                )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ipam_name: typing.Optional[builtins.str] = None,
        operating_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ipam_name: (experimental) Name of IPAM that can be used for tagging resource. Default: none
        :param operating_region: (experimental) The operating Regions for an IPAM. Operating Regions are AWS Regions where the IPAM is allowed to manage IP address CIDRs For more information about operating Regions, see `Create an IPAM <https://docs.aws.amazon.com//vpc/latest/ipam/create-ipam.html>`_ in the *Amazon VPC IPAM User Guide* . Default: Stack.region if defined else []

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ed6f6a471c5154b59132e6c943218845868bcf0ef72feac08ef9ecf58fda24)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IpamProps(ipam_name=ipam_name, operating_region=operating_region)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addScope")
    def add_scope(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ipam_scope_name: typing.Optional[builtins.str] = None,
    ) -> IIpamScopeBase:
        '''(experimental) Function to add custom scope to an existing IPAM Custom scopes can only be private.

        :param scope: -
        :param id: -
        :param ipam_scope_name: (experimental) IPAM scope name that will be used for tagging. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296863e23505efe3c05687294f941735dfb8c507dbfd2ba189d45b4953c95ac0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = IpamScopeOptions(ipam_scope_name=ipam_scope_name)

        return typing.cast(IIpamScopeBase, jsii.invoke(self, "addScope", [scope, id, options]))

    @builtins.property
    @jsii.member(jsii_name="ipamId")
    def ipam_id(self) -> builtins.str:
        '''(experimental) Access to Ipam resource id that can be used later to add a custom private scope to this IPAM.

        :stability: experimental
        :attribute: IpamId
        '''
        return typing.cast(builtins.str, jsii.get(self, "ipamId"))

    @builtins.property
    @jsii.member(jsii_name="operatingRegions")
    def operating_regions(self) -> typing.List[builtins.str]:
        '''(experimental) List of operating regions for IPAM.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "operatingRegions"))

    @builtins.property
    @jsii.member(jsii_name="privateScope")
    def private_scope(self) -> IIpamScopeBase:
        '''(experimental) Provides access to default private IPAM scope through add pool method.

        Usage: To add an Ipam Pool to a default private scope

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipamscope.html
        :stability: experimental
        '''
        return typing.cast(IIpamScopeBase, jsii.get(self, "privateScope"))

    @builtins.property
    @jsii.member(jsii_name="publicScope")
    def public_scope(self) -> IIpamScopeBase:
        '''(experimental) Provides access to default public IPAM scope through add pool method.

        Usage: To add an Ipam Pool to a default public scope

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipamscope.html
        :stability: experimental
        '''
        return typing.cast(IIpamScopeBase, jsii.get(self, "publicScope"))

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[IIpamScopeBase]:
        '''(experimental) List of scopes created under this IPAM.

        :stability: experimental
        '''
        return typing.cast(typing.List[IIpamScopeBase], jsii.get(self, "scopes"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.IpamOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cidr_block_name": "cidrBlockName",
        "ipam_pool": "ipamPool",
        "netmask_length": "netmaskLength",
    },
)
class IpamOptions:
    def __init__(
        self,
        *,
        cidr_block_name: builtins.str,
        ipam_pool: typing.Optional[IIpamPool] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for configuring an IP Address Manager (IPAM).

        For more information, see the {@link https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipam.html}.

        :param cidr_block_name: (experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource.
        :param ipam_pool: (experimental) Ipv4 or an Ipv6 IPAM pool Only required when using AWS Ipam. Default: - None
        :param netmask_length: (experimental) CIDR Mask for Vpc Only required when using AWS Ipam. Default: - None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            stack = Stack()
            ipam = Ipam(self, "Ipam",
                operating_region=["us-west-1"]
            )
            ipam_public_pool = ipam.public_scope.add_pool("PublicPoolA",
                address_family=vpc_v2.AddressFamily.IP_V6,
                aws_service=AwsServiceName.EC2,
                locale="us-west-1",
                public_ip_source=vpc_v2.IpamPoolPublicIpSource.AMAZON
            )
            ipam_public_pool.provision_cidr("PublicPoolACidrA", netmask_length=52)
            
            ipam_private_pool = ipam.private_scope.add_pool("PrivatePoolA",
                address_family=vpc_v2.AddressFamily.IP_V4
            )
            ipam_private_pool.provision_cidr("PrivatePoolACidrA", netmask_length=8)
            
            vpc_v2.VpcV2(self, "Vpc",
                primary_address_block=vpc_v2.IpAddresses.ipv4("10.0.0.0/24"),
                secondary_address_blocks=[
                    vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonIpv6"),
                    vpc_v2.IpAddresses.ipv6_ipam(
                        ipam_pool=ipam_public_pool,
                        netmask_length=52,
                        cidr_block_name="ipv6Ipam"
                    ),
                    vpc_v2.IpAddresses.ipv4_ipam(
                        ipam_pool=ipam_private_pool,
                        netmask_length=8,
                        cidr_block_name="ipv4Ipam"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef69b77e361363d19bbc896e7549828dabe3c8a5aa6a3470fe28e6b811c0a845)
            check_type(argname="argument cidr_block_name", value=cidr_block_name, expected_type=type_hints["cidr_block_name"])
            check_type(argname="argument ipam_pool", value=ipam_pool, expected_type=type_hints["ipam_pool"])
            check_type(argname="argument netmask_length", value=netmask_length, expected_type=type_hints["netmask_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr_block_name": cidr_block_name,
        }
        if ipam_pool is not None:
            self._values["ipam_pool"] = ipam_pool
        if netmask_length is not None:
            self._values["netmask_length"] = netmask_length

    @builtins.property
    def cidr_block_name(self) -> builtins.str:
        '''(experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource.

        :stability: experimental
        '''
        result = self._values.get("cidr_block_name")
        assert result is not None, "Required property 'cidr_block_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipam_pool(self) -> typing.Optional[IIpamPool]:
        '''(experimental) Ipv4 or an Ipv6 IPAM pool Only required when using AWS Ipam.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("ipam_pool")
        return typing.cast(typing.Optional[IIpamPool], result)

    @builtins.property
    def netmask_length(self) -> typing.Optional[jsii.Number]:
        '''(experimental) CIDR Mask for Vpc Only required when using AWS Ipam.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("netmask_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpamOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.IpamPoolCidrProvisioningOptions",
    jsii_struct_bases=[],
    name_mapping={"cidr": "cidr", "netmask_length": "netmaskLength"},
)
class IpamPoolCidrProvisioningOptions:
    def __init__(
        self,
        *,
        cidr: typing.Optional[builtins.str] = None,
        netmask_length: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options to provision CIDRs to an IPAM pool.

        Used to create a new IpamPoolCidr

        :param cidr: (experimental) Ipv6 CIDR block for the IPAM pool. Default: none
        :param netmask_length: (experimental) Ipv6 Netmask length for the CIDR. Default: none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipampoolcidr.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            stack = Stack()
            ipam = Ipam(self, "Ipam",
                operating_region=["us-west-1"]
            )
            ipam_public_pool = ipam.public_scope.add_pool("PublicPoolA",
                address_family=vpc_v2.AddressFamily.IP_V6,
                aws_service=AwsServiceName.EC2,
                locale="us-west-1",
                public_ip_source=vpc_v2.IpamPoolPublicIpSource.AMAZON
            )
            ipam_public_pool.provision_cidr("PublicPoolACidrA", netmask_length=52)
            
            ipam_private_pool = ipam.private_scope.add_pool("PrivatePoolA",
                address_family=vpc_v2.AddressFamily.IP_V4
            )
            ipam_private_pool.provision_cidr("PrivatePoolACidrA", netmask_length=8)
            
            vpc_v2.VpcV2(self, "Vpc",
                primary_address_block=vpc_v2.IpAddresses.ipv4("10.0.0.0/24"),
                secondary_address_blocks=[
                    vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonIpv6"),
                    vpc_v2.IpAddresses.ipv6_ipam(
                        ipam_pool=ipam_public_pool,
                        netmask_length=52,
                        cidr_block_name="ipv6Ipam"
                    ),
                    vpc_v2.IpAddresses.ipv4_ipam(
                        ipam_pool=ipam_private_pool,
                        netmask_length=8,
                        cidr_block_name="ipv4Ipam"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d9b15700233762113ea1f831e611edef9363690ea36470a160f478fbe21dd0)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument netmask_length", value=netmask_length, expected_type=type_hints["netmask_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidr is not None:
            self._values["cidr"] = cidr
        if netmask_length is not None:
            self._values["netmask_length"] = netmask_length

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        '''(experimental) Ipv6 CIDR block for the IPAM pool.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask_length(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Ipv6 Netmask length for the CIDR.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("netmask_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpamPoolCidrProvisioningOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ec2-alpha.IpamPoolPublicIpSource")
class IpamPoolPublicIpSource(enum.Enum):
    '''(experimental) The IP address source for pools in the public scope.

    Only used for provisioning IP address CIDRs to pools in the public scope.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipampool.html#cfn-ec2-ipampool-publicipsource
    :stability: experimental
    :exampleMetadata: infused

    Example::

        stack = Stack()
        ipam = Ipam(self, "Ipam",
            operating_region=["us-west-1"]
        )
        ipam_public_pool = ipam.public_scope.add_pool("PublicPoolA",
            address_family=vpc_v2.AddressFamily.IP_V6,
            aws_service=AwsServiceName.EC2,
            locale="us-west-1",
            public_ip_source=vpc_v2.IpamPoolPublicIpSource.AMAZON
        )
        ipam_public_pool.provision_cidr("PublicPoolACidrA", netmask_length=52)
        
        ipam_private_pool = ipam.private_scope.add_pool("PrivatePoolA",
            address_family=vpc_v2.AddressFamily.IP_V4
        )
        ipam_private_pool.provision_cidr("PrivatePoolACidrA", netmask_length=8)
        
        vpc_v2.VpcV2(self, "Vpc",
            primary_address_block=vpc_v2.IpAddresses.ipv4("10.0.0.0/24"),
            secondary_address_blocks=[
                vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonIpv6"),
                vpc_v2.IpAddresses.ipv6_ipam(
                    ipam_pool=ipam_public_pool,
                    netmask_length=52,
                    cidr_block_name="ipv6Ipam"
                ),
                vpc_v2.IpAddresses.ipv4_ipam(
                    ipam_pool=ipam_private_pool,
                    netmask_length=8,
                    cidr_block_name="ipv4Ipam"
                )
            ]
        )
    '''

    BYOIP = "BYOIP"
    '''(experimental) BYOIP Ipv6 to be registered under IPAM.

    :stability: experimental
    '''
    AMAZON = "AMAZON"
    '''(experimental) Amazon Provided Ipv6 range.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.IpamProps",
    jsii_struct_bases=[],
    name_mapping={"ipam_name": "ipamName", "operating_region": "operatingRegion"},
)
class IpamProps:
    def __init__(
        self,
        *,
        ipam_name: typing.Optional[builtins.str] = None,
        operating_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options to create a new Ipam in the account.

        :param ipam_name: (experimental) Name of IPAM that can be used for tagging resource. Default: none
        :param operating_region: (experimental) The operating Regions for an IPAM. Operating Regions are AWS Regions where the IPAM is allowed to manage IP address CIDRs For more information about operating Regions, see `Create an IPAM <https://docs.aws.amazon.com//vpc/latest/ipam/create-ipam.html>`_ in the *Amazon VPC IPAM User Guide* . Default: Stack.region if defined else []

        :stability: experimental
        :exampleMetadata: infused

        Example::

            stack = Stack()
            ipam = Ipam(self, "Ipam",
                operating_region=["us-west-1"]
            )
            ipam_public_pool = ipam.public_scope.add_pool("PublicPoolA",
                address_family=vpc_v2.AddressFamily.IP_V6,
                aws_service=AwsServiceName.EC2,
                locale="us-west-1",
                public_ip_source=vpc_v2.IpamPoolPublicIpSource.AMAZON
            )
            ipam_public_pool.provision_cidr("PublicPoolACidrA", netmask_length=52)
            
            ipam_private_pool = ipam.private_scope.add_pool("PrivatePoolA",
                address_family=vpc_v2.AddressFamily.IP_V4
            )
            ipam_private_pool.provision_cidr("PrivatePoolACidrA", netmask_length=8)
            
            vpc_v2.VpcV2(self, "Vpc",
                primary_address_block=vpc_v2.IpAddresses.ipv4("10.0.0.0/24"),
                secondary_address_blocks=[
                    vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonIpv6"),
                    vpc_v2.IpAddresses.ipv6_ipam(
                        ipam_pool=ipam_public_pool,
                        netmask_length=52,
                        cidr_block_name="ipv6Ipam"
                    ),
                    vpc_v2.IpAddresses.ipv4_ipam(
                        ipam_pool=ipam_private_pool,
                        netmask_length=8,
                        cidr_block_name="ipv4Ipam"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f718be906e882bf24bd25534ed4d857392b590d6c147225d8e6b56b22b1781d7)
            check_type(argname="argument ipam_name", value=ipam_name, expected_type=type_hints["ipam_name"])
            check_type(argname="argument operating_region", value=operating_region, expected_type=type_hints["operating_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ipam_name is not None:
            self._values["ipam_name"] = ipam_name
        if operating_region is not None:
            self._values["operating_region"] = operating_region

    @builtins.property
    def ipam_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of IPAM that can be used for tagging resource.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("ipam_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operating_region(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The operating Regions for an IPAM.

        Operating Regions are AWS Regions where the IPAM is allowed to manage IP address CIDRs
        For more information about operating Regions, see `Create an IPAM <https://docs.aws.amazon.com//vpc/latest/ipam/create-ipam.html>`_ in the *Amazon VPC IPAM User Guide* .

        :default: Stack.region if defined else []

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipam.html#cfn-ec2-ipam-operatingregions
        :stability: experimental
        '''
        result = self._values.get("operating_region")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.IpamScopeOptions",
    jsii_struct_bases=[],
    name_mapping={"ipam_scope_name": "ipamScopeName"},
)
class IpamScopeOptions:
    def __init__(
        self,
        *,
        ipam_scope_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Being used in IPAM class to add pools to default scope created by IPAM.

        :param ipam_scope_name: (experimental) IPAM scope name that will be used for tagging. Default: none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ec2_alpha as ec2_alpha
            
            ipam_scope_options = ec2_alpha.IpamScopeOptions(
                ipam_scope_name="ipamScopeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18fc2fc30cb847c875d0d2bc1bf84a72aea509aa638af404c53fa7ab0776fa1)
            check_type(argname="argument ipam_scope_name", value=ipam_scope_name, expected_type=type_hints["ipam_scope_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ipam_scope_name is not None:
            self._values["ipam_scope_name"] = ipam_scope_name

    @builtins.property
    def ipam_scope_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) IPAM scope name that will be used for tagging.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("ipam_scope_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpamScopeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ec2-alpha.IpamScopeType")
class IpamScopeType(enum.Enum):
    '''(experimental) Refers to two possible scope types under IPAM.

    :stability: experimental
    '''

    DEFAULT = "DEFAULT"
    '''(experimental) Default scopes created by IPAM.

    :stability: experimental
    '''
    CUSTOM = "CUSTOM"
    '''(experimental) Custom scope created using method.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-ec2-alpha.NatConnectivityType")
class NatConnectivityType(enum.Enum):
    '''(experimental) Indicates whether the NAT gateway supports public or private connectivity.

    The default is public connectivity.
    See: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-natgateway.html#cfn-ec2-natgateway-connectivitytype

    :stability: experimental
    :exampleMetadata: infused

    Example::

        my_vpc = vpc_v2.VpcV2(self, "Vpc")
        route_table = vpc_v2.RouteTable(self, "RouteTable",
            vpc=my_vpc
        )
        subnet = vpc_v2.SubnetV2(self, "Subnet",
            vpc=my_vpc,
            availability_zone="eu-west-2a",
            ipv4_cidr_block=IpCidr("10.0.0.0/24"),
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        )
        
        natgw = vpc_v2.NatGateway(self, "NatGW",
            subnet=subnet,
            vpc=my_vpc,
            connectivity_type=NatConnectivityType.PRIVATE,
            private_ip_address="10.0.0.42"
        )
        vpc_v2.Route(self, "NatGwRoute",
            route_table=route_table,
            destination="0.0.0.0/0",
            target={"gateway": natgw}
        )
    '''

    PUBLIC = "PUBLIC"
    '''(experimental) Sets Connectivity type to PUBLIC.

    :stability: experimental
    '''
    PRIVATE = "PRIVATE"
    '''(experimental) Sets Connectivity type to PRIVATE.

    :stability: experimental
    '''


@jsii.implements(IRouteTarget)
class NatGateway(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.NatGateway",
):
    '''(experimental) Creates a network address translation (NAT) gateway.

    :stability: experimental
    :resource: AWS::EC2::NatGateway
    :exampleMetadata: infused

    Example::

        my_vpc = vpc_v2.VpcV2(self, "Vpc")
        route_table = vpc_v2.RouteTable(self, "RouteTable",
            vpc=my_vpc
        )
        subnet = vpc_v2.SubnetV2(self, "Subnet",
            vpc=my_vpc,
            availability_zone="eu-west-2a",
            ipv4_cidr_block=IpCidr("10.0.0.0/24"),
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        )
        
        natgw = vpc_v2.NatGateway(self, "NatGW",
            subnet=subnet,
            vpc=my_vpc,
            connectivity_type=NatConnectivityType.PRIVATE,
            private_ip_address="10.0.0.42"
        )
        vpc_v2.Route(self, "NatGwRoute",
            route_table=route_table,
            destination="0.0.0.0/0",
            target={"gateway": natgw}
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
        allocation_id: typing.Optional[builtins.str] = None,
        connectivity_type: typing.Optional[NatConnectivityType] = None,
        max_drain_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        nat_gateway_name: typing.Optional[builtins.str] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        secondary_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        secondary_private_ip_address_count: typing.Optional[jsii.Number] = None,
        secondary_private_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc: typing.Optional[IVpcV2] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param subnet: (experimental) The subnet in which the NAT gateway is located.
        :param allocation_id: (experimental) AllocationID of Elastic IP address that's associated with the NAT gateway. This property is required for a public NAT gateway and cannot be specified with a private NAT gateway. Default: attr.allocationID of a new Elastic IP created by default //TODO: ADD L2 for elastic ip
        :param connectivity_type: (experimental) Indicates whether the NAT gateway supports public or private connectivity. Default: public
        :param max_drain_duration: (experimental) The maximum amount of time to wait before forcibly releasing the IP addresses if connections are still in progress. Default: 350 seconds
        :param nat_gateway_name: (experimental) The resource name of the NAT gateway. Default: none
        :param private_ip_address: (experimental) The private IPv4 address to assign to the NAT gateway. If you don't provide an address, a private IPv4 address will be automatically assigned. Default: none
        :param secondary_allocation_ids: (experimental) Secondary EIP allocation IDs. Default: none
        :param secondary_private_ip_address_count: (experimental) The number of secondary private IPv4 addresses you want to assign to the NAT gateway. ``SecondaryPrivateIpAddressCount`` and ``SecondaryPrivateIpAddresses`` cannot be set at the same time. Default: none
        :param secondary_private_ip_addresses: (experimental) Secondary private IPv4 addresses. ``SecondaryPrivateIpAddressCount`` and ``SecondaryPrivateIpAddresses`` cannot be set at the same time. Default: none
        :param vpc: (experimental) The ID of the VPC in which the NAT gateway is located. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3204c5cc1ee92d73075b1e2c597a7d7bb9eb73b154f33262369b6b4ac9ec33f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NatGatewayProps(
            subnet=subnet,
            allocation_id=allocation_id,
            connectivity_type=connectivity_type,
            max_drain_duration=max_drain_duration,
            nat_gateway_name=nat_gateway_name,
            private_ip_address=private_ip_address,
            secondary_allocation_ids=secondary_allocation_ids,
            secondary_private_ip_address_count=secondary_private_ip_address_count,
            secondary_private_ip_addresses=secondary_private_ip_addresses,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnNatGateway:
        '''(experimental) The NAT gateway CFN resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnNatGateway, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="routerTargetId")
    def router_target_id(self) -> builtins.str:
        '''(experimental) The ID of the route target.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routerTargetId"))

    @builtins.property
    @jsii.member(jsii_name="routerType")
    def router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''(experimental) The type of router used in the route.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.RouterType, jsii.get(self, "routerType"))

    @builtins.property
    @jsii.member(jsii_name="connectivityType")
    def connectivity_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Indicates whether the NAT gateway supports public or private connectivity.

        :default: public

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectivityType"))

    @builtins.property
    @jsii.member(jsii_name="maxDrainDuration")
    def max_drain_duration(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum amount of time to wait before forcibly releasing the IP addresses if connections are still in progress.

        :default: 350 seconds

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "maxDrainDuration"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.NatGatewayProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnet": "subnet",
        "allocation_id": "allocationId",
        "connectivity_type": "connectivityType",
        "max_drain_duration": "maxDrainDuration",
        "nat_gateway_name": "natGatewayName",
        "private_ip_address": "privateIpAddress",
        "secondary_allocation_ids": "secondaryAllocationIds",
        "secondary_private_ip_address_count": "secondaryPrivateIpAddressCount",
        "secondary_private_ip_addresses": "secondaryPrivateIpAddresses",
        "vpc": "vpc",
    },
)
class NatGatewayProps:
    def __init__(
        self,
        *,
        subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
        allocation_id: typing.Optional[builtins.str] = None,
        connectivity_type: typing.Optional[NatConnectivityType] = None,
        max_drain_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        nat_gateway_name: typing.Optional[builtins.str] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        secondary_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        secondary_private_ip_address_count: typing.Optional[jsii.Number] = None,
        secondary_private_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc: typing.Optional[IVpcV2] = None,
    ) -> None:
        '''(experimental) Properties to define a NAT gateway.

        :param subnet: (experimental) The subnet in which the NAT gateway is located.
        :param allocation_id: (experimental) AllocationID of Elastic IP address that's associated with the NAT gateway. This property is required for a public NAT gateway and cannot be specified with a private NAT gateway. Default: attr.allocationID of a new Elastic IP created by default //TODO: ADD L2 for elastic ip
        :param connectivity_type: (experimental) Indicates whether the NAT gateway supports public or private connectivity. Default: public
        :param max_drain_duration: (experimental) The maximum amount of time to wait before forcibly releasing the IP addresses if connections are still in progress. Default: 350 seconds
        :param nat_gateway_name: (experimental) The resource name of the NAT gateway. Default: none
        :param private_ip_address: (experimental) The private IPv4 address to assign to the NAT gateway. If you don't provide an address, a private IPv4 address will be automatically assigned. Default: none
        :param secondary_allocation_ids: (experimental) Secondary EIP allocation IDs. Default: none
        :param secondary_private_ip_address_count: (experimental) The number of secondary private IPv4 addresses you want to assign to the NAT gateway. ``SecondaryPrivateIpAddressCount`` and ``SecondaryPrivateIpAddresses`` cannot be set at the same time. Default: none
        :param secondary_private_ip_addresses: (experimental) Secondary private IPv4 addresses. ``SecondaryPrivateIpAddressCount`` and ``SecondaryPrivateIpAddresses`` cannot be set at the same time. Default: none
        :param vpc: (experimental) The ID of the VPC in which the NAT gateway is located. Default: none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            my_vpc = vpc_v2.VpcV2(self, "Vpc")
            route_table = vpc_v2.RouteTable(self, "RouteTable",
                vpc=my_vpc
            )
            subnet = vpc_v2.SubnetV2(self, "Subnet",
                vpc=my_vpc,
                availability_zone="eu-west-2a",
                ipv4_cidr_block=IpCidr("10.0.0.0/24"),
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
            
            natgw = vpc_v2.NatGateway(self, "NatGW",
                subnet=subnet,
                vpc=my_vpc,
                connectivity_type=NatConnectivityType.PRIVATE,
                private_ip_address="10.0.0.42"
            )
            vpc_v2.Route(self, "NatGwRoute",
                route_table=route_table,
                destination="0.0.0.0/0",
                target={"gateway": natgw}
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c6c285bd9604aa1bbf23945426abd3cb4259870f0a85edd40b87eb08b29903)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument allocation_id", value=allocation_id, expected_type=type_hints["allocation_id"])
            check_type(argname="argument connectivity_type", value=connectivity_type, expected_type=type_hints["connectivity_type"])
            check_type(argname="argument max_drain_duration", value=max_drain_duration, expected_type=type_hints["max_drain_duration"])
            check_type(argname="argument nat_gateway_name", value=nat_gateway_name, expected_type=type_hints["nat_gateway_name"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument secondary_allocation_ids", value=secondary_allocation_ids, expected_type=type_hints["secondary_allocation_ids"])
            check_type(argname="argument secondary_private_ip_address_count", value=secondary_private_ip_address_count, expected_type=type_hints["secondary_private_ip_address_count"])
            check_type(argname="argument secondary_private_ip_addresses", value=secondary_private_ip_addresses, expected_type=type_hints["secondary_private_ip_addresses"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet": subnet,
        }
        if allocation_id is not None:
            self._values["allocation_id"] = allocation_id
        if connectivity_type is not None:
            self._values["connectivity_type"] = connectivity_type
        if max_drain_duration is not None:
            self._values["max_drain_duration"] = max_drain_duration
        if nat_gateway_name is not None:
            self._values["nat_gateway_name"] = nat_gateway_name
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if secondary_allocation_ids is not None:
            self._values["secondary_allocation_ids"] = secondary_allocation_ids
        if secondary_private_ip_address_count is not None:
            self._values["secondary_private_ip_address_count"] = secondary_private_ip_address_count
        if secondary_private_ip_addresses is not None:
            self._values["secondary_private_ip_addresses"] = secondary_private_ip_addresses
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def subnet(self) -> _aws_cdk_aws_ec2_ceddda9d.ISubnet:
        '''(experimental) The subnet in which the NAT gateway is located.

        :stability: experimental
        '''
        result = self._values.get("subnet")
        assert result is not None, "Required property 'subnet' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISubnet, result)

    @builtins.property
    def allocation_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) AllocationID of Elastic IP address that's associated with the NAT gateway.

        This property is required for a public NAT
        gateway and cannot be specified with a private NAT gateway.

        :default:

        attr.allocationID of a new Elastic IP created by default
        //TODO: ADD L2 for elastic ip

        :stability: experimental
        '''
        result = self._values.get("allocation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connectivity_type(self) -> typing.Optional[NatConnectivityType]:
        '''(experimental) Indicates whether the NAT gateway supports public or private connectivity.

        :default: public

        :stability: experimental
        '''
        result = self._values.get("connectivity_type")
        return typing.cast(typing.Optional[NatConnectivityType], result)

    @builtins.property
    def max_drain_duration(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum amount of time to wait before forcibly releasing the IP addresses if connections are still in progress.

        :default: 350 seconds

        :stability: experimental
        '''
        result = self._values.get("max_drain_duration")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def nat_gateway_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The resource name of the NAT gateway.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("nat_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''(experimental) The private IPv4 address to assign to the NAT gateway.

        If you don't provide an
        address, a private IPv4 address will be automatically assigned.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_allocation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Secondary EIP allocation IDs.

        :default: none

        :see: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html#nat-gateway-creating
        :stability: experimental
        '''
        result = self._values.get("secondary_allocation_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secondary_private_ip_address_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of secondary private IPv4 addresses you want to assign to the NAT gateway.

        ``SecondaryPrivateIpAddressCount`` and ``SecondaryPrivateIpAddresses`` cannot be
        set at the same time.

        :default: none

        :see: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html#nat-gateway-creating
        :stability: experimental
        '''
        result = self._values.get("secondary_private_ip_address_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secondary_private_ip_addresses(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Secondary private IPv4 addresses.

        ``SecondaryPrivateIpAddressCount`` and ``SecondaryPrivateIpAddresses`` cannot be
        set at the same time.

        :default: none

        :see: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html#nat-gateway-creating
        :stability: experimental
        '''
        result = self._values.get("secondary_private_ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[IVpcV2]:
        '''(experimental) The ID of the VPC in which the NAT gateway is located.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[IVpcV2], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NatGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.PoolOptions",
    jsii_struct_bases=[],
    name_mapping={
        "address_family": "addressFamily",
        "aws_service": "awsService",
        "ipv4_provisioned_cidrs": "ipv4ProvisionedCidrs",
        "locale": "locale",
        "public_ip_source": "publicIpSource",
    },
)
class PoolOptions:
    def __init__(
        self,
        *,
        address_family: AddressFamily,
        aws_service: typing.Optional[AwsServiceName] = None,
        ipv4_provisioned_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        locale: typing.Optional[builtins.str] = None,
        public_ip_source: typing.Optional[IpamPoolPublicIpSource] = None,
    ) -> None:
        '''(experimental) Options for configuring an IPAM pool.

        :param address_family: (experimental) addressFamily - The address family of the pool (ipv4 or ipv6).
        :param aws_service: (experimental) Limits which service in AWS that the pool can be used in. "ec2", for example, allows users to use space for Elastic IP addresses and VPCs. Default: - No service
        :param ipv4_provisioned_cidrs: (experimental) Information about the CIDRs provisioned to the pool. Default: - No CIDRs are provisioned
        :param locale: (experimental) The locale (AWS Region) of the pool. Should be one of the IPAM operating region. Only resources in the same Region as the locale of the pool can get IP address allocations from the pool. You can only allocate a CIDR for a VPC, for example, from an IPAM pool that shares a locale with the VPC’s Region. Note that once you choose a Locale for a pool, you cannot modify it. If you choose an AWS Region for locale that has not been configured as an operating Region for the IPAM, you'll get an error. Default: - Current operating region
        :param public_ip_source: (experimental) The IP address source for pools in the public scope. Only used for IPv6 address Only allowed values to this are 'byoip' or 'amazon' Default: amazon

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipampool.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            stack = Stack()
            ipam = Ipam(self, "Ipam",
                operating_region=["us-west-1"]
            )
            ipam_public_pool = ipam.public_scope.add_pool("PublicPoolA",
                address_family=vpc_v2.AddressFamily.IP_V6,
                aws_service=AwsServiceName.EC2,
                locale="us-west-1",
                public_ip_source=vpc_v2.IpamPoolPublicIpSource.AMAZON
            )
            ipam_public_pool.provision_cidr("PublicPoolACidrA", netmask_length=52)
            
            ipam_private_pool = ipam.private_scope.add_pool("PrivatePoolA",
                address_family=vpc_v2.AddressFamily.IP_V4
            )
            ipam_private_pool.provision_cidr("PrivatePoolACidrA", netmask_length=8)
            
            vpc_v2.VpcV2(self, "Vpc",
                primary_address_block=vpc_v2.IpAddresses.ipv4("10.0.0.0/24"),
                secondary_address_blocks=[
                    vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonIpv6"),
                    vpc_v2.IpAddresses.ipv6_ipam(
                        ipam_pool=ipam_public_pool,
                        netmask_length=52,
                        cidr_block_name="ipv6Ipam"
                    ),
                    vpc_v2.IpAddresses.ipv4_ipam(
                        ipam_pool=ipam_private_pool,
                        netmask_length=8,
                        cidr_block_name="ipv4Ipam"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b5a95424fdb1e7fb6ae3da82efaf806f125de298a951d9b7f9b24181fd5c41)
            check_type(argname="argument address_family", value=address_family, expected_type=type_hints["address_family"])
            check_type(argname="argument aws_service", value=aws_service, expected_type=type_hints["aws_service"])
            check_type(argname="argument ipv4_provisioned_cidrs", value=ipv4_provisioned_cidrs, expected_type=type_hints["ipv4_provisioned_cidrs"])
            check_type(argname="argument locale", value=locale, expected_type=type_hints["locale"])
            check_type(argname="argument public_ip_source", value=public_ip_source, expected_type=type_hints["public_ip_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_family": address_family,
        }
        if aws_service is not None:
            self._values["aws_service"] = aws_service
        if ipv4_provisioned_cidrs is not None:
            self._values["ipv4_provisioned_cidrs"] = ipv4_provisioned_cidrs
        if locale is not None:
            self._values["locale"] = locale
        if public_ip_source is not None:
            self._values["public_ip_source"] = public_ip_source

    @builtins.property
    def address_family(self) -> AddressFamily:
        '''(experimental) addressFamily - The address family of the pool (ipv4 or ipv6).

        :stability: experimental
        '''
        result = self._values.get("address_family")
        assert result is not None, "Required property 'address_family' is missing"
        return typing.cast(AddressFamily, result)

    @builtins.property
    def aws_service(self) -> typing.Optional[AwsServiceName]:
        '''(experimental) Limits which service in AWS that the pool can be used in.

        "ec2", for example, allows users to use space for Elastic IP addresses and VPCs.

        :default: - No service

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipampool.html#cfn-ec2-ipampool-awsservice
        :stability: experimental
        '''
        result = self._values.get("aws_service")
        return typing.cast(typing.Optional[AwsServiceName], result)

    @builtins.property
    def ipv4_provisioned_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Information about the CIDRs provisioned to the pool.

        :default: - No CIDRs are provisioned

        :stability: experimental
        '''
        result = self._values.get("ipv4_provisioned_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def locale(self) -> typing.Optional[builtins.str]:
        '''(experimental) The locale (AWS Region) of the pool.

        Should be one of the IPAM operating region.
        Only resources in the same Region as the locale of the pool can get IP address allocations from the pool.
        You can only allocate a CIDR for a VPC, for example, from an IPAM pool that shares a locale with the VPC’s Region.
        Note that once you choose a Locale for a pool, you cannot modify it. If you choose an AWS Region for locale that has not been configured as an operating Region for the IPAM, you'll get an error.

        :default: - Current operating region

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ipampool.html#cfn-ec2-ipampool-locale
        :stability: experimental
        '''
        result = self._values.get("locale")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ip_source(self) -> typing.Optional[IpamPoolPublicIpSource]:
        '''(experimental) The IP address source for pools in the public scope.

        Only used for IPv6 address
        Only allowed values to this are 'byoip' or 'amazon'

        :default: amazon

        :stability: experimental
        '''
        result = self._values.get("public_ip_source")
        return typing.cast(typing.Optional[IpamPoolPublicIpSource], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PoolOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRouteV2)
class Route(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.Route",
):
    '''(experimental) Creates a new route with added functionality.

    :stability: experimental
    :resource: AWS::EC2::Route
    :exampleMetadata: infused

    Example::

        my_vpc = vpc_v2.VpcV2(self, "Vpc")
        route_table = vpc_v2.RouteTable(self, "RouteTable",
            vpc=my_vpc
        )
        subnet = vpc_v2.SubnetV2(self, "Subnet",
            vpc=my_vpc,
            availability_zone="eu-west-2a",
            ipv4_cidr_block=IpCidr("10.0.0.0/24"),
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        )
        
        natgw = vpc_v2.NatGateway(self, "NatGW",
            subnet=subnet,
            vpc=my_vpc,
            connectivity_type=NatConnectivityType.PRIVATE,
            private_ip_address="10.0.0.42"
        )
        vpc_v2.Route(self, "NatGwRoute",
            route_table=route_table,
            destination="0.0.0.0/0",
            target={"gateway": natgw}
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        destination: builtins.str,
        route_table: _aws_cdk_aws_ec2_ceddda9d.IRouteTable,
        target: "RouteTargetType",
        route_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param destination: (experimental) The IPv4 or IPv6 CIDR block used for the destination match. Routing decisions are based on the most specific match.
        :param route_table: (experimental) The ID of the route table for the route.
        :param target: (experimental) The gateway or endpoint targeted by the route.
        :param route_name: (experimental) The resource name of the route. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4a94ed3246ec1926122f93a061896a8268de25ae7a4cc12e59846ba76bd6b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RouteProps(
            destination=destination,
            route_table=route_table,
            target=target,
            route_name=route_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        '''(experimental) The IPv4 or IPv6 CIDR block used for the destination match.

        Routing decisions are based on the most specific match.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="routeTable")
    def route_table(self) -> _aws_cdk_aws_ec2_ceddda9d.IRouteTable:
        '''(experimental) The route table for the route.

        :stability: experimental
        :attribute: routeTable
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IRouteTable, jsii.get(self, "routeTable"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "RouteTargetType":
        '''(experimental) The gateway or endpoint targeted by the route.

        :stability: experimental
        '''
        return typing.cast("RouteTargetType", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="targetRouterType")
    def target_router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''(experimental) The type of router the route is targetting.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.RouterType, jsii.get(self, "targetRouterType"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnRoute]:
        '''(experimental) The route CFN resource.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnRoute], jsii.get(self, "resource"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.RouteProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "route_table": "routeTable",
        "target": "target",
        "route_name": "routeName",
    },
)
class RouteProps:
    def __init__(
        self,
        *,
        destination: builtins.str,
        route_table: _aws_cdk_aws_ec2_ceddda9d.IRouteTable,
        target: "RouteTargetType",
        route_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to define a route.

        :param destination: (experimental) The IPv4 or IPv6 CIDR block used for the destination match. Routing decisions are based on the most specific match.
        :param route_table: (experimental) The ID of the route table for the route.
        :param target: (experimental) The gateway or endpoint targeted by the route.
        :param route_name: (experimental) The resource name of the route. Default: none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            my_vpc = vpc_v2.VpcV2(self, "Vpc")
            route_table = vpc_v2.RouteTable(self, "RouteTable",
                vpc=my_vpc
            )
            subnet = vpc_v2.SubnetV2(self, "Subnet",
                vpc=my_vpc,
                availability_zone="eu-west-2a",
                ipv4_cidr_block=IpCidr("10.0.0.0/24"),
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
            
            natgw = vpc_v2.NatGateway(self, "NatGW",
                subnet=subnet,
                vpc=my_vpc,
                connectivity_type=NatConnectivityType.PRIVATE,
                private_ip_address="10.0.0.42"
            )
            vpc_v2.Route(self, "NatGwRoute",
                route_table=route_table,
                destination="0.0.0.0/0",
                target={"gateway": natgw}
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda2cbb996081e5d873ecff8f8ff6450468388a42bf4745882a9caf33d55d197)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument route_table", value=route_table, expected_type=type_hints["route_table"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument route_name", value=route_name, expected_type=type_hints["route_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "route_table": route_table,
            "target": target,
        }
        if route_name is not None:
            self._values["route_name"] = route_name

    @builtins.property
    def destination(self) -> builtins.str:
        '''(experimental) The IPv4 or IPv6 CIDR block used for the destination match.

        Routing decisions are based on the most specific match.

        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_table(self) -> _aws_cdk_aws_ec2_ceddda9d.IRouteTable:
        '''(experimental) The ID of the route table for the route.

        :stability: experimental
        :attribute: routeTable
        '''
        result = self._values.get("route_table")
        assert result is not None, "Required property 'route_table' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IRouteTable, result)

    @builtins.property
    def target(self) -> "RouteTargetType":
        '''(experimental) The gateway or endpoint targeted by the route.

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("RouteTargetType", result)

    @builtins.property
    def route_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The resource name of the route.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IRouteTable, _constructs_77d1e7e8.IDependable)
class RouteTable(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.RouteTable",
):
    '''(experimental) Creates a route table for the specified VPC.

    :stability: experimental
    :resource: AWS::EC2::RouteTable
    :exampleMetadata: infused

    Example::

        stack = Stack()
        my_vpc = vpc_v2.VpcV2(self, "Vpc")
        route_table = vpc_v2.RouteTable(self, "RouteTable",
            vpc=my_vpc
        )
        subnet = vpc_v2.SubnetV2(self, "Subnet",
            vpc=my_vpc,
            availability_zone="eu-west-2a",
            ipv4_cidr_block=IpCidr("10.0.0.0/24"),
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        )
        
        igw = vpc_v2.InternetGateway(self, "IGW",
            vpc=my_vpc
        )
        vpc_v2.Route(self, "IgwRoute",
            route_table=route_table,
            destination="0.0.0.0/0",
            target={"gateway": igw}
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: IVpcV2,
        route_table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: (experimental) The ID of the VPC.
        :param route_table_name: (experimental) The resource name of the route table. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa486baea72e1e0413e458ea1f52d60725dbcdfeed33f2e810006af4c66d5a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RouteTableProps(vpc=vpc, route_table_name=route_table_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnRouteTable:
        '''(experimental) The route table CFN resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnRouteTable, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> builtins.str:
        '''(experimental) The ID of the route table.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeTableId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.RouteTableProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc", "route_table_name": "routeTableName"},
)
class RouteTableProps:
    def __init__(
        self,
        *,
        vpc: IVpcV2,
        route_table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to define a route table.

        :param vpc: (experimental) The ID of the VPC.
        :param route_table_name: (experimental) The resource name of the route table. Default: none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            stack = Stack()
            my_vpc = vpc_v2.VpcV2(self, "Vpc")
            route_table = vpc_v2.RouteTable(self, "RouteTable",
                vpc=my_vpc
            )
            subnet = vpc_v2.SubnetV2(self, "Subnet",
                vpc=my_vpc,
                availability_zone="eu-west-2a",
                ipv4_cidr_block=IpCidr("10.0.0.0/24"),
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
            
            igw = vpc_v2.InternetGateway(self, "IGW",
                vpc=my_vpc
            )
            vpc_v2.Route(self, "IgwRoute",
                route_table=route_table,
                destination="0.0.0.0/0",
                target={"gateway": igw}
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271dc5ccfa2e958efecaeb52a22e0ecbf03734c62d76ebbf18cb73e88deea29f)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument route_table_name", value=route_table_name, expected_type=type_hints["route_table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if route_table_name is not None:
            self._values["route_table_name"] = route_table_name

    @builtins.property
    def vpc(self) -> IVpcV2:
        '''(experimental) The ID of the VPC.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(IVpcV2, result)

    @builtins.property
    def route_table_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The resource name of the route table.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("route_table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouteTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.RouteTargetProps",
    jsii_struct_bases=[],
    name_mapping={"endpoint": "endpoint", "gateway": "gateway"},
)
class RouteTargetProps:
    def __init__(
        self,
        *,
        endpoint: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint] = None,
        gateway: typing.Optional[IRouteTarget] = None,
    ) -> None:
        '''(experimental) The type of endpoint or gateway being targeted by the route.

        :param endpoint: (experimental) The endpoint route target. This is used for targets such as VPC endpoints. Default: none
        :param gateway: (experimental) The gateway route target. This is used for targets such as egress-only internet gateway or VPC peering connection. Default: none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ec2_alpha as ec2_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # route_target: ec2_alpha.IRouteTarget
            # vpc_endpoint: ec2.VpcEndpoint
            
            route_target_props = ec2_alpha.RouteTargetProps(
                endpoint=vpc_endpoint,
                gateway=route_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777e37951fe65e456a56f7503992af6a79e1c8be4aeaf3a7544650f38247d64b)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if gateway is not None:
            self._values["gateway"] = gateway

    @builtins.property
    def endpoint(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint]:
        '''(experimental) The endpoint route target.

        This is used for targets such as
        VPC endpoints.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint], result)

    @builtins.property
    def gateway(self) -> typing.Optional[IRouteTarget]:
        '''(experimental) The gateway route target.

        This is used for targets such as
        egress-only internet gateway or VPC peering connection.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("gateway")
        return typing.cast(typing.Optional[IRouteTarget], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouteTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RouteTargetType(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.RouteTargetType",
):
    '''(experimental) The gateway or endpoint targeted by the route.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        my_vpc = vpc_v2.VpcV2(self, "Vpc")
        route_table = vpc_v2.RouteTable(self, "RouteTable",
            vpc=my_vpc
        )
        subnet = vpc_v2.SubnetV2(self, "Subnet",
            vpc=my_vpc,
            availability_zone="eu-west-2a",
            ipv4_cidr_block=IpCidr("10.0.0.0/24"),
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        )
        
        natgw = vpc_v2.NatGateway(self, "NatGW",
            subnet=subnet,
            vpc=my_vpc,
            connectivity_type=NatConnectivityType.PRIVATE,
            private_ip_address="10.0.0.42"
        )
        vpc_v2.Route(self, "NatGwRoute",
            route_table=route_table,
            destination="0.0.0.0/0",
            target={"gateway": natgw}
        )
    '''

    def __init__(
        self,
        *,
        endpoint: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint] = None,
        gateway: typing.Optional[IRouteTarget] = None,
    ) -> None:
        '''
        :param endpoint: (experimental) The endpoint route target. This is used for targets such as VPC endpoints. Default: none
        :param gateway: (experimental) The gateway route target. This is used for targets such as egress-only internet gateway or VPC peering connection. Default: none

        :stability: experimental
        '''
        props = RouteTargetProps(endpoint=endpoint, gateway=gateway)

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint]:
        '''(experimental) The endpoint route target.

        This is used for targets such as
        VPC endpoints.

        :default: none

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint], jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> typing.Optional[IRouteTarget]:
        '''(experimental) The gateway route target.

        This is used for targets such as
        egress-only internet gateway or VPC peering connection.

        :default: none

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IRouteTarget], jsii.get(self, "gateway"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.SecondaryAddressProps",
    jsii_struct_bases=[],
    name_mapping={"cidr_block_name": "cidrBlockName"},
)
class SecondaryAddressProps:
    def __init__(self, *, cidr_block_name: builtins.str) -> None:
        '''(experimental) Additional props needed for secondary Address.

        :param cidr_block_name: (experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            stack = Stack()
            my_vpc = vpc_v2.VpcV2(self, "Vpc",
                secondary_address_blocks=[
                    vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonProvidedIp")
                ]
            )
            
            vpc_v2.SubnetV2(self, "subnetA",
                vpc=my_vpc,
                availability_zone="us-east-1a",
                ipv4_cidr_block=vpc_v2.IpCidr("10.0.0.0/24"),
                ipv6_cidr_block=vpc_v2.IpCidr("2a05:d02c:25:4000::/60"),
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9433843cde495b2d9551feec9fd15a488c151e944cfd2262b5fc2613ca397870)
            check_type(argname="argument cidr_block_name", value=cidr_block_name, expected_type=type_hints["cidr_block_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr_block_name": cidr_block_name,
        }

    @builtins.property
    def cidr_block_name(self) -> builtins.str:
        '''(experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource.

        :stability: experimental
        '''
        result = self._values.get("cidr_block_name")
        assert result is not None, "Required property 'cidr_block_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecondaryAddressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISubnetV2)
class SubnetV2(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.SubnetV2",
):
    '''(experimental) The SubnetV2 class represents a subnet within a VPC (Virtual Private Cloud) in AWS.

    It extends the Resource class and implements the ISubnet interface.

    Instances of this class can be used to create and manage subnets within a VpcV2 instance.
    Subnets can be configured with specific IP address ranges (IPv4 and IPv6), availability zones,
    and subnet types (e.g., public, private, isolated).

    :stability: experimental
    :resource: AWS::EC2::Subnet
    :exampleMetadata: infused

    Example::

        stack = Stack()
        my_vpc = vpc_v2.VpcV2(self, "Vpc")
        route_table = vpc_v2.RouteTable(self, "RouteTable",
            vpc=my_vpc
        )
        subnet = vpc_v2.SubnetV2(self, "Subnet",
            vpc=my_vpc,
            availability_zone="eu-west-2a",
            ipv4_cidr_block=IpCidr("10.0.0.0/24"),
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        )
        
        igw = vpc_v2.InternetGateway(self, "IGW",
            vpc=my_vpc
        )
        vpc_v2.Route(self, "IgwRoute",
            route_table=route_table,
            destination="0.0.0.0/0",
            target={"gateway": igw}
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        availability_zone: builtins.str,
        ipv4_cidr_block: IpCidr,
        subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
        vpc: IVpcV2,
        assign_ipv6_address_on_creation: typing.Optional[builtins.bool] = None,
        ipv6_cidr_block: typing.Optional[IpCidr] = None,
        route_table: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IRouteTable] = None,
        subnet_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructs a new SubnetV2 instance.

        :param scope: The parent Construct that this resource will be part of.
        :param id: The unique identifier for this resource.
        :param availability_zone: (experimental) Custom AZ for the subnet.
        :param ipv4_cidr_block: (experimental) ipv4 cidr to assign to this subnet. See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-ec2-subnet-cidrblock
        :param subnet_type: (experimental) The type of Subnet to configure. The Subnet type will control the ability to route and connect to the Internet. TODO: Add validation check ``subnetType`` when adding resources (e.g. cannot add NatGateway to private)
        :param vpc: (experimental) VPC Prop.
        :param assign_ipv6_address_on_creation: (experimental) Indicates whether a network interface created in this subnet receives an IPv6 address. If you specify AssignIpv6AddressOnCreation, you must also specify Ipv6CidrBlock. Default: false
        :param ipv6_cidr_block: (experimental) Ipv6 CIDR Range for subnet. Default: No Ipv6 address
        :param route_table: (experimental) Custom Route for subnet. Default: Default route table
        :param subnet_name: (experimental) Subnet name. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9294d0dd8fd099bad5e4bd408f0f8b8bffbcdc6e4f624de6a1bf54199885b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SubnetV2Props(
            availability_zone=availability_zone,
            ipv4_cidr_block=ipv4_cidr_block,
            subnet_type=subnet_type,
            vpc=vpc,
            assign_ipv6_address_on_creation=assign_ipv6_address_on_creation,
            ipv6_cidr_block=ipv6_cidr_block,
            route_table=route_table,
            subnet_name=subnet_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="associateNetworkAcl")
    def associate_network_acl(
        self,
        id: builtins.str,
        network_acl: _aws_cdk_aws_ec2_ceddda9d.INetworkAcl,
    ) -> None:
        '''(experimental) Associate a Network ACL with this subnet.

        :param id: The unique identifier for this association.
        :param network_acl: The Network ACL to associate with this subnet. This allows controlling inbound and outbound traffic for instances in this subnet.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ecedf09cdae417f7675efd5f583cb5bfabde2a1b69f4f330c6434c1020e903)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network_acl", value=network_acl, expected_type=type_hints["network_acl"])
        return typing.cast(None, jsii.invoke(self, "associateNetworkAcl", [id, network_acl]))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        '''(experimental) The Availability Zone the subnet is located in.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    def internet_connectivity_established(self) -> _constructs_77d1e7e8.IDependable:
        '''(experimental) Dependencies for internet connectivity This Property exposes the RouteTable-Subnet association so that other resources can depend on it.

        :stability: experimental
        '''
        return typing.cast(_constructs_77d1e7e8.IDependable, jsii.get(self, "internetConnectivityEstablished"))

    @builtins.property
    @jsii.member(jsii_name="ipv4CidrBlock")
    def ipv4_cidr_block(self) -> builtins.str:
        '''(experimental) The IPv4 CIDR block for this subnet.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ipv4CidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="networkAcl")
    def network_acl(self) -> _aws_cdk_aws_ec2_ceddda9d.INetworkAcl:
        '''(experimental) Returns the Network ACL associated with this subnet.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.INetworkAcl, jsii.get(self, "networkAcl"))

    @builtins.property
    @jsii.member(jsii_name="routeTable")
    def route_table(self) -> _aws_cdk_aws_ec2_ceddda9d.IRouteTable:
        '''(experimental) The route table for this subnet.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IRouteTable, jsii.get(self, "routeTable"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        '''(experimental) The subnetId for this particular subnet.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @builtins.property
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        '''(experimental) The type of subnet (public or private) that this subnet represents.

        :stability: experimental
        :attribute: SubnetType
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetType, jsii.get(self, "subnetType"))

    @builtins.property
    @jsii.member(jsii_name="ipv6CidrBlock")
    def ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
        '''(experimental) The IPv6 CIDR Block for this subnet.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6CidrBlock"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.SubnetV2Props",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "ipv4_cidr_block": "ipv4CidrBlock",
        "subnet_type": "subnetType",
        "vpc": "vpc",
        "assign_ipv6_address_on_creation": "assignIpv6AddressOnCreation",
        "ipv6_cidr_block": "ipv6CidrBlock",
        "route_table": "routeTable",
        "subnet_name": "subnetName",
    },
)
class SubnetV2Props:
    def __init__(
        self,
        *,
        availability_zone: builtins.str,
        ipv4_cidr_block: IpCidr,
        subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
        vpc: IVpcV2,
        assign_ipv6_address_on_creation: typing.Optional[builtins.bool] = None,
        ipv6_cidr_block: typing.Optional[IpCidr] = None,
        route_table: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IRouteTable] = None,
        subnet_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to define subnet for VPC.

        :param availability_zone: (experimental) Custom AZ for the subnet.
        :param ipv4_cidr_block: (experimental) ipv4 cidr to assign to this subnet. See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-ec2-subnet-cidrblock
        :param subnet_type: (experimental) The type of Subnet to configure. The Subnet type will control the ability to route and connect to the Internet. TODO: Add validation check ``subnetType`` when adding resources (e.g. cannot add NatGateway to private)
        :param vpc: (experimental) VPC Prop.
        :param assign_ipv6_address_on_creation: (experimental) Indicates whether a network interface created in this subnet receives an IPv6 address. If you specify AssignIpv6AddressOnCreation, you must also specify Ipv6CidrBlock. Default: false
        :param ipv6_cidr_block: (experimental) Ipv6 CIDR Range for subnet. Default: No Ipv6 address
        :param route_table: (experimental) Custom Route for subnet. Default: Default route table
        :param subnet_name: (experimental) Subnet name. Default: none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            stack = Stack()
            my_vpc = vpc_v2.VpcV2(self, "Vpc")
            route_table = vpc_v2.RouteTable(self, "RouteTable",
                vpc=my_vpc
            )
            subnet = vpc_v2.SubnetV2(self, "Subnet",
                vpc=my_vpc,
                availability_zone="eu-west-2a",
                ipv4_cidr_block=IpCidr("10.0.0.0/24"),
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
            
            igw = vpc_v2.InternetGateway(self, "IGW",
                vpc=my_vpc
            )
            vpc_v2.Route(self, "IgwRoute",
                route_table=route_table,
                destination="0.0.0.0/0",
                target={"gateway": igw}
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ce99f8025433ac8b79825abef6ff91da4dfd0693fd24dadedcee63eb93d668)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument ipv4_cidr_block", value=ipv4_cidr_block, expected_type=type_hints["ipv4_cidr_block"])
            check_type(argname="argument subnet_type", value=subnet_type, expected_type=type_hints["subnet_type"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument assign_ipv6_address_on_creation", value=assign_ipv6_address_on_creation, expected_type=type_hints["assign_ipv6_address_on_creation"])
            check_type(argname="argument ipv6_cidr_block", value=ipv6_cidr_block, expected_type=type_hints["ipv6_cidr_block"])
            check_type(argname="argument route_table", value=route_table, expected_type=type_hints["route_table"])
            check_type(argname="argument subnet_name", value=subnet_name, expected_type=type_hints["subnet_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "ipv4_cidr_block": ipv4_cidr_block,
            "subnet_type": subnet_type,
            "vpc": vpc,
        }
        if assign_ipv6_address_on_creation is not None:
            self._values["assign_ipv6_address_on_creation"] = assign_ipv6_address_on_creation
        if ipv6_cidr_block is not None:
            self._values["ipv6_cidr_block"] = ipv6_cidr_block
        if route_table is not None:
            self._values["route_table"] = route_table
        if subnet_name is not None:
            self._values["subnet_name"] = subnet_name

    @builtins.property
    def availability_zone(self) -> builtins.str:
        '''(experimental) Custom AZ for the subnet.

        :stability: experimental
        '''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipv4_cidr_block(self) -> IpCidr:
        '''(experimental) ipv4 cidr to assign to this subnet.

        See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-ec2-subnet-cidrblock

        :stability: experimental
        '''
        result = self._values.get("ipv4_cidr_block")
        assert result is not None, "Required property 'ipv4_cidr_block' is missing"
        return typing.cast(IpCidr, result)

    @builtins.property
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        '''(experimental) The type of Subnet to configure.

        The Subnet type will control the ability to route and connect to the
        Internet.

        TODO: Add validation check ``subnetType`` when adding resources (e.g. cannot add NatGateway to private)

        :stability: experimental
        '''
        result = self._values.get("subnet_type")
        assert result is not None, "Required property 'subnet_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetType, result)

    @builtins.property
    def vpc(self) -> IVpcV2:
        '''(experimental) VPC Prop.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(IVpcV2, result)

    @builtins.property
    def assign_ipv6_address_on_creation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether a network interface created in this subnet receives an IPv6 address.

        If you specify AssignIpv6AddressOnCreation, you must also specify Ipv6CidrBlock.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("assign_ipv6_address_on_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ipv6_cidr_block(self) -> typing.Optional[IpCidr]:
        '''(experimental) Ipv6 CIDR Range for subnet.

        :default: No Ipv6 address

        :stability: experimental
        '''
        result = self._values.get("ipv6_cidr_block")
        return typing.cast(typing.Optional[IpCidr], result)

    @builtins.property
    def route_table(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IRouteTable]:
        '''(experimental) Custom Route for subnet.

        :default: Default route table

        :stability: experimental
        '''
        result = self._values.get("route_table")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IRouteTable], result)

    @builtins.property
    def subnet_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Subnet name.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("subnet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubnetV2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRouteTarget)
class VPNGateway(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.VPNGateway",
):
    '''(experimental) Creates a virtual private gateway.

    :stability: experimental
    :resource: AWS::EC2::VPNGateway
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ec2_alpha as ec2_alpha
        from aws_cdk import aws_ec2 as ec2
        
        # vpc_v2: ec2_alpha.VpcV2
        
        v_pNGateway = ec2_alpha.VPNGateway(self, "MyVPNGateway",
            type=ec2.VpnConnectionType.IPSEC_1,
            vpc=vpc_v2,
        
            # the properties below are optional
            amazon_side_asn=123,
            vpn_gateway_name="vpnGatewayName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        type: _aws_cdk_aws_ec2_ceddda9d.VpnConnectionType,
        vpc: IVpcV2,
        amazon_side_asn: typing.Optional[jsii.Number] = None,
        vpn_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param type: (experimental) The type of VPN connection the virtual private gateway supports.
        :param vpc: (experimental) The ID of the VPC for which to create the VPN gateway.
        :param amazon_side_asn: (experimental) The private Autonomous System Number (ASN) for the Amazon side of a BGP session. Default: none
        :param vpn_gateway_name: (experimental) The resource name of the VPN gateway. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6669efe999b4d7fb070da87ce4f6945c7b3b900d1c035c2e7a3dbb26415c28f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VPNGatewayProps(
            type=type,
            vpc=vpc,
            amazon_side_asn=amazon_side_asn,
            vpn_gateway_name=vpn_gateway_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnVPNGateway:
        '''(experimental) The VPN gateway CFN resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnVPNGateway, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="routerTargetId")
    def router_target_id(self) -> builtins.str:
        '''(experimental) The ID of the route target.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routerTargetId"))

    @builtins.property
    @jsii.member(jsii_name="routerType")
    def router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''(experimental) The type of router used in the route.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.RouterType, jsii.get(self, "routerType"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        '''(experimental) The ID of the VPC for which to create the VPN gateway.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.VPNGatewayProps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "vpc": "vpc",
        "amazon_side_asn": "amazonSideAsn",
        "vpn_gateway_name": "vpnGatewayName",
    },
)
class VPNGatewayProps:
    def __init__(
        self,
        *,
        type: _aws_cdk_aws_ec2_ceddda9d.VpnConnectionType,
        vpc: IVpcV2,
        amazon_side_asn: typing.Optional[jsii.Number] = None,
        vpn_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to define a VPN gateway.

        :param type: (experimental) The type of VPN connection the virtual private gateway supports.
        :param vpc: (experimental) The ID of the VPC for which to create the VPN gateway.
        :param amazon_side_asn: (experimental) The private Autonomous System Number (ASN) for the Amazon side of a BGP session. Default: none
        :param vpn_gateway_name: (experimental) The resource name of the VPN gateway. Default: none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ec2_alpha as ec2_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # vpc_v2: ec2_alpha.VpcV2
            
            v_pNGateway_props = ec2_alpha.VPNGatewayProps(
                type=ec2.VpnConnectionType.IPSEC_1,
                vpc=vpc_v2,
            
                # the properties below are optional
                amazon_side_asn=123,
                vpn_gateway_name="vpnGatewayName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c064120251b11ed07bf6eabe8a01edd24bed2a26cc286de8870e231ea63a31b)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument amazon_side_asn", value=amazon_side_asn, expected_type=type_hints["amazon_side_asn"])
            check_type(argname="argument vpn_gateway_name", value=vpn_gateway_name, expected_type=type_hints["vpn_gateway_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "vpc": vpc,
        }
        if amazon_side_asn is not None:
            self._values["amazon_side_asn"] = amazon_side_asn
        if vpn_gateway_name is not None:
            self._values["vpn_gateway_name"] = vpn_gateway_name

    @builtins.property
    def type(self) -> _aws_cdk_aws_ec2_ceddda9d.VpnConnectionType:
        '''(experimental) The type of VPN connection the virtual private gateway supports.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpngateway.html#cfn-ec2-vpngateway-type
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.VpnConnectionType, result)

    @builtins.property
    def vpc(self) -> IVpcV2:
        '''(experimental) The ID of the VPC for which to create the VPN gateway.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(IVpcV2, result)

    @builtins.property
    def amazon_side_asn(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The private Autonomous System Number (ASN) for the Amazon side of a BGP session.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("amazon_side_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_gateway_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The resource name of the VPN gateway.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("vpn_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VPNGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.VpcCidrOptions",
    jsii_struct_bases=[],
    name_mapping={
        "amazon_provided": "amazonProvided",
        "cidr_block_name": "cidrBlockName",
        "dependencies": "dependencies",
        "ipv4_cidr_block": "ipv4CidrBlock",
        "ipv4_ipam_pool": "ipv4IpamPool",
        "ipv4_netmask_length": "ipv4NetmaskLength",
        "ipv6_cidr_block": "ipv6CidrBlock",
        "ipv6_ipam_pool": "ipv6IpamPool",
        "ipv6_netmask_length": "ipv6NetmaskLength",
    },
)
class VpcCidrOptions:
    def __init__(
        self,
        *,
        amazon_provided: typing.Optional[builtins.bool] = None,
        cidr_block_name: typing.Optional[builtins.str] = None,
        dependencies: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.CfnResource]] = None,
        ipv4_cidr_block: typing.Optional[builtins.str] = None,
        ipv4_ipam_pool: typing.Optional[IIpamPool] = None,
        ipv4_netmask_length: typing.Optional[jsii.Number] = None,
        ipv6_cidr_block: typing.Optional[builtins.str] = None,
        ipv6_ipam_pool: typing.Optional[IIpamPool] = None,
        ipv6_netmask_length: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Consolidated return parameters to pass to VPC construct.

        :param amazon_provided: (experimental) Use amazon provided IP range. Default: false
        :param cidr_block_name: (experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource. Default: : no name for primary addresses
        :param dependencies: (experimental) Dependency to associate Ipv6 CIDR block. Default: - No dependency
        :param ipv4_cidr_block: (experimental) IPv4 CIDR Block. Default: - '10.0.0.0/16'
        :param ipv4_ipam_pool: (experimental) Ipv4 IPAM Pool. Default: - Only required when using IPAM Ipv4
        :param ipv4_netmask_length: (experimental) CIDR Mask for Vpc. Default: - Only required when using IPAM Ipv4
        :param ipv6_cidr_block: (experimental) Implementing Ipv6. Default: - No ipv6 address
        :param ipv6_ipam_pool: (experimental) Ipv6 IPAM pool id for VPC range, can only be defined under public scope. Default: - no pool id
        :param ipv6_netmask_length: (experimental) CIDR Mask for Vpc. Default: - Only required when using AWS Ipam

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ec2_alpha as ec2_alpha
            import aws_cdk as cdk
            
            # cfn_resource: cdk.CfnResource
            # ipam_pool: ec2_alpha.IIpamPool
            
            vpc_cidr_options = ec2_alpha.VpcCidrOptions(
                amazon_provided=False,
                cidr_block_name="cidrBlockName",
                dependencies=[cfn_resource],
                ipv4_cidr_block="ipv4CidrBlock",
                ipv4_ipam_pool=ipam_pool,
                ipv4_netmask_length=123,
                ipv6_cidr_block="ipv6CidrBlock",
                ipv6_ipam_pool=ipam_pool,
                ipv6_netmask_length=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc5a774224468f268ba34d837f3aec361583306c8694ae77cdb19bb4ce6122f4)
            check_type(argname="argument amazon_provided", value=amazon_provided, expected_type=type_hints["amazon_provided"])
            check_type(argname="argument cidr_block_name", value=cidr_block_name, expected_type=type_hints["cidr_block_name"])
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument ipv4_cidr_block", value=ipv4_cidr_block, expected_type=type_hints["ipv4_cidr_block"])
            check_type(argname="argument ipv4_ipam_pool", value=ipv4_ipam_pool, expected_type=type_hints["ipv4_ipam_pool"])
            check_type(argname="argument ipv4_netmask_length", value=ipv4_netmask_length, expected_type=type_hints["ipv4_netmask_length"])
            check_type(argname="argument ipv6_cidr_block", value=ipv6_cidr_block, expected_type=type_hints["ipv6_cidr_block"])
            check_type(argname="argument ipv6_ipam_pool", value=ipv6_ipam_pool, expected_type=type_hints["ipv6_ipam_pool"])
            check_type(argname="argument ipv6_netmask_length", value=ipv6_netmask_length, expected_type=type_hints["ipv6_netmask_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amazon_provided is not None:
            self._values["amazon_provided"] = amazon_provided
        if cidr_block_name is not None:
            self._values["cidr_block_name"] = cidr_block_name
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if ipv4_cidr_block is not None:
            self._values["ipv4_cidr_block"] = ipv4_cidr_block
        if ipv4_ipam_pool is not None:
            self._values["ipv4_ipam_pool"] = ipv4_ipam_pool
        if ipv4_netmask_length is not None:
            self._values["ipv4_netmask_length"] = ipv4_netmask_length
        if ipv6_cidr_block is not None:
            self._values["ipv6_cidr_block"] = ipv6_cidr_block
        if ipv6_ipam_pool is not None:
            self._values["ipv6_ipam_pool"] = ipv6_ipam_pool
        if ipv6_netmask_length is not None:
            self._values["ipv6_netmask_length"] = ipv6_netmask_length

    @builtins.property
    def amazon_provided(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use amazon provided IP range.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("amazon_provided")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cidr_block_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Required to set Secondary cidr block resource name in order to generate unique logical id for the resource.

        :default: : no name for primary addresses

        :stability: experimental
        '''
        result = self._values.get("cidr_block_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependencies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnResource]]:
        '''(experimental) Dependency to associate Ipv6 CIDR block.

        :default: - No dependency

        :stability: experimental
        '''
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnResource]], result)

    @builtins.property
    def ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''(experimental) IPv4 CIDR Block.

        :default: - '10.0.0.0/16'

        :stability: experimental
        '''
        result = self._values.get("ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4_ipam_pool(self) -> typing.Optional[IIpamPool]:
        '''(experimental) Ipv4 IPAM Pool.

        :default: - Only required when using IPAM Ipv4

        :stability: experimental
        '''
        result = self._values.get("ipv4_ipam_pool")
        return typing.cast(typing.Optional[IIpamPool], result)

    @builtins.property
    def ipv4_netmask_length(self) -> typing.Optional[jsii.Number]:
        '''(experimental) CIDR Mask for Vpc.

        :default: - Only required when using IPAM Ipv4

        :stability: experimental
        '''
        result = self._values.get("ipv4_netmask_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
        '''(experimental) Implementing Ipv6.

        :default: - No ipv6 address

        :stability: experimental
        '''
        result = self._values.get("ipv6_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_ipam_pool(self) -> typing.Optional[IIpamPool]:
        '''(experimental) Ipv6 IPAM pool id for VPC range, can only be defined under public scope.

        :default: - no pool id

        :stability: experimental
        '''
        result = self._values.get("ipv6_ipam_pool")
        return typing.cast(typing.Optional[IIpamPool], result)

    @builtins.property
    def ipv6_netmask_length(self) -> typing.Optional[jsii.Number]:
        '''(experimental) CIDR Mask for Vpc.

        :default: - Only required when using AWS Ipam

        :stability: experimental
        '''
        result = self._values.get("ipv6_netmask_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcCidrOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IVpcV2)
class VpcV2Base(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-ec2-alpha.VpcV2Base",
):
    '''(experimental) Base class for creating a VPC (Virtual Private Cloud) in AWS.

    For more information, see the {@link https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Vpc.html AWS CDK Documentation on VPCs}.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6eb90e3be796c2f978cd0f80c5571eb321f8dc6456107e14e0363d3dd777fb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addClientVpnEndpoint")
    def add_client_vpn_endpoint(
        self,
        id: builtins.str,
        *,
        cidr: builtins.str,
        server_certificate_arn: builtins.str,
        authorize_all_users_to_vpc_cidr: typing.Optional[builtins.bool] = None,
        client_certificate_arn: typing.Optional[builtins.str] = None,
        client_connection_handler: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IClientVpnConnectionHandler] = None,
        client_login_banner: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging: typing.Optional[builtins.bool] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        log_stream: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogStream] = None,
        port: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.VpnPort] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        self_service_portal: typing.Optional[builtins.bool] = None,
        session_timeout: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ClientVpnSessionTimeout] = None,
        split_tunnel: typing.Optional[builtins.bool] = None,
        transport_protocol: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.TransportProtocol] = None,
        user_based_authentication: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ClientVpnUserBasedAuthentication] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.ClientVpnEndpoint:
        '''(experimental) Adds a new client VPN endpoint to this VPC.

        :param id: -
        :param cidr: The IPv4 address range, in CIDR notation, from which to assign client IP addresses. The address range cannot overlap with the local CIDR of the VPC in which the associated subnet is located, or the routes that you add manually. Changing the address range will replace the Client VPN endpoint. The CIDR block should be /22 or greater.
        :param server_certificate_arn: The ARN of the server certificate.
        :param authorize_all_users_to_vpc_cidr: Whether to authorize all users to the VPC CIDR. This automatically creates an authorization rule. Set this to ``false`` and use ``addAuthorizationRule()`` to create your own rules instead. Default: true
        :param client_certificate_arn: The ARN of the client certificate for mutual authentication. The certificate must be signed by a certificate authority (CA) and it must be provisioned in AWS Certificate Manager (ACM). Default: - use user-based authentication
        :param client_connection_handler: The AWS Lambda function used for connection authorization. The name of the Lambda function must begin with the ``AWSClientVPN-`` prefix Default: - no connection handler
        :param client_login_banner: Customizable text that will be displayed in a banner on AWS provided clients when a VPN session is established. UTF-8 encoded characters only. Maximum of 1400 characters. Default: - no banner is presented to the client
        :param description: A brief description of the Client VPN endpoint. Default: - no description
        :param dns_servers: Information about the DNS servers to be used for DNS resolution. A Client VPN endpoint can have up to two DNS servers. Default: - use the DNS address configured on the device
        :param logging: Whether to enable connections logging. Default: true
        :param log_group: A CloudWatch Logs log group for connection logging. Default: - a new group is created
        :param log_stream: A CloudWatch Logs log stream for connection logging. Default: - a new stream is created
        :param port: The port number to assign to the Client VPN endpoint for TCP and UDP traffic. Default: VpnPort.HTTPS
        :param security_groups: The security groups to apply to the target network. Default: - a new security group is created
        :param self_service_portal: Specify whether to enable the self-service portal for the Client VPN endpoint. Default: true
        :param session_timeout: The maximum VPN session duration time. Default: ClientVpnSessionTimeout.TWENTY_FOUR_HOURS
        :param split_tunnel: Indicates whether split-tunnel is enabled on the AWS Client VPN endpoint. Default: false
        :param transport_protocol: The transport protocol to be used by the VPN session. Default: TransportProtocol.UDP
        :param user_based_authentication: The type of user-based authentication to use. Default: - use mutual authentication
        :param vpc_subnets: Subnets to associate to the client VPN endpoint. Default: - the VPC default strategy

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e22ab92bf67ef2717b155efcdb6ba2134d3e9bdc0a53f7c0965eca62768610)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_ec2_ceddda9d.ClientVpnEndpointOptions(
            cidr=cidr,
            server_certificate_arn=server_certificate_arn,
            authorize_all_users_to_vpc_cidr=authorize_all_users_to_vpc_cidr,
            client_certificate_arn=client_certificate_arn,
            client_connection_handler=client_connection_handler,
            client_login_banner=client_login_banner,
            description=description,
            dns_servers=dns_servers,
            logging=logging,
            log_group=log_group,
            log_stream=log_stream,
            port=port,
            security_groups=security_groups,
            self_service_portal=self_service_portal,
            session_timeout=session_timeout,
            split_tunnel=split_tunnel,
            transport_protocol=transport_protocol,
            user_based_authentication=user_based_authentication,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ClientVpnEndpoint, jsii.invoke(self, "addClientVpnEndpoint", [id, options]))

    @jsii.member(jsii_name="addFlowLog")
    def add_flow_log(
        self,
        id: builtins.str,
        *,
        destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
        log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
        max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
        traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.FlowLog:
        '''(experimental) Adds a new flow log to this VPC.

        :param id: -
        :param destination: Specifies the type of destination to which the flow log data is to be published. Flow log data can be published to CloudWatch Logs or Amazon S3 Default: FlowLogDestinationType.toCloudWatchLogs()
        :param log_format: The fields to include in the flow log record, in the order in which they should appear. If multiple fields are specified, they will be separated by spaces. For full control over the literal log format string, pass a single field constructed with ``LogFormat.custom()``. See https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records Default: - default log format is used.
        :param max_aggregation_interval: The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record. When creating flow logs for a Transit Gateway or Transit Gateway Attachment, this property must be ONE_MINUTES. Default: - FlowLogMaxAggregationInterval.ONE_MINUTES if creating flow logs for Transit Gateway, otherwise FlowLogMaxAggregationInterval.TEN_MINUTES.
        :param traffic_type: The type of traffic to log. You can log traffic that the resource accepts or rejects, or all traffic. When the target is either ``TransitGateway`` or ``TransitGatewayAttachment``, setting the traffic type is not possible. Default: ALL

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7850660c1ecf7a7ac0db1c351e57f6badfb401f4e64b3ab778905b283b503a85)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_ec2_ceddda9d.FlowLogOptions(
            destination=destination,
            log_format=log_format,
            max_aggregation_interval=max_aggregation_interval,
            traffic_type=traffic_type,
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.FlowLog, jsii.invoke(self, "addFlowLog", [id, options]))

    @jsii.member(jsii_name="addGatewayEndpoint")
    def add_gateway_endpoint(
        self,
        id: builtins.str,
        *,
        service: _aws_cdk_aws_ec2_ceddda9d.IGatewayVpcEndpointService,
        subnets: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpoint:
        '''(experimental) Adds a new gateway endpoint to this VPC.

        :param id: -
        :param service: The service to use for this gateway VPC endpoint.
        :param subnets: Where to add endpoint routing. By default, this endpoint will be routable from all subnets in the VPC. Specify a list of subnet selection objects here to be more specific. Default: - All subnets in the VPC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691a60119fb65c37ce80f2a4735370d526e48b5ee2e6fdcbb3161e850a4499da)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions(
            service=service, subnets=subnets
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpoint, jsii.invoke(self, "addGatewayEndpoint", [id, options]))

    @jsii.member(jsii_name="addInterfaceEndpoint")
    def add_interface_endpoint(
        self,
        id: builtins.str,
        *,
        service: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpointService,
        lookup_supported_azs: typing.Optional[builtins.bool] = None,
        open: typing.Optional[builtins.bool] = None,
        private_dns_enabled: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpoint:
        '''(experimental) Adds a new interface endpoint to this VPC.

        :param id: -
        :param service: The service to use for this interface VPC endpoint.
        :param lookup_supported_azs: Limit to only those availability zones where the endpoint service can be created. Setting this to 'true' requires a lookup to be performed at synthesis time. Account and region must be set on the containing stack for this to work. Default: false
        :param open: Whether to automatically allow VPC traffic to the endpoint. If enabled, all traffic to the endpoint from within the VPC will be automatically allowed. This is done based on the VPC's CIDR range. Default: true
        :param private_dns_enabled: Whether to associate a private hosted zone with the specified VPC. This allows you to make requests to the service using its default DNS hostname. Default: set by the instance of IInterfaceVpcEndpointService, or true if not defined by the instance of IInterfaceVpcEndpointService
        :param security_groups: The security groups to associate with this interface VPC endpoint. Default: - a new security group is created
        :param subnets: The subnets in which to create an endpoint network interface. At most one per availability zone. Default: - private subnets

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cbad96bdbea562df222ed5faebcc6f505e346aac5ded2fa222b915b642f9dc2)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointOptions(
            service=service,
            lookup_supported_azs=lookup_supported_azs,
            open=open,
            private_dns_enabled=private_dns_enabled,
            security_groups=security_groups,
            subnets=subnets,
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpoint, jsii.invoke(self, "addInterfaceEndpoint", [id, options]))

    @jsii.member(jsii_name="addVpnConnection")
    def add_vpn_connection(
        self,
        id: builtins.str,
        *,
        ip: builtins.str,
        asn: typing.Optional[jsii.Number] = None,
        static_routes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel_options: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnTunnelOption, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.VpnConnection:
        '''(experimental) Adds a new VPN connection to this VPC.

        :param id: -
        :param ip: The ip address of the customer gateway.
        :param asn: The ASN of the customer gateway. Default: 65000
        :param static_routes: The static routes to be routed from the VPN gateway to the customer gateway. Default: Dynamic routing (BGP)
        :param tunnel_options: The tunnel options for the VPN connection. At most two elements (one per tunnel). Duplicates not allowed. Default: Amazon generated tunnel options

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7bea01b8937a479893951a9d249dafac5eb677589e384aaf4163753c97055a5)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions(
            ip=ip, asn=asn, static_routes=static_routes, tunnel_options=tunnel_options
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.VpnConnection, jsii.invoke(self, "addVpnConnection", [id, options]))

    @jsii.member(jsii_name="enableVpnGateway")
    def enable_vpn_gateway(
        self,
        *,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: builtins.str,
        amazon_side_asn: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Adds a VPN Gateway to this VPC.

        :param vpn_route_propagation: Provide an array of subnets where the route propagation should be added. Default: noPropagation
        :param type: Default type ipsec.1.
        :param amazon_side_asn: Explicitly specify an Asn or let aws pick an Asn for you. Default: 65000

        :stability: experimental
        '''
        options = _aws_cdk_aws_ec2_ceddda9d.EnableVpnGatewayOptions(
            vpn_route_propagation=vpn_route_propagation,
            type=type,
            amazon_side_asn=amazon_side_asn,
        )

        return typing.cast(None, jsii.invoke(self, "enableVpnGateway", [options]))

    @jsii.member(jsii_name="selectSubnetObjects")
    def _select_subnet_objects(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        one_per_az: typing.Optional[builtins.bool] = None,
        subnet_filters: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SubnetFilter]] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        subnet_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetType] = None,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) Return the subnets appropriate for the placement strategy.

        :param availability_zones: Select subnets only in the given AZs. Default: no filtering on AZs is done
        :param one_per_az: If true, return at most one subnet per AZ. Default: false
        :param subnet_filters: List of provided subnet filters. Default: - none
        :param subnet_group_name: Select the subnet group with the given name. Select the subnet group with the given name. This only needs to be used if you have multiple subnet groups of the same type and you need to distinguish between them. Otherwise, prefer ``subnetType``. This field does not select individual subnets, it selects all subnets that share the given subnet group name. This is the name supplied in ``subnetConfiguration``. At most one of ``subnetType`` and ``subnetGroupName`` can be supplied. Default: - Selection by type instead of by name
        :param subnets: Explicitly select individual subnets. Use this if you don't want to automatically use all subnets in a group, but have a need to control selection down to individual subnets. Cannot be specified together with ``subnetType`` or ``subnetGroupName``. Default: - Use all subnets in a selected group (all private subnets by default)
        :param subnet_type: Select all subnets of the given type. At most one of ``subnetType`` and ``subnetGroupName`` can be supplied. Default: SubnetType.PRIVATE_WITH_EGRESS (or ISOLATED or PUBLIC if there are no PRIVATE_WITH_EGRESS subnets)

        :stability: experimental
        '''
        selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(
            availability_zones=availability_zones,
            one_per_az=one_per_az,
            subnet_filters=subnet_filters,
            subnet_group_name=subnet_group_name,
            subnets=subnets,
            subnet_type=subnet_type,
        )

        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.invoke(self, "selectSubnetObjects", [selection]))

    @jsii.member(jsii_name="selectSubnets")
    def select_subnets(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        one_per_az: typing.Optional[builtins.bool] = None,
        subnet_filters: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SubnetFilter]] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        subnet_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetType] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.SelectedSubnets:
        '''(experimental) Return information on the subnets appropriate for the given selection strategy.

        Requires that at least one subnet is matched, throws a descriptive
        error message otherwise.

        :param availability_zones: Select subnets only in the given AZs. Default: no filtering on AZs is done
        :param one_per_az: If true, return at most one subnet per AZ. Default: false
        :param subnet_filters: List of provided subnet filters. Default: - none
        :param subnet_group_name: Select the subnet group with the given name. Select the subnet group with the given name. This only needs to be used if you have multiple subnet groups of the same type and you need to distinguish between them. Otherwise, prefer ``subnetType``. This field does not select individual subnets, it selects all subnets that share the given subnet group name. This is the name supplied in ``subnetConfiguration``. At most one of ``subnetType`` and ``subnetGroupName`` can be supplied. Default: - Selection by type instead of by name
        :param subnets: Explicitly select individual subnets. Use this if you don't want to automatically use all subnets in a group, but have a need to control selection down to individual subnets. Cannot be specified together with ``subnetType`` or ``subnetGroupName``. Default: - Use all subnets in a selected group (all private subnets by default)
        :param subnet_type: Select all subnets of the given type. At most one of ``subnetType`` and ``subnetGroupName`` can be supplied. Default: SubnetType.PRIVATE_WITH_EGRESS (or ISOLATED or PUBLIC if there are no PRIVATE_WITH_EGRESS subnets)

        :stability: experimental
        '''
        selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(
            availability_zones=availability_zones,
            one_per_az=one_per_az,
            subnet_filters=subnet_filters,
            subnet_group_name=subnet_group_name,
            subnets=subnets,
            subnet_type=subnet_type,
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets, jsii.invoke(self, "selectSubnets", [selection]))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        '''(experimental) AZs for this VPC.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    @abc.abstractmethod
    def internet_connectivity_established(self) -> _constructs_77d1e7e8.IDependable:
        '''(experimental) Dependable that can be depended upon to force internet connectivity established on the VPC.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ipv4CidrBlock")
    @abc.abstractmethod
    def ipv4_cidr_block(self) -> builtins.str:
        '''(experimental) The primary IPv4 CIDR block associated with the VPC.

        Needed in order to validate the vpc range of subnet
        current prop vpcCidrBlock refers to the token value
        For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-sizing-ipv4}.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="isolatedSubnets")
    @abc.abstractmethod
    def isolated_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) List of isolated subnets in this VPC.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) List of private subnets in this VPC.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.get(self, "privateSubnets"))

    @builtins.property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) List of public subnets in this VPC.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.get(self, "publicSubnets"))

    @builtins.property
    @jsii.member(jsii_name="secondaryCidrBlock")
    @abc.abstractmethod
    def secondary_cidr_block(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnVPCCidrBlock]:
        '''(experimental) Secondary IPs for the VPC, can be multiple Ipv4 or Ipv6 Ipv4 should be within RFC#1918 range.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcArn")
    @abc.abstractmethod
    def vpc_arn(self) -> builtins.str:
        '''(experimental) Arn of this VPC.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcCidrBlock")
    @abc.abstractmethod
    def vpc_cidr_block(self) -> builtins.str:
        '''(experimental) CIDR range for this VPC.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    @abc.abstractmethod
    def vpc_id(self) -> builtins.str:
        '''(experimental) Identifier for this VPC.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Returns the id of the VPN Gateway (if enabled).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnGatewayId"))

    @builtins.property
    @jsii.member(jsii_name="incompleteSubnetDefinition")
    def _incomplete_subnet_definition(self) -> builtins.bool:
        '''(experimental) If this is set to true, don't error out on trying to select subnets.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "incompleteSubnetDefinition"))

    @_incomplete_subnet_definition.setter
    def _incomplete_subnet_definition(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072197b57e17e2499221b9aaf0906eb11fd406cafb9318f2400beeef9e8484d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "incompleteSubnetDefinition", value) # pyright: ignore[reportArgumentType]


class _VpcV2BaseProxy(
    VpcV2Base,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    def internet_connectivity_established(self) -> _constructs_77d1e7e8.IDependable:
        '''(experimental) Dependable that can be depended upon to force internet connectivity established on the VPC.

        :stability: experimental
        '''
        return typing.cast(_constructs_77d1e7e8.IDependable, jsii.get(self, "internetConnectivityEstablished"))

    @builtins.property
    @jsii.member(jsii_name="ipv4CidrBlock")
    def ipv4_cidr_block(self) -> builtins.str:
        '''(experimental) The primary IPv4 CIDR block associated with the VPC.

        Needed in order to validate the vpc range of subnet
        current prop vpcCidrBlock refers to the token value
        For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-sizing-ipv4}.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ipv4CidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="isolatedSubnets")
    def isolated_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) List of isolated subnets in this VPC.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.get(self, "isolatedSubnets"))

    @builtins.property
    @jsii.member(jsii_name="secondaryCidrBlock")
    def secondary_cidr_block(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnVPCCidrBlock]:
        '''(experimental) Secondary IPs for the VPC, can be multiple Ipv4 or Ipv6 Ipv4 should be within RFC#1918 range.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnVPCCidrBlock], jsii.get(self, "secondaryCidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="vpcArn")
    def vpc_arn(self) -> builtins.str:
        '''(experimental) Arn of this VPC.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcArn"))

    @builtins.property
    @jsii.member(jsii_name="vpcCidrBlock")
    def vpc_cidr_block(self) -> builtins.str:
        '''(experimental) CIDR range for this VPC.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcCidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        '''(experimental) Identifier for this VPC.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, VpcV2Base).__jsii_proxy_class__ = lambda : _VpcV2BaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ec2-alpha.VpcV2Props",
    jsii_struct_bases=[],
    name_mapping={
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "primary_address_block": "primaryAddressBlock",
        "secondary_address_blocks": "secondaryAddressBlocks",
        "vpc_name": "vpcName",
    },
)
class VpcV2Props:
    def __init__(
        self,
        *,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        primary_address_block: typing.Optional[IIpAddresses] = None,
        secondary_address_blocks: typing.Optional[typing.Sequence[IIpAddresses]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to define VPC [disable-awslint:from-method].

        :param default_instance_tenancy: (experimental) The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
        :param enable_dns_hostnames: (experimental) Indicates whether the instances launched in the VPC get DNS hostnames. Default: true
        :param enable_dns_support: (experimental) Indicates whether the DNS resolution is supported for the VPC. Default: true
        :param primary_address_block: (experimental) A must IPv4 CIDR block for the VPC https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html. Default: - Ipv4 CIDR Block ('10.0.0.0/16')
        :param secondary_address_blocks: (experimental) The secondary CIDR blocks associated with the VPC. Can be IPv4 or IPv6, two IPv4 ranges must follow RFC#1918 convention For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-resize}. Default: - No secondary IP address
        :param vpc_name: (experimental) Physical name for the VPC. Default: : autogenerated by CDK

        :stability: experimental
        :exampleMetadata: infused

        Example::

            stack = Stack()
            my_vpc = vpc_v2.VpcV2(self, "Vpc",
                secondary_address_blocks=[
                    vpc_v2.IpAddresses.amazon_provided_ipv6(cidr_block_name="AmazonProvidedIp")
                ]
            )
            
            vpc_v2.SubnetV2(self, "subnetA",
                vpc=my_vpc,
                availability_zone="us-east-1a",
                ipv4_cidr_block=vpc_v2.IpCidr("10.0.0.0/24"),
                ipv6_cidr_block=vpc_v2.IpCidr("2a05:d02c:25:4000::/60"),
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f915ef5e4a9fa4854227228067c81d198633b3f6b9621c83cee1390bc703549)
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument primary_address_block", value=primary_address_block, expected_type=type_hints["primary_address_block"])
            check_type(argname="argument secondary_address_blocks", value=secondary_address_blocks, expected_type=type_hints["secondary_address_blocks"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if primary_address_block is not None:
            self._values["primary_address_block"] = primary_address_block
        if secondary_address_blocks is not None:
            self._values["secondary_address_blocks"] = secondary_address_blocks
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        '''(experimental) The default tenancy of instances launched into the VPC.

        By setting this to dedicated tenancy, instances will be launched on
        hardware dedicated to a single AWS customer, unless specifically specified
        at instance launch time. Please note, not all instance types are usable
        with Dedicated tenancy.

        :default: DefaultInstanceTenancy.Default (shared) tenancy

        :stability: experimental
        '''
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the instances launched in the VPC get DNS hostnames.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the DNS resolution is supported for the VPC.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def primary_address_block(self) -> typing.Optional[IIpAddresses]:
        '''(experimental) A must IPv4 CIDR block for the VPC https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html.

        :default: - Ipv4 CIDR Block ('10.0.0.0/16')

        :stability: experimental
        '''
        result = self._values.get("primary_address_block")
        return typing.cast(typing.Optional[IIpAddresses], result)

    @builtins.property
    def secondary_address_blocks(self) -> typing.Optional[typing.List[IIpAddresses]]:
        '''(experimental) The secondary CIDR blocks associated with the VPC.

        Can be  IPv4 or IPv6, two IPv4 ranges must follow RFC#1918 convention
        For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-resize}.

        :default: - No secondary IP address

        :stability: experimental
        '''
        result = self._values.get("secondary_address_blocks")
        return typing.cast(typing.Optional[typing.List[IIpAddresses]], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Physical name for the VPC.

        :default: : autogenerated by CDK

        :stability: experimental
        '''
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcV2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRouteTarget)
class EgressOnlyInternetGateway(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.EgressOnlyInternetGateway",
):
    '''(experimental) Creates an egress-only internet gateway.

    :stability: experimental
    :resource: AWS::EC2::EgressOnlyInternetGateway
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ec2_alpha as ec2_alpha
        
        # vpc_v2: ec2_alpha.VpcV2
        
        egress_only_internet_gateway = ec2_alpha.EgressOnlyInternetGateway(self, "MyEgressOnlyInternetGateway",
            vpc=vpc_v2,
        
            # the properties below are optional
            egress_only_internet_gateway_name="egressOnlyInternetGatewayName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: IVpcV2,
        egress_only_internet_gateway_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: (experimental) The ID of the VPC for which to create the egress-only internet gateway.
        :param egress_only_internet_gateway_name: (experimental) The resource name of the egress-only internet gateway. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff67e43de6a050a1b2238939edd2b432686ecfc1a3e2758af2b927323727412)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EgressOnlyInternetGatewayProps(
            vpc=vpc,
            egress_only_internet_gateway_name=egress_only_internet_gateway_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnEgressOnlyInternetGateway:
        '''(experimental) The egress-only internet gateway CFN resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnEgressOnlyInternetGateway, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="routerTargetId")
    def router_target_id(self) -> builtins.str:
        '''(experimental) The ID of the route target.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routerTargetId"))

    @builtins.property
    @jsii.member(jsii_name="routerType")
    def router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''(experimental) The type of router used in the route.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.RouterType, jsii.get(self, "routerType"))


class VpcV2(
    VpcV2Base,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ec2-alpha.VpcV2",
):
    '''(experimental) This class provides a foundation for creating and configuring a VPC with advanced features such as IPAM (IP Address Management) and IPv6 support.

    For more information, see the {@link https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Vpc.html AWS CDK Documentation on VPCs}.

    :stability: experimental
    :resource: AWS::EC2::VPC
    :exampleMetadata: infused

    Example::

        my_vpc = vpc_v2.VpcV2(self, "Vpc")
        route_table = vpc_v2.RouteTable(self, "RouteTable",
            vpc=my_vpc
        )
        subnet = vpc_v2.SubnetV2(self, "Subnet",
            vpc=my_vpc,
            availability_zone="eu-west-2a",
            ipv4_cidr_block=IpCidr("10.0.0.0/24"),
            subnet_type=ec2.SubnetType.PRIVATE
        )
        
        dynamo_endpoint = ec2.GatewayVpcEndpoint(self, "DynamoEndpoint",
            service=ec2.GatewayVpcEndpointAwsService.DYNAMODB,
            vpc=my_vpc,
            subnets=[subnet]
        )
        vpc_v2.Route(self, "DynamoDBRoute",
            route_table=route_table,
            destination="0.0.0.0/0",
            target={"endpoint": dynamo_endpoint}
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        primary_address_block: typing.Optional[IIpAddresses] = None,
        secondary_address_blocks: typing.Optional[typing.Sequence[IIpAddresses]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param default_instance_tenancy: (experimental) The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
        :param enable_dns_hostnames: (experimental) Indicates whether the instances launched in the VPC get DNS hostnames. Default: true
        :param enable_dns_support: (experimental) Indicates whether the DNS resolution is supported for the VPC. Default: true
        :param primary_address_block: (experimental) A must IPv4 CIDR block for the VPC https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html. Default: - Ipv4 CIDR Block ('10.0.0.0/16')
        :param secondary_address_blocks: (experimental) The secondary CIDR blocks associated with the VPC. Can be IPv4 or IPv6, two IPv4 ranges must follow RFC#1918 convention For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-resize}. Default: - No secondary IP address
        :param vpc_name: (experimental) Physical name for the VPC. Default: : autogenerated by CDK

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43890f4b3ccf690abe4140abf07c3436fde6604bac35ff6b2e8fe5da2a20b481)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpcV2Props(
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            primary_address_block=primary_address_block,
            secondary_address_blocks=secondary_address_blocks,
            vpc_name=vpc_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="dnsHostnamesEnabled")
    def dns_hostnames_enabled(self) -> builtins.bool:
        '''(experimental) Indicates if instances launched in this VPC will have public DNS hostnames.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "dnsHostnamesEnabled"))

    @builtins.property
    @jsii.member(jsii_name="dnsSupportEnabled")
    def dns_support_enabled(self) -> builtins.bool:
        '''(experimental) Indicates if DNS support is enabled for this VPC.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "dnsSupportEnabled"))

    @builtins.property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    def internet_connectivity_established(self) -> _constructs_77d1e7e8.IDependable:
        '''(experimental) To define dependency on internet connectivity.

        :stability: experimental
        '''
        return typing.cast(_constructs_77d1e7e8.IDependable, jsii.get(self, "internetConnectivityEstablished"))

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> IIpAddresses:
        '''(experimental) The provider of ipv4 addresses.

        :stability: experimental
        '''
        return typing.cast(IIpAddresses, jsii.get(self, "ipAddresses"))

    @builtins.property
    @jsii.member(jsii_name="ipv4CidrBlock")
    def ipv4_cidr_block(self) -> builtins.str:
        '''(experimental) The primary IPv4 CIDR block associated with the VPC.

        Needed in order to validate the vpc range of subnet
        current prop vpcCidrBlock refers to the token value
        For more information, see the {@link https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html#vpc-sizing-ipv4}.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ipv4CidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="ipv6CidrBlocks")
    def ipv6_cidr_blocks(self) -> typing.List[builtins.str]:
        '''(experimental) The IPv6 CIDR blocks for the VPC.

        See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html#aws-resource-ec2-vpc-return-values

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipv6CidrBlocks"))

    @builtins.property
    @jsii.member(jsii_name="isolatedSubnets")
    def isolated_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) Isolated Subnets that are part of this VPC.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.get(self, "isolatedSubnets"))

    @builtins.property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) Pbulic Subnets that are part of this VPC.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.get(self, "privateSubnets"))

    @builtins.property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) Public Subnets that are part of this VPC.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.get(self, "publicSubnets"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnVPC:
        '''(experimental) The AWS CloudFormation resource representing the VPC.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnVPC, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="secondaryCidrBlock")
    def secondary_cidr_block(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnVPCCidrBlock]:
        '''(experimental) reference to all secondary blocks attached.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnVPCCidrBlock], jsii.get(self, "secondaryCidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="useIpv6")
    def use_ipv6(self) -> builtins.bool:
        '''(experimental) For validation to define IPv6 subnets, set to true in case of Amazon Provided IPv6 cidr range IPv6 addresses can be attached to the subnets.

        :default: false

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "useIpv6"))

    @builtins.property
    @jsii.member(jsii_name="vpcArn")
    def vpc_arn(self) -> builtins.str:
        '''(experimental) Arn of this VPC.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcArn"))

    @builtins.property
    @jsii.member(jsii_name="vpcCidrBlock")
    def vpc_cidr_block(self) -> builtins.str:
        '''(experimental) CIDR range for this VPC.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcCidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        '''(experimental) Identifier for this VPC.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))


__all__ = [
    "AddressFamily",
    "AwsServiceName",
    "EgressOnlyInternetGateway",
    "EgressOnlyInternetGatewayProps",
    "IIpAddresses",
    "IIpamPool",
    "IIpamScopeBase",
    "IRouteTarget",
    "IRouteV2",
    "ISubnetV2",
    "IVpcV2",
    "InternetGateway",
    "InternetGatewayProps",
    "IpAddresses",
    "IpCidr",
    "Ipam",
    "IpamOptions",
    "IpamPoolCidrProvisioningOptions",
    "IpamPoolPublicIpSource",
    "IpamProps",
    "IpamScopeOptions",
    "IpamScopeType",
    "NatConnectivityType",
    "NatGateway",
    "NatGatewayProps",
    "PoolOptions",
    "Route",
    "RouteProps",
    "RouteTable",
    "RouteTableProps",
    "RouteTargetProps",
    "RouteTargetType",
    "SecondaryAddressProps",
    "SubnetV2",
    "SubnetV2Props",
    "VPNGateway",
    "VPNGatewayProps",
    "VpcCidrOptions",
    "VpcV2",
    "VpcV2Base",
    "VpcV2Props",
]

publication.publish()

def _typecheckingstub__a1cb0281052a85d3461453c956e87b81e82be05002c1ac33451b382cfcf0ea7e(
    *,
    vpc: IVpcV2,
    egress_only_internet_gateway_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bc97652054ab6c0bbc03431c16bfd7acb0fddbb3d48a9495d8b53ad88d5dc8(
    id: builtins.str,
    *,
    cidr: typing.Optional[builtins.str] = None,
    netmask_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab59e34a032c2ecbc5b1f46184e5eafc041fe87fd1c685e9d6723df4798da29(
    id: builtins.str,
    *,
    address_family: AddressFamily,
    aws_service: typing.Optional[AwsServiceName] = None,
    ipv4_provisioned_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    locale: typing.Optional[builtins.str] = None,
    public_ip_source: typing.Optional[IpamPoolPublicIpSource] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ed9b26ff938b529db1af6f12978e1aa57b9cdaf5a5c589675cf7b8f2c6fe6a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: IVpcV2,
    internet_gateway_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4699002455f77fce358247d059e2af25aa232257e94012a7ff9adcc0f4d4268(
    *,
    vpc: IVpcV2,
    internet_gateway_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023808e0046a190f50dc770cc212c33e5f498063e503f04733eccd089bee0a1c(
    ipv4_cidr: builtins.str,
    *,
    cidr_block_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a863e7a355c78c90751f90234cc17db747d36357a2406915207b6aa4fd217e08(
    props: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ed6f6a471c5154b59132e6c943218845868bcf0ef72feac08ef9ecf58fda24(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ipam_name: typing.Optional[builtins.str] = None,
    operating_region: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296863e23505efe3c05687294f941735dfb8c507dbfd2ba189d45b4953c95ac0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ipam_scope_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef69b77e361363d19bbc896e7549828dabe3c8a5aa6a3470fe28e6b811c0a845(
    *,
    cidr_block_name: builtins.str,
    ipam_pool: typing.Optional[IIpamPool] = None,
    netmask_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d9b15700233762113ea1f831e611edef9363690ea36470a160f478fbe21dd0(
    *,
    cidr: typing.Optional[builtins.str] = None,
    netmask_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f718be906e882bf24bd25534ed4d857392b590d6c147225d8e6b56b22b1781d7(
    *,
    ipam_name: typing.Optional[builtins.str] = None,
    operating_region: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18fc2fc30cb847c875d0d2bc1bf84a72aea509aa638af404c53fa7ab0776fa1(
    *,
    ipam_scope_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3204c5cc1ee92d73075b1e2c597a7d7bb9eb73b154f33262369b6b4ac9ec33f4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
    allocation_id: typing.Optional[builtins.str] = None,
    connectivity_type: typing.Optional[NatConnectivityType] = None,
    max_drain_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    nat_gateway_name: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    secondary_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    secondary_private_ip_address_count: typing.Optional[jsii.Number] = None,
    secondary_private_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc: typing.Optional[IVpcV2] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c6c285bd9604aa1bbf23945426abd3cb4259870f0a85edd40b87eb08b29903(
    *,
    subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
    allocation_id: typing.Optional[builtins.str] = None,
    connectivity_type: typing.Optional[NatConnectivityType] = None,
    max_drain_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    nat_gateway_name: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    secondary_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    secondary_private_ip_address_count: typing.Optional[jsii.Number] = None,
    secondary_private_ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc: typing.Optional[IVpcV2] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b5a95424fdb1e7fb6ae3da82efaf806f125de298a951d9b7f9b24181fd5c41(
    *,
    address_family: AddressFamily,
    aws_service: typing.Optional[AwsServiceName] = None,
    ipv4_provisioned_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    locale: typing.Optional[builtins.str] = None,
    public_ip_source: typing.Optional[IpamPoolPublicIpSource] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4a94ed3246ec1926122f93a061896a8268de25ae7a4cc12e59846ba76bd6b1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    destination: builtins.str,
    route_table: _aws_cdk_aws_ec2_ceddda9d.IRouteTable,
    target: RouteTargetType,
    route_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda2cbb996081e5d873ecff8f8ff6450468388a42bf4745882a9caf33d55d197(
    *,
    destination: builtins.str,
    route_table: _aws_cdk_aws_ec2_ceddda9d.IRouteTable,
    target: RouteTargetType,
    route_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa486baea72e1e0413e458ea1f52d60725dbcdfeed33f2e810006af4c66d5a6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: IVpcV2,
    route_table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271dc5ccfa2e958efecaeb52a22e0ecbf03734c62d76ebbf18cb73e88deea29f(
    *,
    vpc: IVpcV2,
    route_table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777e37951fe65e456a56f7503992af6a79e1c8be4aeaf3a7544650f38247d64b(
    *,
    endpoint: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint] = None,
    gateway: typing.Optional[IRouteTarget] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9433843cde495b2d9551feec9fd15a488c151e944cfd2262b5fc2613ca397870(
    *,
    cidr_block_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9294d0dd8fd099bad5e4bd408f0f8b8bffbcdc6e4f624de6a1bf54199885b6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    availability_zone: builtins.str,
    ipv4_cidr_block: IpCidr,
    subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
    vpc: IVpcV2,
    assign_ipv6_address_on_creation: typing.Optional[builtins.bool] = None,
    ipv6_cidr_block: typing.Optional[IpCidr] = None,
    route_table: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IRouteTable] = None,
    subnet_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ecedf09cdae417f7675efd5f583cb5bfabde2a1b69f4f330c6434c1020e903(
    id: builtins.str,
    network_acl: _aws_cdk_aws_ec2_ceddda9d.INetworkAcl,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ce99f8025433ac8b79825abef6ff91da4dfd0693fd24dadedcee63eb93d668(
    *,
    availability_zone: builtins.str,
    ipv4_cidr_block: IpCidr,
    subnet_type: _aws_cdk_aws_ec2_ceddda9d.SubnetType,
    vpc: IVpcV2,
    assign_ipv6_address_on_creation: typing.Optional[builtins.bool] = None,
    ipv6_cidr_block: typing.Optional[IpCidr] = None,
    route_table: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IRouteTable] = None,
    subnet_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6669efe999b4d7fb070da87ce4f6945c7b3b900d1c035c2e7a3dbb26415c28f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    type: _aws_cdk_aws_ec2_ceddda9d.VpnConnectionType,
    vpc: IVpcV2,
    amazon_side_asn: typing.Optional[jsii.Number] = None,
    vpn_gateway_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c064120251b11ed07bf6eabe8a01edd24bed2a26cc286de8870e231ea63a31b(
    *,
    type: _aws_cdk_aws_ec2_ceddda9d.VpnConnectionType,
    vpc: IVpcV2,
    amazon_side_asn: typing.Optional[jsii.Number] = None,
    vpn_gateway_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5a774224468f268ba34d837f3aec361583306c8694ae77cdb19bb4ce6122f4(
    *,
    amazon_provided: typing.Optional[builtins.bool] = None,
    cidr_block_name: typing.Optional[builtins.str] = None,
    dependencies: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.CfnResource]] = None,
    ipv4_cidr_block: typing.Optional[builtins.str] = None,
    ipv4_ipam_pool: typing.Optional[IIpamPool] = None,
    ipv4_netmask_length: typing.Optional[jsii.Number] = None,
    ipv6_cidr_block: typing.Optional[builtins.str] = None,
    ipv6_ipam_pool: typing.Optional[IIpamPool] = None,
    ipv6_netmask_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6eb90e3be796c2f978cd0f80c5571eb321f8dc6456107e14e0363d3dd777fb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e22ab92bf67ef2717b155efcdb6ba2134d3e9bdc0a53f7c0965eca62768610(
    id: builtins.str,
    *,
    cidr: builtins.str,
    server_certificate_arn: builtins.str,
    authorize_all_users_to_vpc_cidr: typing.Optional[builtins.bool] = None,
    client_certificate_arn: typing.Optional[builtins.str] = None,
    client_connection_handler: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IClientVpnConnectionHandler] = None,
    client_login_banner: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging: typing.Optional[builtins.bool] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_stream: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogStream] = None,
    port: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.VpnPort] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    self_service_portal: typing.Optional[builtins.bool] = None,
    session_timeout: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ClientVpnSessionTimeout] = None,
    split_tunnel: typing.Optional[builtins.bool] = None,
    transport_protocol: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.TransportProtocol] = None,
    user_based_authentication: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ClientVpnUserBasedAuthentication] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7850660c1ecf7a7ac0db1c351e57f6badfb401f4e64b3ab778905b283b503a85(
    id: builtins.str,
    *,
    destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
    log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
    max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
    traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691a60119fb65c37ce80f2a4735370d526e48b5ee2e6fdcbb3161e850a4499da(
    id: builtins.str,
    *,
    service: _aws_cdk_aws_ec2_ceddda9d.IGatewayVpcEndpointService,
    subnets: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbad96bdbea562df222ed5faebcc6f505e346aac5ded2fa222b915b642f9dc2(
    id: builtins.str,
    *,
    service: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpointService,
    lookup_supported_azs: typing.Optional[builtins.bool] = None,
    open: typing.Optional[builtins.bool] = None,
    private_dns_enabled: typing.Optional[builtins.bool] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7bea01b8937a479893951a9d249dafac5eb677589e384aaf4163753c97055a5(
    id: builtins.str,
    *,
    ip: builtins.str,
    asn: typing.Optional[jsii.Number] = None,
    static_routes: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel_options: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnTunnelOption, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072197b57e17e2499221b9aaf0906eb11fd406cafb9318f2400beeef9e8484d1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f915ef5e4a9fa4854227228067c81d198633b3f6b9621c83cee1390bc703549(
    *,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    primary_address_block: typing.Optional[IIpAddresses] = None,
    secondary_address_blocks: typing.Optional[typing.Sequence[IIpAddresses]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff67e43de6a050a1b2238939edd2b432686ecfc1a3e2758af2b927323727412(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: IVpcV2,
    egress_only_internet_gateway_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43890f4b3ccf690abe4140abf07c3436fde6604bac35ff6b2e8fe5da2a20b481(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    primary_address_block: typing.Optional[IIpAddresses] = None,
    secondary_address_blocks: typing.Optional[typing.Sequence[IIpAddresses]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
