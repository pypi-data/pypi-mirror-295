import click
import os


#
@click.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.option("-b", "--branch_or_tag", default=None, type=click.STRING, help="分支或Tag")
@click.option("-s", "--startdate", default=None, type=click.STRING,
              help="统计开始时间，格式：xxxx-xx-xx")
@click.option("-e", "--enddate", default=None, type=click.STRING,
              help="统计结束时间，格式：xxxx-xx-xx")
@click.option("-c", "--code_path", default=None, type=click.STRING, help="代码路径")
def cli(branch_or_tag, startdate, enddate=None, code_path=None):
    """Git提交代码统计"""

    from read_commit._cargo import git_control
    code_path = code_path if code_path else os.getcwd()
    git_control(branch_or_tag, startdate, enddate, code_path)


if __name__ == "__main__":
    code_path = "/home/Hugh/autotest_uos_system"
    branch_or_tag = "at-develop/eagle"
    startdate = "2024-08-01"
    enddate = "2024-08-09"

    cli(branch_or_tag, startdate, enddate, code_path)
    # cli(branch_or_tag, startdate)
