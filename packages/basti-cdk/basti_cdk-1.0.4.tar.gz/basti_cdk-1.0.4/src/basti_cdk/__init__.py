r'''
<h1 align="center">Basti CDK</h1><div align="center">
  <a href="https://www.npmjs.com/package/basti-cdk">
    <img alt="NPM Package" src="https://img.shields.io/npm/v/basti-cdk?color=green">
  </a>
  <a href="https://pypi.org/project/basti-cdk">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/basti-cdk?color=blue">
  </a>
  <a href="https://github.com/basti-app/basti/blob/main/packages/basti-cdk/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/github/license/basti-app/basti">
  </a>
</div><br/><div align="center">
  <a href="https://github.com/basti-app/basti/tree/main/packages/basti-cdk">Basti CDK</a> is a construct library that allows you to create cost-efficient <a href="https://en.wikipedia.org/wiki/Bastion_host">bastion instances</a> and easily connect to your infrastructure with <a href="https://github.com/basti-app/basti">Basti CLI</a>.
  <br/>
  <br/>
  💵 <em>No idle costs.</em>  🔑 <em>No SSH keys.</em> 🔒 <em>Fully IAM-driven.</em>
</div><br/><div align="center">
  <img alt="Diagram" src="https://github.com/basti-app/basti/assets/45905756/1fa0762e-d6a1-4449-9e83-da87b53c3604">
</div><br/><!-- The following toc is generated with the Markdown All in One VSCode extension (https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) --><!-- omit from toc -->

## Table of contents

* [Why Basti?](#why-basti)
* [How it works](#how-it-works)
* [Installation](#installation)

  * [NPM](#npm)
  * [PyPI](#pypi)
* [API reference](#api-reference)
* [Examples](#examples)
* [Basic usage](#basic-usage)

  * [Set up Basti instance](#set-up-basti-instance)
  * [Allow connection to target](#allow-connection-to-target)
  * [Connect to target](#connect-to-target)
* [Advanced usage](#advanced-usage)

  * [Importing existing Basti instance](#importing-existing-basti-instance)
  * [Granting access to use Basti instance](#granting-access-to-use-basti-instance)
* [License](#license)

<br/>

## Why Basti?

With [Basti](https://github.com/basti-app/basti), you can securely connect to your RDS/Aurora/Elasticache/EC2 instances in private VPC subnets from a local machine or CI/CD pipeline almost for free!

## How it works

* 🏰 Using Basti CDK, you set up a bastion instance in the connection target's VPC.
* 🧑‍💻 You use [Basti CLI](https://github.com/basti-app/basti) to conveniently connect to your target through the bastion instance.
* 💵 Basti takes care of keeping the bastion instance stopped when it's not used to make the solution cost as low as **≈ 0.01 USD** per hour of connection plus **≈ 0.80 USD** per month of maintaining the instance in a stopped state.
* 🔒 Security completely relies on AWS Session Manager and IAM policies. The bastion instance is not accessible from the Internet and no SSH keys are used.

## Installation

The construct is available in multiple languages thanks to [JSII](https://github.com/aws/jsii).

### NPM

```bash
npm install basti-cdk
```

### PyPI

```bash
pip install basti-cdk
```

## API reference

See the full API reference [on Construct Hub](https://constructs.dev/packages/basti-cdk).

## Examples

See [the test CDK apps](https://github.com/basti-app/basti/tree/main/packages/basti-cdk/test/cdk-apps) for working examples of each feature the library provides.

## Basic usage

Basti constructs can be imported from the `basti-cdk` package.

```python
import { BastiAccessSecurityGroup, BastiInstance } from 'basti-cdk';
```

> 💡 RDS instance is used as an example target. You can use Basti to connect to any other AWS resource that supports security groups.

### Set up Basti instance

Use `BastiInstance` construct to create Basti EC2 instance.

```python
const bastiInstance = new BastiInstance(
  stack,
  'BastiInstance',
  {
    vpc,

    // Optional. Randomly generated if omitted.
    // Used to name the EC2 instance and other resources.
    // The resulting name will be "basti-instance-my-bastion"
    bastiId: 'my-bastion'
  }
);
```

### Allow connection to target

Use `BastiAccessSecurityGroup` construct to create a security group for your target. This security group will allow the Basti instance to connect to the target.

```python
// Create a security group for your target
const bastiAccessSecurityGroup = new BastiAccessSecurityGroup(
  stack,
  'BastiAccessSecurityGroup',
  {
    vpc,

    // Optional. Randomly generated if omitted.
    // Used to name the security group and other resources.
    // The resulting name will be "basti-access-my-target"
    bastiId: 'my-target'
  }
);

// Create the target
const rdsInstance = new aws_rds.DatabaseInstance(
  stack,
  'RdsInstance',
  {
    // Unrelated properties are omitted for brevity

    vpc,
    port: 5432,

    securityGroups: [
      bastiAccessSecurityGroup
    ]
  }
);

// Allow the Basti instance to connect to the target on the specified port
bastiAccessSecurityGroup.allowBastiInstanceConnection(
  bastiInstance,
  aws_ec2.Port.tcp(rdsInstance.instanceEndpoint.port)
);
```

### Connect to target

When the stack is deployed, you can use [Basti CLI](https://github.com/basti-app/basti) to connect to your target.

```sh
basti connect
```

## Advanced usage

### Importing existing Basti instance

When sharing a Basti instance across stacks, you can just pass it as a property to the other stack. In case you need to import a Basti instance created in a separate CDK app or not managed by CDK at all, you can use the `BastiInstance.fromBastiId` method. The method returns an `IBastiInstance` object which is sufficient for granting access to a connection target.

```python
// Most likely, the VPC was created separately as well
const vpc = aws_ec2.Vpc.fromLookup(stack, 'Vpc', {
    vpcName: 'existing-vpc-id',
});

const bastiInstance = BastiInstance.fromBastiId(
    this,
    'BastiInstance',
    // The BastiID of the Basti instance you want to import
    'existing-basti-id',
    vpc
);

// bastiInstance can now be used to allow access to a connection target
bastiAccessSecurityGroup.allowBastiInstanceConnection(
  bastiInstance,
  aws_ec2.Port.tcp(1717)
);
```

### Granting access to use Basti instance

You can grant the ability to connect to a Basti instance to other resources (users, roles, etc.) using the `grantBastiCliConnect` method of an existing Basti instance.

```python
const bastiInstance = new BastiInstance(/*...*/);
const grantee = new aws_iam.Role(/*...*/);

bastiInstance.grantBastiCliConnect(grantee);
```

## License

Usage is provided under the MIT License. See [LICENSE](https://github.com/basti-app/basti/blob/main/packages/basti-cdk/LICENSE) for the full details.
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


class BastiAccessSecurityGroup(
    _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
    metaclass=jsii.JSIIMeta,
    jsii_type="basti-cdk.BastiAccessSecurityGroup",
):
    '''The Basti access security group.

    This security group is used to allow access to a connection
    target from a Basti instance.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        basti_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: The VPC in which to create the security group.
        :param basti_id: (Optional) The ID of the Basti access security group. The ID will be used to identify any resources created within this construct. If not specified, a random ID will be generated. Default: An 8-character pseudo-random string
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01948589ed1a60919700df630bf7069a9d8c730904dc0053525f1ca445fc0678)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BastiAccessSecurityGroupProps(vpc=vpc, basti_id=basti_id)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="allowBastiInstanceConnection")
    def allow_basti_instance_connection(
        self,
        basti_instance: "IBastiInstance",
        port: _aws_cdk_aws_ec2_ceddda9d.Port,
    ) -> None:
        '''Allows connection from the provided Basti instance to the given port by creating an ingress rule.

        :param basti_instance: The Basti instance.
        :param port: The port to allow access to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d033d471ed35bb19d7d2268c0a4a86abc74b88e32fdb3c7330adb7ad118b4dd)
            check_type(argname="argument basti_instance", value=basti_instance, expected_type=type_hints["basti_instance"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        return typing.cast(None, jsii.invoke(self, "allowBastiInstanceConnection", [basti_instance, port]))

    @builtins.property
    @jsii.member(jsii_name="bastiId")
    def basti_id(self) -> builtins.str:
        '''The ID of the Basti access security group.'''
        return typing.cast(builtins.str, jsii.get(self, "bastiId"))


@jsii.data_type(
    jsii_type="basti-cdk.BastiAccessSecurityGroupProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc", "basti_id": "bastiId"},
)
class BastiAccessSecurityGroupProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        basti_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The properties for the Basti access security group.

        :param vpc: The VPC in which to create the security group.
        :param basti_id: (Optional) The ID of the Basti access security group. The ID will be used to identify any resources created within this construct. If not specified, a random ID will be generated. Default: An 8-character pseudo-random string
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80155f9d79726f26f5e96ec5e5bf13d3e3dc94dac96daf7a46bfc6f5da964648)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument basti_id", value=basti_id, expected_type=type_hints["basti_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if basti_id is not None:
            self._values["basti_id"] = basti_id

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC in which to create the security group.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def basti_id(self) -> typing.Optional[builtins.str]:
        '''(Optional) The ID of the Basti access security group.

        The ID will be used to identify
        any resources created within this construct. If not specified, a random ID will be generated.

        :default: An 8-character pseudo-random string
        '''
        result = self._values.get("basti_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastiAccessSecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="basti-cdk.BastiInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "basti_id": "bastiId",
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "vpc_subnets": "vpcSubnets",
    },
)
class BastiInstanceProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        basti_id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The properties for the Basti instance.

        :param vpc: The VPC to deploy the bastion instance into.
        :param basti_id: (Optional) The ID of the Basti instance. The ID will be used to identify any resources created within this construct. If not specified, a random ID will be generated. Default: An 8-character pseudo-random string
        :param instance_type: (Optional) The instance type to use for the bastion instance. Default: t2.micro (subject to change)
        :param machine_image: (Optional) The machine image to use for the bastion instance. The specified machine image must have SSM agent installed and configured. If not specified, the latest Amazon Linux 2 - Kernel 5.10 AMI will be used. Default: Latest Amazon Linux 2 - Kernel 5.10
        :param vpc_subnets: (Optional) The subnet selection to deploy the bastion instance into. If not specified, any public subnet in the VPC will be used. Default: Public subnets in the VPC
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d790d9587a6020f94a791d6203069ecee283da08187ad5d31fa051a251fb8c17)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument basti_id", value=basti_id, expected_type=type_hints["basti_id"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if basti_id is not None:
            self._values["basti_id"] = basti_id
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC to deploy the bastion instance into.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def basti_id(self) -> typing.Optional[builtins.str]:
        '''(Optional) The ID of the Basti instance.

        The ID will be used to identify
        any resources created within this construct. If not specified, a random ID will be generated.

        :default: An 8-character pseudo-random string
        '''
        result = self._values.get("basti_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(Optional) The instance type to use for the bastion instance.

        :default: t2.micro (subject to change)
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def machine_image(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage]:
        '''(Optional) The machine image to use for the bastion instance.

        The specified machine image must have SSM agent installed and configured.
        If not specified, the latest  Amazon Linux 2 - Kernel 5.10 AMI will be used.

        :default: Latest Amazon Linux 2 - Kernel 5.10
        '''
        result = self._values.get("machine_image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(Optional) The subnet selection to deploy the bastion instance into.

        If not specified, any public subnet in the VPC will be used.

        :default: Public subnets in the VPC
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastiInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="basti-cdk.IBastiInstance")
class IBastiInstance(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="bastiId")
    def basti_id(self) -> builtins.str:
        '''The ID of the Basti instance.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''The bastion instance role.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''The bastion instance security group.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC the bastion instance is deployed into.'''
        ...


class _IBastiInstanceProxy:
    __jsii_type__: typing.ClassVar[str] = "basti-cdk.IBastiInstance"

    @builtins.property
    @jsii.member(jsii_name="bastiId")
    def basti_id(self) -> builtins.str:
        '''The ID of the Basti instance.'''
        return typing.cast(builtins.str, jsii.get(self, "bastiId"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''The bastion instance role.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''The bastion instance security group.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC the bastion instance is deployed into.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBastiInstance).__jsii_proxy_class__ = lambda : _IBastiInstanceProxy


@jsii.implements(IBastiInstance)
class BastiInstance(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="basti-cdk.BastiInstance",
):
    '''The Basti instance.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        basti_id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: The VPC to deploy the bastion instance into.
        :param basti_id: (Optional) The ID of the Basti instance. The ID will be used to identify any resources created within this construct. If not specified, a random ID will be generated. Default: An 8-character pseudo-random string
        :param instance_type: (Optional) The instance type to use for the bastion instance. Default: t2.micro (subject to change)
        :param machine_image: (Optional) The machine image to use for the bastion instance. The specified machine image must have SSM agent installed and configured. If not specified, the latest Amazon Linux 2 - Kernel 5.10 AMI will be used. Default: Latest Amazon Linux 2 - Kernel 5.10
        :param vpc_subnets: (Optional) The subnet selection to deploy the bastion instance into. If not specified, any public subnet in the VPC will be used. Default: Public subnets in the VPC
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4158f394054ae1209b1cd72557325674fee43baac5126ca6abae5e7e35b0c4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BastiInstanceProps(
            vpc=vpc,
            basti_id=basti_id,
            instance_type=instance_type,
            machine_image=machine_image,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromBastiId")
    @builtins.classmethod
    def from_basti_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        basti_id: builtins.str,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    ) -> IBastiInstance:
        '''Looks up an existing Basti instance from its ID.

        :param scope: CDK construct scope.
        :param id: CDK construct ID.
        :param basti_id: The ID of the Basti instance.
        :param vpc: The VPC that the bastion is deployed into.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae0feb86b982d3c8e869368ffcf99385131903782b5b5e3650e5b9879d098e34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument basti_id", value=basti_id, expected_type=type_hints["basti_id"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        return typing.cast(IBastiInstance, jsii.sinvoke(cls, "fromBastiId", [scope, id, basti_id, vpc]))

    @jsii.member(jsii_name="grantBastiCliConnect")
    def grant_basti_cli_connect(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> None:
        '''Grants an IAM principal permission to connect to the Basti instance via Basti CLI.

        :param grantee: The principal to grant permission to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f801a712fc6f5ade326c40f89b291d3c6c5b376f582c4a0877eea1a50117b9a5)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantBastiCliConnect", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="bastiId")
    def basti_id(self) -> builtins.str:
        '''The ID of the Basti instance.'''
        return typing.cast(builtins.str, jsii.get(self, "bastiId"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> _aws_cdk_aws_ec2_ceddda9d.Instance:
        '''The bastion instance.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Instance, jsii.get(self, "instance"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''The bastion instance role.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''The bastion instance security group.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC the bastion instance is deployed into.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))


__all__ = [
    "BastiAccessSecurityGroup",
    "BastiAccessSecurityGroupProps",
    "BastiInstance",
    "BastiInstanceProps",
    "IBastiInstance",
]

publication.publish()

def _typecheckingstub__01948589ed1a60919700df630bf7069a9d8c730904dc0053525f1ca445fc0678(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    basti_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d033d471ed35bb19d7d2268c0a4a86abc74b88e32fdb3c7330adb7ad118b4dd(
    basti_instance: IBastiInstance,
    port: _aws_cdk_aws_ec2_ceddda9d.Port,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80155f9d79726f26f5e96ec5e5bf13d3e3dc94dac96daf7a46bfc6f5da964648(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    basti_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d790d9587a6020f94a791d6203069ecee283da08187ad5d31fa051a251fb8c17(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    basti_id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4158f394054ae1209b1cd72557325674fee43baac5126ca6abae5e7e35b0c4b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    basti_id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0feb86b982d3c8e869368ffcf99385131903782b5b5e3650e5b9879d098e34(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    basti_id: builtins.str,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f801a712fc6f5ade326c40f89b291d3c6c5b376f582c4a0877eea1a50117b9a5(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass
