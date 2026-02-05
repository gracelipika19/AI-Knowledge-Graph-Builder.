from groq import Groq

class RagAnswer:
    def __init__(self, hybrid, api_key):
        self.hybrid = hybrid
        self.client = Groq(api_key=api_key)

    def ask(self, q):
        ctx = self.hybrid.query(q)
        prompt = self.build_prompt(q, ctx)

        resp = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message.content

    def build_prompt(self, q, ctx):
        t=f"USER QUESTION: {q}\n\nGRAPH CONTEXT:\n"
        for g in ctx["graph"]:
            t+=f"- {g['neighbor']} ({g['rel']})\n"
        t+="\nTEXT CONTEXT:\n"
        for v in ctx["vector"][:3]:
            t+=f"- {v['meta']['text'][:200]}...\n"
        t+="\nUse above facts to answer concisely."
        return t
