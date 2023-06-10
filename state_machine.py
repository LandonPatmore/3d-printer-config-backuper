import asyncio
from abc import ABC
import questionary
from github_arbiter import GithubArbiter
from github_arbiter import SuccessfulToken
from info_reader import InfoReader
from questions_repository import QuestionsRepository
from setup import SetupArbiter
from static_view_generator import StaticViewGenerator

class ScriptState(ABC) :
  pass

class LoadData(ScriptState) :
  pass

class Intro(ScriptState) :
  pass

class GetGithubLoginInfo(ScriptState) :
  pass

class GetQuestionAnswers(ScriptState) :
  def __init__(self, emails: list[str]) :
    self.emails = emails

class CheckAnswers(ScriptState) :
  pass

class SelectIncorrectAnswer(ScriptState) :
  pass

class EditAnswer(ScriptState) :
  def __init__(self, index: int) :
    self.index = index

class ExecuteSetup(ScriptState) :
  pass

class Finished(ScriptState) :
  pass

class StateMachine :
  """
  The main loop of the script.
  """

  def __init__(self) :
    self.current_state: ScriptState = ExecuteSetup()
    self.info_reader = InfoReader()
    self.github_arbiter = GithubArbiter()
    self.static_view_generator = StaticViewGenerator()
    self.questions = QuestionsRepository()
    self.setup = SetupArbiter(github_arbiter=self.github_arbiter)

  def run(self) :
    """
    Runs the state machine to walk the user through the script.
    """

    while True :
      match self.current_state :
        case LoadData() :
          self.__load_data()
        case Intro() :
          self.__intro()
        case GetGithubLoginInfo() :
          self.__generate_fine_grained_token()
        case GetQuestionAnswers() :
          self.__get_question_answers(emails=self.current_state.emails)
        case CheckAnswers() :
          self.__check_answers()
        case SelectIncorrectAnswer() :
          self.__select_incorrect_answer()
        case EditAnswer() :
          self.__edit_answer(index=self.current_state.step_number)
        case ExecuteSetup() :
          self.__execute_setup()
        case Finished() :
          self.__finished()
          break

  def __load_data(self) :
    """
    Loads data that must be there before the script can be run.
    """

    self.info_reader.read(file_name="info.yaml")

    self.current_state = Intro()

  def __intro(self) :
    """
    Shows the intro for the user to select whether they would like to
    run the script or exit.
    """

    self.static_view_generator.info_panel(info_reader=self.info_reader)

    cont = questionary.confirm("Would you like to continue?").ask()
    if cont :
      self.current_state = GetGithubLoginInfo()
    else :
      self.current_state = Finished()

  def __generate_fine_grained_token(self) :
    """
    Retrieves the required Github info (username and password) and then
    calls out to Github to generate a fine-grained token that the rest
    of the script will use to interact with Github's APIs.
    """

    while True :
      self.questions.github_login_questions()

      asyncio.run(
        self.github_arbiter.retrieve_token(
          username=self.questions.github_username,
          password=self.questions.github_password,
          version=self.info_reader.version
        )
      )

      self.questions.clear_password_answer()

      if isinstance(
          self.github_arbiter.token_result,
          SuccessfulToken
      ) :
        emails = self.github_arbiter.get_emails()

        self.current_state = GetQuestionAnswers(emails=emails)
        break
      else :
        print(f'Error: {self.github_arbiter.token_result.reason}')

        if not self.github_arbiter.token_result.can_retry :
          exit(0)

  def __get_question_answers(self, emails: list[str]) :
    """
    Asks the user questions needed to properly set up backing up their
    printer files.

    :param emails: list of emails we get back from Github so the user of the
    script can select one they would prefer to be associated with their
    printer config local repo
    """

    self.questions.setup_questions(github_emails=emails)
    self.current_state = CheckAnswers()

  def __check_answers(self) :
    """
    Asks the user if their answers they answered previously are correct. If
    they are, then the script will execute the setup. Otherwise, it will
    bring them to select which answer was incorrect.
    """

    input_correct = self.questions.ask_if_answers_are_correct()

    if input_correct :
      self.current_state = ExecuteSetup()
    else :
      self.current_state = SelectIncorrectAnswer()

  def __select_incorrect_answer(self) :
    """
    Asks the user to select the incorrect answer that they would like tom
    modify.
    """

    step_number = self.questions.select_incorrect_answer()

    self.current_state = EditAnswer(index=step_number)

  def __edit_answer(self, index: int) :
    """
    Asks the user the question they selected that was incorrect once again.

    :param index: the index of the question that was requested to be edited
    """

    self.questions.ask_question_again(index=index)

    self.current_state = CheckAnswers()

  def __execute_setup(self) :
    """
    Executes the setup of the backup of the user's printer config files.
    """

    print("Execute setup")

    # self.setup.run(
    #   name=self.github_arbiter.name,
    #   email=self.questions.github_email,
    #   repository_name=self.questions.repository_name,
    #   repository_visibility=self.questions.is_repository_private,
    #   printer_config_path=self.questions.printer_config_folder_path,
    #   auto_commit_schedule=self.questions.auto_commit_schedule
    # )

    self.setup.run(
      name="Landon Patmore",
      email="landon.patmore@gmail.com",
      repository_name="test_printer_repo3",
      repository_visibility=False,
      printer_config_path="/home/dietpi/test_dir",
      auto_commit_schedule="* * */6 * *"
    )
    self.current_state = Finished()

  @staticmethod
  def __finished() :
    print("Finished")
