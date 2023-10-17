# Getting Started With the QR code Certificate Verification Web App

## Cloning Our Repository into Our Local Machine
To get started with using and testing the project on our local machine, we have to clone the remote repository onto our local repostory, We can get this done by copy and pasting this code to our terminal:

`git clone https://github.com/mqnifestkelvin/django_QRCode_Certificate_Verification_App.git`

**Note, If you don't have git installed on your local machine follow the direction below according to the platform you currently make use of**
   * For windows, click [here](#https://git-scm.com/download/win) to install and get started and start using git. Also for those who are new to using git here is a useful [video](#https://www.simplilearn.com/tutorials/git-tutorial/git-installation-on-windows) on how to get started using git for cloning on windows.
    * For Linux all you need to do is run the codes below and you are all set:
    
`sudo apt-get update
`

`apt-get install git
`

## Creating Over Virtual Environment
This is very important as it helps isolate certain project dependencies from another preventing the overwriting of important dependencies necessary for the proper functioning of various other packages and application. Therefore, getting a virtual environment setup is necessary to get this project up and running as it suppose to. This can be done by copy pasting and running the codes below

`pip install virtualenv`

`virualenv env`

**Note the keyword env could be any word at all, this just depends on you. Although the use of env is just a naming convention**

## Installing Necessary Dependencies

