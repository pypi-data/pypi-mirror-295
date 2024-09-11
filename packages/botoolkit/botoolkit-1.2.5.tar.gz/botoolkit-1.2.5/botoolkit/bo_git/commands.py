from argparse import (
    Namespace,
)
from distutils.util import (
    strtobool,
)
from pathlib import (
    Path,
)
from typing import (
    List,
    Optional,
    Tuple,
)

from git import (
    GitCommandError,
    Reference,
    RemoteReference,
    Repo,
)
from jira import (
    JIRAError,
)

from botoolkit.bo_git.mixins import (
    WebBBBranchesArgumentsMixin,
)
from botoolkit.bo_git.settings import (
    TOOL_NAME as BOGIT_TOOL_NAME,
)
from botoolkit.bo_jira.api import (
    JiraAPIClient,
)
from botoolkit.bo_jira.enums import (
    JiraIssueStatusEnum,
)
from botoolkit.bo_jira.mixins import (
    JiraArgumentsMixin,
)
from botoolkit.bo_jira.settings import (
    TOOL_NAME as BOJIRA_TOOL_NAME,
)
from botoolkit.bo_toolkit.settings import (
    TOOL_NAME as BOTOOLKIT_TOOL_NAME,
)
from botoolkit.core.commands import (
    BOConfiguredToolConfigureCommand,
    BOConfiguredToolLister,
)
from botoolkit.core.consts import (
    ALLOWED_ALL_EMPTY_CONFIG_PARAMETERS,
)
from botoolkit.core.helpers import (
    findfirst,
)
from botoolkit.core.loggers import (
    logger,
)


class ConfigureBOWebBBCommand(
    WebBBBranchesArgumentsMixin,
    BOConfiguredToolConfigureCommand,
):
    """
    Команда конфигурирования инструмента bowebbb
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        self.description = (
            'Configure bogit for working with Git repositories of projects.'
        )

    def get_tool_name(self):
        return BOGIT_TOOL_NAME

    def get_allowed_empty_config_parameters(self):
        return ALLOWED_ALL_EMPTY_CONFIG_PARAMETERS

    def get_required_config_tool_names(self):
        required_config_tool_names = super().get_required_config_tool_names()

        required_config_tool_names.append(BOTOOLKIT_TOOL_NAME)

        return required_config_tool_names


class ShowRemoteBranchesCommand(
    BOConfiguredToolLister,
):
    """
    Команда вывода списка всех существующих веток проекта
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.description = (
            """Команда проверки наличия веток уже закрытых задач в Jira с возможностью их удаления из удаленного 
            репозитория.
            """
        )

        self._repository: Optional[Repo] = None
        self._branches: List[Reference] = []

    def get_required_config_tool_names(self):
        required_config_tool_names = super().get_required_config_tool_names()

        required_config_tool_names.extend(
            (
                BOTOOLKIT_TOOL_NAME,
            )
        )

        return required_config_tool_names

    def get_parser(
        self,
        prog_name,
    ):
        """
        Подготовка дополнительных параметров
        """
        parser = super().get_parser(
            prog_name=prog_name,
        )

        parser.add_argument(
            '--project_path',
            action='store',
            type=str,
            help='Абсолютный путь до директории проекта.',
        )

        return parser

    def _prepare_result(self):
        """
        Подготовка результата для вывода в виде таблицы
        """
        columns = (
            'Index',
            'Branch',
        )

        rows = (
            (
                index,
                branch.name,
            )
            for index, branch in enumerate(self._branches, start=1)
        )

        return columns, rows

    def _prepare_repository(self):
        """
        Инициализация git-репозитория
        """
        self._repository = Repo(
            path=self._parsed_args.project_path,
        )

        assert not self._repository.bare

    def _collect_branches(self):
        """
        Формирование списка веток в репозитории
        """
        self._branches = [branch for branch in self._repository.remote().refs]

    def take_action(
        self,
        parsed_args: Namespace,
    ):
        super().take_action(
            parsed_args=parsed_args,
        )

        self._prepare_repository()
        self._collect_branches()

        result = self._prepare_result()

        return result


class CheckClosedIssueRemoteBranchCommand(
    JiraArgumentsMixin,
    BOConfiguredToolLister,
):
    """
    Команда проверки наличия веток уже закрытых задач с возможностью их удаления из удаленного репозитория
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.description = (
            """Команда проверки наличия веток уже закрытых задач в Jira с возможностью их удаления из удаленного 
            репозитория.
            """
        )

        self._repository: Optional[Repo] = None
        self._issue_branches: List[Tuple[str, Reference]] = []

    def get_required_config_tool_names(self):
        required_config_tool_names = super().get_required_config_tool_names()

        required_config_tool_names.extend(
            (
                BOJIRA_TOOL_NAME,
                BOTOOLKIT_TOOL_NAME,
            )
        )

        return required_config_tool_names

    def get_parser(
        self,
        prog_name,
    ):
        """
        Подготовка дополнительных параметров
        """
        parser = super().get_parser(
            prog_name=prog_name,
        )

        parser.add_argument(
            '--projects',
            action='store',
            type=lambda p: list(map(lambda x: x.strip(), p.split(','))),
            help=(
                'Проекты в Jira. Например, BOBUH,BOZIK.'
            ),
        )

        parser.add_argument(
            '--project_path',
            action='store',
            type=str,
            help='Абсолютный путь до директории проекта или содержащей проекты.',
        )

        parser.add_argument(
            '--find_sub_dirs',
            dest='find_sub_dirs',
            action='store',
            default=False,
            type=lambda x: bool(strtobool(x)),
            help='Искать проекты в дочерних директориях.',
        )

        parser.add_argument(
            '--additional_jira_statuses',
            dest='additional_jira_statuses',
            action='store',
            default=[],
            type=lambda statuses: [s.strip() for s in statuses.strip().split(',')],
            help=(
                'Дополнительные статусы задачи в Jira, для задач в которых должны быть удалены ветки из удаленного '
                'репозитория. Перечисление производится через запятую без пробелов. Например, Приемка,Анализ'
            ),
        )

        parser.add_argument(
            '--remove',
            dest='remove',
            action='store',
            default=False,
            type=lambda x: bool(strtobool(x)),
            help='Удаление веток уже закрытых задач. По умолчанию: False.',
        )

        return parser

    def _prepare_result(self):
        """
        Подготовка результата для вывода в виде таблицы
        """
        columns = (
            'Index',
            'Jira issue',
            'Branch',
        )

        rows = (
            (
                index,
                jira_issue,
                branch.name,
            )
            for index, (jira_issue, branch) in enumerate(self._issue_branches, start=1)
        )

        return columns, rows

    def _prepare_repository(self, repository_path: Path):
        """
        Инициализация git-репозитория
        """
        self._repository = Repo(
            path=repository_path,
        )

        assert not self._repository.bare

    def _prepare_jira_client(self):
        """
        Подготовка клиента Jira
        """
        self._jira_client = JiraAPIClient(
            url=self._bojira_config['jira']['url'].value,
            username=self._bojira_config['jira']['username'].value,
            password=self._bojira_config['jira']['password'].value,
        )

    def _collect_closed_project_issue_branches(
        self,
        project: str,
        references: List[RemoteReference],
    ):
        """Формирование списка веток в репозитории, относящихся к задачам указанного проекта."""
        regex = f'{project.upper()}-[\d]+|{project.lower()}-[\d]+'

        for repository_branch in references:
            match_issue_id = findfirst(regex, repository_branch.name)

            if match_issue_id:
                issue_id = match_issue_id.group(0).upper()

                try:
                    issue = self._jira_client.get_issue(
                        issue_id=issue_id,
                    )
                except JIRAError as e:
                    issue = None

                    logger.write(f'Для ветки {repository_branch.name} была обнаружена ошибка доступа к задаче!\n{e}\n')

                if (
                    issue and (
                        issue.fields.status.name == JiraIssueStatusEnum.CLOSED.value
                        or issue.fields.status.name in self._parsed_args.additional_jira_statuses
                    )
                ):
                    self._issue_branches.append((issue_id, repository_branch))

    def _collect_closed_projects_issues_branches(self):
        """Формирование списка веток в репозитории, относящихся к задачам указанных проектов."""
        references = [reference for reference in self._repository.references if isinstance(reference, RemoteReference)]

        for project in self._parsed_args.projects:
            self._collect_closed_project_issue_branches(
                project=project,
                references=references,
            )

        logger.write(
            f'Всего обнаружено {len(references)} веток из них {len(self._issue_branches)} закрытых '
            f'задач\n'
        )

    def _remove_remote_branches(self):
        """
        Удаление веток из удаленного репозитория
        """
        logger.write('Начато удаление веток закрытых задач..\n')

        remote_name = 'origin'

        remote = self._repository.remote(
            name=remote_name,
        )

        for _, branch in self._issue_branches:
            try:
                remote.push(refspec=f':{branch.remote_head}')
            except ValueError:
                # Значит ветка является локальной
                pass
            except GitCommandError as e:
                logger.write(f'Не удалось удалить ветку {branch.name}!\n{e}\n')
            else:
                logger.write(f'Ветка "{branch.name}" была удалена\n')

        logger.write('Удаление веток закрытых задач завершено.\n')

    def _process_repository(self, repository_path: Path):
        """"""
        self._prepare_repository(
            repository_path=repository_path,
        )

        logger.write(f'Обработка репозитория по пути {repository_path}..\n')

        self._collect_closed_projects_issues_branches()

        if self._parsed_args.remove:
            self._remove_remote_branches()

        self._issue_branches = []
        self._repository = None

    def _process_repositories(self):
        """"""
        directory_path = Path(self._parsed_args.project_path)

        if self._parsed_args.find_sub_dirs:
            for sub_directory_path in directory_path.iterdir():
                if sub_directory_path.is_dir():
                    try:
                        self._process_repository(sub_directory_path)
                    except Exception as e:
                        logger.write(f'Возникла ошибка при обработке директории {sub_directory_path}!\n{e}\n')
        else:
            self._process_repository(directory_path)

    def take_action(
        self,
        parsed_args: Namespace,
    ):
        super().take_action(
            parsed_args=parsed_args,
        )

        self._prepare_jira_client()

        self._process_repositories()

        result = self._prepare_result()

        return result
