from git import Repo, Tree

from flashcommit import RepoDetails


def get_name_from_url(url: str):
    path = url.split("/")[-1]
    if path.endswith(".git"):
        return path[0:-4]
    else:
        return path


def _repo_from_url(url):
    return {
        'owner': None,
        'repository': get_name_from_url(url),
        'url': url
    }


class GitClient(object):

    def __init__(self):
        super().__init__()
        self.repo = Repo(".")
        self.repo_url = self._get_repo()["url"]
        # print(self.get_repo_details().repository)

    def _get_repo(self):
        for remote in self.repo.remotes:
            for url in remote.urls:
                return _repo_from_url(url)
        return _repo_from_url(f"file:///{self.repo.common_dir}")

    def get_repo_details(self) -> RepoDetails:
        return RepoDetails(**self._get_repo())

    def get_diff(self):
        t = self.repo.head.commit.tree
        return self.repo.git.diff(t)

    def get_git_files(self):
        files = list()
        tree = self.repo.tree()
        self._read_tree(files, tree)
        return files

    def _read_tree(self, files: list[str], tree: Tree):
        for f in tree:
            if f.type == "blob":
                files.append(f.path)
            elif f.type == "tree":
                self._read_tree(files, f)
