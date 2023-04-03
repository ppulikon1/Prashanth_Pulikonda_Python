Name: Prashanth Pulikonda
Stevens Username: pppulikon

Github URL: https://github.com/ppulikon1/Prashanth_Pulikonda_Python

Estimated hours per day: 6-8 hours. For the whole project, it takes almost 50-70 hours.

Testing code: I tried to run GitHub automation but I couldn't get it to work, so I did manual testing. Doing manual testing took a long time for me to complete the project implementation.

Bugs and issues: Before the submission day, I had implemented the game over logic through assets map, but when making changes to the game code on the submission day, I got completely stuck. Before 1 hour of submission, I gave up and implemented a hard-coded game over function. I also had implemented lock doors and unlock doors, but I encountered errors while uploading into gradescope, so I removed everything and focused on the core gameplay.

Bugs resolved:

1) Without items key in dictionaries, if we try to access items with get verb or drop verb, it gives an error. I overcame this by adding a key at the time of the player trying to access items from dictionaries.

2)Implementing abbreviations took a lot of time for me to do. First, I implemented exits room, and later, I did the same for get verbs too.
Three extensions:

1) go

2) get

3) drop

1) With go verb, we can access the rooms from one room to another.

2) With get verb, we can get items from the room.

3) With drop verb, we can drop items from inventory. If there is nothing to drop, it shows "You're not carrying anything."

Coming to my map and gameplay:
I had implemented the following extensions:

1) go...
2) get...
3) drop...
4) look
5) inventory
6) help
7) quit
8) Directions become verbs
9) Abbreviations for verbs, directions, and items
10) you can call verbs with abbreviations eg: look as loo

My Game Play :

My gameplay is simple the player has to load choose.map. It's a simple map with four rooms, and you can move from one room to another with go or with the room name. You can look, drop items, pick items, and see inventory.

Winning and losing conditions:
The game starts in the white room.

1) You have to choose go east.
2) You will be in the red room.
3) You have to go north.
4) You are in the green room, and you have to choose which items to pick. The items will decide whether you win or lose the game.
5) After picking items, you have to go west.
6) Entering the blue room with the items, the game decides your winning.