#	 
# Database access functions for the web forum.
#   

import time
import psycopg2
import bleach

## Database connection
DB = "dbname=forum" 
## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    conn = psycopg2.connect(DB)
    cursor = conn.cursor()
    cursor.execute("select time, content from posts order by time desc;")
    records= cursor.fetchall()
    print "Records:"
    print records
#    conn.close()
    posts = []
    for r in records:
    	posts.append({'time': r[0], 'content': r[1]})
    #print posts
    #posts.sort(key=lambda row: row['time'], reverse=True)
    #return dict(posts)
    return posts
## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    content = bleach.clean(content)
    t = time.strftime('%c', time.localtime())
    conn = psycopg2.connect(DB)
    cursor = conn.cursor()
    safeTuple = (t,content)
    cursor.execute('INSERT into posts(time, content) VALUES (%s, %s)  ', safeTuple)
    conn.commit()
    conn.close()
    #DB.append((t, content))
    #DB.commit()
