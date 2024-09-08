from cumulonimbus_models.system import SoftwareInstallationMethods


def test_system():
    from cumulonimbus_models.system import Software, SystemInfo, SystemUpdateRequest

    assert SystemUpdateRequest(
        system_info=SystemInfo(
            os='test',
            hostname='test',
            software=[
                Software(
                    name='test',
                    version='test',
                    installation_method=SoftwareInstallationMethods.PIP,
                    installation_data={'test': 'test'},
                    config_data={'test': 'test'}
                )
            ]
        )
    )