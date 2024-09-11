from setuptools import setup, find_packages

# Setting Up

setup(
      
      name = "anaplan",
      version = "1.2.5",
      author = "Hasan Can Beydili",
      author_email = "tchasancan@gmail.com",
      description= "Circles activation added.",
      packages=find_packages(),
      package_data={
        'anaplan': ['*.mp4']
      },
      include_package_data=True,
      keywords = ["model evaluation", "classifcation", 'potentiation learning artficial neural networks'],

      
      )