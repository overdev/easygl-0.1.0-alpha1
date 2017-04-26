from distutils.core import setup

setup(
    name='easygl',
    version='0.1.0a1',
    packages=['easygl', 'easygl.arrays', 'easygl.display', 'easygl.prefabs', 'easygl.shaders', 'easygl.textures',
              'easygl.structures'],
    url='https://github.com/overdev/easygl-0.1.0-alpha1',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programmin Language :: Python :: 3.4',
    ],
    install_requires=['pygame', 'PyOpenGL', 'typing'],
    keywords='games easygl opengl gl graphics textures geometry rendering gamedev pygame PyOpenGL',
    author='Jorge A. G.',
    author_email='jorgegomes83@hotmail.com',
    description='A small library for easy OpenGL 2D rendering.'
)
