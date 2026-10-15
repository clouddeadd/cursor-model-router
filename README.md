# Model picker

This is a small program Cursor runs on your computer. It chooses a named model for the task. A rule then tells the agent to do the work on that model and to start its reply with `MODEL:` and the name.

It does not ask anyone to change the model menu. It does not print Auto.

## How it chooses

The program reads the task and uses the first matching rule.

| If the task mentions | It picks |
| --- | --- |
| security, privacy, credentials, production, an incident | Claude Opus 5 Thinking High |
| review, audit, a whole repo | Claude Fable 5.1 Thinking High |
| refactor, migrate, TypeScript, a Python module | GPT-5.3 Codex |
| a rename, a typo, formatting, lint | Composer 2.5 Fast |
| build, fix, debug, or most other work | Grok 4.7 High Fast |

If none of those match, it still picks Grok 4.7 High Fast.

Those names are the ones Cursor accepted when this was built. Another account can reject a name Cursor does not offer there.

## What is not in this copy

Chat history, logs, email addresses, and private project files are not in this repository. The program can write a local note of each pick on the computer that runs it. That note is not uploaded here.

## Install

Click the install link once. Cursor asks you to confirm. That installs the picker program from this repository. Then click the rule link once so replies start with `MODEL:` and the chosen name. Start a new chat after both are installed.

Picker: <https://cursor.com/link/mcp/install?name=cursor-model-router&config=eyJjb21tYW5kIjoicHl0aG9uMyIsImFyZ3MiOlsiLWMiLCJpbXBvcnQgb3MscGF0aGxpYixzeXMsdXJsbGliLnJlcXVlc3RcbnJvb3Q9cGF0aGxpYi5QYXRoLmhvbWUoKS8nLmN1cnNvcicvJ21vZGVsLXJvdXRlcidcbnJvb3QubWtkaXIocGFyZW50cz1UcnVlLCBleGlzdF9vaz1UcnVlKVxuYmFzZT0naHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2Nsb3VkZGVhZGQvY3Vyc29yLW1vZGVsLXJvdXRlci9tYWluLydcbmZvciBuYW1lIGluICgnc2VydmVyLnB5Jywncm91dGVyLnB5Jyk6XG4gICAgdXJsbGliLnJlcXVlc3QudXJscmV0cmlldmUoYmFzZStuYW1lLCByb290L25hbWUpXG5vcy5leGVjdihzeXMuZXhlY3V0YWJsZSxbc3lzLmV4ZWN1dGFibGUsc3RyKHJvb3QvJ3NlcnZlci5weScpXSkiXX0=>

Rule: <https://cursor.com/link/rule?name=model-router&text=%23+Agent+picks+the+model%0A%0AOn+every+new+user+request%3A%0A%0A1.+Call+MCP+%60pick_model%60+with+the+user+task+text.%0A2.+Run+the+work+with+the+Cursor+%60Task%60+tool%2C+passing+%60model%60+%3D+the+returned+%60SLUG%60.%0A3.+First+line+of+the+user-facing+reply%3A+%60MODEL%3A+%3Cdisplay+name%3E%60.%0A%0ADo+not+ask+the+user+to+change+the+Cursor+model+picker.+Do+not+print+Auto+or+default+as+the+model+name.>

## Forum post

I use a Cursor plugin that picks a named model for each task and shows that name at the top of the reply. The agent then runs the work on that model. It does not leave the choice on Auto, and it does not ask me to change the model menu.

The choice is a fixed list. Security, privacy, and production tasks go to Claude Opus 5 Thinking High. Long reviews go to Claude Fable 5.1 Thinking High. Refactors go to GPT-5.3 Codex. Tiny edits go to Composer 2.5 Fast. Everything else goes to Grok 4.7 High Fast.

Install it from the plugin link once, then start a new chat.
