from distutils.core import setup
setup(
  name = 'chatget',         # How you named your package folder (MyLib)
  packages = ['chatget'],   # Chose the same as "name"
  version = '1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple library that allows the user to very easily grab the contents of a Twitch chat!',   # Give a short description about your library
  author = 'tachophobicat',                   # Type in your name
  author_email = 'tachophobicat@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/aidan-octane/chatget',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/aidan-octane/chatGET/archive/refs/tags/v1.3.tar.gz',    # I explain this later on
  keywords = ['Twitch', 'chat', 'get', 'easy', 'simple'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'websockets',
          'asyncio',
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)