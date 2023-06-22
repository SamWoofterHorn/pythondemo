# pylint: disable=invalid-name

# Core Python packages
import shutil
import tempfile

# Third-party packages
from invoke import task


@task(help={
    'ref': 'The git reference to build, usually a tag'
})
def build(c, ref):
    """
    Build a Portal-Site Docker container at the specified tag.

    The container is tagged and uploaded to dockerhub.
    """
    try:
        build_path = tempfile.mkdtemp()

        c.run(f'git clone --shallow-submodules --branch={ref} . {build_path}')

        with c.cd(build_path):
            c.run('docker buildx build --platform linux/amd64 -t'
                  + f'altalang/pythondemo:{ref} .')

    finally:
        if build_path:
            shutil.rmtree(build_path)


@task(help={
    'ref': 'The git reference to build, usually a tag'
})
def stage(c, ref):
    build(c, ref)

    c.run(f'docker tag altalang/pythondemo:{ref} altalang/pythondemo:staging')

    c.run(f'docker push altalang/pythondemo:{ref}')
    c.run('docker push altalang/pythondemo:staging')

    c.run('kubectl set image deployment pythondemo-staging '
          + f'pythondemo-staging=altalang/pythondemo:{ref}')

    c.run('kubectl rollout status deployment pythondemo-staging')
