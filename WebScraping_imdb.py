### import all packages here
import numpy as np 
import pandas as pd 
import requests 
from matplotlib import pyplot as plt 
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings("ignore")

url = "https://www.imdb.com/chart/toptv"
### Top rated Tv shows by imdb 
class Webscrap(object):
    """
    Blueprint for webscraping html file. 
    """
    def __init__(self,url):
        """
        init:
            This is a constructor which takes in input values for the method 

        Arg:
            url: the url links to the html data. This is unstructure data of top-rated tv shows by imdb. 
        """
        self.url = url 
    
    def tvshows_actors(self,input="td.titleColumn a"):

        """
        input: 
            Takes takes a the tags of interest for extraction. 
            This does operation on the inner tags of the tv shows tags  
        operation:
            Extract all text in the file. after the html is collected.
        return:
            Returns the value for movietitle and actors from the tags 


        """
        tags_actors_movie = self.html(input)
        movietitle = [movie.text for movie in tags_actors_movie]
        actors = [actor["title"] for actor in tags_actors_movie]

        return movietitle , actors 

    def get_year(self,input="td.titleColumn"):

        """
        input:
            Takes in the Tv show tags. 
        return: 
            The year of of the tv show. List of years of show.
        """
        
        textvalues = self.html(input)
        years = []
        for year in textvalues: ### perform an iteration over the text. 
            val_year = year.text.split()[-1]
            years.append(int(val_year[1:5]))
        """
        Return:
            The list of  years 
        """
        return years
    
    def rating_tvshow(self,input="td.posterColumn span[name=ir]"):
        """
        Input:
            Takes the rating tags as input.
        Return:
            returns list of float values. 
        """
        ratingtvshow = self.html(input)
        rating_lists = [float(rating["data-value"]) for rating in ratingtvshow] ### return the list float of rating. 

        """
        Return:
            list of float values showing the rating of tvshow by imdb
        """

        return rating_lists



    
    def html(self,input):
        """
        Method: 
            To retrieve the html file 
        return: 
            Return the values for 
        """
        response = requests.get(self.url)
        html = response.text
        htmlfile = BeautifulSoup(html,"html.parser")
        text = htmlfile.select(input)
        return text

    

def main():
    """
    Operation:
        Runs the main operation.
    """
    webscrap = Webscrap(url="https://www.imdb.com/chart/toptv")

    tvshows, actors = webscrap.tvshows_actors("td.titleColumn a")
    years = webscrap.get_year("td.titleColumn")
    rating = webscrap.rating_tvshow("td.posterColumn span[name=ir]")
    


    done = True 
    ### generate a random tvshow for the user 
    while  done:
        index = np.random.randint(0,len(years))
        print(f"availabe show {tvshows[index]} produced in the year {years[index]} by {actors[index]} with rating {rating[index]}")

        request = input("Do you like to view another tvshows y/[n]?: ") ## request to generate another tvshow available 
        if request == "n": ### if the input is no then you break 
           break
    ### Create a dataframe for the extract data from the webpage. 
    Data = pd.DataFrame({
        "Tv shows": tvshows,
        "Actors" : actors,
        "Rating" : rating, 

    },index = years)
    print(Data.head())
    Data.to_csv("tvshows_data.csv")

    ### Visualize the rating of tvshows over the years. 
    for index, tvshow in enumerate(tvshows):
        plt.scatter(years[index],rating[index])
        plt.text(years[index] + .03,rating[index] + .03,tvshow,fontsize=7)
    plt.xlabel("year of tvshows")
    plt.ylabel("tv shows")
    plt.title("Rating of tv shows over the years")
    plt.savefig("tvshow.png")
    plt.show()




 



### Run the main function using the condition.
if __name__ == "__main__":
    main()