from distutils.core import setup

# setup(name='amz_parser',
#       version='0.9.8',
#       description='Extract useful data from Amazon pages.',
#       author='lonely',
#       packages=['amz_parser'],
#       package_dir={'amz_parser': 'amz_parser'},
#       install_requires=['dateparser>=1.1.4', 'pyquery>=1.4.3']
#       )


setup(name='amz_extractor',
      version='1.0.0',
      description='提取亚马逊详情页和评论信息',
      author='__token__',
      packages=['amz_extractor'],
      package_dir={'amz_extractor': 'amz_extractor'},
      install_requires=['dateparser>=1.1.4', 'pyquery>=1.4.3']
      )
