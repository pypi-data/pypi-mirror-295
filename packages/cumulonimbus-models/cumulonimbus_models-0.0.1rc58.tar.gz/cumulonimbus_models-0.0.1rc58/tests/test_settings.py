import os


def test_default_settings():
    from cumulonimbus_models.settings import MySettings
    settings = MySettings()
    assert settings.base_url is None


def test_modified_settings():
    os.environ['CUMULONIMBUS_MODELS_BASE_URL'] = 'TEST_URL'
    from cumulonimbus_models.settings import MySettings
    settings = MySettings()
    assert settings.base_url == 'TEST_URL'
