from setuptools import setup

setup(name='UNI_botcore',
      version='0.2',
      description='TELEGRAM BOT API CORE',
      packages=[
            'UNI', 
            'UNI/Bot_Under_Methods', 
            'UNI/Communicate', 
            'UNI/Converters', 
            'UNI/Datas', 
            'UNI/Sides',
            'UNI/Types'
      ],
      author_email='dev.nevermore696@gmail.com',
      zip_safe=False)