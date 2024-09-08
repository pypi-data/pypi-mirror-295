from typing import Optional
from pydantic import ConfigDict, Field, BaseModel


class Credentials(BaseModel):
    email: str = Field(
        ...,
        description="Login email",
        alias="MLX_USERNAME",
    )

    @property
    def username(self):
        return self.email

    @username.setter
    def username(self, value):
        self.email = value

    password: str = Field(
        ...,
        description="Login password",
        alias="MLX_PASSWORD",
    )
    refresh_token: Optional[str] = Field(
        None,
        description="Refresh token retrieved by API",
        alias="MLX_REFRESH_TOKEN",
    )
    token: Optional[str] = Field(None, description="Auth token", alias="MLX_TOKEN")
    workspace_id: Optional[str] = Field(
        None,
        description="workspace id assigned to the user",
        alias="MLX_WORKSPACE_ID",
    )

    model_config = ConfigDict(populate_by_name=True)
