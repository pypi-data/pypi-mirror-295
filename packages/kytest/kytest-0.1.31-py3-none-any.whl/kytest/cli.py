import click
from . import __version__
from .scaffold import create_scaffold
from .genetor import generate_case


@click.group()
@click.version_option(version=__version__, help="Show version.")
# 老是变，等最后定下来再搞，目前也没啥用
def main():
    pass


@main.command()
@click.option('-p', '--platform', help="Specify the platform.")
def create(platform):
    """
    创建新项目
    @param platform: 平台，如api、android、ios、web
    @return:
    """
    create_scaffold(platform)


@main.command()
@click.option('-p', '--project', help='Specify the project.')
@click.option('-c', '--controller', default=None, help="Specify the controller.")
@click.option('-b', '--base_path', default='tests', help="Specify the base path.")
def generate(project, controller, base_path):
    """
    在当前目录生成用例，有相同的则进行覆盖
    @param project: tms导入的接口项目
    @param controller：指定生成哪个controller，不指定就生成所有的controller，有空格需要用引号包括
    @param base_path：指定生成目录，默认当前目录
    @return:
    """
    generate_case(project, controller, base_path)
