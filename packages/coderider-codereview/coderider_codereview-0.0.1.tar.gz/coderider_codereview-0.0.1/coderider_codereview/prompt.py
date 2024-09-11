from coderider_codereview.gitlab_client import GitlabClient


class Prompt:

    def __init__(self):
        self._gl_client = GitlabClient()

    def system_message(self):
        content = """
        You are a Code Review master.
        """.strip()

        return {
            "role": "system",
            "content": content
        }

    def user_command_message(self):
        content = """
        分析上面的代码变更, 在代码安全、执行效率、代码风格方面进行评审,
        将发现的问题进行简要总结，描述其特征、对整体功能和性能的潜在影响, 尽可能给出改进方案和代码示例.
        对每一项评审意见, 务必标明序号, 请用中文回答, 注意使用委婉的语气.
        """.strip()

        return {
            "role": "user",
            "content": content
        }

    def code_diff_messages(self, diff_file):
        # https://docs.gitlab.com/ee/user/project/merge_requests/changes.html#collapse-generated-files
        if diff_file["generated_file"]:
            return []

        # https://docs.gitlab.com/ee/api/merge_requests.html#list-merge-request-diffs
        file_name_content = ""
        if diff_file["new_file"]:
            file_name_content = f"Added the new file: `{diff_file['new_path']}`"
        elif diff_file["deleted_file"]:
            file_name_content = f"Deleted the old file: `{diff_file['old_path']}`"
        elif diff_file["renamed_file"]:
            file_name_content = f"Renamed file from `{diff_file['old_path']}` to `{diff_file['new_path']}`"
        else:
            file_name_content = f"Changed file `{diff_file['old_path']}`"

        diff_content = f"Code changes with Diff Format"
        content = f"{file_name_content}.\n\n{diff_content}:\n\n```diff\n{diff_file['diff']}```\n"

        return [
            {
                "role": "user",
                "content": content
            },
            {
                "role": "assistant",
                "content": "Got it"
            }
        ]

    def all_messages(self):
        messages = [self.system_message()]

        mr_code_diffs = self._gl_client.mr_code_diffs()
        diff_files = mr_code_diffs.diffs
        for diff_file in diff_files:
            msgs = self.code_diff_messages(diff_file)
            messages.extend(msgs)

        messages.append(self.user_command_message())

        return messages


if __name__ == '__main__':
    prompt = Prompt()
    all_messages = prompt.all_messages()
    print("end")
