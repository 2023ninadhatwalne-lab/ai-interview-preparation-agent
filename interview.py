import random

TOPICS = ["Python", "SQL", "Machine Learning", "NLP", "RAG", "FastAPI & APIs", "Cloud & DevOps", "System Design", "Data Structures & Algorithms", "OOP & Java"]

ROLE_PRESETS = {
    "Python Developer": ["Python", "SQL", "OOP & Java", "FastAPI & APIs", "Data Structures & Algorithms"],
    "Machine Learning Engineer": ["Python", "Machine Learning", "NLP", "SQL", "RAG"],
    "AI / NLP Engineer": ["Python", "Machine Learning", "NLP", "RAG", "FastAPI & APIs"],
    "Data Engineer": ["Python", "SQL", "Cloud & DevOps", "System Design"],
    "Backend Developer": ["Python", "SQL", "FastAPI & APIs", "System Design", "Cloud & DevOps"],
    "Software Engineer": ["Data Structures & Algorithms", "OOP & Java", "SQL", "System Design", "Python"],
}

BANK = {
"Python": [
("What is the difference between a list, tuple, set, and dictionary in Python?", "easy", ["mutable","immutable","unique","key","value","ordered"]),
("Explain Python decorators and give a practical use case.", "medium", ["function","wrapper","@","arguments","logging","authentication"]),
("How does Python manage memory and what is garbage collection?", "medium", ["reference count","heap","garbage collection","cyclic","memory"]),
],
"SQL": [
("Explain INNER JOIN versus LEFT JOIN with an example.", "easy", ["matching","rows","left","null","join"]),
("What is the difference between WHERE and HAVING?", "easy", ["rows","groups","aggregate","group by","filter"]),
("How would you find the second-highest salary in each department?", "medium", ["partition","rank","dense_rank","department","salary"]),
],
"Machine Learning": [
("Explain the bias-variance tradeoff.", "medium", ["bias","variance","underfitting","overfitting","generalization"]),
("How do you handle an imbalanced classification dataset?", "medium", ["class weight","resampling","precision","recall","f1","stratified"]),
("What is the difference between bagging and boosting?", "medium", ["parallel","sequential","variance","bias","ensemble"]),
],
"NLP": [
("Explain tokenization, stemming, and lemmatization.", "easy", ["token","word","root","lemma","context"]),
("What is TF-IDF and why is it useful?", "easy", ["term frequency","inverse document frequency","rare","document","weight"]),
("How does attention work in a Transformer?", "hard", ["query","key","value","attention","weight","context"]),
],
"RAG": [
("Describe the end-to-end architecture of a Retrieval-Augmented Generation system.", "medium", ["chunk","embedding","vector","retrieval","context","generation"]),
("How would you evaluate a RAG system?", "hard", ["recall","precision","faithfulness","relevance","grounded","latency"]),
("What is the difference between sparse and dense retrieval?", "medium", ["BM25","keyword","embedding","semantic","vector"]),
],
"FastAPI & APIs": [
("What is the difference between GET, POST, PUT, and PATCH?", "easy", ["retrieve","create","replace","partial","idempotent"]),
("How does dependency injection work in FastAPI?", "medium", ["depends","dependency","reuse","validation","request"]),
("How would you secure a REST API?", "medium", ["authentication","authorization","JWT","HTTPS","validation","rate"]),
],
"Cloud & DevOps": [
("Explain Docker images and containers.", "easy", ["image","container","isolated","runtime","layers"]),
("Describe a CI/CD pipeline for deploying an API.", "medium", ["build","test","deploy","pipeline","monitor","rollback"]),
("A Kubernetes deployment is healthy but the app is unreachable. How do you debug it?", "hard", ["service","selector","port","ingress","logs","probe"]),
],
"System Design": [
("How would you design a URL shortening service?", "medium", ["hash","database","cache","redirect","collision","scale"]),
("How would you design a system that handles sudden traffic spikes?", "hard", ["load balancer","cache","queue","autoscaling","database","monitor"]),
("Explain horizontal versus vertical scaling.", "easy", ["machines","resources","instances","scale","capacity"]),
],
"Data Structures & Algorithms": [
("Explain the two-pointer technique and when you would use it.", "easy", ["pointers","sorted","array","linear","complexity"]),
("How would you detect a cycle in a linked list?", "medium", ["slow","fast","pointer","Floyd","cycle"]),
("Explain the time complexity of binary search and why it is logarithmic.", "easy", ["sorted","half","logarithmic","O(log n)","search"]),
],
"OOP & Java": [
("Explain the four pillars of object-oriented programming.", "easy", ["encapsulation","inheritance","polymorphism","abstraction"]),
("What is the difference between an interface and an abstract class in Java?", "medium", ["contract","implementation","multiple","state","abstract"]),
("How does HashMap work internally in Java?", "hard", ["hash","bucket","collision","equals","key","tree"]),
],
}

def generate_question(role, topics, level="Fresher"):
    topic = random.choice(topics or ROLE_PRESETS.get(role, TOPICS))
    q, difficulty, keywords = random.choice(BANK.get(topic, BANK["Python"]))
    if level == "Fresher" and difficulty == "hard": difficulty = "medium"
    return {"topic":topic, "question":q, "difficulty":difficulty, "keywords":keywords}

def evaluate_answer(question, answer):
    text = answer.lower()
    keywords = question["keywords"]
    found = [k for k in keywords if k.lower() in text]
    coverage = len(found) / max(1, len(keywords))
    words = len(answer.split())
    structure = min(1, words / 100)
    technical = round(min(10, 2 + coverage * 8), 1)
    communication = round(min(10, 3 + structure * 4 + (1 if any(x in text for x in ["for example","because","therefore","first","then"]) else 0)), 1)
    score = round(technical * .75 + communication * .25, 1)
    missing = [k for k in keywords if k not in found]
    strengths = [f"You covered {len(found)} of {len(keywords)} key concepts."]
    if words >= 80: strengths.append("Your answer has enough detail to assess.")
    improvements = []
    if coverage < .6: improvements.append("Add the missing technical concepts: " + ", ".join(missing[:5]) + ".")
    if words < 60: improvements.append("Expand the explanation with a short example and explain why the concept matters.")
    if not improvements: improvements.append("Add a concrete real-world example and mention trade-offs or complexity.")
    model = f"Start with a one-sentence definition of {question['topic']}. Explain the key steps or components, cover {', '.join(keywords[:4])}, then give a practical example and mention one limitation or trade-off."
    return {"score":score,"technical":technical,"communication":communication,"strengths":strengths,"improvements":improvements,"keywords":keywords,"model_answer":model}

def build_revision(topic):
    return [f"Review the core definition and terminology of {topic}.",
            f"Explain one practical {topic} example aloud in 2 minutes.",
            f"Solve two beginner and one intermediate interview question on {topic}.",
            "Write a short summary from memory, then compare it with your notes."]
