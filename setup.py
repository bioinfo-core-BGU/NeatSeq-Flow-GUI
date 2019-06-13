#from distutils.core import setup
from setuptools import find_packages, setup,os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join( path, filename))
    return paths

extra_files = package_files("neatseq_flow_gui")

setup(
    name                = 'NeatSeq-Flow GUI',
    version             = '1.0.0',
    author              = 'Liron Levin',
    author_email        = 'levinl@post.bgu.ac.il',
    maintainer          = 'Liron Levin',
    maintainer_email    = 'levinl@post.bgu.ac.il',
    url                 = 'http://neatseq-flow.readthedocs.io/en/latest/',
    description         = 'Package for creation of workflow scripts for execution on computer clusters',
    license             = 'GNU3',
    long_description    =  open('README.md').read(),
    download_url        = 'https://github.com/bioinfo-core-BGU/NeatSeq-Flow-GUI.git',
    platforms           = ["POSIX","Windows"],
    packages            = find_packages(),
    include_package_data= True,  # See  MANIFEST.in
    scripts             = ['bin/neatseq_flow_monitor.py',
                            'bin/NeatSeq_Flow_GUI.py',
                            ],
    data_files          = [('neatseq_flow_gui',[os.path.join('neatseq_flow_gui','NeatSeq_Flow.ico')]),
                            ('neatseq_flow_gui',extra_files),
                            (os.path.join('neatseq_flow_gui','TEMPLATES'),[os.path.join('neatseq_flow_gui','TEMPLATES','MODULES_TEMPLATES.yaml')])],
    install_requires    = [
                        "pyyaml >= 3.12",
                        "munch",
                        "wxpython",
                        "pandas"],
    classifiers         = [
                          'Development Status :: 4 - Beta',
                          'Environment :: Console',
                          'Intended Audience :: End Users',
                          'Intended Audience :: Developers',
                          'License :: OSI Approved :: Python Software Foundation License',
                          'Operating System :: Microsoft :: Windows',
                          'Operating System :: POSIX',
                          'Programming Language :: Python',
                          ],
    )
    
