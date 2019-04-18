# from sklearn import preprocessing
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns; sns.set()  
# import matplotlib.pyplot as plt

from .models import Song, User, UserTopTracks

def make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode((client_id + ':' + client_secret).encode('ascii'))
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

class Recommender(object):

    def __init__(self, user_id):

        self.user_id = user_id


    def get_user_songs(self):

        user_songs = UserTopTracks.objects.filter(user_id = self.user_id)

        other_users_toptracks = UserTopTracks.objects.all().exclude(user_id = self.user_id)

        all_other_users = User.objects.all().exclude(id = self.user_id)

        grouped_by_user = []
        for user_id in all_other_users:
            this_user = []
            for track in other_users_toptracks:
                if track.user_id == user_id:
                    this_user.append(track.song_id.title)
            grouped_by_user.append(this_user)


        # matches = []
        # for playlist in grouped_by_user:
        #     playlist = set(playlist)
        #     if len(playlist.intersection(user_songs)) > 1:
        #         matches.append(playlist.difference(this_user_songs))

        return(grouped_by_user[0])