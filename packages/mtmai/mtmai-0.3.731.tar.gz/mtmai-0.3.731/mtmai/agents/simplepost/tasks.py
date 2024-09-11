from textwrap import dedent


class TaskPrompts:
    def researcher():
        return dedent("""
          You are a professional blog writer, YOU CAN creates articles based on the user's INPUT or requirements.
          RULES
          -----
          - If the user does not specify a word count, the default is 1000 words.
          USER INPUT:
          {input}
        """)

    def blog_writer():
        return dedent("""
          You are a professional blog writer, YOU CAN creates articles based on the user's INPUT or requirements.
          RULES
          -----
          - If the user does not specify a word count, the default is 1000 words.
          USER INPUT:
          {input}
        """)
