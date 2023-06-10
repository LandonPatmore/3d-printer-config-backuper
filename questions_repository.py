import textwrap

from questionnaire_generator import QuestionnaireGenerator
from static_view_generator import StaticViewGenerator

class QuestionsRepository :
  """
  Repository responsible for holding all information about the questions that
  will be asked to get setup.
  """

  def __init__(self) :
    self.github_username: str = ""
    self.github_password: str = ""
    self.github_email: str = ""
    self.repository_name: str = ""
    self.is_repository_private: bool = True
    self.printer_config_folder_path: str = ""
    self.auto_commit_schedule: str = ""
    self.questionnaire_generator = QuestionnaireGenerator()

    self.list_of_emails: list[str]|None = None

  def __set_github_username(self) :
    StaticViewGenerator.question_panel(
      description=textwrap.dedent(
        """
        This is the username you used to sign up for Github with.

        Click this link: https://github.com/settings/profile
        
        Look in the top left and you will see something like:
        
        John Smith (TheJohnSmith123)
        
        You want the "TheJohnSmith123" part.
        """
      )
    )

    self.github_username = self.questionnaire_generator.ask_question(
      question_type=0,
      validation_type=0,
      question="What is your github username?"
    )

  def __set_github_password(self) :
    StaticViewGenerator.question_panel(
      description=textwrap.dedent(
        """
        This is the password you used to sign up for Github with.

        NOTE: Your password is used by this script to generate a personal fine grained token. Once that 
        happens, it is then deleted.
        """
      )
    )

    self.github_password = self.questionnaire_generator.ask_question(
      question_type=1,
      validation_type=0,
      question="What is your github password?"
    )

  def __set_github_email(self, emails: list[str]) :
    # Make sure we grabbed their list of emails from the Github api first
    assert len(emails) != 0
    self.list_of_emails = emails

    StaticViewGenerator.question_panel(
      description=textwrap.dedent(
        """
        You will see a list of emails associated with your Github account. Use the arrow keys to select 
        which email you would like use for your local git instance.

        This email will be the one that is tied to your auto commits. This allows Github to recognize who is 
        making the commits and tags them appropriately.
        """
      )
    )

    self.github_email = self.questionnaire_generator.ask_question(
      question_type=3,
      validation_type=0,
      question="What is your github email?",
      choices_answer_type=0,
      choices=emails
    )

  def __set_repository_name(self) :
    StaticViewGenerator.question_panel(
      description=textwrap.dedent(
        """
        This will be the name of the repository your files will be stored in.

        You can either enter a name, or the default name will be:

        3d-printer-config-files
        """
      )
    )

    self.repository_name = self.questionnaire_generator.ask_question(
      question_type=0,
      validation_type=0,
      question="What would you like to name your repository?",
      default_value="3d-printer-config-files"
    )

  def __set_repository_visibility(self) :
    StaticViewGenerator.question_panel(
      description=textwrap.dedent(
        """
        This will be the visibility of your repository.

        This determines whether or not anyone on the internet can see your config files without you having to 
        explicitly share it with them.

        Private - Will only be visible to you and those you share it with
        Public - Will be visible to everyone on the internet
        """
      )
    )

    answer = self.questionnaire_generator.ask_question(
      question_type=3,
      validation_type=0,
      question="What type of visibility shall the repository have?",
      choices_answer_type=2,
      choices=["Public", "Private"]
    )

    self.is_repository_private = bool(answer)

  def __set_printer_config_folder_path(self) :
    StaticViewGenerator.question_panel(
      description=textwrap.dedent(
        """
        This will be the folder where your printer config files are located.

        For most instances if you haven't modified anything already, they should be located at:

        ~/printer_data/config
        """
      )
    )

    self.printer_config_folder_path = self.questionnaire_generator.ask_question(
      question_type=2,
      validation_type=1,
      question="Enter the path to your printer config folder. (Use tab to autocomplete the path)"
    )

  def __set_auto_commit_schedule(self) :
    StaticViewGenerator.question_panel(
      description=textwrap.dedent(
        """
        This will be the schedule your raspberry pi will use to automatically backup your printer config files.

        Click this link: https://crontab-generator.org/

        This will help you generate your crontab configuration.

        Once you are done generating your crontab configuration, you will see something like:

        * 7 1 * * <random words>

        You want the "* 7 1 * *" part.
        """
      )
    )

    self.auto_commit_schedule = self.questionnaire_generator.ask_question(
      question_type=0,
      validation_type=2,
      question="Enter your auto commit schedule"
    )

  def clear_password_answer(self) :
    """
    Clears the password answer since we do not need it once the personal token
    is generated.
    """

    self.github_password = ""

  def github_login_questions(self) :
    """
    The questions to get login info for Github.
    """

    self.__set_github_username()
    self.__set_github_password()

  def setup_questions(self, github_emails: list[str]) :
    """
    The questions to get info for setting up the backup of local files.

    :param github_emails: list of Github emails
    """

    self.__set_github_email(emails=github_emails)
    self.__set_repository_name()
    self.__set_repository_visibility()
    self.__set_printer_config_folder_path()
    self.__set_auto_commit_schedule()

  def ask_if_answers_are_correct(self) -> bool :
    """
    Asks if the answers input are correct or not.

    :return: were they correct or not
    """

    answer = self.questionnaire_generator.ask_question(
      question_type=4,
      validation_type=0,
      question=textwrap.dedent(
        """Is all entered info correct? 
        
        We are not showing Github username/password since to get to this point, those steps had to be 
        correct and cannot be changed now.
        
        Github email: {github_email}
        Repo name: {repo_name}
        Is repository private?: {repo_vis}
        Printer config path: {config_path}
        Auto commit schedule: {schedule}
        """.format(
          github_email=self.github_email,
          repo_name=self.repository_name,
          repo_vis=self.is_repository_private,
          config_path=self.printer_config_folder_path,
          schedule=self.auto_commit_schedule
        )
      )
    )

    return bool(answer)

  def select_incorrect_answer(self) -> int :
    """
    Asks which answer is incorrect.

    :return: index of the incorrect answer
    """

    index = self.questionnaire_generator.ask_question(
      question_type=3,
      validation_type=0,
      question="Which step is incorrect?",
      choices_answer_type=1,
      choices=[
        "Github email",
        "Repository name",
        "Is repository private?",
        "Printer config path",
        "Auto commit schedule"
      ]
    )

    return int(index)

  def ask_question_again(self, index: int) :
    """
    Asks a question again.

    :param index: index of the question that should be asked again
    """

    match index :
      case 0 :
        self.__set_github_email(emails=self.list_of_emails)
      case 1 :
        self.__set_repository_name()
      case 2 :
        self.__set_repository_visibility()
      case 3 :
        self.__set_printer_config_folder_path()
      case 4 :
        self.__set_auto_commit_schedule()
      case _ :
        raise ValueError(f'{index} is not a valid index of a question')
