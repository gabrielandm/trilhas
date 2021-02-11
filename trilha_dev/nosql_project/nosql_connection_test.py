from pymongo import MongoClient
import pprint

client = MongoClient("mongodb+srv://login:Password123@cluster0.iaj61.mongodb.net/repo?retryWrites=true&w=majority") # Connection string
mydatabase = client['repo'] # Connection to DB
collection = mydatabase['repo_names'] # Connection to Collection

def print_all():
    for repo in collection.find():
        pprint.pprint(repo)
    return

def save_repositories(username: str):
    data = [ # Simple data creation
        {"repo_name": "fake_repo_1", "repo_user": username},
        {"repo_name": "fake_repo_2", "repo_user": username}
    ]

    collection.insert_many(data)

save_repositories("fake_username")
print_all()
