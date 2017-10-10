import pickle
import xml.etree.ElementTree as ET

"""
Useful XML Attributes & Values in Posts.xml (non-exhaustive):

1. ID
2. PostTypeID: '1' (Question), '2' (Answer)
3. AcceptedAnswerID (if PostTypeID = '1')
4. ParentID (if PostTypeID = '2')
5. AnswerCount (nullable)
6. Tags: '&lt;tag_name&gt;' repeated (nullable)

37,215,530 lines. 37,215,527 post <row>s.
"""

threads_threshold = 500
tag = "<java>"  # ET parses &lt; and &gt;

question_posts = set()
threads = {}
num_of_threads = 0

# Get threads from XML file.
for event, elem in ET.iterparse('data/uncompressed/Posts.xml'):
    if elem.tag == "row":
        attr = elem.attrib

        # Add question post if it has needed tag & enough answers.
        if attr["PostTypeId"] == "1" and attr["Tags"].find(tag) != -1:
            if int(attr["AnswerCount"]) >= 1:
                threads[attr["Id"]] = []
                threads[attr["Id"]].append(attr)
                question_posts.add(attr["Id"])
                num_of_threads += 1
        # Add answer post if question post has been added.
        elif attr["PostTypeId"] == "2" and attr["ParentId"] in question_posts:
            threads[attr["ParentId"]].append(attr)

        if num_of_threads >= threads_threshold:
            # Check for valid threads (i.e. >= 2 posts)
            num_of_valid_threads = 0
            for posts in list(threads.values()):
                if len(posts) >= 2:
                    num_of_valid_threads += 1

            # Stop searching once threshold is met.
            if num_of_valid_threads >= threads_threshold:
                break

# Delete threads that are not valid.
num_of_posts = 0
for questionId, posts in list(threads.items()):
    if len(posts) < 2:
        del threads[questionId]
    else:
        num_of_posts += len(posts)

# Print dataset statistics.
print("Threads: %d" % (len(threads)))
print("Posts: %d" % (num_of_posts))

# Pickle threads dataset.
with open("pickles/threads.pkl", "wb") as f:
    pickle.dump(threads, f)
