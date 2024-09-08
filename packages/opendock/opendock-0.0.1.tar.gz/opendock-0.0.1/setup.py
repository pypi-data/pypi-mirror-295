from setuptools import setup

"""
Description of how to make a python package

https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

"""

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='opendock',
      version='0.0.1',
      long_description=readme(),
      long_description_content_type="text/markdown", 
      description='Zelixir Open-Docking Framework.',
      url='',
      author='Qiuyue Hu,Zechen Wang, Liangzhen Zheng',
      author_email='qy.hu@siat.ac.cn',
      license='GPL-3.0',
      packages=['opendock.core', 'opendock.scorer','opendock.data',
                'opendock.sampler', 'opendock'],
      install_requires=[
          'numpy',
          'pandas',
          #'pytorch',
      ],
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.6',
      )