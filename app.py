from flask import Flask,render_template,request
import pickle
import pandas as pd
import numpy as np
import pickle
import json
import requests

movies=pd.read_csv(r"C:\Users\kannu\OneDrive\Desktop\DataScience\Projects\Movie_Recommender_System\datasets\movies.csv")
with open(r"C:\Users\kannu\OneDrive\Desktop\DataScience\Projects\Movie_Recommender_System\datasets\similarity.pkl","rb") as file:
    cv_similarity=pickle.load(file)



new_movies=pd.read_csv(r'C:\Users\kannu\OneDrive\Desktop\DataScience\Projects\Movie_Recommender_System\datasets\new_movies.csv')
new_movies.drop(new_movies[new_movies['id_x']==333355].index[0],axis=0,inplace=True)







app=Flask(__name__)
@app.route('/')
def home():
    def genre(data):
        if data:
            return str(data).split()[0].lower()

    
    

    new_movies["new_genre"]=new_movies['genres_x'].apply(genre)
    action=new_movies.groupby('new_genre').get_group("action").sort_values('vote_average',ascending=False)[["id_x","title",'vote_average']][:8]
    animation=new_movies.groupby('new_genre').get_group("animation").sort_values('vote_average',ascending=False)[["id_x","title",'vote_average']][:8]
    SciFi=new_movies.groupby('new_genre').get_group("sciencefiction").sort_values('vote_average',ascending=False)[["id_x","title",'vote_average']][:8]
    romance=new_movies.groupby('new_genre').get_group("romance").sort_values('vote_average',ascending=False)[["id_x","title",'vote_average']][:8]
    action_title=[]
    action_link=[]
    action_rating=[]
    for id_,title,rat in action.values:
        action_title.append(title)
        action_rating.append(rat)
        try:
            link=json.loads(requests.get(r"https://api.themoviedb.org/3/movie/"+str(id_)+r"?api_key=7ab54985896c47067dda1312d9b6add1").text)['poster_path']
        except:
            pass
        complete_link="https://image.tmdb.org/t/p/original/"+link
        action_link.append(complete_link)

    action_dict={'title':action_title,"link":action_link,"rating":action_rating}
    action_df=pd.DataFrame(action_dict)

    animation_title=[]
    animation_link=[]
    animation_rating=[]
    for id_,title,rat in animation.values:
        animation_title.append(title)
        animation_rating.append(rat)
        try:
            link=json.loads(requests.get(r"https://api.themoviedb.org/3/movie/"+str(id_)+r"?api_key=7ab54985896c47067dda1312d9b6add1").text)['poster_path']
        except:
            pass
        complete_link="https://image.tmdb.org/t/p/original/"+link
        animation_link.append(complete_link)
    
    animation_dict={'title':animation_title,"link":animation_link,"rating":animation_rating}
    animation_df=pd.DataFrame(animation_dict)

    SciFi_title=[]
    SciFi_link=[]
    SciFi_rating=[]
    for id_,title,rat in SciFi.values:
        SciFi_title.append(title)
        SciFi_rating.append(rat)
        try:
            link=json.loads(requests.get(r"https://api.themoviedb.org/3/movie/"+str(id_)+r"?api_key=7ab54985896c47067dda1312d9b6add1").text)['poster_path']
        except:
            pass
        complete_link="https://image.tmdb.org/t/p/original/"+link
        SciFi_link.append(complete_link)

    SciFi_dict={'title':SciFi_title,"link":SciFi_link,"rating":SciFi_rating}
    SciFi_df=pd.DataFrame(SciFi_dict)


    romance_title=[]
    romance_link=[]
    romance_rating=[]
    for id_,title,rat in romance.values:
        romance_title.append(title)
        romance_rating.append(rat)
        try:
            link=json.loads(requests.get(r"https://api.themoviedb.org/3/movie/"+str(id_)+r"?api_key=7ab54985896c47067dda1312d9b6add1").text)['poster_path']
        except:
            pass
        complete_link="https://image.tmdb.org/t/p/original/"+link
        romance_link.append(complete_link)
    
    romance_dict={'title':romance_title,"link":romance_link,"rating":romance_rating}
    romance_df=pd.DataFrame(romance_dict)

    return render_template ('index.html',action_df=action_df,animation_df=animation_df,SciFi_df=SciFi_df,romance_df=romance_df)

@app.route("/results",methods=["GET","POST"])
def results():
    title=request.form['movie_name']
    # Using contains so that any movie keyword can be checked.
    if len(movies[movies['title'].apply(lambda x: x.lower()).str.contains(title.lower())]):
        index=movies[movies['title'].apply(lambda x: x.lower()).str.contains(title.lower())].index[0]
        similarity=list(enumerate(cv_similarity[index]))
        similar_5=sorted(similarity,reverse=True,key=lambda x:x[1])[0:10]
        movie_name=[]
        movie_link=[]
        rating=[]
        for data in similar_5:
            movie_name.append(movies['title'][data[0]])
            
            try:
                link=json.loads(requests.get(r"https://api.themoviedb.org/3/movie/"+str(movies['id'][data[0]])+r"?api_key=7ab54985896c47067dda1312d9b6add1").text)['poster_path']
            except:
                pass
            complete_link="https://image.tmdb.org/t/p/original/"+link
            movie_link.append(complete_link)
            rating.append(movies['vote_average'][data[0]])

        recomm_dict={"id":movie_link,"name":movie_name,"rating":rating}
        recomm_df=pd.DataFrame(recomm_dict)
        movie=recomm_df.iloc[0:1,:]
           
        return render_template("test.html",recomm_df=recomm_df.iloc[1:,],movie=movie)
    else:
         return render_template('not_found.html')



if __name__=="__main__":
 app.run(debug=True)