from distutils.core import setup
setup(
  name = 'PyLabEHPY',         # How you named your package folder (MyLib)
  packages = ['PyLabEHPY'],   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Pacote para interagir com o PyLab do EHPY',   # Give a short description about your library
  author = 'Ulisses Alves',                   # Type in your name
  author_email = 'ulisses.alves@protonmail.com',      # Type in your E-Mail
  url = 'https://github.com/ualvesdias/PyLabEHPY',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ualvesdias/PyLabEHPY/archive/refs/tags/0.4.tar.gz',    # I explain this later on
  keywords = ['PyLabEHPY'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.12',
  ],
)
