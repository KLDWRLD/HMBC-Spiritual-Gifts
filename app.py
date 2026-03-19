from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "change-this-key"

# 72 questions (replace with your real text)
QUESTIONS = [
    "I like organizing services and events.",
    "I am interested in starting new churches.",
    "I enjoy working with my hands.",
    "I can tell when someone is insincere.",
    "I pray daily for people who don’t know Jesus.",
    "Encouraging others is a high priority in my life.",
    "I trust God to provide for my daily needs.",
    "I am passionate about financially investing in the Kingdom of God.",
    "I look for opportunities to pray for the sick.",
    "I enjoy doing little things that others typically do not enjoy.",
    "I often have people over to my house.",
    "I enjoy spending hours in prayer for other people.",
    "Education is very important to me.",
    "I tend to motivate others to get involved.",
    "I hurt when I see others hurting.",
    "I believe God will use me to enact His miracles.",
    "I enjoy sharing the Gospel with other people groups and nationalities.",
    "I’ve devoted considerable time to mastering my voice and/or musical instrument.",
    "Caring for the hurting is one of my highest priorities.",
    "I get frustrated when people knowingly sin.",
    "I enjoy serving behind the scenes.",
    "I like creating outlines of the Bible.",
    "God has used me to interpret what someone speaking in tongues is saying.",
    "I enjoy the book of Proverbs more than any other book in the Bible.",
    "I am passionate about managing details.",
    "I like to help start new ministry projects.",
    "I consider myself a craftsman or craftswoman.",
    "I sense when situations are spiritually unhealthy.",
    "I am greatly motivated by seeing people who don’t know God be saved.",
    "I come across as loving and caring.",
    "Asking God for a list of seemingly impossible things is exciting to me.",
    "I find ways to give offerings above my tithe.",
    "I believe miraculous healing is possible and still happens.",
    "Helping others is one of my greatest motivations.",
    "Creating a warm and welcoming environment is important to me.",
    "I am burdened to pray for situations affecting the world.",
    "People come to me to learn more about God and the Bible.",
    "I prefer to take the lead whenever possible.",
    "I'm very sensitive to sad stories.",
    "Miracles often happen when I'm nearby.",
    "The idea of living in another country to benefit the Gospel is exciting to me.",
    "I desire to serve the church through worship.",
    "I enjoy connecting, caring for, and coaching others.",
    "Confronting someone about a sin in their life is important to me.",
    "It bothers me when people sit around and do nothing.",
    "I share Biblical truth with others to help them grow.",
    "I pray in tongues daily.",
    "When I study Scripture, I receive unique insights from God.",
    "Creating a task list is easy and enjoyable for me.",
    "I am attracted to ministries that start new churches.",
    "Building something with my hands is very satisfying to me.",
    "I can pinpoint issues or problems quickly.",
    "Sharing the Gospel with someone I do not know is exciting and natural for me.",
    "I look for ways to encourage other people.",
    "I trust that God has my back in every situation.",
    "I want to make more money so that I can give more.",
    "God has used me to bring healing to those who are sick.",
    "Being a part of the process is fulfilling to me.",
    "I tend to make total strangers feel at home.",
    "People often ask me to pray for them.",
    "I enjoy knowing Biblical details and helping others understand them too.",
    "I delegate responsibilities to accomplish tasks.",
    "I am motivated to help people in need.",
    "I have a constant hunger to see God's miraculous power.",
    "I focus a lot on reaching the lost for Christ.",
    "I gain my deepest satisfaction through leading others in vocal or instrumental worship.",
    "I enjoy helping people who are going through a difficult time.",
    "I enjoy hearing passionate and clear preaching of God's Word.",
    "I like to do small things that others overlook.",
    "I prefer to teach and study the Bible topically rather than verse by verse.",
    "Praying in tongues is encouraging and important to me.",
    "When faced with difficulty, I tend to make wise decisions."
]

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:24]

LABELS = {
    'A': "Administration",
    'B': "Apostleship",
    'C': "Craftsmanship",
    'D': "Discernment",
    'E': "Evangelism",
    'F': "Exhortation",
    'G': "Faith",
    'H': "Giving",
    'I': "Healing",
    'J': "Helps",
    'K': "Hospitality",
    'L': "Intercession",
    'M': "Knowledge",
    'N': "Leadership",
    'O': "Mercy",
    'P': "Miracles",
    'Q': "Missionary",
    'R': "Music/Worship",
    'S': "Pastor/Shepherd",
    'T': "Prophecy",
    'U': "Service",
    'V': "Teaching",
    'W': "Tongues (and Interpretation)",
    'X': "Wisdom"
}

GIFT_DETAILS = {
    'A': {
        "definition": "The divine strength or ability to organize multiple tasks and groups of people to accomplish these tasks.",
        "verses": "Luke 14:28–30; Acts 6:1–7; 1 Corinthians 12:28",
        "applications": "Registration, Cool Kids Check-in, Production, Setup/Takedown"
    },
    'B': {
        "definition": "The divine strength or ability to pioneer new churches and ministries through planting, overseeing, and training.",
        "verses": "Acts 15:22–35; 1 Corinthians 12:28; 2 Corinthians 12:12; Galatians 2:7–10; Ephesians 4:11",
        "applications": "Outreach, Growth Track Host, Connect Group Leadership"
    },
    'C': {
        "definition": "The divine strength or ability to plan, build, and work with your hands in construction environments.",
        "verses": "Exodus 30:22; 31:3–11; 2 Chronicles 34:9–13; Acts 18:2–3",
        "applications": "Cool Kids, Production"
    },
    'D': {
        "definition": "The divine strength or ability to spiritually identify falsehood and distinguish between right and wrong motives.",
        "verses": "Matthew 16:21–23; Acts 5:1–11; 16:16–18; 1 Corinthians 12:10; 1 John 4:6",
        "applications": "Growth Track Host, Cool Kids Check-in, Connect Group, Host"
    },
    'E': {
        "definition": "The divine strength or ability to help non-Christians take steps toward becoming Christ followers.",
        "verses": "Acts 8:5–6, 26–40; 14:21; Ephesians 4:11–14",
        "applications": "Outreach, Connect Group Leadership"
    },
    'F': {
        "definition": "The divine strength or ability to encourage others through written or spoken word and Biblical truth.",
        "verses": "Acts 14:22; Romans 12:8; 1 Timothy 4:13; Hebrews 10:24–25",
        "applications": "Host, Events, Greeters, Growth Track Host, Cool Kids, Security, Connect Group Leadership"
    },
    'G': {
        "definition": "The divine strength or ability to believe in God for unseen supernatural results in every area of life.",
        "verses": "Acts 11:22–24; Romans 4:18–21; 1 Corinthians 12:9; Hebrews 11",
        "applications": "All Teams"
    },
    'H': {
        "definition": "The divine strength or ability to produce wealth and give generously to advance the Kingdom of God.",
        "verses": "Mark 12:41–44; Romans 12:8; 2 Corinthians 8:1–7; 9:2–7",
        "applications": "All Teams"
    },
    'I': {
        "definition": "The divine strength or ability to act in faith, prayer, and laying on of hands for healing.",
        "verses": "Acts 3:1–8; Acts 5:12–16; 1 Corinthians 12:9, 28",
        "applications": "All Teams"
    },
    'J': {
        "definition": "The divine strength or ability to work in a supportive role to accomplish ministry tasks.",
        "verses": "Mark 15:40; Acts 9:36; Romans 16:1–2; 1 Corinthians 12:28",
        "applications": "Host, Outreach, Events"
    },
    'K': {
        "definition": "The divine strength or ability to create warm, welcoming environments for others.",
        "verses": "Acts 16:14–15; Romans 12:13; 16:23; Hebrews 13:1–2; 1 Peter 4:9",
        "applications": "Host, Events, Greeters, Growth Track Host, Cool Kids, Security"
    },
    'L': {
        "definition": "The divine strength or ability to stand in the gap in prayer for someone or something.",
        "verses": "Hebrews 7:25; Colossians 1:9–12; 4:12–13; James 5:14–16",
        "applications": "Connect Group Leadership"
    },
    'M': {
        "definition": "The divine strength or ability to understand and bring clarity to situations, often with a word from God.",
        "verses": "Acts 5:1–11; 1 Corinthians 12:8; Colossians 2:2–3",
        "applications": "Connect Group Leadership, Host"
    },
    'N': {
        "definition": "The divine strength or ability to influence people while directing them toward a vision.",
        "verses": "Romans 12:8; 1 Timothy 3:1–13; 5:17; Hebrews 13:17",
        "applications": "Connect Group Leadership, All Teams"
    },
    'O': {
        "definition": "The divine strength or ability to feel empathy and care for those who are hurting.",
        "verses": "Matthew 9:35–36; Mark 9:41; Romans 12:8; 1 Thessalonians 5:14",
        "applications": "All Teams"
    },
    'P': {
        "definition": "The divine strength or ability to alter natural outcomes through prayer, faith, and divine direction.",
        "verses": "Acts 9:36–42; 19:11–12; Romans 15:18–19; 1 Corinthians 12:10, 28",
        "applications": "AM Teams"
    },
    'Q': {
        "definition": "The divine strength or ability to reach people outside your culture or nationality.",
        "verses": "Acts 8:4; 13:2–3; 22:21; Romans 10:15",
        "applications": "Outreach, Connect Group Leadership"
    },
    'R': {
        "definition": "The divine strength or ability to sing, dance, or play instruments to help others worship.",
        "verses": "Deuteronomy 31:22; 1 Samuel 16:16; 1 Chronicles 16:41–42; 2 Chronicles 5:12–13; Psalm 150",
        "applications": "Cool Kids, Worship, Connect Group Leadership"
    },
    'S': {
        "definition": "The divine strength or ability to care for the personal needs of others.",
        "verses": "John 10:1–18; Ephesians 4:11; 1 Timothy 3:1–7; 1 Peter 5:1–5",
        "applications": "Outreach, Growth Track Host, Cool Kids, Connect Group Leadership, Host"
    },
    'T': {
        "definition": "The divine strength or ability to boldly speak and bring clarity to scriptural truth.",
        "verses": "Acts 2:37–40; 7:51–53; 26:24–29; 1 Corinthians 14:1–4; 1 Thessalonians 1:5",
        "applications": "Connect Group Leadership"
    },
    'U': {
        "definition": "The divine strength or ability to do small or large tasks for the good of the church.",
        "verses": "Acts 6:1–7; Romans 12:7; Galatians 6:10; 1 Timothy 1:16–18; Titus 3:14",
        "applications": "Outreach, Host, Events"
    },
    'V': {
        "definition": "The divine strength or ability to study and teach Scripture for understanding and growth.",
        "verses": "Acts 18:24–28; Romans 12:7; 1 Corinthians 12:28; Ephesians 4:11–14",
        "applications": "Connect Group Leadership"
    },
    'W': {
        "definition": "The divine strength or ability to pray in a heavenly language and interpret tongues.",
        "verses": "Acts 2:1–13; 1 Corinthians 12:10; 14:1–14",
        "applications": "Prayer"
    },
    'X': {
        "definition": "The divine strength or ability to apply Scripture in practical ways producing fruit.",
        "verses": "Acts 6:3,10; Romans 12:8; 1 Corinthians 2:3–5",
        "applications": "Outreach, Worship, Connect Group Leadership, Host"
    }
}


@app.route("/")
def start():
    session["answers"] = []
    return redirect(url_for("question", index=0))

@app.route("/question/<int:index>", methods=["GET", "POST"])
def question(index):
    if "answers" not in session:
        session["answers"] = []

    answers = session["answers"]

    if request.method == "POST":
        value = int(request.form["value"])
        answers.append(value)
        session["answers"] = answers

        if index + 1 >= len(QUESTIONS):
            return redirect(url_for("results"))
        return redirect(url_for("question", index=index + 1))

    question_text = QUESTIONS[index]
    return render_template(
        "question.html",
        question=question_text,
        q_number=index + 1,
        total=len(QUESTIONS)
    )

def compute_scores(answers):
    group_scores = [0] * 24
    for i, val in enumerate(answers):
        group_index = i % 24
        group_scores[group_index] += val

    results = []
    for i, score in enumerate(group_scores):
        letter = LETTERS[i]
        word = LABELS.get(letter, "")
        results.append({
            "group": i + 1,
            "letter": letter,
            "word": word,
            "score": score
        })
    return results

@app.route("/results")
def results():
    answers = session.get("answers", [])
    if len(answers) != len(QUESTIONS):
        return redirect(url_for("start"))

    results = compute_scores(answers)

    # Attach gift details for high scores
    for r in results:
        if r["score"] >= 8:
            r["details"] = GIFT_DETAILS.get(r["letter"], {})

    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
