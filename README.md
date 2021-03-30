# multilinks_prj
Django 3 multilinks - it's my own little project for practice. Main idea is to built something similar such as 'smarturl.it', 'linktr.ee' and many more others

This one is my project i've been developing around 5 month's.

Ok, little story:
I decided to learn python because i got bored of doing what i've been doing. So, django go close with python and i start learning django after... Well, I quit for about a year after a few weeks because of some situations in life and because it took a lot of time for which I was not paid.
But when pandemic started i decided to go back to django learning during quarantine. Two months i spend on reading books and watching videos. Finally, i decided to practice my skills by doing my own project and i decided to do something which is not really regular.
I've been developing this web app for about half a year. I had a lot of errors and i've been solving them for weeks. Sometimes i just wanted to quit it, a specially in a summer time.
But finally i finished it. That was a happy day.

Check attached video to see the whole process of using this web app.

Functions:

- Fully custom admin panel for users
- Registration and Auth
- Registration and Auth by Vkontakte (Russian social app)
- Receive mail when you registered
- Every person has own personal link to his card
- Change password
- Receive mail to change password if you forgot it

The user has the opportunity to create his own card and add:

- Avatar
- Heading
- Description
- Large direct call button
- Slider of quick links to social networks, instant messengers, mail and more
- YouTube video gallery
- Picture gallery
- Price table with names and categories
- Frequently asked questions and answers to them
- Change the background color of your page

The principle is that you need to create a block, and then choose which module will be in the block.
All modules and blocks can be named whatever you want, swap them in the queue and, if desired, everything can be edited (colors, icons, names, order, etc.).

The main idea and idea of ​​the blocks is that they can be collapsed to save space. To do this, in the control panel when creating a block, you can select the 'Collapse' option.

Example of a card 'django-links.herokuapp.com/erik'
One tiny nuance, the heroku server deletes media files that the user uploads himself, so when you watch the 'sample user card' or create your own, your avatar will disappear after a while. To avoid this, I need to connect a separate storage for media files and spend money on it, so I don't see any sense in this yet.

Check this video to see the whole process of using this web app - https://youtu.be/cAAFygMsDaM
