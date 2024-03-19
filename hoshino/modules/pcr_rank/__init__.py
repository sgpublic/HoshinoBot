from hoshino import Service

sv_help = '''
[日/台/陆rank] rank推荐表
'''.strip()

sv = Service("pcr-rank", help_=sv_help, bundle="pcr-rank")
