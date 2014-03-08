from distutils.core import setup, Extension

module = Extension('depth',
        include_dirs = ['/usr/local/include', '/opt/softkinetic/DepthSenseSDK/include'],
        libraries = ['turbojpeg', 'DepthSensePlugins', 'DepthSense', 'python2.7'],
        library_dirs = ['/usr/local/lib', '/opt/softkinetic/DepthSenseSDK/lib'],
        extra_compile_args = ['-std=c++11'],
        sources = ['depth.cxx'])

setup (name = 'DepthSense',
        version = '1.0',
        description = 'This is a demo package',
        author = 'Abdi Dahir',
        author_email = 'abdi.dahir@outlook.com',
        url = 'http://github.com/snkz',
        long_description = '''This is really just a demo package.''',
        ext_modules = [module])
