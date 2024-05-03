
agents = [
    {
        "name": "SUMMARY",
        "instruction": "Summarize the given context in a polite manner",
    },
    {
        "name": "TODO",
        "instruction": """Create a list of to-do items from the given context. 
        for each to-do item, create bullet points of owner, action items, due dates, and key stakeholders.
        put n/a in due dates if there's no due date mentioned in the given context.
        rank them in the order of priority.""",
    },
    {
        "name": "QUESTIONS",
        "instruction": """Create a list of detailed follow-up questions to key stakeholders regarding the TODO items. 
        if you miss any key information to complete the items, you need to come up with good questions to ask.
        Write questions for each todo items.""",
        "additional_context": ["TODO"],
    },
    {
        "name": "Key Facts",
        "instruction": "Create a list of key facts, expected deliverables, or due dates to remember from the given context.",
    },
    {
        "name": "FW EMAIL",
        "instruction": "Create a follow-up email from the given context for appropriate person.",
    },
    {
        "name": "SLACK REPLY",
        "instruction": "Create a slack reply from the given context for appropriate person",
    },
    {
        "name": "SNS",
        "instruction": "Create a twitter promotion from the given conetxt.",
    },
    {
        "name": "BRAINSTORM",
        "instruction": "Create an agenda for a brainstorming session from the given context.",
    },
]