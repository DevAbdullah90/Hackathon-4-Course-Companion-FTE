from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import Course, Module, Chapter, Quiz

# Curriculum Data
CURRICULUM = [
    {
        "title": "Module 1: Foundations of AI Agents",
        "description": "Core concepts and architectural patterns for building autonomous systems.",
        "order": 1,
        "chapters": [
            {
                "title": "Deterministic vs Agentic",
                "slug": "deterministic-vs-agentic",
                "order": 1,
                "content": """# Deterministic vs Agentic Systems

## What implies "Deterministic"?
In traditional software engineering, we build **deterministic systems**. 
- **Input A** always leads to **Output B**.
- Logic is hard-coded: `if x > 10: do_y()`.
- Reliability comes from predictability.

## The Shift to Agentic
AI Agents introduce **probabilistic reasoning**.
- You give a **Goal** (e.g., "Plan a trip to Paris").
- The Agent decides the **Current State**, **Available Tools**, and **Next Steps**.
- The output varies based on context and the LLM's reasoning.

### Key Difference
> "Deterministic systems follow a script. Agentic systems write the script as they go."

## When to use which?
| Feature | Deterministic | Agentic |
| :--- | :--- | :--- |
| ** predictability** | High | Low/Variable |
| **Complexity** | Linear | Exponential |
| **Use Case** | Payroll, CRUD APIs | Research, creative writing, complex workflows |
""",
                "quiz": {
                    "questions": [
                        {
                            "id": "q1",
                            "text": "What is the main characteristic of a deterministic system?",
                            "options": [
                                "It uses probabilistic reasoning",
                                "Input A always leads to Output B",
                                "It writes its own script",
                                "It requires an LLM"
                            ],
                            "correct_answer": 1
                        },
                         {
                            "id": "q2",
                            "text": "Which use case is best suited for an Agentic system?",
                            "options": [
                                "Payroll processing",
                                "Simple CRUD API",
                                "Complex research with variable steps",
                                "Static website hosting"
                            ],
                            "correct_answer": 2
                        }
                    ]
                }
            },
            {
                "title": "The Loop Pattern",
                "slug": "the-loop-pattern",
                "order": 2,
                "content": """# The Agent Loop

At the heart of every agent is **The Loop**. This is the `while` loop that keeps the agent running until the goal is met.

## The OODA Loop
Adapted from military strategy (Observe, Orient, Decide, Act):
1.  **Observe**: Read user input, tool outputs, and environment state.
2.  **Orient**: Update internal context, memory, and reasoning.
3.  **Decide**: Select the next action (or Tool) to take.
4.  **Act**: Execute the tool.
5.  **Repeat**.

## Python Example
```python
while not goal_achieved:
    observation = env.observe()
    thought = llm.think(observation)
    action = llm.decide_action(thought)
    
    if action == "FINISH":
        break
        
    result = env.execute(action)
    memory.add(observation, action, result)
```

## Stopping Conditions
- Goal Achieved (Success)
- Max Iterations Reached (Timeout/Cost prevention)
- Human Intervention Required
"""
            },
             {
                "title": "Tools & Interfaces",
                "slug": "tools-and-interfaces",
                "order": 3,
                "content": """# Tools: The Agent's Hands

An LLM is a brain in a jar. **Tools** give it hands to interact with the world.

## What is a Tool?
A tool is simply a function that the LLM knows how to call. It has:
1.  **Name**: `google_search`
2.  **Description**: "Searches the web for current information."
3.  **Schema**: JSON structure of arguments (e.g., `{"query": "string"}`).

## Function Calling API
OpenAI and Anthropic have native "Function Calling" support. You pass a list of tool definitions, and the model returns a structured JSON to call them, instead of text.

### Example Tool Definition
```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"]
      }
    },
    "required": ["location"]
  }
}
```
"""
            }
        ]
    },
    {
        "title": "Module 2: Memory & Context",
        "description": "Managing state and long-term knowledge retrieval.",
        "order": 2,
        "chapters": [
            {
                "title": "Context Window Management",
                "slug": "context-window-management",
                "order": 1,
                "content": """# The Finite Context Window

Every LLM has a limit (e.g., 8k, 32k, 128k tokens). You cannot feed it infinite history.

## FIFO (First-In, First-Out)
The simplest strategy. When the conversation fills the window, you drop the oldest messages.
- **Pros**: Easy to implement.
- **Cons**: You lose early instructions or key facts from the start.

## Summarization
Periodically ask an LLM to summarize the conversation so far, and replace the detailed logs with the summary.
- **Pros**: Retains high-level context indefinitely.
- **Cons**: Details get lost; "resolution" of memory decreases.

## Selective Retention
Keep crucial messages (System Prompt, User Goals) pinned, while rotating the middle chat logs.
"""
            },
            {
                "title": "RAG: Retrieval Augmented Generation",
                "slug": "rag-fundamentals",
                "order": 2,
                "content": """# RAG (Retrieval Augmented Generation)

RAG connects your agent to external data (PDFs, Wikis, Databases).

## The Workflow
1.  **Chunking**: Split document into small pieces (e.g., 500 chars).
2.  **Embedding**: Convert text to vectors (lists of numbers) using models like `text-embedding-3-small`.
3.  **Indexing**: Store vectors in a Vector DB (Pinecone, Chroma, Qdrant).
4.  **Retrieval**: When user asks a question, embed the query and find "nearest neighbors" in the DB.
5.  **Generation**: Stuff the retrieved chunks into the prompt context.

> "Answer the user question based ONLY on the following context..."
"""
            },
            {
                "title": "Vector Databases 101",
                "slug": "vector-databases-101",
                "order": 3,
                "content": """# Vector Databases

A Vector DB is optimized for storing and querying high-dimensional vectors.

## Key Concepts
- **Dimensions**: The size of the vector (e.g., 1536 for OpenAI).
- **Metric**: How to measure distance (Cosine Similarity, Euclidean Distance, Dot Product).
- **Metadata**: Storing original text and source info alongside the vector.

## Popular Options
- **Pinecone**: Managed, scalable.
- **Chroma**: Open-source, local-first.
- **Qdrant**: Fast, Rust-based.
- **pgvector**: Postgres extension (Great for keeping data together!).
"""
            }
        ]
    },
    {
        "title": "Module 3: Advanced Patterns",
        "description": "Techniques for robust and intelligent agent behavior.",
        "order": 3,
        "chapters": [
             {
                "title": "ReAct Pattern",
                "slug": "react-pattern",
                "order": 1,
                "content": """# ReAct: Reason + Act

Proposed in the paper "ReAct: Synergizing Reasoning and Acting in Language Models".

## The Concept
Instead of just acting, the model should explicitely **Think** before it **Acts**.

## The Template
```text
Question: What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?

Thought 1: I need to search Colorado orogeny, find the area that the eastern sector extends into, then find the elevation range of the area.
Action 1: Search[Colorado orogeny]
Observation 1: The Colorado orogeny was an episode of mountain building (an orogeny) in Colorado and surrounding areas.

Thought 2: It does not mention the eastern sector. So I need to look up eastern sector.
...
```

This "Thinking" step allows the model to correct course and break down complex problems.
"""
            },
            {
                "title": "Plan-and-Solve",
                "slug": "plan-and-solve",
                "order": 2,
                "content": """# Plan-and-Solve

For very complex tasks, "thinking as you go" (ReAct) can get lost in the weeds.

## The Strategy
1.  **Plan**: First, ask the model to generate a high-level plan.
    - "First, I will research X."
    - "Second, I will write code for Y."
    - "Third, I will test it."
2.  **Execute**: Then, have the agent execute the plan step-by-step.

## Benefits
- Prevents the agent from forgetting the overall goal.
- Allows for human review of the plan before execution (Human-in-the-loop).
"""
            },
            {
                 "title": "Evaluations (Evals)",
                 "slug": "evaluations-evals",
                 "order": 3,
                 "content": """# Evaluations (Evals)

How do you know if your agent is good?

## Unit Tests for Agents
You can't assert strict string equality. You need **LLM-based assert**.
- "Did the agent provide a polite response?" -> Ask an LLM to judge (Yes/No).
- "Did the agent find the correct answer?" -> Compare against a Gold Standard.

## Frameworks
- **DeepEval**: Open-source testing framework.
- **LangSmith**: Tracing and evaluation platform by LangChain.
- **Promptfoo**: CLI for testing prompts.
"""
            }
        ]
    },
      {
        "title": "Module 4: Multi-Agent Systems",
        "description": "Orchestrating teams of specialized agents.",
        "order": 4,
        "chapters": [
             {
                "title": "Single vs Multi-Agent",
                "slug": "single-vs-multi-agent",
                "order": 1,
                "content": """# Single vs Multi-Agent

## The Generalist (Single)
One giant prompt handling everything.
- **Pros**: Simple context sharing.
- **Cons**: Gets confused easily; prompt becomes unmanageable.

## The Specialists (Multi-Agent)
Split the task into roles.
- **Researcher Agent**: Only knows how to search and summarize.
- **Writer Agent**: Only knows how to write blog posts.
- **Editor Agent**: Reviews the Writer's work.

## Handoffs
The key challenge is **handoffs**. How does the Researcher pass data to the Writer?
- **Shared State**: A global blackboard.
- **Direct Messaging**: Agents extracting outputs for the next agent's input.
"""
            },
            {
                "title": "Hierarchical Teams",
                "slug": "hierarchical-teams",
                "order": 2,
                "content": """# Hierarchical Teams (Boss & Workers)

A strict structure often works best.

## The Supervisor
A "Router" or "Manager" agent.
- Receives the User request.
- Breaks it down.
- Assigns tasks to Worker agents.
- Aggregates results.

This centralized control prevents agents from getting into infinite loops or arguing with each other.
"""
            },
             {
                "title": "Sequential vs Parallel",
                "slug": "sequential-vs-parallel",
                "order": 3,
                 "content": """# Execution Flow

## Sequential Chain
`Agent A -> Agent B -> Agent C`
- Good for pipelines (Research -> Write -> Edit).
- Latency is additive (slow).

## Parallel Execution
`Manager -> [Agent A, Agent B, Agent C] -> Manager`
- Agent A searches Google.
- Agent B searches Wikipedia.
- Agent C searches Arxiv.
- All run at the same time.
- Manager synthesizes the results.
- **Pros**: Fast.
- **Cons**: Complex to manage async state.
"""
            }
        ]
    },
     {
        "title": "Module 3: Building Autonomous Agents",
        "description": "Equipping agents with tools, memory, and reasoning capabilities.",
        "order": 3,
        "chapters": [
            {
                "title": "Tools & Function Calling",
                "slug": "tools-and-function-calling",
                "order": 1,
                "content": """# Tools & Function Calling

## Turning Text into Action
LLMs output text. To do things (search web, query DB), they need **Tools**.
- **Function Calling**: The LLM outputs structured JSON (e.g., `{"tool": "search", "query": "weather"}`).
- **Runtime**: Your code executes the function and feeds the result back to the LLM.

## Defining Tools
- **Name**: "search_google"
- **Description**: "Searches the web for current information."
- **Schema**: JSON Schema defining arguments.

## Best Practices
- Keep tool descriptions clear.
- valid JSON output is critical (use libraries like Pydantic).
"""
            },
            {
                "title": "Memory & State",
                "slug": "memory-and-state",
                "order": 2,
                "content": """# Memory & State Management

## The Stateless Problem
LLMs are stateless. They don't remember previous messages unless you send them again.

## Types of Memory
1.  **Short-term (Window)**: Passage of recent conversation history. Limited by context window.
2.  **Long-term (Vector DB)**: RAG. Storing memories as embeddings and retrieving relevant ones.
3.  **Entity Memory**: Extracting facts about the user (e.g., "User likes Python") and storing them in a dedicated profile DB.
"""
            },
            {
                 "title": "Planning & Reasoning",
                 "slug": "planning-and-reasoning",
                 "order": 3,
                 "content": """# Planning & Reasoning

## "Think before you act"
- **Chain of Thought (CoT)**: Ask the model to "think step by step".
- **ReAct Pattern**: **Re**ason + **Act**.
    1. Thought: I need to find the weather.
    2. Action: Call `get_weather`.
    3. Observation: It's sunny.
    4. Thought: I can answer the user now.

## Decomposition
Breaking a complex goal ("Book a trip") into sub-tasks ("Book flight", "Book hotel").
"""
            }
        ]
    },
    {
        "title": "Module 4: Advanced Patterns",
        "description": "Architectures for complex, robust agentic systems.",
        "order": 4,
        "chapters": [
             {
                "title": "RAG for Agents",
                "slug": "rag-for-agents",
                "order": 1,
                "content": """# RAG for Agents

## Context is King
Retrieval-Augmented Generation (RAG) isn't just for chat. Agents use it to:
- Look up documentation.
- Recall past mistakes.
- Access dynamic business data.

## Tool-use vs RAG
- **Tool**: Active (searching, calculating).
- **RAG**: Passive (remembering, looking up).
Often combined: An agent uses a "Search Knowledge Base" tool.
"""
            },
             {
                "title": "Human-in-the-loop",
                "slug": "human-in-the-loop",
                "order": 2,
                "content": """# Human-in-the-loop (HITL)

## Trust but Verify
For high-stakes actions (sending money, deploying code), fully autonomous agents are risky.
- **Authorization**: Agent proposes an action -> Human approves -> Agent executes.
- **Feedback**: Human edits the agent's draft -> Agent learns.
- **Interrupts**: Human stops a runaway agent.
"""
            },
            {
                "title": "Self-Correction",
                "slug": "self-correction",
                "order": 3,
                "content": """# Self-Correction & Reflection

## "Did I do that right?"
Agents can critique their own work.
- **Loop**: Generate -> Critique -> Refine.
- **Example**: Coding agent writes code -> tries to run it -> sees error -> rewrites code.
- **Reflection**: Periodically asking "Am I getting closer to the goal?"
"""
            }
        ]
    },
     {
        "title": "Module 5: Productization",
        "description": "Taking agents from prototype to production.",
        "order": 5,
        "chapters": [
             {
                "title": "Cost & Latency",
                "slug": "cost-and-latency",
                "order": 1,
                "content": """# The Economics of Agents

## Token Costs
- GPT-4o is expensive.
- Agents run in loops. A bad loop can burn $10 in minutes.
- **Solution**: Use cheaper models (GPT-4o-mini, Claude Haiku) for the "inner loop" and big models only for final synthesis.

## Latency
- Users hate waiting.
- **Streaming**: Always stream tokens to the UI.
- **Optimistic UI**: Show "Thinking..." or intermediate steps (like "Searching Google...") so the user knows it's working.
"""
            },
            {
                "title": "Safety & Guardrails",
                "slug": "safety-and-guardrails",
                "order": 2,
                "content": """# Guardrails

Never let an agent output raw text to a user without checking it.

## Input Guardrails
- Check for Jailbreaks ("Ignore previous instructions").
- Check for PII (Personal Identifiable Information).

## Output Guardrails
- Ensure the JSON is valid.
- Ensure the tone is appropriate.
- Verify facts against the retrieved context (Hallucination check).

Tools like **NeMo Guardrails** or **Guardrails AI** help enforce these rules.
"""
            }
        ]
    }
]

def seed_data():
    print("Beginning Database Seeding...")
    with Session(engine) as session:
        # 1. Get or Create Course
        course = session.exec(select(Course).where(Course.slug == "ai-agent-dev")).first()
        if not course:
            course = Course(title="AI Agent Dev", slug="ai-agent-dev", description="Master the art of building autonomous AI agents.", is_published=True)
            session.add(course)
            session.commit()
            session.refresh(course)
        print(f"Course: {course.title}")

        # 2. Iterate Modules
        for mod_data in CURRICULUM:
            # Check if module exists
            module = session.exec(select(Module).where(Module.course_id == course.id).where(Module.order_index == mod_data["order"])).first()
            if not module:
                module = Module(
                    title=mod_data["title"],
                    description=mod_data["description"],
                    order_index=mod_data["order"],
                    course_id=course.id
                )
                session.add(module)
                session.commit()
                session.refresh(module)
                print(f"  Created Module: {module.title}")
            else:
                 # Update title/desc if needed
                module.title = mod_data["title"]
                module.description = mod_data["description"]
                session.add(module)
                session.commit()
                # print(f"  Updated Module: {module.title}")

            # 3. Iterate Chapters
            for chap_data in mod_data["chapters"]:
                chapter = session.exec(select(Chapter).where(Chapter.slug == chap_data["slug"]).where(Chapter.module_id == module.id)).first()
                
                # Check if slug exists globally (to avoid collision if we moved modules) - strict check
                if not chapter:
                     chapter = session.exec(select(Chapter).where(Chapter.slug == chap_data["slug"])).first()
                     if chapter:
                         # Move it to correct module if needed configuration changed
                         chapter.module_id = module.id

                if not chapter:
                    chapter = Chapter(
                        title=chap_data["title"],
                        slug=chap_data["slug"],
                        r2_key=f"{chap_data['slug']}.md", # Legacy field, but we keep it populated
                        content=chap_data["content"],
                        order_index=chap_data["order"],
                        module_id=module.id,
                        is_published=True
                    )
                    session.add(chapter)
                    print(f"    Created Chapter: {chapter.title}")
                else:
                    # Update content
                    chapter.title = chap_data["title"]
                    chapter.content = chap_data["content"]
                    chapter.order_index = chap_data["order"]
                    session.add(chapter)
                    # print(f"    Updated Chapter: {chapter.title}")

                # 4. Create/Update Quiz (if defined in curriculum)
                if "quiz" in chap_data:
                    quiz = session.exec(select(Quiz).where(Quiz.chapter_id == chapter.id)).first()
                    if not quiz:
                        quiz = Quiz(
                            chapter_id=chapter.id,
                            title=f"Quiz: {chap_data['title']}",
                            content=chap_data["quiz"]
                        )
                        session.add(quiz)
                        print(f"      Created Quiz for: {chapter.title}")
                    else:
                        quiz.content = chap_data["quiz"]
                        session.add(quiz)
                        # print(f"      Updated Quiz for: {chapter.title}")
            
            session.commit()
    
    print("Database Seeding Complete! 🚀")

if __name__ == "__main__":
    seed_data()
