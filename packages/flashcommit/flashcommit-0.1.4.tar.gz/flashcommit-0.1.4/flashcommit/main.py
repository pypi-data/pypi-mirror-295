import argparse
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress

from flashcommit import get_api_url
from flashcommit.gitclient import GitClient
from flashcommit.wsclient import WSClient, PlatformAdapter

NO_API_KEY_MSG = "CODEX_API_KEY environment variable not set"

NO_CHANGES_FOUND_MSG = "[yellow]No changes found.[/yellow]"

REVIEWING_PROGRESS_MSG = "[cyan]Reviewing your changes..."
COMMIT_MSG_PROGRESS_MSG = "[cyan]Generating your commit message..."

COMMIT_MSG_PROMPT_TEMPLATE = """
Below is a diff of all staged changes, coming from the command:
---BEGIN DIFF---                                                                                                                                                                                                                                                                                                   
{diff}                                                                                                                                                                                                                                                                                                             
---END DIFF--- 
Please generate a concise, one-line commit message for these changes."
"""

DIFF_PROMPT_TEMPLATE = """                                                                                                                                                                                                                                                                                         
Review the following code diff and give actionable advice to improve the code. If possible show a proper solution as real code.:                                                                                                                                                                                   
---BEGIN DIFF---                                                                                                                                                                                                                                                                                                   
{diff}                                                                                                                                                                                                                                                                                                             
---END DIFF---                                                                                                                                                                                                                                                                                                     
"""


class LocalFilesystemAdapter(PlatformAdapter):
    def __init__(self, git_client: GitClient):
        self.git_client = git_client

    def read_file(self, file: str) -> Optional[str]:
        if self.is_readable(file):
            return Path(file).read_text()
        return None

    def get_file_list(self) -> list[str]:
        return [f for f in self.git_client.get_git_files() if self.is_readable(f)]

    @staticmethod
    def is_readable(file: str) -> bool:
        return os.path.isfile(file) and os.access(file, os.R_OK)


class FlashCommit:
    def __init__(self):
        load_dotenv()
        self.git_client = GitClient()
        self.console = Console()
        self.client = self.create_client()

    @contextmanager
    def show_progress(self, description: str):
        with Progress(refresh_per_second=10) as progress:
            task = progress.add_task(description, total=None, transient=True)
            yield
            progress.update(task, completed=True)

    def review(self) -> None:
        try:
            prompt = self.get_review_prompt()
            if prompt:
                with self.show_progress(REVIEWING_PROGRESS_MSG):
                    comments = self.client.query(prompt)
                self.display_answer(comments)
            else:
                self.console.print(NO_CHANGES_FOUND_MSG)
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] {str(e)}")

    def create_client(self) -> WSClient:
        apikey = self.get_api_key()
        platform_adapter = LocalFilesystemAdapter(self.git_client)
        client = WSClient(get_api_url(), apikey, platform_adapter)
        client.auth()
        return client

    @staticmethod
    def get_api_key()  -> Optional[str]:
        apikey = os.getenv("CODEX_API_KEY")
        if not apikey:
            raise ValueError(NO_API_KEY_MSG)
        return apikey

    def get_review_prompt(self) -> Optional[str]:
        diff = self.git_client.get_diff()
        if not diff:
            return None
        return DIFF_PROMPT_TEMPLATE.format(diff=diff)

    def display_answer(self, comments: str) -> None:
        md = Markdown(comments)
        self.console.print(md)

    def get_commit_message_prompt(self) -> Optional[str]:
        diff = self.git_client.get_diff()
        if not diff:
            return None
        return COMMIT_MSG_PROMPT_TEMPLATE.format(diff=diff)

    def generate_message(self) -> None:
        try:
            prompt = self.get_commit_message_prompt()
            if prompt:
                with self.show_progress(COMMIT_MSG_PROGRESS_MSG):
                    msg = self.client.query(prompt)
                self.display_answer(msg)
            else:
                self.console.print(NO_CHANGES_FOUND_MSG)
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] {str(e)}")

    def commit(self, message: str) -> None:
        pass


def main():
    flash = FlashCommit()
    parser = argparse.ArgumentParser(description='Flash Commit')
    parser.add_argument('-m', '--message', help='Generate a commit message', action='store_true')
    parser.add_argument('-c', '--commit', help='Generate a commit message and commit the changes (implies -m)',
                        action='store_true')
    args = parser.parse_args()
    if args.message:
        flash.generate_message()
    elif args.commit:
        flash.commit(flash.generate_message())
    else:
        flash.review()


if __name__ == "__main__":
    main()
