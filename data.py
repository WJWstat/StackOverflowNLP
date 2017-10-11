def print_thread(thread):
    question = thread[0]
    answers = thread[1:]

    print("Question:")
    print("")
    print(question["Body"].strip())

    print("")
    print("======")
    print("")

    print("Answers:")
    for ans in answers:
        print("")
        print("----")
        print(ans["Body"].strip())
