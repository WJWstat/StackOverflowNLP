import pickle
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

"""
Useful XML Attributes & Values in Posts.xml (non-exhaustive):

1. ID
2. Body
3. PostTypeID: '1' (Question), '2' (Answer)
4. AcceptedAnswerID (if PostTypeID = '1')
5. ParentID (if PostTypeID = '2')
6. AnswerCount (nullable)
7. Tags: '&lt;tag_name&gt;' repeated (nullable)

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

# Delete threads that are not valid and analyze the dataset.
num_of_posts = 0
thread_stats = {}
for question_id, posts in list(threads.items()):
    posts_in_thread = len(posts)

    if posts_in_thread < 2:
        del threads[question_id]
    else:
        num_of_posts += posts_in_thread

        if posts_in_thread in thread_stats:
            thread_stats[posts_in_thread] += 1
        else:
            thread_stats[posts_in_thread] = 1

# Print dataset statistics.
print("Threads: %d" % (len(threads)))
print("Posts: %d" % (num_of_posts))
print("Questions: %d" % (len(threads)))
print("Answers: %d" % (num_of_posts - len(threads)))
print("Thread Count per No. of Posts: %s" % (str(thread_stats)))

# Plot thread_stats.
plt.figure()
plt.bar(list(thread_stats.keys()), list(thread_stats.values()))
plt.xlabel("No. of Posts")
plt.ylabel("No. of Threads")
plt.tight_layout()
plt.savefig("plots/thread_stats.png", dpi=800)
plt.close("all")

# Pickle data.
with open("pickles/threads.pkl", "wb") as f:
    pickle.dump(threads, f)
