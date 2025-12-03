REPORT = []

def log_step(desc, status="PASS"):
    REPORT.append((desc, status))
    print(f"{desc}: {status}")
