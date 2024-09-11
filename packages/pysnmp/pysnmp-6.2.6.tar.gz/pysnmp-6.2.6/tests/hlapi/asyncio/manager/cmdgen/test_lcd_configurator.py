from unittest import mock

from pysnmp.hlapi.asyncio import *
from pysnmp.hlapi.asyncio.lcd import CommandGeneratorLcdConfigurator


@mock.patch("pysnmp.entity.config.addV3User")
@mock.patch("pysnmp.entity.config.delV3User")
def test_usm_auth_cache_cleared(delV3User, addV3User):
    """
    Ensure auth cache is cleared when auth data is changed.
    """
    snmpEngine = SnmpEngine()
    transportTarget = UdpTransportTarget(("198.51.100.1", 161))

    authDataValues = {
        "userName": "username",
        "authKey": "authkey1",
        "authProtocol": usmHMACMD5AuthProtocol,
        "privKey": "privkey1",
        "privProtocol": usmAesCfb128Protocol,
    }

    lcd = CommandGeneratorLcdConfigurator()
    initialAuthData = UsmUserData(**authDataValues)
    lcd.configure(snmpEngine, initialAuthData, transportTarget)
    addV3User.assert_called_with(
        snmpEngine,
        initialAuthData.userName,
        initialAuthData.authProtocol,
        initialAuthData.authKey,
        initialAuthData.privProtocol,
        initialAuthData.privKey,
        securityEngineId=initialAuthData.securityEngineId,
        securityName=initialAuthData.securityName,
        authKeyType=initialAuthData.authKeyType,
        privKeyType=initialAuthData.privKeyType,
    )

    # Ensure we do not add/delete if nothing changes
    addV3User.reset_mock()
    lcd.configure(snmpEngine, initialAuthData, transportTarget)
    addV3User.assert_not_called()
    delV3User.assert_not_called()

    changeAuthValues = {
        "authKey": "authKey2",
        "privProtocol": usmDESPrivProtocol,
        "authProtocol": usmHMACSHAAuthProtocol,
        "privKey": "privKey2",
    }

    for field, value in changeAuthValues.items():
        addV3User.reset_mock()
        delV3User.reset_mock()

        authDataValues[field] = value
        authData = UsmUserData(**authDataValues)
        lcd.configure(snmpEngine, authData, transportTarget)

        delV3User.assert_called_with(
            snmpEngine,
            authData.userName,
            authData.securityEngineId,
        )

        addV3User.assert_called_with(
            snmpEngine,
            authData.userName,
            authData.authProtocol,
            authData.authKey,
            authData.privProtocol,
            authData.privKey,
            securityEngineId=authData.securityEngineId,
            securityName=authData.securityName,
            authKeyType=authData.authKeyType,
            privKeyType=authData.privKeyType,
        )
