# Amanda Gomes

#  youtubeAnalysis.py searches YouTube for videos matching a search term and analyzes the data to find the top 5 videos with the highest views, highest like percentage, and highest dislike percentage

# To run from terminal window: python3 youtubeAnalysis.py 

import csv

from apiclient.discovery import build      # use build function to create a service object

import unidecode   #  need for processing text fields in the search results

# put your API key into the API_KEY field below, in quotes
API_KEY = "AIzaSyBEPLBDsdP2Pn5Mat8CYCEoblexoMY5Zk8"

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version

#  function youtube_search retrieves the YouTube records

def youtube_search(s_term, s_max):
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)

    search_response = youtube.search().list(q=s_term, part="id,snippet", maxResults=s_max).execute()

    # creating header
    with open('search.csv', 'w', newline = '') as csvfile:
        # defining fields for csv
        fields = ['Title', 'Video ID', 'View Count', 'Like Count', 'Dislike Count', 'Comment Count' ]
        # writing fields to csv
        thewriter = csv.DictWriter(csvfile, fieldnames = fields)
        thewriter.writeheader()
    # search for videos matching search term;
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                # gets title
                title = search_result["snippet"]["title"]
                title = unidecode.unidecode(title)  
                # gets video ID
                videoId = search_result["id"]["videoId"]
                # gets stats from video ID
                video_response = youtube.videos().list(id=videoId,part="statistics").execute()
                for video_results in video_response.get("items",[]):
                    # gets view count
                    viewCount = video_results["statistics"]["viewCount"]
                    # gets like count if it exists
                    if 'likeCount' not in video_results["statistics"]:
                        likeCount = 0
                    else:
                        likeCount = video_results["statistics"]["likeCount"]
                    # gets dislike count if exists
                    if 'dislikeCount' not in video_results["statistics"]:
                        dislikeCount = 0
                    else:
                        dislikeCount = video_results["statistics"]["dislikeCount"]
                    # gets comment count if it exists
                    if 'commentCount' not in video_results["statistics"]:
                        commentCount = 0
                    else:
                        commentCount = video_results["statistics"]["commentCount"]
                # writing search results to csv file
                thewriter.writerow({'Title': title, 'Video ID': videoId, 'View Count': viewCount, 'Like Count': likeCount, 'Dislike Count': dislikeCount, 'Comment Count': commentCount})

def analyze():
    with open('search.csv', 'r') as csvfile:
        videos = []
        theReader = csv.DictReader(csvfile)
         # puts data from csv into a 2D array
        for row in theReader:
            # calculates the like percentage
            likePercent = int(row['Like Count'])/int(row['View Count'])
            # calculates the dislike percentage
            dislikePercent = int(row['Dislike Count'])/int(row['View Count'])
            # adds each row from the csv file into a list
            videos.append([row['Title'], row['Video ID'], int(row['View Count']), int(row['Like Count']), int(row['Dislike Count']), int(row['Comment Count']), likePercent, dislikePercent])

        
        print("Top 5 Videos with the Highest Views")
        # sorting by views in decreasing order by looping through the first five elements in the sorted list
        videos.sort(key = lambda x : x[2], reverse = True)
        # printing out ranking
        for i in range(5):
            print(str(i + 1) + ". " + videos[i][0] + ", " + videos[i][1] + ", " + str(videos[i][2]))
        print()

        
        print("Top 5 Videos with the Highest Like Percentage")
        # sorting by likePercent in decreasing order by looping through the first five elements in the sorted list
        videos.sort(key = lambda x : x[6], reverse = True)
        # printing out ranking
        for i in range(5):
            print(str(i + 1) + ". " + videos[i][0] + ", " + videos[i][1] + ", " + str(videos[i][6]))
        print()

        
        print("Top 5 Videos with the Highest Dislike Percentage")
        # sorting by dislikePercent in decreasing order
        videos.sort(key = lambda x : x[7], reverse = True)
        # printing out ranking
        for i in range(5):
            print(str(i + 1) + ". " + videos[i][0] + ", " + videos[i][1] + ", " + str(videos[i][7]))

        return


# main routine
search_term = input("Enter a word to search: ")
search_max = int(input("Enter the maximum number of results you want to appear: "))
# printing out search term and search max
print()
print("Search Term: " + search_term)
print("Search Max: " + str(search_max))
print()
youtube_search(search_term, search_max)
analyze()   

