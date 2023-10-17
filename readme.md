# Getting Started With the QR code Certificate Verification Web App

## Cloning Our Repository into Our Local Machine
To get started with using and testing the project on our local machine, we have to clone the remote repository onto our local repostory, We can get this done by copy and pasting this code to our terminal:

```
git clone https://github.com/mqnifestkelvin/django_QRCode_Certificate_Verification_App.git
```

**Note**: If you don't have git installed on your local machine follow the direction below according to the platform you currently make use of
   * For windows, click [here](https://git-scm.com/download/win) to install and get started and start using git. Also for those who are new to using git here is a useful [video](https://www.simplilearn.com/tutorials/git-tutorial/git-installation-on-windows) on how to get started using git for cloning on windows.
   
   * For Linux all you need to do is run the codes below and you are all set:
    
```
sudo apt-get update
```

```
apt-get install git
```

## Creating Our Virtual Environment
This is very important as it helps isolate certain project dependencies from another preventing the overwriting of important dependencies necessary for the proper functioning of various other packages and application. Therefore, getting a virtual environment setup is necessary to get this project up and running as it suppose to. This can be done by copy pasting and running the command below:

```
pip install virtualenv
```

```
virualenv env
```
**Note**: The keyword env could be any word at all, this just depends on you. Although the use of env is just a naming convention

**Note**: Change directory into the location where the virtual environment was created then run the code below:

### For Windows
```
env\Scripts\activate
```

### For Linux
```
source env/bin/activate
```

## Installing Necessary Dependencies
For the application to function as intended, it is important the required dependencies are installed onto the virtual environment we created earlier. To do this we can simple run the code below:

```
pip install -r requirements.txt
```

## Creating a Superuser
This is import for managing the local database the project depends on. For the sake of simplicity and for the sake of the project we will be making use of sqlite. We can create a superuser account by running the command:

```
python manage.py createsuperuser
```

While doing this, this will prompt us to input our name email address and input suitable passwords. You can skip inputing a user name if you prefer to make use of the default name.

**Note***: This makes use of the computer's default name. Input your password and hit enter and you are all set.


## Making Migration 
Our model have already been setup, all we need to do is instanciate it to add structure all we need to do is instanciate it to add structure to our database. We can achieve this by running the following commands.

```
python manage.py makemigrations
```

```
python manage.py migrate
```

## Running a Local Instance of the Application
If everything has been properly setup this should spawn a web instance of the certificate verification web application. To get this up and running we need to run the command:

```
python manage.py runserver
```
This will authomaticall create a server at 

```
http://127.0.0.1:8000/
```

**Note**: If a brower instance is not automatically started, we can easily copy paste the IP address above to view the running instance.
After we have successfully creaated the server, we can proceed to creating our certificate from the backend by pasting the address into our browser:

```
http://127.0.0.1:8000/admin
```

After this is done, navigate towards adding a new certificate and save. 
**Note**: Do not fill in the last three three columns these fields auto generate with unique values which are used to autogen the user unique QR codes:
`slug`, `Encrypted byte code` and `Encrypted byte code redirect link`.  