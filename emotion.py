import text2emotion as te


def emotion_mining(data):
    df = data.iloc[:20,:]
    
    emotion_list = []
    

    for line in df["Review_content"]:
        emotion_list.append(te.get_emotion(line))

        
    var = list(emotion_list[0].keys())
    for item in var:
        df[item] = [x[item] for x in emotion_list]

    emot_list = []
    for i in range(len(df)):
        person = {}
        person["Name"] = df["Name"][i]
        person["Angry"] = df["Angry"][i]
        person["Happy"] = df["Happy"][i]
        person["Sad"] = df["Sad"][i]
        person["Fear"] = df["Fear"][i]
        person["Surprise"] = df["Surprise"][i]
        emot_list.append(person)
        print(emot_list)



    return emot_list