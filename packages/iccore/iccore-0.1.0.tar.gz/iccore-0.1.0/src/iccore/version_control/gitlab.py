class GitlabToken:

    def __init__(self, value: str, token_type: str = "PRIVATE-TOKEN"):
        self.value = value
        self.type = token_type


class GitlabResource:

    def __init__(self, name: str, id: int = 0) -> None:
        self.name = name
        self.id = id


class GitlabReleaseAssetCollection:

    def __init__(self) -> None:
        self.names: list[str] = []


class GitlabReleaseAssetLink:

    def __init__(
        self,
        name: str,
        base_url: str,
        archive_name: str = "",
        link_type: str = "package",
    ) -> None:
        self.name = name
        self.url = f"{base_url}/{name}"

        self.direct_asset_path = "/"
        if archive_name:
            self.direct_asset_path += f"{archive_name}/"
        self.direct_asset_path += name
        self.link_type = link_type

    def serialize(self):
        return {
            "name": self.name,
            "url": self.url,
            "direct_asset_path": self.direct_asset_path,
            "link_type": self.link_type,
        }


class GitlabReleaseManifest:

    def __init__(
        self, project_version: str, base_url: str, assets: GitlabReleaseAssetCollection
    ) -> None:
        self.name = f"Release {project_version}"
        self.tag_name = f"v{project_version}"
        self.ref = "master"
        self.assets = assets

        self.asset_links: list = []
        for name in self.assets.names:
            self.asset_links.append(GitlabReleaseAssetLink(name, base_url))

    def serialize(self):

        return {
            "name": self.name,
            "tag_name": self.tag_name,
            "ref": self.ref,
            "assets": {"links": [a.serialize() for a in self.asset_links]},
        }


class GitlabRelease:

    def __init__(self):
        self.manifest: GitlabReleaseManifest | None = None


class GitlabProject(GitlabResource):
    def __init__(self, name: str = "", id: int = 0, group_name: str = "") -> None:
        super().__init__(name, id)
        self.group_name = group_name
        self.releases: list[GitlabRelease] = []


class GitlabGroup(GitlabResource):

    def __init__(self, name: str, id: int = 0):
        super().__init__(name, id)
        self.projects: list[GitlabProject] = []


class GitlabInstance:

    def __init__(self, url: str):
        self.url = url
        self.api_url = f"{url}/api/v4"
        self.groups: list[GitlabGroup] = []
