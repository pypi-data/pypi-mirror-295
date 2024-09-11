from coderider_codereview.coderider_client import CoderiderClient
from coderider_codereview.gitlab_client import GitlabClient
from coderider_codereview.prompt import Prompt


def main():
    cr_client = CoderiderClient().login()
    llm_resp = cr_client.chat_completions(Prompt().all_messages())
    content = llm_resp["choices"][0]["message"]["content"]
    GitlabClient().create_note(content)
    print(content)
    print("Left a code review comment to the MR.")


if __name__ == '__main__':
    main()
