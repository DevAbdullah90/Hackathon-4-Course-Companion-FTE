from pypdf import PdfReader

reader = PdfReader("../Course Companion FTE Hackathon IV.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully wrote requirements.txt")
