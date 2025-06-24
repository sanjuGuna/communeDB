from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from groq import Groq
from rapidfuzz import process  # For fuzzy table name matching

# Replace this with your actual Groq API key or load from .env securely
groq_client = Groq(api_key="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")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_dynamic_engine(conn):
    try:
        db_url = (
            f"mysql+pymysql://{conn['user']}:{conn['password']}"
            f"@{conn['host']}:{conn['port']}/{conn['database']}"
        )
        return create_engine(db_url)
    except Exception as e:
        raise ValueError(f"Invalid connection: {e}")

# Fuzzy correct a mistyped table name against actual ones
def correct_table_name(mistyped, actual_tables):
    match, score, _ = process.extractOne(mistyped, actual_tables)
    return match if score > 70 else mistyped  # adjust threshold if needed

@app.post("/query")
async def query_db(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    conn_info = body.get("connection", {})

    if not prompt or not conn_info:
        return {"error": "Prompt or DB connection details missing."}

    try:
        engine = create_dynamic_engine(conn_info)

        # Step 1: Get all actual table names from DB
        with engine.begin() as conn:
            result = conn.execute(text("SHOW TABLES"))
            actual_tables = [row[0] for row in result]

        # Step 2: Use Groq to extract table names from the prompt
        table_names_resp = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "Extract table names used in the prompt. Comma-separated, no explanation."},
                {"role": "user", "content": prompt}
            ]
        )
        raw_tables = [t.strip() for t in table_names_resp.choices[0].message.content.split(",")]

        # Step 3: Correct mistyped table names using fuzzy match
        corrected_tables = [correct_table_name(t, actual_tables) for t in raw_tables]

        # Step 4: Get schema for each table
        schema_parts = []
        with engine.begin() as conn:
            for table in corrected_tables:
                try:
                    rows = conn.execute(text(f"DESCRIBE `{table}`")).fetchall()
                    columns = [f"{row[0]} {row[1]}" for row in rows]
                    schema_parts.append(f"{table}({', '.join(columns)})")
                except Exception as e:
                    return {"error": f"Schema error for '{table}': {e}"}

        schema = "\n".join(schema_parts)

        # Step 5: Ask Groq to generate SQL based on prompt and schema
        system_prompt = f"""You are a MySQL expert.
Use the schema below to write a valid SQL query for the user's prompt.

{schema}

Return only the SQL query, nothing else.
"""
        sql_response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        sql = sql_response.choices[0].message.content.strip()

        # Step 6: Execute the SQL query
        with engine.begin() as conn:
            result = conn.execute(text(sql))
            if sql.lower().startswith("select"):
                rows = [dict(row._mapping) for row in result]
                return {"sql": sql, "data": rows}
            else:
                return {"sql": sql, "message": f"{result.rowcount} rows affected."}

    except Exception as e:
        return {"error": f"Server error: {e}"}
