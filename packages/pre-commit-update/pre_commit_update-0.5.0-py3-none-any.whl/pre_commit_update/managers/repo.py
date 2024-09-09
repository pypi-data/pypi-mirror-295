import re
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Tuple

import git
from packaging.version import InvalidVersion
from packaging.version import parse as parse_version

from ..repo import Repo
from . import MessageManager


class RepoManager:
    def __init__(
        self,
        repos_data: Dict,
        all_versions: bool,
        jobs: Optional[int],
        exclude: Tuple,
        keep: Tuple,
        bleeding_edge: Tuple,
        tag_prefix: Tuple,
    ) -> None:
        self._all_versions: bool = all_versions
        self._jobs: Optional[int] = jobs
        self._exclude: Tuple = exclude
        self._keep: Tuple = keep
        self._bleeding_edge: Tuple = bleeding_edge
        self._tag_prefix: Tuple = tag_prefix
        self._repos_data: Dict = self._add_trim_to_repos_data(repos_data)
        self._repos_tags_and_hashes: List[Dict] = self._get_repos_tags_and_hashes()
        self._repos_latest_hashes: List = self._get_repos_latest_hash()
        self._repos_list: List[Repo] = self._get_repos_list()

    @property
    def repos_data(self) -> Dict:
        return self._remove_trim_from_repos_data(self._repos_data)

    def _add_trim_to_repos_data(self, repos_data: Dict) -> Dict:
        for i, repo in enumerate(repos_data):
            if not self._is_repo_remote(repo["repo"]):
                continue
            repo["trim"] = repo["repo"].split("/")[-1]
            repos_data[i] = repo
        return repos_data

    @staticmethod
    def _remove_trim_from_repos_data(repos_data: Dict) -> Dict:
        for i, repo in enumerate(repos_data):
            repo.pop("trim", None)
            repos_data[i] = repo
        return repos_data

    @staticmethod
    def _get_repo_fixed_tags_and_hashes(
        tag_hash: Optional[Dict], tag_prefix: Optional[str]
    ) -> Dict:
        # Due to various prefixes that devs choose for tags, strip them down to semantic version numbers only.
        # Take tag_prefix into consideration ("pre-commit-tag-v0.1.1")
        # Store it inside the dict ("ver1.2.3": "1.2.3") and parse the value to get the correct sort.
        # Remove invalid suffixes ("-test", "-split", ...)
        # Return the original value (key) once everything is parsed/sorted.
        if not tag_hash:
            return {}
        fixed_tags: Dict = {}
        for tag in tag_hash.keys():
            tag_no_prefix: str = tag.replace(tag_prefix, "") if tag_prefix else tag
            for prefix in re.findall("([a-zA-Z]*)\\d*.*", tag_no_prefix):
                prefix = prefix.strip()
                try:
                    version: str = tag_no_prefix[len(prefix) :]
                    fixed_tags[tag] = parse_version(version)
                except InvalidVersion:
                    continue
        fixed_tags = {
            k: v
            for k, v in sorted(
                fixed_tags.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        }
        return {k: tag_hash[k] for k in fixed_tags.keys()}

    def _get_repo_tags_and_hashes(self, repo: Dict) -> Optional[Dict]:
        url: str = repo["repo"]
        if not self._is_repo_remote(url) or self._is_repo_excluded(repo["trim"]):
            return None
        try:
            remote_tags: List = (
                git.cmd.Git()
                .ls_remote("--exit-code", "--tags", url, sort="v:refname")
                .split("\n")
            )
            tag_hash: Dict = {}
            for tag in remote_tags:
                commit_hash, parsed_tag = re.split(r"\t+", tag)
                parsed_tag = parsed_tag.replace("refs/tags/", "").replace("^{}", "")
                tag_prefix: Optional[str] = self._get_repo_tag_prefix(repo["trim"])
                if tag_prefix and not parsed_tag.startswith(tag_prefix):
                    continue
                tag_hash[parsed_tag] = commit_hash
            return tag_hash
        except Exception:
            return None

    def _get_repo_latest_hash(self, repo: Dict) -> Optional[str]:
        if not self._is_repo_remote(repo["repo"]) or self._is_repo_excluded(
            repo["trim"]
        ):
            return None
        try:
            return (
                git.cmd.Git().ls_remote("--exit-code", repo["repo"], "HEAD").split()[0]
            )
        except Exception:
            return None

    def _get_repos_tags_and_hashes(self) -> List[Dict]:
        with ThreadPoolExecutor(max_workers=self._jobs) as pool:
            tasks: List = []
            for repo in self._repos_data:
                tasks.append(pool.submit(self._get_repo_tags_and_hashes, repo))
        return [
            self._get_repo_fixed_tags_and_hashes(
                tasks[i].result(), self._get_repo_tag_prefix(repo.get("trim"))
            )
            for i, repo in enumerate(self._repos_data)
        ]

    def _get_repos_latest_hash(self) -> List[Optional[str]]:
        with ThreadPoolExecutor(max_workers=self._jobs) as pool:
            tasks: List = []
            for repo in self._repos_data:
                tasks.append(pool.submit(self._get_repo_latest_hash, repo))
        return [task.result() for task in tasks]

    def _get_repos_list(self) -> List[Repo]:
        repo_list: List[Repo] = []
        for i, repo in enumerate(self._repos_data):
            if not self._is_repo_remote(repo["repo"]):
                continue
            repo_list.append(
                Repo(
                    repo=repo,
                    tags_and_hashes=self._repos_tags_and_hashes[i],
                    tag_prefix=self._get_repo_tag_prefix(repo["trim"]),
                    latest_hash=self._repos_latest_hashes[i],
                    all_versions=self._all_versions,
                    bleeding_edge=self._is_repo_bleeding_edge(repo["trim"]),
                )
            )
        return repo_list

    @staticmethod
    def _is_repo_remote(repo_url: str) -> bool:
        return repo_url.startswith("http")

    def _is_repo_excluded(self, repo_trim: str) -> bool:
        return repo_trim in self._exclude or self._exclude == ("*",)

    def _is_repo_kept(self, repo_trim: str) -> bool:
        return repo_trim in self._keep or self._keep == ("*",)

    def _is_repo_bleeding_edge(self, repo_trim: str) -> bool:
        return repo_trim in self._bleeding_edge or self._bleeding_edge == ("*",)

    def _get_repo_tag_prefix(self, repo_trim: str) -> Optional[str]:
        prefix_element: Optional[Tuple] = next(
            (t for t in self._tag_prefix if t[0] == repo_trim), None
        )
        return prefix_element[1] if prefix_element else None

    def get_updates(self, messages: MessageManager) -> None:
        for i, repo in enumerate(self._repos_list):
            if not repo.has_tags_and_hashes and not self._is_repo_excluded(repo.trim):
                messages.add_warning_message(repo.trim, "0 tags/hashes fetched")
                continue
            if self._is_repo_excluded(repo.trim):
                messages.add_excluded_message(repo.trim, repo.current_version)
                continue
            if self._is_repo_kept(repo.trim):
                messages.add_kept_message(
                    repo.trim, repo.current_version, repo.latest_version
                )
                continue
            if repo.current_version != repo.latest_version:
                messages.add_to_update_message(
                    repo.trim, repo.current_version, repo.latest_version
                )
                self._repos_data[i]["rev"] = repo.latest_version
                continue
            messages.add_no_update_message(repo.trim, repo.current_version)
