import sys
from lynq.backendutils.lynq.pwsh import pwsh

match sys.argv[1]:
    case "visit":
        match sys.argv[2]:
            case "lynq-github":
                pwsh(f"start https://github.com/elemenom/lynq/")

            case "lynq-pypi":
                pwsh(f"start https://pypi.org/project/lynq/")

            case "lynq-github-issues":
                pwsh(f"start https://github.com/elemenom/lynq/issues/")

            case "lynq-github-pr":
                pwsh(f"start https://github.com/elemenom/lynq/pulls/")

            case "lynq-github-pr-new":
                pwsh(f"start https://github.com/elemenom/lynq/compare/")

            case "lynq-github-insights":
                pwsh(f"start https://github.com/elemenom/lynq/pulse/")

            case "lynq-documentation":
                pwsh(f"start https://github.com/elemenom/lynq?tab=readme-ov-file#welcome-to-lynq/")

            case "lynq-license":
                pwsh(f"start https://github.com/elemenom/lynq/blob/main/LICENSE")

            case "author-github":
                pwsh(f"start https://github.com/elemenom/")

            case "author-pypi":
                pwsh(f"start https://pypi.org/user/elemenom/")

            case "lynq-github-download":
                pwsh(f"start https://github.com/elemenom/lynq/releases/")

    case "upgrade":
        pwsh("pip install lynq --upgrade")

    case "install":
        pwsh("pip install lynq")

    case "install-version":
        pwsh(f"pip install lynq=={sys.argv[2]}")

    case "info":
        pwsh("pip show lynq")

    case "uninstall":
        pwsh("pip uninstall lynq")

    case "documentation":
        import lynq

        print(lynq.__doc__)

    case "feedback":
        pwsh(f"start https://github.com/elemenom/lynq/issues/new/")

    case "license":
        import lynq.backendutils.server.standard as random_lynq_file

        print(random_lynq_file.__doc__)