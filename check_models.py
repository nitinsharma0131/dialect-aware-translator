from google import genai

client = genai.Client(api_key="AIzaSyAd-3ciZd9tzGOrj7robtHQvRyMvTWZ4_A")

print("Models available to this API key:\n")

try:
    models = list(client.models.list())
    if not models:
        print("❌ No models found")
    else:
        for m in models:
            print("✅", m.name)
except Exception as e:
    print("❌ Error:", e)
