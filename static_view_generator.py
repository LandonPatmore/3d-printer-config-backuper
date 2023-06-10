import os
import textwrap
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from info_reader import InfoReader

class StaticViewGenerator :
  """
  Generates static views to show to the user.
  """

  @staticmethod
  def cls() :
    """
    Clears the screen.
    """

    os.system('cls' if os.name == 'nt' else 'clear')

  @staticmethod
  def info_panel(info_reader: InfoReader) :
    """
    Displays an overall info view.

    :param info_reader: the info reader object to get data out of
    """

    StaticViewGenerator.cls()

    info = Text(
      text=textwrap.dedent(
        """
        Author: {author}
        Repo: {repo}
        License: {license}
        """.format(
          author=info_reader.author,
          repo=info_reader.repo,
          license=info_reader.license
        )
      ),
      justify="center"
    )

    panel = Panel(
      title=f'{info_reader.title} (v{info_reader.version})',
      renderable=Group(
        Text(text=info_reader.description, justify="center"),
        Text(text=f'NOTICE: {info_reader.notice}', justify="center"),
        Text(""),
        info
      ),
    )

    rprint(panel)

  @staticmethod
  def question_panel(description: str) :
    """
    Displays a question view.

    :param description: question description
    """

    StaticViewGenerator.cls()

    panel = Panel(
      title="Question description",
      renderable=Text(text=description, justify="center")
    )

    rprint(panel)
