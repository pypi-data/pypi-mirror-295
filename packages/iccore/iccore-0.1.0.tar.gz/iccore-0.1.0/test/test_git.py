from pathlib import Path
from iccore.version_control import GitRepo

def test_git_repo():

    repo = GitRepo(Path(), read_user=False)
    repo.get_branch()
