from tests.__init__ import *
from psplpy.dynamic_compose import DynamicCompose

dc_rc_dir = rc_dir / 'dynamic_compose'
dc_compose_dir = dc_rc_dir / '.compose'
compose_dumped_file = dc_compose_dir / 'compose-dumped.yml'
dockerfile_dumped_file = dc_compose_dir / 'Dockerfile-dumped'


def lines_rstrip(text: str) -> str:
    lines = text.splitlines()
    stripped_lines = [line.rstrip() for line in lines]
    result = '\n'.join(stripped_lines)
    return result


def tests():
    DynamicCompose.CWD = dc_rc_dir
    dc = DynamicCompose()
    dc.arg['GPU'] = '''    
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]'''
    dc.arg['IMAGE'] = 'python:3.10'
    print(dc.env)
    print(dc.arg)
    dc.compose_dir = dc_compose_dir

    dc.format_compose()
    dc.format_dockerfile()
    dc.dump()

    assert compose_dumped_file.read_text().strip() == lines_rstrip(dc.compose_file.read_text().strip())
    # dc.compose_file.unlink()
    assert dockerfile_dumped_file.read_text().strip() == lines_rstrip(dc.dockerfile_file.read_text().strip())
    # dc.dockerfile_file.unlink()

    dc.up()


if __name__ == '__main__':
    tests()
