# Lesson 3.4: Make Classes
# Mini-Project: Movies Website

# In this file, you will define instances of the class Movie defined
# in media.py. After you follow along with Kunal, make some instances
# of your own!

# After you run this code, open the file fresh_tomatoes.html to
# see your webpage!

import media
import fresh_tomatoes

# My favorite movies
twenty_one = media.Movie('21',
                         'The MIT students play card in Las Vegas Casinos',
                         'https://upload.wikimedia.org/wikipedia/en/thumb/a/a8/\
                         21_%282008_film%29.jpg/220px-21_%282008_film%29.jpg',
                         'https://www.youtube.com/watch?v=I3HpXzaewlM')

the_nightmare_before_christmas = media.Movie(
    'The Nightmare Before Christmas',
    'The story of Jack Skellington, a resident from "Halloween Town" who \
    stumbles through a portal to "Christmas Town" and decides to \
    celebrate the holiday, with some dastardly and comical consequences.',
    'https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/\
    The_nightmare_before_christmas_poster.jpg/220px-The_nightmare_before_\
    christmas_poster.jpg',
    'https://www.youtube.com/watch?v=wr6N_hZyBCk'
    )

iron_man_1 = media.Movie(
    'Iron Man',
    'Marvel hero Iron Man',
    'https://upload.wikimedia.org/wikipedia/en/thumb/7/70/Ironmanposter.JPG/\
    220px-Ironmanposter.JPG',
    'https://www.youtube.com/watch?v=8hYlB38asDY'
    )

iron_man_2 = media.Movie(
    'Iron Man 2',
    'Marvel hero Iron Man',
    'https://upload.wikimedia.org/wikipedia/en/thumb/e/ed/\
    Iron_Man_2_poster.jpg/220px-Iron_Man_2_poster.jpg',
    'https://www.youtube.com/watch?v=BoohRoVA9WQ'
    )


iron_man_3 = media.Movie(
    'Iron Man 3',
    'Marvel hero Iron Man',
    'https://upload.wikimedia.org/wikipedia/en/thumb/d/d5/\
    Iron_Man_3_theatrical_poster.jpg/220px-Iron_Man_3_\
    theatrical_poster.jpg',
    'https://www.youtube.com/watch?v=oYSD2VQagc4'
    )

deadpool = media.Movie(
    'DeadPool',
    'Antihero Deadpool hunts the man who nearly destroyed his life \
    while also trying to reunite with his lost love.',
    'https://upload.wikimedia.org/wikipedia/en/thumb/4/46/\
    Deadpool_poster.jpg/220px-Deadpool_poster.jpg',
    'https://www.youtube.com/watch?v=ONHBaC-pfsk'
    )

jumper = media.Movie(
    'Jumper',
    'A young man capable of teleporting as he is chased by \
    a secret society intent on killing him.',
    'https://upload.wikimedia.org/wikipedia/en/thumb/3/37/\
    Jumperposter.jpg/215px-Jumperposter.jpg',
    'https://www.youtube.com/watch?v=X5ZNG3Oveh4'
    )


# Instructor's favorite movie
'''toy_story = media.Movie('Toy Story',
                        'A stroy of a boy and his toys that come to life',
                        'http://upload.wikimedia.org/wikipedia/en/1/13/\
                        Toy_Story.jpg',
                        'https://www.youtube.com/watch?v=vwyZH85NQC4')

avatar = media.Movie('Avatar',
                     'A marine on an alien planet',
                     'http://upload.wikimedia.org/wikipedia/id/b/b0/\
                     Avatar-Teaser-Poster.jpg',
                     'https://www.youtube.com/watch?v=5PSNL1qE6VY')'''


movies = [
    iron_man_1, iron_man_2, iron_man_3, deadpool,
    jumper, twenty_one, the_nightmare_before_christmas
    ]
fresh_tomatoes.open_movies_page(movies)
