import argparse
import json
import sys

parser = argparse.ArgumentParser(prog="mxee", description="mxee", epilog="Making things easier.")
parser.add_argument("--bookmarks", action="store_true", help="test")
parser.add_argument("--test", action="store_true", help="test")
parser.add_argument("--texel", action="store_true", help="test")


args = parser.parse_args()


if args.bookmarks:
    print("Die Tagersschau https://www.google.com")
    sys.exit(0)




def row_handler(row_idx, headers, row, rowa, rown, context):
    print(row_idx)
    print(headers)
    print(row)
    print(rowa)
    print(rown)
    print()


if args.test:
    import mxee
    import mxee.helper
    import mxee.actions

    #mxee.helper.xlsx_rows("git-report.xlsx", mxee.helper.xlsx_sheetnames("git-report.xlsx")[0], row_callback=row_handler, context={})

    #xlsx_named_columns
    data = mxee.helper.xlsx_named_columns("test.xlsx")
    print(json.dumps(data, indent=4))

    # ws=mxee.config("main.workspace")
    # mxee.actions.git_projects_status(ws)

    sys.exit(0)


if args.texel:
    import mxee.helper
    import sys
    data = []
    for line in sys.stdin.readlines():
        data.append(line.strip().split("\t"))
    mxee.helper.xlsx_out("out.xlsx", {'stdin': {'data': data}})
    sys.exit(0)
