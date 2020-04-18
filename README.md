# Elimination
The purpose of this software will be to administer a game of Assassin. This will
a be web-based service that manages players activity. The system will serve the
role of Game Admin in the traditional game of Assassin. The appeal of this
game is that it is live-action. This is not a game which involves a large amount
of screen time which makes it an outlier in the gaming market. This is a social
game full of tactics, laughs, and uneasiness.

# Game Description
Assassin is a live-action game in which players try to eliminate one another in
order to become the last man standing. Game-play may occur for hours and
there are no boundaries. This game is played during a regular day, you must
evade your attacker while going about a normal day. The Game admin will
begin the game by inviting a large group of users to review the rules and join
the game. Each player is assigned a target. Upon eliminating a target, you are
then given the person your target was supposed to eliminate. As in the figure
one, after Jeff eliminates Jacob he is assigned Jack. The detailed rules, such
as rules of Elimination, vary from group to group. The admin will declare the
ruleset and the players will agree before joining the game. Some groups play
with Nerf guns, others ”poison” there target by marking on the bottom of their
target’s cup before they drink. Be creative but also be safe.

# Build instructions
insure you have an updated version of pip "python package manager"

1) clone the repo\
    $git clone https://github.com/masonamccallum/Elimination.git
2) go into that directory\
    $cd Elimination
3) create virtual Environment\
   python3 -m venv <name of env>\
    $python3 -m venv venv
4) activate Environment\
    $source venv/bin/activate\
5) download requirements\
    $pip install -r docs/requirements.txt
6) set environment variables\
    $export FLASK_APP="flasky.py"
7) start flask\
    $flask run --host 0.0.0.0
8) when done stop the server\
    Ctrl-C
9) stop the virtual environment\
    $deactivate

