from invoke import task


@task
def clean(c, docs=False, bytecode=True, dist=True, extra=''):
    patterns = ['build']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if dist:
        patterns.append('dist/*')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))


@task
def unit(c):
    c.run("pip install -r requirements-test.txt")
    c.run("python tests.py")


@task
def deploy(c):
    c.run("python setup.py build")
