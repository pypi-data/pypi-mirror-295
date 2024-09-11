import os
import gitlab


class GitlabClient:
    def __init__(self):
        self._mr = None
        self._project = None
        self._latest_version = None
        self._code_diffs = None

        self._project_path = os.environ.get("CI_MERGE_REQUEST_PROJECT_PATH")
        self._mr_iid = os.environ.get("CI_MERGE_REQUEST_IID")
        self._gitlab_host = os.environ.get("GITLAB_HOST") or os.environ.get(
            "CI_SERVER_URL") or "https://jihulab.com:443"
        self._pat = os.environ.get("AI_BOT_PERSONAL_ACCESS_TOKEN")

        self._client = gitlab.Gitlab(url=self._gitlab_host, private_token=self._pat, per_page=100)
        if os.environ.get("DEBUG") == 'true':
            self._client.enable_debug()

    def project(self):
        if not self._project:
            self._project = self._client.projects.get(self._project_path)

        return self._project

    def mr(self):
        if not self._mr:
            mr_iid = os.environ.get("CI_MERGE_REQUEST_IID")
            self._mr = self.project().mergerequests.get(mr_iid)

        return self._mr

    def latest_version(self):
        if not self._latest_version:
            versions = self.mr().diffs.list(order_by='id', sort='desc', page=1, per_page=1)
            self._latest_version = versions[0]

        return self._latest_version

    def mr_code_diffs(self):
        if not self._code_diffs:
            latest_version = self.latest_version()
            self._code_diffs = self.mr().diffs.get(latest_version.id, unidiff="true")

        return self._code_diffs

    def create_note(self, content):
        resp = self.mr().notes.create({'body': content})
        return resp


if __name__ == '__main__':
    client = GitlabClient()
    mr_code_diffs = client.mr_code_diffs()
    print("end")
