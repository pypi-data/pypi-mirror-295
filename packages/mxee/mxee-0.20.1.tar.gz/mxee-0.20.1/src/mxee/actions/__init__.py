import mxee
import os
import subprocess


def git_projects_status(workspace_base_directory):
    ws = workspace_base_directory
    items = os.listdir(ws)


    #         A             B       C                 D        E                   F
    data = [['Repository', 'Path', 'Current Branch', 'State', 'Remote-Sync-Diff', 'Remote']]
    data_unsorted = {}

    for x in items:
        print(x)
        y = os.path.join(ws, x)
        ygit = os.path.join(ws, x, ".git")
        if os.path.isdir(y) and os.path.isdir(ygit):
            git_status = subprocess.check_output("""/bin/bash -c 'cd "%s" && git status'""" % y, shell=True, universal_newlines=True).strip().split("\n")
            git_status_p = subprocess.check_output("""/bin/bash -c 'cd "%s" && git status --porcelain'""" % y, shell=True, universal_newlines=True).strip().split("\n")

            git_status_b = subprocess.check_output("""/bin/bash -c 'cd "%s" && git status --porcelain -b | grep "^##"'""" % y, shell=True, universal_newlines=True).strip().split("\n")[0].strip()
            
            git_remote = subprocess.check_output("""/bin/bash -c 'cd "%s" && git remote -v | tr "\t" " " | cut -d " " -f 2 | uniq;exit 0'""" % y, shell=True, universal_newlines=True).strip().split("\n")[0].strip()
            if git_remote == "":
                git_remote = "-"
            
            branch_name = subprocess.check_output("""/bin/bash -c 'cd "%s" && git rev-parse --abbrev-ref HEAD 2>/dev/null;exit 0'""" % y, shell=True, universal_newlines=True).strip().split("\n")[0].strip()
            if branch_name == "HEAD":
                branch_name = "-"


            state_string = "OK"
            if branch_name == "-":
                state_string = "-"
            else:
                if "".join(git_status_p).strip() != "":
                    state_string = "UNCOMMITED-CHANGES"

            local_ahead_string = "-"
            if branch_name == "-" or git_remote == "-":
                local_ahead_string = "-"
            else:
                if 'ahead' in git_status_b or 'behind' in git_status_b:
                    local_ahead_string = git_status_b.split("[")[1].replace("]", "").strip()

            #      A  B  C            D             E
            row = [x, y, branch_name, state_string, local_ahead_string, git_remote]
            data_unsorted[x] = row

    sorted_keys = list(sorted(data_unsorted.keys()))
    data += [ data_unsorted[k] for k in sorted_keys ]

    mxee.helper.xlsx_out(
        "git-report.xlsx",
        sheets={
            'Workspace_Git_Repositories': {
                'data': data,
                'cw':{
                    'A': 30,
                    'B': 60,
                    'C': 30,
                    'D': 30,
                    'E': 30,
                    'F': 80
                }
            }
        }
    )
