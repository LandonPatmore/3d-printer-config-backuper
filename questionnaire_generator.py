import os
import questionary
from cron_validator import CronValidator
from questionary import Choice
from typing import Callable

class QuestionnaireGenerator :
  """
  Helper class to generate question prompts properly.
  """

  def __init__(self) :
    self.cron_validator: CronValidator = CronValidator()

  @staticmethod
  def __text_validation(string_to_validate: str) :
    return len(str.strip(string_to_validate)) != 0

  @staticmethod
  def __path_validation(string_to_validate: str) :
    sanitized_path = string_to_validate.replace("~", os.path.expanduser("~"))
    return os.path.isdir(sanitized_path)

  def __cron_validation(self, string_to_validate: str) :
    try :
      return self.cron_validator.parse(string_to_validate) is not None
    except ValueError :
      return False

  def __determine_validation(self, validation_type: int) -> Callable :
    """
    Determines the proper validation method to use when asking a question.
    
    :param validation_type: the type of validation
    :return: the function to use
    """
    match validation_type :
      case 0 :
        return self.__text_validation
      case 1 :
        return self.__path_validation
      case 2 :
        return self.__cron_validation
      case _ :
        raise ValueError(f'{validation_type} is not a valid validation type')

  def ask_question(
      self,
      question_type: int,
      validation_type: int,
      question: str,
      default_value: str = "",
      choices_answer_type: int = 0,
      choices: list[str] = None
  ) -> str :
    """
    Asks the question with the proper prompt based on passed in data.

    :param question_type: the type of question
    :param validation_type: the type of validation
    :param question: the actual question
    :param default_value: default value if there is one
    :param choices_answer_type: the type of choices answer return type
    :param choices: the list of choices if there are any
    :return: answer as a string
    """

    validation_strategy = self.__determine_validation(
      validation_type=validation_type
    )

    match question_type :
      case 0 :
        return questionary.text(
          message=question,
          default=default_value,
          validate=validation_strategy
        ).ask()
      case 1 :
        return questionary.password(
          message=question,
          validate=validation_strategy
        ).ask()
      case 2 :
        path = questionary.path(
          message=question,
          validate=validation_strategy
        ).ask()

        return path.replace("~", os.path.expanduser("~"))
      case 3 :
        if choices_answer_type == 0 :
          choices = choices
        elif choices_answer_type == 1 :
          choices = list(
            map(
              lambda choice : Choice(title=choice[1], value=choice[0]),
              enumerate(choices)
            )
          )
        elif choices_answer_type == 2 :
          choices = list(
            map(
              lambda choice : Choice(title=choice[1], value=bool(choice[0])),
              enumerate(choices)
            )
          )
        else :
          raise ValueError(
            f'{choices_answer_type} is not a valid choices answer type'
          )

        return questionary.select(
          message=question,
          choices=choices
        ).ask()
      case 4 :
        return questionary.confirm(message=question).ask()
      case _ :
        raise ValueError(f'{question_type} is not a valid question type')
