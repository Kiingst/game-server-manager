import os

#run.py only creates and starts the application 
#import create_app from app

from app import create_app 


app = create_app()





if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)