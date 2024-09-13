r'''
This CDK construct creates an [AWS Codebuild](https://www.sonarsource.com/products/sonarcloud/) action to perform static code analysis using [Sonarcloud](https://www.sonarsource.com/products/sonarcloud/).

# Getting started

Here is how to include the construct in your CDK code :

```javascript
const sonarcloudScan = new CDKCodeBuildSonarcloud(this, 'SonarcloudBuildAction', {
      sourceOutput: sourceOutput,
      sonarOrganizationName: 'my-sonarcloud-organization-name',
      sonarProjectName: 'my-sonarcloud-project-name',
});
```

Check [Here](/examples/codepipeline-example.ts) for an example on how to use the construct.

# Security

A Sonarcloud account is required to use this construct. Create a Sonarcloud [token](https://docs.sonarsource.com/sonarcloud/advanced-setup/user-accounts/#user-tokens) to connect securely to Sonarcloud from AWS CodeBuild. Store this token in your AWS account in AWS Secret Manager, name the secret "sonar-token" and use "SONAR_TOKEN" as the secret key.

Please review the [AWS Secret Manager security best practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/secure-sensitive-data-secrets-manager-terraform/best-practices.html) in order to securely create and manage your secret.
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

import aws_cdk.aws_codepipeline as _aws_cdk_aws_codepipeline_ceddda9d
import aws_cdk.aws_codepipeline_actions as _aws_cdk_aws_codepipeline_actions_ceddda9d
import constructs as _constructs_77d1e7e8


class CDKCodeBuildSonarcloud(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-codebuild-sonarcloud.CDKCodeBuildSonarcloud",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        sonar_organization_name: builtins.str,
        sonar_project_name: builtins.str,
        source_output: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param sonar_organization_name: 
        :param sonar_project_name: 
        :param source_output: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed53f02decaf21a9ec63b477498e75f944692fd6f67be22c5d3d639f6785b0b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CDKCodeBuildSonarcloudProps(
            sonar_organization_name=sonar_organization_name,
            sonar_project_name=sonar_project_name,
            source_output=source_output,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="buildAction")
    def build_action(
        self,
    ) -> _aws_cdk_aws_codepipeline_actions_ceddda9d.CodeBuildAction:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_codepipeline_actions_ceddda9d.CodeBuildAction, jsii.get(self, "buildAction"))


@jsii.data_type(
    jsii_type="cdk-codebuild-sonarcloud.CDKCodeBuildSonarcloudProps",
    jsii_struct_bases=[],
    name_mapping={
        "sonar_organization_name": "sonarOrganizationName",
        "sonar_project_name": "sonarProjectName",
        "source_output": "sourceOutput",
    },
)
class CDKCodeBuildSonarcloudProps:
    def __init__(
        self,
        *,
        sonar_organization_name: builtins.str,
        sonar_project_name: builtins.str,
        source_output: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
    ) -> None:
        '''
        :param sonar_organization_name: 
        :param sonar_project_name: 
        :param source_output: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eac6c9a1b503ce3846c4dcaa4e478651733fe6a8aaf69c24732c71099b573e1)
            check_type(argname="argument sonar_organization_name", value=sonar_organization_name, expected_type=type_hints["sonar_organization_name"])
            check_type(argname="argument sonar_project_name", value=sonar_project_name, expected_type=type_hints["sonar_project_name"])
            check_type(argname="argument source_output", value=source_output, expected_type=type_hints["source_output"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sonar_organization_name": sonar_organization_name,
            "sonar_project_name": sonar_project_name,
            "source_output": source_output,
        }

    @builtins.property
    def sonar_organization_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("sonar_organization_name")
        assert result is not None, "Required property 'sonar_organization_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sonar_project_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("sonar_project_name")
        assert result is not None, "Required property 'sonar_project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_output(self) -> _aws_cdk_aws_codepipeline_ceddda9d.Artifact:
        '''
        :stability: experimental
        '''
        result = self._values.get("source_output")
        assert result is not None, "Required property 'source_output' is missing"
        return typing.cast(_aws_cdk_aws_codepipeline_ceddda9d.Artifact, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CDKCodeBuildSonarcloudProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CDKCodeBuildSonarcloud",
    "CDKCodeBuildSonarcloudProps",
]

publication.publish()

def _typecheckingstub__ed53f02decaf21a9ec63b477498e75f944692fd6f67be22c5d3d639f6785b0b0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    sonar_organization_name: builtins.str,
    sonar_project_name: builtins.str,
    source_output: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eac6c9a1b503ce3846c4dcaa4e478651733fe6a8aaf69c24732c71099b573e1(
    *,
    sonar_organization_name: builtins.str,
    sonar_project_name: builtins.str,
    source_output: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
) -> None:
    """Type checking stubs"""
    pass
