import sys
from abc import ABC
from datetime import timedelta
from github import Github, GithubException
from github_fine_grained_token_client import (
  BlockingPromptTwoFactorOtpProvider,
  GithubCredentials,
  AccountPermission,
  PermissionValue,
  RepositoryPermission,
  async_client, 
  UsernameError, 
  PasswordError, 
  LoginError, 
  AllRepositories,
  TwoFactorAuthenticationError
)

class GithubTokenResult(ABC) :
  pass

class SuccessfulToken(GithubTokenResult) :
  def __init__(self, token) :
    self.token = token

  def __str__(self):
    return self.token

class FailedToken(GithubTokenResult) :
  def __init__(self, reason: str, can_retry: bool) :
    self.reason = reason
    self.can_retry = can_retry

  def __str__(self) :
    return f'{self.reason} | {self.can_retry}'

class GithubArbiter :
  """
  Deals with anything related to talking to Github.
  """

  def __init__(self) :
    # I do not like this, but I don't know of another way to get the value out
    # of asyncio.run()
    self.token_result: GithubTokenResult|None = None
    self.github: Github|None = Github(login_or_token="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")
    self.name: str = ""

  async def retrieve_token(self, username: str, password: str, version: str) :
    """
    Retrieves the token from Github to be used for talking to Github's API.

    :param username: the Github username
    :param password: the Github account's password
    :param version: the version of the script
    """

    async with async_client(
        credentials=GithubCredentials(username=username, password=password),
        two_factor_otp_provider=BlockingPromptTwoFactorOtpProvider(),
    ) as session :
      try :
        fine_grained_token = await session.create_token(
          name=f'3dbakup (v{version}) script token',
          expires=timedelta(days=7),
          description="Token used to setup automatic backups of 3d printer config files.",
          scope=AllRepositories(),
          permissions={
            AccountPermission.KEYS :              PermissionValue.WRITE,
            AccountPermission.EMAILS :            PermissionValue.READ,
            RepositoryPermission.ADMINISTRATION : PermissionValue.WRITE,
            RepositoryPermission.METADATA :       PermissionValue.READ,
          }
        )

        self.github = Github(login_or_token=fine_grained_token)
        self.set_name()
        self.token_result = SuccessfulToken(token=fine_grained_token)
      except BaseException as e :
        self.token_result = self.handle_token_exceptions(exception=e)

  @staticmethod
  def handle_token_exceptions(exception) -> GithubTokenResult :
    """
    Returns a FailedToken instance and determines if the exception that was
    thrown is recoverable or not.

    :param exception: the exception that was returned by the token retrieval
    function.
    :return: FailedToken and if it is retryable
    """

    if isinstance(
        exception, (
            LoginError, UsernameError, PasswordError,
            TwoFactorAuthenticationError)
    ) :
      return FailedToken(reason=str(exception), can_retry=True)
    else :
      return FailedToken(reason=str(exception), can_retry=False)

  @staticmethod
  def github_failure(exception) :
    """
    If we get here, the script will exit with the exception.

    :param exception: exception that was thrown
    :return:
    """
    sys.exit(f'Error: {exception}')

  def get_emails(self) -> list[str] :
    """
    Retrieves the emails associated with the Github account.

    :return: list of emails
    """

    try :
      email_data = self.github.get_user().get_emails()
      return list(map(lambda git : git.email, email_data))
    except GithubException as e :
      self.github_failure(e)

  # We save the name since it is not associated with a step, thus this is the next best place
  def set_name(self) :
    """
    Retrieves the name associated with the Github account.

    We save the name since it is not associated with a step, thus this is the
    next best place
    """

    try :
      self.name = self.github.get_user().name
    except GithubException as e :
      self.github_failure(e)
