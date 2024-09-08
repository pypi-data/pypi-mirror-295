from pydantic import SecretStr as SecretStr


class PartialSecretStr(SecretStr):
    """
    Allow obfuscating only portions of the string rather than wholly
    """

    def _secret_display(self, value: str) -> str:
        pass
        # return _secret_display(self._secret_value)


# if __name__ == "__main__":
#     print(PartialSecretStr("password123"))
