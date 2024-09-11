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

from .._jsii import *

import aws_cdk.aws_efs as _aws_cdk_aws_efs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d


@jsii.data_type(
    jsii_type="shady-island.configuration.AddDirectoryOptions",
    jsii_struct_bases=[],
    name_mapping={"group": "group", "mode": "mode", "owner": "owner"},
)
class AddDirectoryOptions:
    def __init__(
        self,
        *,
        group: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for the ``ShellCommands.addDirectory`` method.

        :param group: The group name or numeric group ID to assign as the directory group.
        :param mode: The file mode, e.g. 2755, 0400.
        :param owner: The username or numeric user ID to assign as the directory owner.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0994962f0188c33e863c7c3d2a2d000cbf1c469ca2de6b605f8250f4a7331f5)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group is not None:
            self._values["group"] = group
        if mode is not None:
            self._values["mode"] = mode
        if owner is not None:
            self._values["owner"] = owner

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''The group name or numeric group ID to assign as the directory group.'''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The file mode, e.g. 2755, 0400.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''The username or numeric user ID to assign as the directory owner.'''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddDirectoryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="shady-island.configuration.OutputFileOptions",
    jsii_struct_bases=[],
    name_mapping={"delimiter": "delimiter", "substitution": "substitution"},
)
class OutputFileOptions:
    def __init__(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        substitution: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options for the ``ShellCommands.outputFile`` method.

        :param delimiter: The bash heredoc delimiter. Default: - END_OF_FILE
        :param substitution: Use ``true`` to enable variable and command substitution inside the heredoc. Default: - disabled
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20657a054da386482746d6fa830e9dd3576a6d27d93d9c78a3c3ecae5282748d)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument substitution", value=substitution, expected_type=type_hints["substitution"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if substitution is not None:
            self._values["substitution"] = substitution

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''The bash heredoc delimiter.

        :default: - END_OF_FILE
        '''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def substitution(self) -> typing.Optional[builtins.bool]:
        '''Use ``true`` to enable variable and command substitution inside the heredoc.

        :default: - disabled
        '''
        result = self._values.get("substitution")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OutputFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ShellCommands(
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.configuration.ShellCommands",
):
    '''A utility class that provides POSIX shell commands for User Data scripts.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addDirectory")
    @builtins.classmethod
    def add_directory(
        cls,
        name: builtins.str,
        *,
        group: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
    ) -> typing.List[builtins.str]:
        '''Uses either ``mkdir`` or ``install`` to create a directory.

        :param name: - The name of the directory to create.
        :param group: The group name or numeric group ID to assign as the directory group.
        :param mode: The file mode, e.g. 2755, 0400.
        :param owner: The username or numeric user ID to assign as the directory owner.

        :return: The shell commands.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e1521624de9cd4f04bc5aa6550677f7d918b1ba4a09f54c46aaecd55b902b7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = AddDirectoryOptions(group=group, mode=mode, owner=owner)

        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "addDirectory", [name, options]))

    @jsii.member(jsii_name="changeOwnership")
    @builtins.classmethod
    def change_ownership(
        cls,
        filename: builtins.str,
        uid: typing.Optional[builtins.str] = None,
        gid: typing.Optional[builtins.str] = None,
    ) -> typing.List[builtins.str]:
        '''Gets a command to change the ownership and/or group membership of a file.

        If both ``uid`` and ``gid`` are provided, this method returns a single
        ``chown`` command to set both values. If just ``uid`` is provided, this method
        returns a single ``chown`` command that sets the owner. If just ``gid`` is
        provided, this method returns a single ``chgrp`` command. If neither are
        provided, this method returns an empty array.

        :param filename: - The local filesystem path to the file or directory.
        :param uid: - Optional. The owner username or uid.
        :param gid: - Optional. The group name or gid.

        :return: The shell commands.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16814cfa23b6c9675dbf36b44def93bb361e99ae2f96a53635ec8bbbd5636bd0)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
            check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "changeOwnership", [filename, uid, gid]))

    @jsii.member(jsii_name="disableUnattendedUpgrades")
    @builtins.classmethod
    def disable_unattended_upgrades(cls) -> typing.List[builtins.str]:
        '''Gets a command to disable unattended package upgrades on Debian/Ubuntu.

        :return: The shell commands.
        '''
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "disableUnattendedUpgrades", []))

    @jsii.member(jsii_name="downloadSecret")
    @builtins.classmethod
    def download_secret(
        cls,
        secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        destination: builtins.str,
    ) -> typing.List[builtins.str]:
        '''Gets the command to download a Secrets Manager secret to the filesystem.

        Be sure to grant your autoscaling group or EC2 instance read access.

        :param secret: - The secret to download.
        :param destination: - The local filesystem path where the secret is stored.

        :return: The shell commands.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__326012a0bf58f709bc56dc6438ccb9490964767013b0d3c93d9cb4cc375eb27f)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "downloadSecret", [secret, destination]))

    @jsii.member(jsii_name="mountElasticFileSystem")
    @builtins.classmethod
    def mount_elastic_file_system(
        cls,
        filesystem: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
        destination: builtins.str,
    ) -> typing.List[builtins.str]:
        '''Gets the command to mount an EFS filesystem to a destination path.

        Be sure to grant your autoscaling group or EC2 instance network access.

        :param filesystem: - The EFS filesystem.
        :param destination: - The local filesystem path for the mount point.

        :return: The shell commands.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__587d6ed009cf11ba74cd134ee0e93a285b966d1809d7fa317ad1d96e93091a03)
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "mountElasticFileSystem", [filesystem, destination]))

    @jsii.member(jsii_name="outputFile")
    @builtins.classmethod
    def output_file(
        cls,
        contents: builtins.str,
        destination: builtins.str,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        substitution: typing.Optional[builtins.bool] = None,
    ) -> typing.List[builtins.str]:
        '''Writes the literal contents of a string to a destination file.

        :param contents: - The file contents.
        :param destination: - The filename to output.
        :param delimiter: The bash heredoc delimiter. Default: - END_OF_FILE
        :param substitution: Use ``true`` to enable variable and command substitution inside the heredoc. Default: - disabled

        :return: The shell commands.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223cbfb5bcff2bb626b3dd2641d391ed7ca2e762e770d1499154a22b3ea5ccca)
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        options = OutputFileOptions(delimiter=delimiter, substitution=substitution)

        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "outputFile", [contents, destination, options]))

    @jsii.member(jsii_name="syncFromBucket")
    @builtins.classmethod
    def sync_from_bucket(
        cls,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        destinations: typing.Mapping[builtins.str, builtins.str],
    ) -> typing.List[builtins.str]:
        '''Gets commands to synchronize objects from an S3 bucket to the filesystem.

        e.g. ``syncFromBucket(bucket, {"nginx-config": "/etc/nginx"})``.

        Be sure to grant your autoscaling group or EC2 instance read access.

        :param bucket: - The source bucket.
        :param destinations: - Record with S3 object keys to filesystem path values.

        :return: The shell commands.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374e266416cc5b0f352fd2dbd94b207a658f7585956ae915ae7dc9eaa04eca4d)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "syncFromBucket", [bucket, destinations]))


__all__ = [
    "AddDirectoryOptions",
    "OutputFileOptions",
    "ShellCommands",
]

publication.publish()

def _typecheckingstub__b0994962f0188c33e863c7c3d2a2d000cbf1c469ca2de6b605f8250f4a7331f5(
    *,
    group: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20657a054da386482746d6fa830e9dd3576a6d27d93d9c78a3c3ecae5282748d(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    substitution: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e1521624de9cd4f04bc5aa6550677f7d918b1ba4a09f54c46aaecd55b902b7(
    name: builtins.str,
    *,
    group: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16814cfa23b6c9675dbf36b44def93bb361e99ae2f96a53635ec8bbbd5636bd0(
    filename: builtins.str,
    uid: typing.Optional[builtins.str] = None,
    gid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__326012a0bf58f709bc56dc6438ccb9490964767013b0d3c93d9cb4cc375eb27f(
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587d6ed009cf11ba74cd134ee0e93a285b966d1809d7fa317ad1d96e93091a03(
    filesystem: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223cbfb5bcff2bb626b3dd2641d391ed7ca2e762e770d1499154a22b3ea5ccca(
    contents: builtins.str,
    destination: builtins.str,
    *,
    delimiter: typing.Optional[builtins.str] = None,
    substitution: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374e266416cc5b0f352fd2dbd94b207a658f7585956ae915ae7dc9eaa04eca4d(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    destinations: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass
